import calendar
from datetime import date

from sqlalchemy.orm import Session

from app.domains.equipment.repository import get_equipment
from app.domains.worksites.repository import get_worksite

from . import repository
from .models import FieldVerification, Inspection, InspectionRequirement
from .schemas import FieldVerificationCreate, InspectionCreate, RequirementCreate


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

    template_version_id = data.template_version_id
    if template_version_id is None and requirement.template_id is not None:
        version = repository.get_published_template_version(
            db,
            requirement.template_id,
        )
        if version is None:
            raise InspectionReferenceError("No published template version available")
        template_version_id = version.id

    next_due = None
    if requirement.interval_months:
        next_due = _add_months(data.performed_at.date(), requirement.interval_months)

    values = data.model_dump(exclude={"template_version_id"})
    inspection = Inspection(
        equipment_id=requirement.equipment_id,
        next_due_date=next_due,
        template_version_id=template_version_id,
        **values,
    )

    requirement.next_due_date = next_due
    db.add(requirement)
    return repository.add_inspection(db, inspection)


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

    if template_id is None and equipment.category is not None:
        template_id = equipment.category.default_inspection_template_id
        if template_id is not None:
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
