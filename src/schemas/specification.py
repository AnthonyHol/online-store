from schemas.base import BaseOrmSchema
from schemas.property import PropertyGetSchema, BasePropertySchema


class SpecificationCreateOrUpdateSchema(BaseOrmSchema):
    guid: str
    name: str


class SpecificationWithPropertiesCreateSchema(SpecificationCreateOrUpdateSchema):
    properties: list[BasePropertySchema]


class SpecificationWithPropertiesGetSchema(SpecificationCreateOrUpdateSchema):
    properties: list[PropertyGetSchema]
