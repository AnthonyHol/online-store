from core.enum import PropertyNamesEnum
from schemas.base import BaseOrmSchema


class BasePropertySchema(BaseOrmSchema):
    name: PropertyNamesEnum
    value: str = ""


class PropertyCreateSchema(BasePropertySchema):
    specification_guid: str


class PropertyBatchCreateSchema(BasePropertySchema): ...


class PropertyGetSchema(PropertyCreateSchema):
    guid: str
