from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class SiteCreate(BaseModel):
    organization_id: int
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    address: str | None = Field(default=None, max_length=300)


class SiteRead(SiteCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool


class WorksiteCreate(BaseModel):
    organization_id: int
    site_id: int | None = None
    code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=250)
    address: str | None = Field(default=None, max_length=300)
    customer: str | None = Field(default=None, max_length=200)
    start_date: date | None = None
    end_date: date | None = None
    remarks: str | None = None


class WorksiteRead(WorksiteCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
