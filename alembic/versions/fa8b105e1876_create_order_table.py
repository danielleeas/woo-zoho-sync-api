"""create order table

Revision ID: fa8b105e1876
Revises: 1ece428a8a4a
Create Date: 2025-02-25 06:39:50.365260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa8b105e1876'
down_revision: Union[str, None] = '1ece428a8a4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, nullable=True, index=True),
        sa.Column('status', sa.String, nullable=True),
        sa.Column('customer_id', sa.Integer, nullable=True),
        sa.Column('currency', sa.String, nullable=True),
        sa.Column('prices_include_tax', sa.Boolean, nullable=True, default=True),
        sa.Column('discount_total', sa.String, nullable=True),
        sa.Column('discount_tax', sa.String, nullable=True),
        sa.Column('shipping_total', sa.String, nullable=True),
        sa.Column('shipping_tax', sa.String, nullable=True),
        sa.Column('cart_tax', sa.String, nullable=True),
        sa.Column('total', sa.String, nullable=True),
        sa.Column('total_tax', sa.String, nullable=True),
        sa.Column('order_key', sa.String, nullable=True),
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
        sa.Column('shipping_state', sa.String, nullable=True),
        sa.Column('shipping_postcode', sa.String, nullable=True),
        sa.Column('shipping_country', sa.String, nullable=True),
        sa.Column('payment_method', sa.String, nullable=True),
        sa.Column('payment_method_title', sa.String, nullable=True),
        sa.Column('transaction_id', sa.String, nullable=True),
        sa.Column('customer_ip_address', sa.String, nullable=True),
        sa.Column('customer_user_agent', sa.String, nullable=True),
        sa.Column('created_via', sa.String, nullable=True),
        sa.Column('customer_note', sa.String, nullable=True),
        sa.Column('date_completed', sa.String, nullable=True),
        sa.Column('date_created', sa.String, nullable=True),
        sa.Column('date_modified', sa.String, nullable=True),
        sa.Column('date_paid', sa.String, nullable=True),
        sa.Column('cart_hash', sa.String, nullable=True),
        sa.Column('number', sa.String, nullable=True),
        sa.Column('payment_url', sa.String, nullable=True),
        sa.Column('currency_symbol', sa.String, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('orders')
