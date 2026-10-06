from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Inspection, InspectionRequirement


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
