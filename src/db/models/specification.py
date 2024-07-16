from db.models.association import goods_specifications
from db.models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.mixins import GUIDMixin


class Specification(BaseModel, GUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    goods: Mapped[list["Good"]] = relationship(  # type: ignore # noqa: F821
        "Good",
        secondary=goods_specifications,
        back_populates="specifications",
        lazy="selectin",
    )

    properties: Mapped[list["Property"]] = relationship(  # type: ignore # noqa: F821
        "Property",
        back_populates="specification",
        foreign_keys="Property.specification_guid",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
