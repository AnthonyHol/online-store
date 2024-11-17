from core.enum import GoodTypesEnum
from db.models.association import goods_specifications, goods_carts
from db.models.base import BaseModel
from sqlalchemy import ForeignKey, String, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.mixins import GUIDMixin


class Good(BaseModel, GUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[GoodTypesEnum] = mapped_column(
        Enum(GoodTypesEnum), default=GoodTypesEnum.REGULAR, nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    filling: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    aroma: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    strength: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    format: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    manufacturing_method: Mapped[str] = mapped_column(
        String(255), nullable=False, default=""
    )
    package: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    block: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    box: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    producing_country: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    image_key: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    good_group_guid: Mapped[str] = mapped_column(
        String(255), ForeignKey("good_groups.guid"), nullable=False
    )

    good_group: Mapped["GoodGroup"] = relationship(  # type: ignore # noqa: F821
        "GoodGroup",
        back_populates="goods",
        foreign_keys="Good.good_group_guid",
        lazy="selectin",
    )

    specifications: Mapped[list["Specification"]] = relationship(  # type: ignore # noqa: F821
        "Specification",
        secondary=goods_specifications,
        back_populates="goods",
        lazy="selectin",
    )

    storages: Mapped[list["GoodStorage"]] = relationship(  # type: ignore # noqa: F821
        "GoodStorage",
        back_populates="good",
        foreign_keys="GoodStorage.good_guid",
        lazy="selectin",
    )

    prices: Mapped[list["Price"]] = relationship(  # type: ignore # noqa: F821
        "Price",
        back_populates="good",
        foreign_keys="Price.good_guid",
        lazy="selectin",
    )

    carts: Mapped[list["Cart"]] = relationship(  # type: ignore # noqa: F821
        "Cart", secondary=goods_carts, back_populates="goods"
    )

    def __repr__(self):
        return f"Good(guid={self.guid}, name='{self.name}', prices={self.prices})>"
