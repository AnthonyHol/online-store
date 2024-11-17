from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import aliased

from db.models import Cart, Good
from db.models.association import goods_carts
from db.repositories.base import BaseDatabaseRepository
from schemas.cart import AddGoodToCartSchema


class CartRepository(BaseDatabaseRepository):
    async def create(self, outlet_guid: str) -> Cart:
        cart = Cart(outlet_guid=outlet_guid)  # type: ignore
        self._session.add(cart)
        await self._session.flush()

        return cart

    async def get_cart_by_outlet_guid(self, outlet_guid: str) -> Cart | None:
        goods_carts_alias = aliased(goods_carts)

        query = (
            select(Cart, goods_carts_alias.c.price_type_guid, goods_carts_alias.c.quantity)
            .join(goods_carts_alias, Cart.outlet_guid == goods_carts_alias.c.outlet_guid)
            .where(Cart.outlet_guid == outlet_guid)
        )

        query_result = await self._session.execute(query)
        results = query_result.fetchall()

        if not results:
            return None

        cart, *_ = results[0]

        return cart

    async def add_good(self, cart: Cart, data: AddGoodToCartSchema) -> None:
        await self._session.execute(cart.add_good(**data.model_dump()))
        await self._session.flush()

