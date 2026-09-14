"""merge warehouse_type and bom_shipment heads

Revision ID: 9fde5cf8e567
Revises: 061337f81d29, u7v8w9x0y1z2
Create Date: 2026-09-08 18:16:48.244094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fde5cf8e567'
down_revision = ('061337f81d29', 'u7v8w9x0y1z2')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
