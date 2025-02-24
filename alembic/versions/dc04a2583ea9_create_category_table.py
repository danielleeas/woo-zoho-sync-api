"""create category table

Revision ID: dc04a2583ea9
Revises: 7da3993d5f3a
Create Date: 2025-02-24 07:23:59.568256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'dc04a2583ea9'
down_revision: Union[str, None] = '7da3993d5f3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("woo_id", sa.Integer(), nullable=False),
        sa.Column("woo_parent_id", sa.Integer(), nullable=False),
        sa.Column("zoho_id", sa.String(), nullable=False),
        sa.Column("zoho_parent_id", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("categories")
