"""add warehouse_type to rma_warehouse_in

Revision ID: u7v8w9x0y1z2
Revises: c1d2e3f4g5h6
Create Date: 2026-09-08
"""
from alembic import op
import sqlalchemy as sa

revision = 'u7v8w9x0y1z2'
down_revision = 'c1d2e3f4g5h6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('rma_warehouse_in', sa.Column('warehouse_type', sa.String(30), nullable=False, server_default='ZERO_COST_FINISHED', comment='入库仓库类型：ZERO_COST_FINISHED/ZERO_COST_SEMI'))


def downgrade():
    op.drop_column('rma_warehouse_in', 'warehouse_type')