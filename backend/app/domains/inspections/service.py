import calendar
from datetime import date

from sqlalchemy.orm import Session

from app.domains.equipment.repository import get_equipment
from app.domains.worksites.repository import get_worksite

from . import repository
from .models import CheckpointResult, FieldVerification, Inspection, InspectionRequirement, InspectionResponse, InspectionTemplate, InspectionTemplateCheckpoint, InspectionTemplateSection, InspectionTemplateVersion
from .schemas import FieldVerificationCreate, InspectionCreate, RequirementCreate, TemplateCreate


class InspectionReferenceError(ValueError):
    pass


def _add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def create_requirement(db: Session, data: RequirementCreate) -> InspectionRequirement:
    equipment = get_equipment(db, data.equipment_id)
    if equipment is None:
        raise InspectionReferenceError("Equipment not found")

    values = data.model_dump()
    if values.get("template_id") is None and equipment.category_id is not None:
        template = repository.get_default_template_for_category(
            db,
            equipment.category_id,
            data.kind,
        )
        if template is not None:
            values["template_id"] = template.id

    if values.get("template_id") is not None:
        if repository.get_template(db, values["template_id"]) is None:
            raise InspectionReferenceError("Inspection template not found")

    return repository.add_requirement(
        db,
        InspectionRequirement(**values),
    )


def record_inspection(db: Session, data: InspectionCreate) -> Inspection:
    requirement = repository.get_requirement(db, data.requirement_id)
    if requirement is None:
        raise InspectionReferenceError("Inspection requirement not found")

    if data.worksite_id is not None and get_worksite(db, data.worksite_id) is None:
        raise InspectionReferenceError("Worksite not found")

    template_version_id = None
    expected_checkpoints = {}
    if requirement.template_id is not None:
        version = repository.get_published_template_version(db, requirement.template_id)
        if version is None:
            raise InspectionReferenceError("No published template version available")
        template_version_id = version.id
        expected_checkpoints = {
            checkpoint.id: checkpoint
            for section in version.sections
            for checkpoint in section.checkpoints
        }

    submitted = {item.checkpoint_id: item for item in data.responses}
    if len(submitted) != len(data.responses):
        raise InspectionReferenceError("Duplicate checkpoint response")

    if expected_checkpoints:
        unknown = set(submitted) - set(expected_checkpoints)
        if unknown:
            raise InspectionReferenceError("Checkpoint does not belong to the selected template version")

        missing = {
            checkpoint_id
            for checkpoint_id, checkpoint in expected_checkpoints.items()
            if checkpoint.is_required and checkpoint_id not in submitted
        }
        if missing:
            raise InspectionReferenceError("Required checkpoint response missing")

        invalid_na = {
            checkpoint_id
            for checkpoint_id, item in submitted.items()
            if item.answer == CheckpointResult.NA
            and not expected_checkpoints[checkpoint_id].allows_na
        }
        if invalid_na:
            raise InspectionReferenceError("NA is not allowed for one or more checkpoints")

    has_nok = any(item.answer == CheckpointResult.NOK for item in data.responses)
    if has_nok and data.outcome == data.outcome.COMPLIANT:
        raise InspectionReferenceError("A control with NOK checkpoints cannot be compliant")

    next_due = None
    if requirement.interval_months and data.outcome == data.outcome.COMPLIANT:
        next_due = _add_months(data.performed_at.date(), requirement.interval_months)

    values = data.model_dump(exclude={"responses"})
    inspection = Inspection(
        equipment_id=requirement.equipment_id,
        next_due_date=next_due,
        template_version_id=template_version_id,
        **values,
    )
    responses = [
        InspectionResponse(
            checkpoint_id=item.checkpoint_id,
            answer=item.answer.value,
            comment=item.comment,
        )
        for item in data.responses
    ]

    try:
        inspection = repository.add_inspection_with_responses(db, inspection, responses)
        if data.outcome == data.outcome.COMPLIANT:
            requirement.next_due_date = next_due
        db.add(requirement)
        db.commit()
        db.refresh(inspection)
        return inspection
    except Exception:
        db.rollback()
        raise


def record_field_verification(
    db: Session,
    data: FieldVerificationCreate,
) -> FieldVerification:
    if get_equipment(db, data.equipment_id) is None:
        raise InspectionReferenceError("Equipment not found")
    if get_worksite(db, data.worksite_id) is None:
        raise InspectionReferenceError("Worksite not found")

    # Deliberately does not update InspectionRequirement.next_due_date.
    return repository.add_field_verification(
        db,
        FieldVerification(**data.model_dump()),
    )


def resolve_template_for_equipment(
    db: Session,
    equipment_id: int,
    requirement_id: int | None = None,
):
    equipment = get_equipment(db, equipment_id)
    if equipment is None:
        raise InspectionReferenceError("Equipment not found")

    template_id = None
    source = None

    if requirement_id is not None:
        requirement = repository.get_requirement_for_equipment(
            db,
            equipment_id,
            requirement_id,
        )
        if requirement is None:
            raise InspectionReferenceError(
                "Inspection requirement not found for this equipment"
            )
        if requirement.template_id is not None:
            template_id = requirement.template_id
            source = "REQUIREMENT"

    if template_id is None and equipment.category_id is not None and requirement_id is not None:
        category_template = repository.get_default_template_for_category(
            db,
            equipment.category_id,
            requirement.kind,
        )
        if category_template is not None:
            template_id = category_template.id
            source = "CATEGORY"

    if template_id is None:
        return None

    template = repository.get_template(db, template_id)
    if template is None or not template.is_active:
        raise InspectionReferenceError("Inspection template not found or inactive")

    version = repository.get_latest_published_template_version(db, template_id)
    if version is None:
        raise InspectionReferenceError(
            "No published version exists for this inspection template"
        )

    return {
        "source": source,
        "template": template,
        "version": version,
    }


class InspectionTemplateConflictError(ValueError):
    pass


def create_template(db: Session, data: TemplateCreate) -> InspectionTemplate:
    code = data.code.strip().upper()
    if repository.get_template_by_code(db, code) is not None:
        raise InspectionTemplateConflictError("Inspection template code already exists")

    template = InspectionTemplate(
        code=code,
        name=data.name.strip(),
    )
    version = InspectionTemplateVersion(
        version=1,
        title=data.title.strip(),
        reminders=data.reminders,
        source_reference=data.source_reference,
        is_published=True,
    )
    template.versions.append(version)

    for section_position, section_data in enumerate(data.sections, start=1):
        section = InspectionTemplateSection(
            title=section_data.title.strip(),
            position=section_position,
        )
        version.sections.append(section)
        for checkpoint_position, checkpoint_data in enumerate(
            section_data.checkpoints,
            start=1,
        ):
            section.checkpoints.append(
                InspectionTemplateCheckpoint(
                    position=checkpoint_position,
                    text=checkpoint_data.text.strip(),
                    allows_na=checkpoint_data.allows_na,
                    is_required=checkpoint_data.is_required,
                )
            )

    return repository.add_template(db, template)
