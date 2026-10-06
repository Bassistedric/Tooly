from __future__ import annotations

import enum
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class InspectionKind(str, enum.Enum):
    INTERNAL_PERIODIC = "INTERNAL_PERIODIC"
    EXTERNAL_PERIODIC = "EXTERNAL_PERIODIC"
    CALIBRATION = "CALIBRATION"
    PRE_USE = "PRE_USE"
    OTHER = "OTHER"


class InspectionOutcome(str, enum.Enum):
    COMPLIANT = "COMPLIANT"
    NOK = "NOK"
    QUARANTINE = "QUARANTINE"
    DECOMMISSIONED = "DECOMMISSIONED"
    NOT_INSPECTED = "NOT_INSPECTED"


class InspectionRequirement(Base):
    __tablename__ = "inspection_requirements"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), index=True)
    code: Mapped[str] = mapped_column(String(80), index=True)
    name: Mapped[str] = mapped_column(String(200))
    kind: Mapped[InspectionKind] = mapped_column(Enum(InspectionKind), index=True)
    interval_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    responsible: Mapped[str | None] = mapped_column(String(150), nullable=True)
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    warning_days: Mapped[int] = mapped_column(Integer, default=30)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    equipment = relationship("Equipment")


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), index=True)
    requirement_id: Mapped[int] = mapped_column(ForeignKey("inspection_requirements.id"), index=True)
    performed_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    outcome: Mapped[InspectionOutcome] = mapped_column(Enum(InspectionOutcome), index=True)
    performed_by: Mapped[str | None] = mapped_column(String(150), nullable=True)
    worksite_id: Mapped[int | None] = mapped_column(ForeignKey("worksites.id"), nullable=True, index=True)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    equipment = relationship("Equipment")
    requirement = relationship("InspectionRequirement")
    worksite = relationship("Worksite")


class FieldVerification(Base):
    __tablename__ = "field_verifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id"),
        index=True,
    )
    worksite_id: Mapped[int] = mapped_column(
        ForeignKey("worksites.id"),
        index=True,
    )
    verified_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    verified_by: Mapped[str | None] = mapped_column(String(150), nullable=True)
    control_in_order: Mapped[bool] = mapped_column(Boolean, default=True)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)

    equipment = relationship("Equipment")
    worksite = relationship("Worksite")
