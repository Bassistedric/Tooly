from fastapi import APIRouter

from app.domains.equipment.router import router as equipment_router
from app.domains.organization.router import router as organization_router

api_router = APIRouter()

api_router.include_router(organization_router)
api_router.include_router(equipment_router)
