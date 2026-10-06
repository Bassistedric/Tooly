from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from . import repository, service
from .schemas import (
    OrganizationCreate,
    OrganizationRead,
    PersonCreate,
    PersonRead,
    VehicleCreate,
    VehicleRead,
)

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


@router.get("/people", response_model=list[PersonRead])
def list_people(db: Session = Depends(get_db)):
    return repository.list_people(db)


@router.post(
    "/people",
    response_model=PersonRead,
    status_code=status.HTTP_201_CREATED,
)
def create_person(data: PersonCreate, db: Session = Depends(get_db)):
    try:
        return service.create_person(db, data)
    except service.OrganizationParentError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/vehicles", response_model=list[VehicleRead])
def list_vehicles(db: Session = Depends(get_db)):
    return repository.list_vehicles(db)


@router.post(
    "/vehicles",
    response_model=VehicleRead,
    status_code=status.HTTP_201_CREATED,
)
def create_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
    try:
        return service.create_vehicle(db, data)
    except service.OrganizationConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except service.OrganizationParentError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
