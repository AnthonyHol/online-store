from pydantic import BaseModel

from schemas.base import BaseOrmSchema
from schemas.good import GoodCardGetSchema, GoodCartCardGetSchema


class AddGoodToCartSchema(BaseModel):
    good_guid: str
    specification_guid: str
    price_type_guid: str
    quantity: int


class GetGoodCartSchema(BaseModel):
    good_guid: str
    specification_guid: str
    price: float
    quantity: int


class GetBaseCartSchema(BaseOrmSchema):
    outlet_guid: str


class GetCartSchema(GetBaseCartSchema):
    total_cost: float
    goods: list[GoodCartCardGetSchema]
