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


class InspectionTemplate(Base):
    __tablename__ = "inspection_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    versions = relationship("InspectionTemplateVersion", back_populates="template")


class InspectionTemplateVersion(Base):
    __tablename__ = "inspection_template_versions"

    id: Mapped[int] = mapped_column(primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("inspection_templates.id"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(250))
    reminders: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_reference: Mapped[str | None] = mapped_column(String(250), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

    template = relationship("InspectionTemplate", back_populates="versions")
    sections = relationship(
        "InspectionTemplateSection",
        back_populates="template_version",
        order_by="InspectionTemplateSection.position",
    )


class InspectionTemplateSection(Base):
    __tablename__ = "inspection_template_sections"

    id: Mapped[int] = mapped_column(primary_key=True)
    template_version_id: Mapped[int] = mapped_column(
        ForeignKey("inspection_template_versions.id"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200))
    position: Mapped[int] = mapped_column(Integer)

    template_version = relationship("InspectionTemplateVersion", back_populates="sections")
    checkpoints = relationship(
        "InspectionTemplateCheckpoint",
        back_populates="section",
        order_by="InspectionTemplateCheckpoint.position",
    )


class InspectionTemplateCheckpoint(Base):
    __tablename__ = "inspection_template_checkpoints"

    id: Mapped[int] = mapped_column(primary_key=True)
    section_id: Mapped[int] = mapped_column(
        ForeignKey("inspection_template_sections.id"),
        index=True,
    )
    position: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    allows_na: Mapped[bool] = mapped_column(Boolean, default=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)

    section = relationship("InspectionTemplateSection", back_populates="checkpoints")
