from fastapi import Depends

from core.exceptions import cart_not_found_exception, no_good_exception, good_not_found_exception
from db.models import Cart
from db.repositories.cart import CartRepository
from db.repositories.good import GoodRepository
from schemas.cart import AddGoodToCartSchema


class CartService:
    def __init__(
        self,
        cart_repository: CartRepository = Depends(),
        good_repository: GoodRepository = Depends(),
    ):
        self._cart_repository = cart_repository
        self._good_repository = good_repository

    async def add_good(self, outlet_guid: str, data: AddGoodToCartSchema) -> Cart:
        good = await self._good_repository.get_by_guid(guid=data.good_guid)

        if not good:
            raise good_not_found_exception

        if not good.storages:
            raise no_good_exception

        for storage in good.storages:
            if (
                storage.specification_guid == data.specification_guid
                and storage.in_stock < data.quantity
            ):
                raise no_good_exception

        cart = await self._cart_repository.get_cart_by_outlet_guid(
            outlet_guid=outlet_guid
        )

        if not cart:
            cart = await self._cart_repository.create(outlet_guid=outlet_guid)

        cart.add_good(**data.model_dump())

        return cart

    async def get_cart(self, outlet_guid: str) -> Cart:
        cart = await self._cart_repository.get_cart_by_outlet_guid(
            outlet_guid=outlet_guid
        )

        if not cart:
            raise cart_not_found_exception

        return cart
