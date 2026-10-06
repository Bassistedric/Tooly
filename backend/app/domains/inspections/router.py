from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from . import repository, service
from .schemas import InspectionCreate, InspectionRead, RequirementCreate, RequirementRead

router = APIRouter(prefix="/inspections", tags=["inspections"])


@router.post("/requirements", response_model=RequirementRead, status_code=status.HTTP_201_CREATED)
def create_requirement(data: RequirementCreate, db: Session = Depends(get_db)):
    try:
        return service.create_requirement(db, data)
    except service.InspectionReferenceError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/requirements/equipment/{equipment_id}", response_model=list[RequirementRead])
def list_requirements(equipment_id: int, db: Session = Depends(get_db)):
    return repository.list_requirements(db, equipment_id)


@router.post("", response_model=InspectionRead, status_code=status.HTTP_201_CREATED)
def record_inspection(data: InspectionCreate, db: Session = Depends(get_db)):
    try:
        return service.record_inspection(db, data)
    except service.InspectionReferenceError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/equipment/{equipment_id}", response_model=list[InspectionRead])
def list_inspections(equipment_id: int, db: Session = Depends(get_db)):
    return repository.list_inspections(db, equipment_id)
