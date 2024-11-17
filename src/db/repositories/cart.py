from db.models import Cart
from db.repositories.base import BaseDatabaseRepository
from schemas.cart import AddGoodToCartSchema


class CartRepository(BaseDatabaseRepository):
    async def create(self, outlet_guid: str) -> Cart:
        cart = Cart(outlet_guid=outlet_guid)  # type: ignore
        self._session.add(cart)
        await self._session.flush()

        return cart

    async def get_cart_by_outlet_guid(self, outlet_guid: str) -> Cart | None:
        return await self._session.get(Cart, outlet_guid)

    async def add_good(self, cart: Cart, data: AddGoodToCartSchema) -> None:
        await self._session.execute(cart.add_good(**data.model_dump()))
        await self._session.flush()
