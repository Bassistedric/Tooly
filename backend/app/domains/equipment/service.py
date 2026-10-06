from sqlalchemy.orm import Session

from app.domains.organization.repository import get_organization

from . import repository
from .models import Equipment, EquipmentCategory
from .schemas import EquipmentCategoryCreate, EquipmentCreate


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
