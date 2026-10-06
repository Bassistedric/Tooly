from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from . import repository, service
from .schemas import SiteCreate, SiteRead, WorksiteCreate, WorksiteRead

router = APIRouter(prefix="/worksites", tags=["worksites"])


@router.get("/sites", response_model=list[SiteRead])
def list_sites(db: Session = Depends(get_db)):
    return repository.list_sites(db)


@router.post(
    "/sites",
    response_model=SiteRead,
    status_code=status.HTTP_201_CREATED,
)
def create_site(data: SiteCreate, db: Session = Depends(get_db)):
    try:
        return service.create_site(db, data)
    except service.WorksiteReferenceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[WorksiteRead])
def list_worksites(
    active_only: bool = True,
    db: Session = Depends(get_db),
):
    return repository.list_worksites(db, active_only=active_only)


@router.post(
    "",
    response_model=WorksiteRead,
    status_code=status.HTTP_201_CREATED,
)
def create_worksite(
    data: WorksiteCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_worksite(db, data)
    except service.WorksiteReferenceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
