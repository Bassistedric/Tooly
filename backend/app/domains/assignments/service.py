from datetime import datetime

from sqlalchemy.orm import Session

from app.domains.equipment.models import EquipmentOperationalStatus
from app.domains.equipment.repository import get_equipment

from . import repository
from .models import AssignmentTargetType, EquipmentAssignment, EquipmentMovement
from .schemas import AssignmentCreate


class AssignmentReferenceError(ValueError):
    pass


def _status_for_target(target_type: AssignmentTargetType) -> EquipmentOperationalStatus:
    if target_type == AssignmentTargetType.QUARANTINE:
        return EquipmentOperationalStatus.QUARANTINE
    if target_type == AssignmentTargetType.STOCK:
        return EquipmentOperationalStatus.IN_STOCK
    return EquipmentOperationalStatus.ASSIGNED


def assign_equipment(
    db: Session,
    data: AssignmentCreate,
) -> EquipmentAssignment:
    equipment = get_equipment(db, data.equipment_id)
    if equipment is None:
        raise AssignmentReferenceError("Equipment not found")

    now = datetime.utcnow()
    current = repository.get_current_assignment(db, data.equipment_id)

    movement = EquipmentMovement(
        equipment_id=data.equipment_id,
        occurred_at=now,
        from_type=current.target_type if current else None,
        from_id=current.target_id if current else None,
        from_label=current.target_label if current else None,
        to_type=data.target_type,
        to_id=data.target_id,
        to_label=data.target_label,
        recorded_by=data.assigned_by,
        remarks=data.remarks,
    )

    if current is not None:
        current.released_at = now

    assignment = EquipmentAssignment(
        **data.model_dump(),
        assigned_at=now,
    )

    equipment.operational_status = _status_for_target(data.target_type)

    db.add(movement)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
