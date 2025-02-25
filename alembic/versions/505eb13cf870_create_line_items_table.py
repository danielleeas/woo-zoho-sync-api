"""create line_items table

Revision ID: 505eb13cf870
Revises: fa8b105e1876
Create Date: 2025-02-25 06:51:21.374296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '505eb13cf870'
down_revision: Union[str, None] = 'fa8b105e1876'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'line_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('order_id', sa.Integer(), nullable=True, index=True),
        sa.Column('name', sa.String(), nullable=False, index=True),
        sa.Column('product_id', sa.Integer(), nullable=False, index=True),
        sa.Column('variation_id', sa.Integer(), nullable=False, default=0),
        sa.Column('quantity', sa.Integer(), nullable=False, default=1),
        sa.Column('tax_class', sa.String(), nullable=True),
        sa.Column('subtotal', sa.String(), nullable=True),
        sa.Column('subtotal_tax', sa.String(), nullable=True),
        sa.Column('total', sa.String(), nullable=True),
        sa.Column('total_tax', sa.String(), nullable=True),
        sa.Column('sku', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False, default=0),
    )


def downgrade() -> None:
    op.drop_table('line_items')
