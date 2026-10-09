from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from . import repository

router = APIRouter(prefix="/inspections", tags=["inspections"])

class TemplateAssignment(BaseModel):
    template_id: int | None = None

@router.patch("/requirements/{requirement_id}/template")
def change_template(requirement_id: int, data: TemplateAssignment, db: Session = Depends(get_db)):
    requirement = repository.get_requirement(db, requirement_id)
    if requirement is None or not requirement.is_active:
        raise HTTPException(status_code=404, detail="Requirement not found")
    if data.template_id is not None:
        template = repository.get_template(db, data.template_id)
        if template is None or not template.is_active:
            raise HTTPException(status_code=404, detail="Template not found")
        if repository.get_latest_published_template_version(db, template.id) is None:
            raise HTTPException(status_code=422, detail="Template has no published version")
    requirement.template_id = data.template_id
    db.add(requirement)
    db.commit()
    db.refresh(requirement)
    return {"requirement_id": requirement.id, "template_id": requirement.template_id}
