"""add replaced_by_sn, replaced_from_sn, current_location to inventory_item

Revision ID: o9p0q1r2s3t4
Revises: n8o9p0q1r2s3
Create Date: 2026-09-04 10:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "o9p0q1r2s3t4"
down_revision = "n8o9p0q1r2s3"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("inventory_item", sa.Column("replaced_by_sn", sa.String(length=50), nullable=True, comment="如果已替换，指向新 SN"))
    op.add_column("inventory_item", sa.Column("replaced_from_sn", sa.String(length=50), nullable=True, comment="如果是维修后新 SN，指向旧 SN"))
    op.add_column(
        "inventory_item",
        sa.Column("current_location", sa.String(length=50), nullable=False, server_default="库房", comment="库房/已发出/维修中/已报废"),
    )


def downgrade():
    op.drop_column("inventory_item", "current_location")
    op.drop_column("inventory_item", "replaced_from_sn")
    op.drop_column("inventory_item", "replaced_by_sn")