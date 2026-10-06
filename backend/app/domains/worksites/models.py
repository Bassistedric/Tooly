from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        index=True,
    )
    code: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[str | None] = mapped_column(String(300), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization = relationship("Organization")


class Worksite(Base):
    __tablename__ = "worksites"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        index=True,
    )
    site_id: Mapped[int | None] = mapped_column(
        ForeignKey("sites.id"),
        nullable=True,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(80), index=True)
    name: Mapped[str] = mapped_column(String(250))
    address: Mapped[str | None] = mapped_column(String(300), nullable=True)
    customer: Mapped[str | None] = mapped_column(String(200), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization = relationship("Organization")
    site = relationship("Site")
