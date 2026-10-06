from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from .models import EquipmentComplianceStatus, EquipmentOperationalStatus


class EquipmentCategoryCreate(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    name_key: str = Field(min_length=1, max_length=150)
    parent_id: int | None = None


class EquipmentCategoryRead(EquipmentCategoryCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool


class EquipmentBase(BaseModel):
    business_number: str = Field(min_length=1, max_length=100)
    serial_number: str | None = Field(default=None, max_length=150)
    external_number: str | None = Field(default=None, max_length=150)
    description: str = Field(min_length=1, max_length=250)
    brand: str | None = Field(default=None, max_length=120)
    model: str | None = Field(default=None, max_length=150)
    notes: str | None = None

    organization_id: int
    category_id: int | None = None

    manufacture_date: date | None = None
    commissioned_date: date | None = None


class EquipmentCreate(EquipmentBase):
    operational_status: EquipmentOperationalStatus = (
        EquipmentOperationalStatus.IN_STOCK
    )
    compliance_status: EquipmentComplianceStatus = (
        EquipmentComplianceStatus.TO_VERIFY
    )


class EquipmentUpdate(BaseModel):
    serial_number: str | None = Field(default=None, max_length=150)
    external_number: str | None = Field(default=None, max_length=150)
    description: str | None = Field(default=None, min_length=1, max_length=250)
    brand: str | None = Field(default=None, max_length=120)
    model: str | None = Field(default=None, max_length=150)
    notes: str | None = None
    organization_id: int | None = None
    category_id: int | None = None
    manufacture_date: date | None = None
    commissioned_date: date | None = None
    operational_status: EquipmentOperationalStatus | None = None
    compliance_status: EquipmentComplianceStatus | None = None


class EquipmentRead(EquipmentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    qr_generated: bool
    qr_installed: bool
    qr_installed_at: datetime | None
    is_archived: bool
    created_at: datetime
    updated_at: datetime


class ReturnToServiceCreate(BaseModel):
    performed_by: str = Field(min_length=1, max_length=150)
    reason: str | None = None
    target_status: EquipmentOperationalStatus = EquipmentOperationalStatus.IN_SERVICE


class EquipmentStatusEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    equipment_id: int
    occurred_at: datetime
    event_type: str
    from_status: str
    to_status: str
    performed_by: str
    reason: str | None
