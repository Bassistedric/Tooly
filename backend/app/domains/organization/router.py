from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from . import repository, service
from .schemas import OrganizationCreate, OrganizationRead

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("", response_model=list[OrganizationRead])
def list_organizations(db: Session = Depends(get_db)):
    return repository.list_organizations(db)


@router.post(
    "",
    response_model=OrganizationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    data: OrganizationCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_organization(db, data)
    except service.OrganizationConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except service.OrganizationParentError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
