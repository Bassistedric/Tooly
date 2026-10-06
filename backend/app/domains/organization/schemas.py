from pydantic import BaseModel, ConfigDict, Field


class OrganizationBase(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    organization_type: str = Field(default="ENTITY", max_length=50)
    parent_id: int | None = None
    is_active: bool = True


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=200)
    organization_type: str | None = Field(default=None, max_length=50)
    parent_id: int | None = None
    is_active: bool | None = None


class OrganizationRead(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PersonCreate(BaseModel):
    organization_id: int
    employee_number: str | None = Field(default=None, max_length=50)
    first_name: str = Field(min_length=1, max_length=120)
    last_name: str = Field(min_length=1, max_length=120)
    email: str | None = Field(default=None, max_length=250)


class PersonRead(PersonCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool


class VehicleCreate(BaseModel):
    organization_id: int
    registration: str = Field(min_length=1, max_length=30)
    description: str | None = Field(default=None, max_length=200)
    assigned_person_id: int | None = None


class VehicleRead(VehicleCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
