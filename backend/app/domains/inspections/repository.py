from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .models import (
    EquipmentCategoryTemplate,
    FieldVerification,
    Inspection,
    InspectionRequirement,
    InspectionTemplate,
    InspectionTemplateVersion,
)


def get_requirement(db: Session, requirement_id: int) -> InspectionRequirement | None:
    return db.get(InspectionRequirement, requirement_id)


def list_requirements(db: Session, equipment_id: int) -> list[InspectionRequirement]:
    return list(db.scalars(
        select(InspectionRequirement)
        .where(
            InspectionRequirement.equipment_id == equipment_id,
            InspectionRequirement.is_active.is_(True),
        )
        .order_by(InspectionRequirement.name)
    ))


def add_requirement(db: Session, requirement: InspectionRequirement) -> InspectionRequirement:
    db.add(requirement)
    db.commit()
    db.refresh(requirement)
    return requirement


def add_inspection(db: Session, inspection: Inspection) -> Inspection:
    db.add(inspection)
    db.commit()
    db.refresh(inspection)
    return inspection


def list_inspections(db: Session, equipment_id: int) -> list[Inspection]:
    return list(db.scalars(
        select(Inspection)
        .where(Inspection.equipment_id == equipment_id)
        .order_by(Inspection.performed_at.desc())
    ))


def add_field_verification(
    db: Session,
    verification: FieldVerification,
) -> FieldVerification:
    db.add(verification)
    db.commit()
    db.refresh(verification)
    return verification


def list_field_verifications(
    db: Session,
    equipment_id: int,
) -> list[FieldVerification]:
    return list(db.scalars(
        select(FieldVerification)
        .where(FieldVerification.equipment_id == equipment_id)
        .order_by(FieldVerification.verified_at.desc())
    ))


def search_templates(db: Session, search: str | None = None) -> list[InspectionTemplate]:
    statement = select(InspectionTemplate).where(InspectionTemplate.is_active.is_(True))
    if search:
        pattern = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                InspectionTemplate.code.ilike(pattern),
                InspectionTemplate.name.ilike(pattern),
            )
        )
    return list(db.scalars(statement.order_by(InspectionTemplate.name)))


def get_template(db: Session, template_id: int) -> InspectionTemplate | None:
    return db.get(InspectionTemplate, template_id)


def get_published_template_version(
    db: Session,
    template_id: int,
) -> InspectionTemplateVersion | None:
    return db.scalar(
        select(InspectionTemplateVersion)
        .where(
            InspectionTemplateVersion.template_id == template_id,
            InspectionTemplateVersion.is_published.is_(True),
        )
        .order_by(InspectionTemplateVersion.version.desc())
    )


def get_default_template_for_category(
    db: Session,
    category_id: int,
    kind,
) -> InspectionTemplate | None:
    return db.scalar(
        select(InspectionTemplate)
        .join(
            EquipmentCategoryTemplate,
            EquipmentCategoryTemplate.template_id == InspectionTemplate.id,
        )
        .where(
            EquipmentCategoryTemplate.category_id == category_id,
            EquipmentCategoryTemplate.kind == kind,
            EquipmentCategoryTemplate.is_default.is_(True),
            InspectionTemplate.is_active.is_(True),
        )
    )
