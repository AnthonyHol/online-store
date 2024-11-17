from db.models import Good
from db.models.association import goods_carts
from db.models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Cart(BaseModel):
    outlet_guid: Mapped[str] = mapped_column(
        String(255), nullable=False, primary_key=True
    )

    goods: Mapped[list["Good"]] = relationship(
        "Good", secondary=goods_carts, back_populates="carts", lazy="selectin",
    )

    def add_good(
        self, good_guid: str, specification_guid: str, price_type_guid: str, quantity: int,
    ):
        association = goods_carts.insert().values(
            outlet_guid=self.outlet_guid,
            good_guid=good_guid,
            specification_guid=specification_guid,
            quantity=quantity,
            price_type_guid=price_type_guid,
        )

        return association

    def __repr__(self):
        return f"Cart(outlet_guid={self.outlet_guid})"
