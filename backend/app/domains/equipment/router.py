from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from . import repository, service
from .schemas import (
    EquipmentCategoryCreate,
    EquipmentCategoryRead,
    EquipmentCreate,
    EquipmentRead,
    EquipmentStatusEventRead,
    ReturnToServiceCreate,
)

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("", response_model=list[EquipmentRead])
def list_equipment(
    search: str | None = Query(default=None, max_length=150),
    db: Session = Depends(get_db),
):
    return repository.list_equipment(db, search=search)


@router.post(
    "",
    response_model=EquipmentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_equipment(
    data: EquipmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_equipment(db, data)
    except service.EquipmentConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except service.EquipmentReferenceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    "/categories",
    response_model=EquipmentCategoryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    data: EquipmentCategoryCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_category(db, data)
    except service.EquipmentConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except service.EquipmentReferenceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{equipment_id}/return-to-service", response_model=EquipmentRead)
def return_to_service(
    equipment_id: int,
    data: ReturnToServiceCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.return_to_service(db, equipment_id, data)
    except service.EquipmentReferenceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/{equipment_id}/status-history",
    response_model=list[EquipmentStatusEventRead],
)
def status_history(equipment_id: int, db: Session = Depends(get_db)):
    if repository.get_equipment(db, equipment_id) is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return repository.list_status_events(db, equipment_id)
