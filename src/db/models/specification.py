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

    storages: Mapped[list["GoodStorage"]] = relationship(  # type: ignore # noqa: F821
        "GoodStorage",
        back_populates="specification",
        foreign_keys="GoodStorage.specification_guid",
        lazy="selectin",
    )

    prices: Mapped[list["Price"]] = relationship(  # type: ignore # noqa: F821
        "Price",
        back_populates="specification",
        foreign_keys="Price.specification_guid",
        lazy="selectin",
    )
