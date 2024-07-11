from core.enum import GoodTypesEnum
from db.models.base import BaseModel
from sqlalchemy import ForeignKey, String, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.mixins import GUIDMixin


class Good(BaseModel, GUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[GoodTypesEnum] = mapped_column(
        Enum(GoodTypesEnum), default=GoodTypesEnum.REGULAR, nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)

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
        back_populates="good",
        foreign_keys="Specification.good_guid",
        lazy="selectin",
    )
