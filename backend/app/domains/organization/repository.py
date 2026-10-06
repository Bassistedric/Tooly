from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Organization


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
