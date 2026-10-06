"""Central SQLAlchemy model imports for metadata and migrations."""

from app.domains.assignments.models import EquipmentAssignment, EquipmentMovement
from app.domains.equipment.models import Equipment, EquipmentCategory, EquipmentStatusEvent
from app.domains.organization.models import Organization, Person, Vehicle
from app.domains.inspections.models import (
    EquipmentCategoryTemplate,
    FieldVerification,
    Inspection,
    InspectionRequirement,
    InspectionResponse,
    InspectionTemplate,
    InspectionTemplateCheckpoint,
    InspectionTemplateSection,
    InspectionTemplateVersion,
)
from app.domains.worksites.models import Site, Worksite

__all__ = [
    "Equipment",
    "EquipmentAssignment",
    "EquipmentCategory",
    "EquipmentMovement",
    "EquipmentStatusEvent",
    "EquipmentCategoryTemplate",
    "FieldVerification",
    "Inspection",
    "InspectionRequirement",
    "InspectionResponse",
    "InspectionTemplate",
    "InspectionTemplateCheckpoint",
    "InspectionTemplateSection",
    "InspectionTemplateVersion",
    "Organization",
    "Person",
    "Site",
    "Vehicle",
    "Worksite",
]
