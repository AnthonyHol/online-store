from core.enum import PropertyNamesEnum
from schemas.base import BaseOrmSchema


class PropertySchema(BaseOrmSchema):
    guid: str | None = None
    name: PropertyNamesEnum
