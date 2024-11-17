from fastapi import APIRouter, status, Depends, Request

from db.models import Cart
from schemas.cart import AddGoodToCartSchema, GetCartSchema, GetBaseCartSchema
from schemas.outlet import OutletSchema
from services.cart import CartService
from services.outlet import OutletService


router = APIRouter(prefix="/outlets", tags=["Торговый точки"])


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[OutletSchema],
)
async def create_auth_session(
    request: Request,
    outlet_service: OutletService = Depends(),
) -> list[OutletSchema]:
    return await outlet_service.get_by_token(token=request.cookies.get("token"))


@router.get(
    "/{outlet_guid}/carts", status_code=status.HTTP_200_OK, response_model=GetCartSchema
)
async def get_cart_by_outlet_guid(
    outlet_guid: str,
    cart_service: CartService = Depends()
) -> GetCartSchema:
    return await cart_service.get_cart(outlet_guid=outlet_guid)


@router.post(
    "/{outlet_guid}/carts",
    status_code=status.HTTP_201_CREATED,
    response_model=GetBaseCartSchema,
)
async def add_product_to_cart(
    outlet_guid: str, data: AddGoodToCartSchema, cart_service: CartService = Depends()
) -> Cart:
    return await cart_service.add_good(outlet_guid=outlet_guid, data=data)
