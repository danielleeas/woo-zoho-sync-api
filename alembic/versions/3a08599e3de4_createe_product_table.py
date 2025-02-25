"""createe product table

Revision ID: 3a08599e3de4
Revises: dc04a2583ea9
Create Date: 2025-02-25 00:20:07.866180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '3a08599e3de4'
down_revision: Union[str, None] = 'dc04a2583ea9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("permalink", sa.String(), nullable=False, unique=True),
        sa.Column("date_created", sa.String(), nullable=False),
        sa.Column("date_modified", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False, default="simple"),
        sa.Column("status", sa.String(), nullable=False, default="publish"),
        sa.Column("featured", sa.Boolean(), nullable=False, default=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sku", sa.String(), nullable=True),
        sa.Column("price", sa.String(), nullable=False, default=0),
        sa.Column("purchase_price", sa.String(), nullable=False, default=0),
        sa.Column("regular_price", sa.String(), nullable=False, default=0),
        sa.Column("stock_quantity", sa.String(), nullable=False, default=0),
        sa.Column("weight", sa.String(), nullable=True),
        sa.Column("length", sa.String(), nullable=True),
        sa.Column("width", sa.String(), nullable=True),
        sa.Column("height", sa.String(), nullable=True),
        sa.Column("categories", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("images", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("attribute_name", sa.String(), nullable=True),
        sa.Column("attribute_value", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("products")
