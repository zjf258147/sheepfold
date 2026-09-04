"""create raw_material_inventory, raw_material_sn, raw_material_inventory_log

Revision ID: p0q1r2s3t4u5
Revises: o9p0q1r2s3t4
Create Date: 2026-09-04 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "p0q1r2s3t4u5"
down_revision = "o9p0q1r2s3t4"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "raw_material_inventory",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sku_id", sa.Integer(), nullable=False, comment="物料 SKU ID"),
        sa.Column("batch_no", sa.String(length=50), nullable=False, comment="批次号"),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0", comment="库存数量"),
        sa.Column("unit", sa.String(length=20), nullable=False, server_default="个", comment="单位"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="IN_STOCK", comment="库存状态"),
        sa.Column("supplier_id", sa.Integer(), nullable=True, comment="供应商 ID"),
        sa.Column("receipt_no", sa.String(length=50), nullable=True, comment="关联到货单号"),
        sa.Column("remark", sa.Text(), nullable=True, comment="备注"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["sku_id"], ["product_sku.id"]),
        sa.ForeignKeyConstraint(["supplier_id"], ["partner.id"]),
    )
    op.create_index("ix_raw_material_inventory_sku_id", "raw_material_inventory", ["sku_id"])
    op.create_index("ix_raw_material_inventory_batch_no", "raw_material_inventory", ["batch_no"])
    op.create_index("ix_raw_material_inventory_supplier_id", "raw_material_inventory", ["supplier_id"])

    op.create_table(
        "raw_material_sn",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("inventory_id", sa.Integer(), nullable=False, comment="库存批次 ID"),
        sa.Column("sn", sa.String(length=100), nullable=False, comment="原材料 SN 号"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="IN_STOCK", comment="SN 状态"),
        sa.Column("remark", sa.Text(), nullable=True, comment="备注"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["inventory_id"], ["raw_material_inventory.id"]),
    )
    op.create_index("ix_raw_material_sn_inventory_id", "raw_material_sn", ["inventory_id"])
    op.create_index("ix_raw_material_sn_sn", "raw_material_sn", ["sn"])

    op.create_table(
        "raw_material_inventory_log",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("inventory_id", sa.Integer(), nullable=False, comment="库存批次 ID"),
        sa.Column("sn_id", sa.Integer(), nullable=True, comment="SN ID（按 SN 扣减时记录）"),
        sa.Column("change_type", sa.String(length=20), nullable=False, comment="INCREASE / DECREASE"),
        sa.Column("change_qty", sa.Integer(), nullable=False, comment="变更数量"),
        sa.Column("before_qty", sa.Integer(), nullable=False, comment="变更前数量"),
        sa.Column("after_qty", sa.Integer(), nullable=False, comment="变更后数量"),
        sa.Column("change_reason", sa.String(length=255), nullable=True, comment="变更原因"),
        sa.Column("related_order_no", sa.String(length=50), nullable=True, comment="关联单号"),
        sa.Column("operator_id", sa.Integer(), nullable=True, comment="操作人 ID"),
        sa.Column("remark", sa.Text(), nullable=True, comment="备注"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="操作时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["inventory_id"], ["raw_material_inventory.id"]),
        sa.ForeignKeyConstraint(["sn_id"], ["raw_material_sn.id"]),
        sa.ForeignKeyConstraint(["operator_id"], ["sys_user.id"]),
    )
    op.create_index("ix_raw_material_inventory_log_inventory_id", "raw_material_inventory_log", ["inventory_id"])


def downgrade():
    op.drop_table("raw_material_inventory_log")
    op.drop_table("raw_material_sn")
    op.drop_table("raw_material_inventory")