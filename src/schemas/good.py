from pydantic import BaseModel

from core.enum import GoodTypesEnum
from schemas.base import BaseOrmSchema
from schemas.specification import SpecificationSchema


class GoodCreateSchema(BaseOrmSchema):
    guid: str
    name: str
    description: str = ""
    good_group_guid: str
    type: GoodTypesEnum = GoodTypesEnum.REGULAR

    filling: str = ""
    aroma: str = ""
    strength: str = ""
    format: str = ""
    manufacturing_method: str = ""
    package: str = ""
    block: str = ""
    box: str = ""
    producing_country: str = ""


class GoodWithSpecsCreateSchema(GoodCreateSchema):
    specifications: list[SpecificationSchema]


class GoodGetSchema(GoodCreateSchema):
    image_key: str | None


class GoodCardGetSchema(BaseOrmSchema):
    guid: str
    name: str
    type: GoodTypesEnum = GoodTypesEnum.REGULAR
    image_key: str | None


class GoodWithSpecsGetSchema(GoodGetSchema):
    specifications: list[SpecificationSchema]
    image_key: str | None


class ImageAddSchema(BaseModel):
    good_guid: str
    image: str


class GoodPageSchema(BaseModel):
    items: list[GoodCardGetSchema]
    page: int
    size: int
    pages: int
    total: int
