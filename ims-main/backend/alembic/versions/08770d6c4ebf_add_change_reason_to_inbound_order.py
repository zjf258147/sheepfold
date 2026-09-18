"""add change_reason to inbound_order

Revision ID: 08770d6c4ebf
Revises: bd138515121c
Create Date: 2026-09-18 13:37:03.017744

"""
from alembic import op
import sqlalchemy as sa


revision = '08770d6c4ebf'
down_revision = 'bd138515121c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('inbound_order', sa.Column('change_reason', sa.String(length=255), nullable=True, comment='变更原因'))


def downgrade():
    op.drop_column('inbound_order', 'change_reason')