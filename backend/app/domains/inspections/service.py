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
    if get_equipment(db, data.equipment_id) is None:
        raise InspectionReferenceError("Equipment not found")
    return repository.add_requirement(db, InspectionRequirement(**data.model_dump()))


def record_inspection(db: Session, data: InspectionCreate) -> Inspection:
    requirement = repository.get_requirement(db, data.requirement_id)
    if requirement is None:
        raise InspectionReferenceError("Inspection requirement not found")

    if data.worksite_id is not None and get_worksite(db, data.worksite_id) is None:
        raise InspectionReferenceError("Worksite not found")

    next_due = None
    if requirement.interval_months:
        next_due = _add_months(data.performed_at.date(), requirement.interval_months)

    inspection = Inspection(
        equipment_id=requirement.equipment_id,
        next_due_date=next_due,
        **data.model_dump(),
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
