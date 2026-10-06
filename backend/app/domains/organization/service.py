from sqlalchemy.orm import Session

from . import repository
from .models import Organization
from .schemas import OrganizationCreate


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
