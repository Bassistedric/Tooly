from __future__ import annotations

import enum
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EquipmentOperationalStatus(str, enum.Enum):
    IN_SERVICE = "IN_SERVICE"
    IN_STOCK = "IN_STOCK"
    ASSIGNED = "ASSIGNED"
    IN_REPAIR = "IN_REPAIR"
    QUARANTINE = "QUARANTINE"
    TO_LOCATE = "TO_LOCATE"
    LOST = "LOST"
    STOLEN = "STOLEN"
    DECOMMISSIONED = "DECOMMISSIONED"


class EquipmentComplianceStatus(str, enum.Enum):
    COMPLIANT = "COMPLIANT"
    DUE_SOON = "DUE_SOON"
    OVERDUE = "OVERDUE"
    NOK = "NOK"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    TO_VERIFY = "TO_VERIFY"


class EquipmentCategory(Base):
    __tablename__ = "equipment_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name_key: Mapped[str] = mapped_column(String(150))
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("equipment_categories.id"),
        nullable=True,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    parent: Mapped["EquipmentCategory | None"] = relationship(
        remote_side=[id],
        back_populates="children",
    )
    children: Mapped[list["EquipmentCategory"]] = relationship(
        back_populates="parent",
    )


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)

    business_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )
    serial_number: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        index=True,
    )
    external_number: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        index=True,
    )

    description: Mapped[str] = mapped_column(String(250))
    brand: Mapped[str | None] = mapped_column(String(120), nullable=True)
    model: Mapped[str | None] = mapped_column(String(150), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        index=True,
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("equipment_categories.id"),
        nullable=True,
        index=True,
    )

    manufacture_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    commissioned_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    operational_status: Mapped[EquipmentOperationalStatus] = mapped_column(
        Enum(EquipmentOperationalStatus),
        default=EquipmentOperationalStatus.IN_STOCK,
    )
    compliance_status: Mapped[EquipmentComplianceStatus] = mapped_column(
        Enum(EquipmentComplianceStatus),
        default=EquipmentComplianceStatus.TO_VERIFY,
    )

    qr_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    qr_installed: Mapped[bool] = mapped_column(Boolean, default=False)
    qr_installed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    organization = relationship("Organization")
    category = relationship("EquipmentCategory")


class EquipmentStatusEvent(Base):
    __tablename__ = "equipment_status_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    event_type: Mapped[str] = mapped_column(String(50), index=True)
    from_status: Mapped[str] = mapped_column(String(50))
    to_status: Mapped[str] = mapped_column(String(50))
    performed_by: Mapped[str] = mapped_column(String(150))
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    equipment = relationship("Equipment")
