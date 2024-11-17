from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import cart_not_found_exception, no_good_exception, good_not_found_exception
from db.models import Cart
from db.repositories.cart import CartRepository
from db.repositories.good import GoodRepository
from db.session import get_session
from schemas.cart import AddGoodToCartSchema, GetCartSchema
from services.good import GoodService
from services.price_type import PriceTypeService


class CartService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        cart_repository: CartRepository = Depends(),
        good_service: GoodService = Depends(),
        price_type_service: PriceTypeService = Depends(),
    ):
        self._session = session

        self._cart_repository = cart_repository
        self._good_service = good_service
        self._price_type_service = price_type_service

    async def add_good(self, outlet_guid: str, data: AddGoodToCartSchema) -> Cart:
        good = await self._good_service.get_by_guid(guid=data.good_guid)
        await self._good_service.check_association_with_specification(good_guid=data.good_guid,
                                                                      specification_guid=data.specification_guid)
        await self._price_type_service.get_by_guid(guid=data.price_type_guid)

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

        await self._cart_repository.add_good(cart=cart, data=data)
        await self._session.commit()

        return cart

    async def get_cart(self, outlet_guid: str) -> GetCartSchema:
        cart = await self._cart_repository.get_cart_by_outlet_guid(
            outlet_guid=outlet_guid
        )

        if not cart:
            raise cart_not_found_exception

        total_cost = sum([good.prices[0].value for good in cart.goods])

        cart_schema = GetCartSchema(
            outlet_guid=outlet_guid,
            goods=cart.goods,
            total_cost=total_cost
        )

        return cart_schema
