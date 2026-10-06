from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .models import Equipment, EquipmentCategory, EquipmentStatusEvent


def list_equipment(db: Session, search: str | None = None) -> list[Equipment]:
    statement = select(Equipment).where(Equipment.is_archived.is_(False))

    if search:
        term = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                Equipment.business_number.ilike(term),
                Equipment.serial_number.ilike(term),
                Equipment.external_number.ilike(term),
                Equipment.description.ilike(term),
                Equipment.brand.ilike(term),
                Equipment.model.ilike(term),
            )
        )

    return list(db.scalars(statement.order_by(Equipment.business_number)))


def get_equipment(db: Session, equipment_id: int) -> Equipment | None:
    return db.get(Equipment, equipment_id)


def get_equipment_by_number(db: Session, business_number: str) -> Equipment | None:
    return db.scalar(
        select(Equipment).where(Equipment.business_number == business_number)
    )


def get_category(db: Session, category_id: int) -> EquipmentCategory | None:
    return db.get(EquipmentCategory, category_id)


def get_category_by_code(db: Session, code: str) -> EquipmentCategory | None:
    return db.scalar(
        select(EquipmentCategory).where(EquipmentCategory.code == code)
    )


def add_equipment(db: Session, equipment: Equipment) -> Equipment:
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


def add_category(db: Session, category: EquipmentCategory) -> EquipmentCategory:
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def list_status_events(db: Session, equipment_id: int) -> list[EquipmentStatusEvent]:
    return list(db.scalars(
        select(EquipmentStatusEvent)
        .where(EquipmentStatusEvent.equipment_id == equipment_id)
        .order_by(EquipmentStatusEvent.occurred_at.desc())
    ))
