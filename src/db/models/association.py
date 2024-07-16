from db.models.base import BaseModel
from sqlalchemy import ForeignKey, Table, Column


goods_specifications = Table(
    "goods_specs",
    BaseModel.metadata,
    Column("good_guid", ForeignKey("goods.guid"), primary_key=True),
    Column("specification_guid", ForeignKey("specifications.guid"), primary_key=True),
)
