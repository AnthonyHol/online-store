from db.models.base import BaseModel
from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship



class GoodStorage(BaseModel):
    in_stock: Mapped[int] = mapped_column(Integer, nullable=False)

    good_guid: Mapped[str] = mapped_column(
        String(255), ForeignKey("goods.guid"), nullable=False, primary_key=True
    )
    specification_guid: Mapped[str] = mapped_column(
        String(255), ForeignKey("specifications.guid"), nullable=False, primary_key=True
    )

    good: Mapped["Good"] = relationship(  # type: ignore # noqa: F821
        "Good",
        back_populates="storages",
        foreign_keys="GoodStorage.good_guid",
        lazy="selectin",
    )

    specification: Mapped["Specification"] = relationship(  # type: ignore # noqa: F821
        "Specification",
        foreign_keys="GoodStorage.specification_guid",
        back_populates="storages",
        lazy="selectin",
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            "good_guid", "specification_guid", name="good_spec_constraint"
        ),
    )
