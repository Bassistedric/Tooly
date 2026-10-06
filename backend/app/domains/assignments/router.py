from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from . import repository, service
from .schemas import AssignmentCreate, AssignmentRead, MovementRead

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post(
    "",
    response_model=AssignmentRead,
    status_code=status.HTTP_201_CREATED,
)
def assign_equipment(
    data: AssignmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.assign_equipment(db, data)
    except service.AssignmentReferenceError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get(
    "/equipment/{equipment_id}/current",
    response_model=AssignmentRead | None,
)
def get_current_assignment(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    return repository.get_current_assignment(db, equipment_id)


@router.get(
    "/equipment/{equipment_id}/history",
    response_model=list[AssignmentRead],
)
def get_assignment_history(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    return repository.list_assignment_history(db, equipment_id)


@router.get(
    "/equipment/{equipment_id}/movements",
    response_model=list[MovementRead],
)
def get_movement_history(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    return repository.list_movement_history(db, equipment_id)
