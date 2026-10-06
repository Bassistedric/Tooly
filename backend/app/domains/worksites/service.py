from sqlalchemy.orm import Session

from app.domains.organization.repository import get_organization

from . import repository
from .models import Site, Worksite
from .schemas import SiteCreate, WorksiteCreate


class WorksiteReferenceError(ValueError):
    pass


def create_site(db: Session, data: SiteCreate) -> Site:
    if get_organization(db, data.organization_id) is None:
        raise WorksiteReferenceError("Organization not found")
    return repository.add_site(db, Site(**data.model_dump()))


def create_worksite(db: Session, data: WorksiteCreate) -> Worksite:
    if get_organization(db, data.organization_id) is None:
        raise WorksiteReferenceError("Organization not found")

    if data.site_id is not None:
        site = repository.get_site(db, data.site_id)
        if site is None:
            raise WorksiteReferenceError("Site not found")
        if site.organization_id != data.organization_id:
            raise WorksiteReferenceError(
                "Site and worksite must belong to the same organization"
            )

    if (
        data.start_date is not None
        and data.end_date is not None
        and data.end_date < data.start_date
    ):
        raise WorksiteReferenceError(
            "Worksite end date cannot precede start date"
        )

    return repository.add_worksite(
        db,
        Worksite(**data.model_dump()),
    )
