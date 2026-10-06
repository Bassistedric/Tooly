from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from . import repository, service
from .schemas import (
    FieldVerificationCreate,
    FieldVerificationRead,
    InspectionCreate,
    InspectionRead,
    RequirementCreate,
    RequirementRead,
)

router = APIRouter(prefix="/inspections", tags=["inspections"])


@router.get("/templates")
def search_templates(search: str | None = None, db: Session = Depends(get_db)):
    templates = repository.search_templates(db, search)
    return [
        {"id": item.id, "code": item.code, "name": item.name}
        for item in templates
    ]


@router.get("/resolve/equipment/{equipment_id}")
def resolve_equipment_template(
    equipment_id: int,
    requirement_id: int | None = None,
    db: Session = Depends(get_db),
):
    try:
        resolved = service.resolve_template_for_equipment(
            db,
            equipment_id,
            requirement_id,
        )
    except service.InspectionReferenceError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if resolved is None:
        return {
            "equipment_id": equipment_id,
            "template": None,
            "reason": "NO_TEMPLATE_CONFIGURED",
        }

    template = resolved["template"]
    version = resolved["version"]
    return {
        "equipment_id": equipment_id,
        "source": resolved["source"],
        "template": {
            "id": template.id,
            "code": template.code,
            "name": template.name,
        },
        "version": {
            "id": version.id,
            "version": version.version,
            "title": version.title,
            "reminders": version.reminders,
            "sections": [
                {
                    "id": section.id,
                    "title": section.title,
                    "position": section.position,
                    "checkpoints": [
                        {
                            "id": checkpoint.id,
                            "position": checkpoint.position,
                            "text": checkpoint.text,
                            "allows_na": checkpoint.allows_na,
                            "is_required": checkpoint.is_required,
                        }
                        for checkpoint in section.checkpoints
                    ],
                }
                for section in version.sections
            ],
        },
    }


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


@router.post(
    "/field-verifications",
    response_model=FieldVerificationRead,
    status_code=status.HTTP_201_CREATED,
)
def record_field_verification(
    data: FieldVerificationCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.record_field_verification(db, data)
    except service.InspectionReferenceError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get(
    "/field-verifications/equipment/{equipment_id}",
    response_model=list[FieldVerificationRead],
)
def list_field_verifications(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    return repository.list_field_verifications(db, equipment_id)
