from schemas.base import BaseOrmSchema
from schemas.property import PropertySchema


class SpecificationSchema(BaseOrmSchema):
    guid: str
    name: str
    properties: list[PropertySchema]
