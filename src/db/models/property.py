from core.enum import PropertyNamesEnum
from db.models.base import BaseModel
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.mixins import GUIDMixin


class Property(BaseModel, GUIDMixin):
    name: Mapped[PropertyNamesEnum] = mapped_column(
        Enum(PropertyNamesEnum), nullable=False
    )

    specification_guid: Mapped[str] = mapped_column(
        String(255), ForeignKey("specifications.guid"), nullable=False
    )
    specification: Mapped["Specification"] = relationship(  # type: ignore # noqa: F821
        "Specification",
        back_populates="properties",
        foreign_keys="Property.specification_guid",
        lazy="selectin",
    )
