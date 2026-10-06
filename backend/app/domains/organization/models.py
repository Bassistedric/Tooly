from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    organization_type: Mapped[str] = mapped_column(String(50), default="ENTITY")
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=True,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    parent: Mapped["Organization | None"] = relationship(
        remote_side=[id],
        back_populates="children",
    )
    children: Mapped[list["Organization"]] = relationship(
        back_populates="parent",
    )


class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        index=True,
    )
    employee_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )
    first_name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120), index=True)
    email: Mapped[str | None] = mapped_column(String(250), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization = relationship("Organization")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        index=True,
    )
    registration: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    assigned_person_id: Mapped[int | None] = mapped_column(
        ForeignKey("people.id"),
        nullable=True,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization = relationship("Organization")
    assigned_person = relationship("Person")
