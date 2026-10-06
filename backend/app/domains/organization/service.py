from sqlalchemy.orm import Session

from . import repository
from .models import Organization, Person, Vehicle
from .schemas import OrganizationCreate, PersonCreate, VehicleCreate


class OrganizationConflictError(ValueError):
    pass


class OrganizationParentError(ValueError):
    pass


def create_organization(db: Session, data: OrganizationCreate) -> Organization:
    if repository.get_organization_by_code(db, data.code):
        raise OrganizationConflictError("Organization code already exists")

    if (
        data.parent_id is not None
        and repository.get_organization(db, data.parent_id) is None
    ):
        raise OrganizationParentError("Parent organization not found")

    return repository.add_organization(
        db,
        Organization(**data.model_dump()),
    )


def create_person(db: Session, data: PersonCreate) -> Person:
    if repository.get_organization(db, data.organization_id) is None:
        raise OrganizationParentError("Organization not found")
    return repository.add_person(db, Person(**data.model_dump()))


def create_vehicle(db: Session, data: VehicleCreate) -> Vehicle:
    if repository.get_organization(db, data.organization_id) is None:
        raise OrganizationParentError("Organization not found")

    registration = data.registration.strip().upper()
    if repository.get_vehicle_by_registration(db, registration):
        raise OrganizationConflictError("Vehicle registration already exists")

    if data.assigned_person_id is not None:
        person = repository.get_person(db, data.assigned_person_id)
        if person is None:
            raise OrganizationParentError("Assigned person not found")
        if person.organization_id != data.organization_id:
            raise OrganizationParentError(
                "Vehicle and assigned person must belong to the same organization"
            )

    values = data.model_dump()
    values["registration"] = registration
    return repository.add_vehicle(db, Vehicle(**values))
