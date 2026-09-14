"""create bom and production task tables for 主线D

Revision ID: t3u4v5w6x7y8
Revises: s2t3u4v5w6x7
Create Date: 2026-09-07 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "t3u4v5w6x7y8"
down_revision = "s2t3u4v5w6x7"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "bom_header",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("bom_no", sa.String(50), nullable=False, comment="BOM编号"),
        sa.Column("bom_name", sa.String(200), nullable=False, comment="BOM名称"),
        sa.Column("version", sa.String(20), nullable=False, comment="版本号"),
        sa.Column("product_sku_id", sa.Integer(), nullable=False, comment="成品物料ID"),
        sa.Column("product_sku_code", sa.String(50), nullable=False, comment="成品物料编码"),
        sa.Column("product_sku_name", sa.String(100), nullable=False, comment="成品物料名称"),
        sa.Column("plan_quantity", sa.Integer(), nullable=False, comment="计划生产数量"),
        sa.Column("status", sa.String(20), server_default=sa.text("'DRAFT'"), nullable=False, comment="状态"),
        sa.Column("remark", sa.Text(), nullable=True, comment="备注"),
        sa.Column("created_by", sa.String(50), nullable=False, comment="创建人"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("bom_no"),
    )
    op.create_index("ix_bom_header_bom_no", "bom_header", ["bom_no"])
    op.create_index("ix_bom_header_product_sku_id", "bom_header", ["product_sku_id"])

    op.create_table(
        "bom_detail",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("bom_id", sa.Integer(), nullable=False, comment="关联BOM主表"),
        sa.Column("material_sku_id", sa.Integer(), nullable=False, comment="原材料物料ID"),
        sa.Column("material_sku_code", sa.String(50), nullable=False, comment="原材料编码"),
        sa.Column("material_sku_name", sa.String(100), nullable=False, comment="原材料名称"),
        sa.Column("spec", sa.String(100), nullable=True, comment="规格"),
        sa.Column("unit", sa.String(10), nullable=False, comment="单位"),
        sa.Column("quantity_per_unit", sa.DECIMAL(10, 3), nullable=False, comment="单台用量"),
        sa.Column("wastage_rate", sa.DECIMAL(5, 2), nullable=True, comment="损耗率(%)"),
        sa.Column("remark", sa.Text(), nullable=True, comment="备注"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["bom_id"], ["bom_header.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["material_sku_id"], ["product_sku.id"]),
    )
    op.create_index("ix_bom_detail_bom_id", "bom_detail", ["bom_id"])

    op.create_table(
        "production_task",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("task_no", sa.String(50), nullable=False, comment="任务编号"),
        sa.Column("bom_id", sa.Integer(), nullable=False, comment="关联BOM"),
        sa.Column("plan_quantity", sa.Integer(), nullable=False, comment="计划生产数量"),
        sa.Column("material_availability", sa.String(20), server_default=sa.text("'SHORTAGE'"), nullable=False, comment="齐套状态"),
        sa.Column("status", sa.String(20), server_default=sa.text("'PENDING'"), nullable=False, comment="状态"),
        sa.Column("start_date", sa.Date(), nullable=True, comment="计划开始日期"),
        sa.Column("end_date", sa.Date(), nullable=True, comment="计划完成日期"),
        sa.Column("created_by", sa.String(50), nullable=False, comment="创建人"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("task_no"),
        sa.ForeignKeyConstraint(["bom_id"], ["bom_header.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_production_task_task_no", "production_task", ["task_no"])
    op.create_index("ix_production_task_bom_id", "production_task", ["bom_id"])


def downgrade():
    op.drop_index("ix_production_task_bom_id", table_name="production_task")
    op.drop_index("ix_production_task_task_no", table_name="production_task")
    op.drop_table("production_task")
    op.drop_index("ix_bom_detail_bom_id", table_name="bom_detail")
    op.drop_table("bom_detail")
    op.drop_index("ix_bom_header_product_sku_id", table_name="bom_header")
    op.drop_index("ix_bom_header_bom_no", table_name="bom_header")
    op.drop_table("bom_header")