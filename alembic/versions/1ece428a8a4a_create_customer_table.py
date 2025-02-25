"""create customer table

Revision ID: 1ece428a8a4a
Revises: 3a08599e3de4
Create Date: 2025-02-25 06:16:46.051515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ece428a8a4a'
down_revision: Union[str, None] = '3a08599e3de4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('woo_id', sa.Integer, nullable=False),
        sa.Column('first_name', sa.String, nullable=True),
        sa.Column('last_name', sa.String, nullable=True),
        sa.Column('username', sa.String, nullable=True),
        sa.Column('email', sa.String, nullable=True),
        sa.Column('billing_first_name', sa.String, nullable=True),
        sa.Column('billing_last_name', sa.String, nullable=True),
        sa.Column('billing_company', sa.String, nullable=True),
        sa.Column('billing_address_1', sa.String, nullable=True),
        sa.Column('billing_address_2', sa.String, nullable=True),
        sa.Column('billing_city', sa.String, nullable=True),
        sa.Column('billing_postcode', sa.String, nullable=True),
        sa.Column('billing_country', sa.String, nullable=True),
        sa.Column('billing_state', sa.String, nullable=True),
        sa.Column('billing_email', sa.String, nullable=True),
        sa.Column('billing_phone', sa.String, nullable=True),
        sa.Column('shipping_first_name', sa.String, nullable=True),
        sa.Column('shipping_last_name', sa.String, nullable=True),
        sa.Column('shipping_company', sa.String, nullable=True),
        sa.Column('shipping_address_1', sa.String, nullable=True),
        sa.Column('shipping_address_2', sa.String, nullable=True),
        sa.Column('shipping_city', sa.String, nullable=True),
        sa.Column('shipping_postcode', sa.String, nullable=True),
        sa.Column('shipping_country', sa.String, nullable=True),
        sa.Column('shipping_state', sa.String, nullable=True),
        sa.Column('shipping_phone', sa.String, nullable=True),
        sa.Column('is_paying_customer', sa.Boolean, nullable=True),
        sa.Column('avatar_url', sa.String, nullable=True),
        sa.Column('created_at', sa.String, nullable=True),
        sa.Column('updated_at', sa.String, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('customers')
