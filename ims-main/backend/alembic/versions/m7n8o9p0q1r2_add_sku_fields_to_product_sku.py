"""add sku_code spec sku_type to product_sku

Revision ID: m7n8o9p0q1r2
Revises: l6m7n8o9p0q1
Create Date: 2026-09-03
"""

from alembic import op
import sqlalchemy as sa

revision = "m7n8o9p0q1r2"
down_revision = "l6m7n8o9p0q1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("product_sku", sa.Column("sku_code", sa.String(50), nullable=True, comment="物料编码（U9编码）"))
    op.add_column("product_sku", sa.Column("spec", sa.String(100), nullable=True, comment="规格型号"))
    op.add_column(
        "product_sku",
        sa.Column("sku_type", sa.String(20), server_default="FINISHED_GOODS", nullable=False, comment="物料类型"),
    )
    op.create_unique_constraint("uq_product_sku_sku_code", "product_sku", ["sku_code"])


def downgrade():
    op.drop_constraint("uq_product_sku_sku_code", "product_sku", type_="unique")
    op.drop_column("product_sku", "sku_type")
    op.drop_column("product_sku", "spec")
    op.drop_column("product_sku", "sku_code")