from db.models.base import BaseModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.mixins import GUIDMixin


class Specification(BaseModel, GUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    good_guid: Mapped[str] = mapped_column(
        String(255), ForeignKey("goods.guid"), nullable=False
    )

    good: Mapped["Good"] = relationship(  # type: ignore # noqa: F821
        "Good",
        back_populates="specifications",
        foreign_keys="Specification.good_guid",
        lazy="selectin",
    )

    properties: Mapped[list["Property"]] = relationship(  # type: ignore # noqa: F821
        "Property",
        back_populates="specification",
        foreign_keys="Property.specification_guid",
        lazy="selectin",
    )
