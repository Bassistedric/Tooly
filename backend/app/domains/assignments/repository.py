from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import EquipmentAssignment, EquipmentMovement


def get_current_assignment(
    db: Session,
    equipment_id: int,
) -> EquipmentAssignment | None:
    return db.scalar(
        select(EquipmentAssignment)
        .where(
            EquipmentAssignment.equipment_id == equipment_id,
            EquipmentAssignment.released_at.is_(None),
        )
        .order_by(EquipmentAssignment.assigned_at.desc())
    )


def list_assignment_history(
    db: Session,
    equipment_id: int,
) -> list[EquipmentAssignment]:
    return list(
        db.scalars(
            select(EquipmentAssignment)
            .where(EquipmentAssignment.equipment_id == equipment_id)
            .order_by(EquipmentAssignment.assigned_at.desc())
        )
    )


def list_movement_history(
    db: Session,
    equipment_id: int,
) -> list[EquipmentMovement]:
    return list(
        db.scalars(
            select(EquipmentMovement)
            .where(EquipmentMovement.equipment_id == equipment_id)
            .order_by(EquipmentMovement.occurred_at.desc())
        )
    )
