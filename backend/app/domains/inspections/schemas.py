from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from .models import CheckpointResult, InspectionKind, InspectionOutcome


class RequirementCreate(BaseModel):
    equipment_id: int
    code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=200)
    kind: InspectionKind
    interval_months: int | None = Field(default=None, ge=1)
    responsible: str | None = Field(default=None, max_length=150)
    next_due_date: date | None = None
    template_id: int | None = None
    warning_days: int = Field(default=30, ge=0)


class RequirementRead(RequirementCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool


class InspectionResponseCreate(BaseModel):
    checkpoint_id: int
    answer: CheckpointResult
    comment: str | None = None


class InspectionCreate(BaseModel):
    requirement_id: int
    performed_at: datetime
    outcome: InspectionOutcome
    performed_by: str | None = Field(default=None, max_length=150)
    worksite_id: int | None = None
    remarks: str | None = None
    responses: list[InspectionResponseCreate] = Field(default_factory=list)


class InspectionRead(InspectionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    equipment_id: int
    next_due_date: date | None


class FieldVerificationCreate(BaseModel):
    equipment_id: int
    worksite_id: int
    verified_at: datetime
    verified_by: str | None = Field(default=None, max_length=150)
    control_in_order: bool = True
    remarks: str | None = None


class FieldVerificationRead(FieldVerificationCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TemplateCheckpointCreate(BaseModel):
    text: str = Field(min_length=1)
    allows_na: bool = True
    is_required: bool = True


class TemplateSectionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    checkpoints: list[TemplateCheckpointCreate]


class TemplateCreate(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=250)
    reminders: str | None = None
    source_reference: str | None = Field(default=None, max_length=250)
    sections: list[TemplateSectionCreate]


class TemplateCheckpointRead(TemplateCheckpointCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    position: int


class TemplateSectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    position: int
    checkpoints: list[TemplateCheckpointRead]


class TemplateVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    version: int
    title: str
    reminders: str | None
    source_reference: str | None
    is_published: bool
    sections: list[TemplateSectionRead]
