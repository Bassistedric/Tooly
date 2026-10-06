from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AssignmentTargetType(str, enum.Enum):
    SITE = "SITE"
    WORKSITE = "WORKSITE"
    VEHICLE = "VEHICLE"
    PERSON = "PERSON"
    STOCK = "STOCK"
    WORKSHOP = "WORKSHOP"
    ROOM = "ROOM"
    QUARANTINE = "QUARANTINE"
    OTHER = "OTHER"


class EquipmentAssignment(Base):
    __tablename__ = "equipment_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id"),
        index=True,
    )
    target_type: Mapped[AssignmentTargetType] = mapped_column(
        Enum(AssignmentTargetType),
        index=True,
    )
    target_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    target_label: Mapped[str] = mapped_column(String(250))
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )
    released_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )
    assigned_by: Mapped[str | None] = mapped_column(String(150), nullable=True)
    requested_by: Mapped[str | None] = mapped_column(String(150), nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)

    equipment = relationship("Equipment")


class EquipmentMovement(Base):
    __tablename__ = "equipment_movements"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id"),
        index=True,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )

    from_type: Mapped[AssignmentTargetType | None] = mapped_column(
        Enum(AssignmentTargetType),
        nullable=True,
    )
    from_id: Mapped[int | None] = mapped_column(nullable=True)
    from_label: Mapped[str | None] = mapped_column(String(250), nullable=True)

    to_type: Mapped[AssignmentTargetType] = mapped_column(
        Enum(AssignmentTargetType)
    )
    to_id: Mapped[int | None] = mapped_column(nullable=True)
    to_label: Mapped[str] = mapped_column(String(250))

    recorded_by: Mapped[str | None] = mapped_column(String(150), nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)

    equipment = relationship("Equipment")
