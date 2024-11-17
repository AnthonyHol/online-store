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
        "Good", secondary=goods_carts, back_populates="carts"
    )

    def add_good(
        self, good_guid: str, specification_guid: str, quantity: int, price: float
    ):
        association = goods_carts.insert().values(
            shopping_cart_guid=self.outlet_guid,
            good_guid=good_guid,
            specification_guid=specification_guid,
            quantity=quantity,
            price=price,
        )

        return association
