"""Init models

Revision ID: 3d56f697d37c
Revises:
Create Date: 2024-07-22 14:17:06.125031

"""

from alembic import op
import sqlalchemy as sa

import db

# revision identifiers, used by Alembic.
revision: str | None = "3d56f697d37c"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "good_groups",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("parent_group_guid", sa.String(length=255), nullable=True),
        sa.Column("guid", db.models.mixins.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parent_group_guid"],
            ["good_groups.guid"],
            name=op.f("good_groups_parent_group_guid_fkey"),
        ),
        sa.PrimaryKeyConstraint("guid", name=op.f("good_groups_pkey")),
    )
    op.create_table(
        "specifications",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("guid", db.models.mixins.GUID(), nullable=False),
        sa.PrimaryKeyConstraint("guid", name=op.f("specifications_pkey")),
    )
    op.create_table(
        "goods",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "type",
            sa.Enum("NEW", "REGULAR", "HIT", name="goodtypesenum"),
            nullable=False,
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("filling", sa.String(length=255), nullable=True),
        sa.Column("aroma", sa.String(length=255), nullable=True),
        sa.Column("strength", sa.String(length=255), nullable=True),
        sa.Column("format", sa.String(length=255), nullable=True),
        sa.Column("manufacturing_method", sa.String(length=255), nullable=False),
        sa.Column("package", sa.String(length=255), nullable=True),
        sa.Column("block", sa.String(length=255), nullable=True),
        sa.Column("box", sa.String(length=255), nullable=True),
        sa.Column("producing_country", sa.String(length=255), nullable=True),
        sa.Column("image_key", sa.Text(), nullable=True),
        sa.Column("good_group_guid", sa.String(length=255), nullable=False),
        sa.Column("guid", db.models.mixins.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["good_group_guid"],
            ["good_groups.guid"],
            name=op.f("goods_good_group_guid_fkey"),
        ),
        sa.PrimaryKeyConstraint("guid", name=op.f("goods_pkey")),
    )
    op.create_table(
        "goods_specs",
        sa.Column("good_guid", db.models.mixins.GUID(), nullable=True),
        sa.Column("specification_guid", db.models.mixins.GUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["good_guid"], ["goods.guid"], name=op.f("goods_specs_good_guid_fkey")
        ),
        sa.ForeignKeyConstraint(
            ["specification_guid"],
            ["specifications.guid"],
            name=op.f("goods_specs_specification_guid_fkey"),
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("goods_specs")
    op.drop_table("goods")
    op.drop_table("specifications")
    op.drop_table("good_groups")
    # ### end Alembic commands ###