from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .models import AssignmentTargetType


class AssignmentCreate(BaseModel):
    equipment_id: int
    target_type: AssignmentTargetType
    target_id: int | None = None
    target_label: str = Field(min_length=1, max_length=250)
    assigned_by: str | None = Field(default=None, max_length=150)
    requested_by: str | None = Field(default=None, max_length=150)
    remarks: str | None = None


class AssignmentRead(AssignmentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assigned_at: datetime
    released_at: datetime | None


class MovementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    equipment_id: int
    occurred_at: datetime
    from_type: AssignmentTargetType | None
    from_id: int | None
    from_label: str | None
    to_type: AssignmentTargetType
    to_id: int | None
    to_label: str
    recorded_by: str | None
    remarks: str | None
