from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Site, Worksite


def get_site(db: Session, site_id: int) -> Site | None:
    return db.get(Site, site_id)


def list_sites(db: Session) -> list[Site]:
    return list(db.scalars(select(Site).order_by(Site.name)))


def add_site(db: Session, site: Site) -> Site:
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


def get_worksite(db: Session, worksite_id: int) -> Worksite | None:
    return db.get(Worksite, worksite_id)


def list_worksites(
    db: Session,
    active_only: bool = True,
) -> list[Worksite]:
    statement = select(Worksite)
    if active_only:
        statement = statement.where(Worksite.is_active.is_(True))
    return list(db.scalars(statement.order_by(Worksite.name)))


def add_worksite(db: Session, worksite: Worksite) -> Worksite:
    db.add(worksite)
    db.commit()
    db.refresh(worksite)
    return worksite
