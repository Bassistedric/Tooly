from sqlalchemy.orm import Session

from app.domains.organization.repository import get_organization

from . import repository
from .models import Equipment, EquipmentCategory, EquipmentComplianceStatus, EquipmentOperationalStatus, EquipmentStatusEvent
from .schemas import EquipmentCategoryCreate, EquipmentCreate, ReturnToServiceCreate


class EquipmentConflictError(ValueError):
    pass


class EquipmentReferenceError(ValueError):
    pass


def create_category(
    db: Session,
    data: EquipmentCategoryCreate,
) -> EquipmentCategory:
    if repository.get_category_by_code(db, data.code):
        raise EquipmentConflictError("Equipment category code already exists")

    if data.parent_id is not None and repository.get_category(db, data.parent_id) is None:
        raise EquipmentReferenceError("Parent equipment category not found")

    return repository.add_category(
        db,
        EquipmentCategory(**data.model_dump()),
    )


def create_equipment(db: Session, data: EquipmentCreate) -> Equipment:
    if repository.get_equipment_by_number(db, data.business_number):
        raise EquipmentConflictError("Equipment business number already exists")

    if get_organization(db, data.organization_id) is None:
        raise EquipmentReferenceError("Organization not found")

    if (
        data.category_id is not None
        and repository.get_category(db, data.category_id) is None
    ):
        raise EquipmentReferenceError("Equipment category not found")

    return repository.add_equipment(
        db,
        Equipment(**data.model_dump()),
    )


def return_to_service(
    db: Session,
    equipment_id: int,
    data: ReturnToServiceCreate,
) -> Equipment:
    equipment = repository.get_equipment(db, equipment_id)
    if equipment is None:
        raise EquipmentReferenceError("Equipment not found")
    if equipment.operational_status not in {
        EquipmentOperationalStatus.QUARANTINE,
        EquipmentOperationalStatus.IN_REPAIR,
    }:
        raise EquipmentReferenceError("Equipment is not in quarantine or repair")
    if equipment.compliance_status != EquipmentComplianceStatus.COMPLIANT:
        raise EquipmentReferenceError("Equipment must be compliant before return to service")
    if data.target_status not in {
        EquipmentOperationalStatus.IN_SERVICE,
        EquipmentOperationalStatus.IN_STOCK,
    }:
        raise EquipmentReferenceError("Invalid return-to-service target status")

    previous = equipment.operational_status
    equipment.operational_status = data.target_status
    event = EquipmentStatusEvent(
        equipment_id=equipment.id,
        event_type="RETURN_TO_SERVICE",
        from_status=previous.value,
        to_status=data.target_status.value,
        performed_by=data.performed_by,
        reason=data.reason,
    )
    try:
        db.add(equipment)
        db.add(event)
        db.commit()
        db.refresh(equipment)
        return equipment
    except Exception:
        db.rollback()
        raise
