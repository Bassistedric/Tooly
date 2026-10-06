from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Organization, Person, Vehicle


def list_organizations(db: Session) -> list[Organization]:
    return list(db.scalars(select(Organization).order_by(Organization.name)))


def get_organization(db: Session, organization_id: int) -> Organization | None:
    return db.get(Organization, organization_id)


def get_organization_by_code(db: Session, code: str) -> Organization | None:
    return db.scalar(select(Organization).where(Organization.code == code))


def add_organization(db: Session, organization: Organization) -> Organization:
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


def get_person(db: Session, person_id: int) -> Person | None:
    return db.get(Person, person_id)


def list_people(db: Session) -> list[Person]:
    return list(
        db.scalars(
            select(Person).where(Person.is_active.is_(True)).order_by(
                Person.last_name,
                Person.first_name,
            )
        )
    )


def add_person(db: Session, person: Person) -> Person:
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def get_vehicle(db: Session, vehicle_id: int) -> Vehicle | None:
    return db.get(Vehicle, vehicle_id)


def get_vehicle_by_registration(
    db: Session,
    registration: str,
) -> Vehicle | None:
    return db.scalar(
        select(Vehicle).where(Vehicle.registration == registration)
    )


def list_vehicles(db: Session) -> list[Vehicle]:
    return list(
        db.scalars(
            select(Vehicle).where(Vehicle.is_active.is_(True)).order_by(
                Vehicle.registration
            )
        )
    )


def add_vehicle(db: Session, vehicle: Vehicle) -> Vehicle:
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle
