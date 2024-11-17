from pydantic import BaseModel

from schemas.base import BaseOrmSchema


class AddGoodToCartSchema(BaseModel):
    good_guid: str
    specification_guid: str
    quantity: str
    price: str


class GetCartSchema(BaseOrmSchema):
    outlet_guid: str
    goods: list[AddGoodToCartSchema]
