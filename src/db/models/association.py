from db.models.base import BaseModel
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Float

goods_specifications = Table(
    "goods_specs",
    BaseModel.metadata,
    Column("good_guid", ForeignKey("goods.guid")),
    Column("specification_guid", ForeignKey("specifications.guid")),
)

goods_carts = (Table(
    "goods_carts",
    BaseModel.metadata,
    Column("good_guid", String(255), ForeignKey("goods.guid"), nullable=False),
    Column("specification_guid", ForeignKey("specifications.guid"), nullable=False),
    Column("outlet_guid", String(255), ForeignKey("carts.outlet_guid"), nullable=False),
    Column("price_type_guid", ForeignKey("price_types.guid"), nullable=False),
    Column("quantity", Integer, nullable=False))
)
