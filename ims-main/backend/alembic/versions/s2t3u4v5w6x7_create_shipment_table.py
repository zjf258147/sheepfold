"""create shipment table for 主线C

Revision ID: s2t3u4v5w6x7
Revises: r1s2t3u4v5w6
Create Date: 2026-09-07 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "s2t3u4v5w6x7"
down_revision = "c1d2e3f4g5h6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "shipment",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("shipment_no", sa.String(50), nullable=False, comment="出货单号 SH"),
        sa.Column("sku_id", sa.Integer(), nullable=False, comment="物料ID"),
        sa.Column("sku_code", sa.String(50), nullable=False, comment="物料编码（U9编码）"),
        sa.Column("sku_name", sa.String(100), nullable=False, comment="物料名称"),
        sa.Column("spec", sa.String(100), nullable=True, comment="规格型号"),
        sa.Column("unit", sa.String(10), nullable=False, server_default=sa.text("'个'"), comment="单位"),
        sa.Column("sn_list", sa.JSON(), nullable=False, comment="出货SN列表"),
        sa.Column("quantity", sa.Integer(), nullable=False, comment="数量"),
        sa.Column("ship_date", sa.Date(), nullable=False, comment="发货日期"),
        sa.Column("address", sa.Text(), nullable=False, comment="收货地址"),
        sa.Column("logistics_provider", sa.String(50), nullable=False, comment="物流供应商"),
        sa.Column("tracking_no", sa.String(50), nullable=False, comment="快递单号"),
        sa.Column("u9_task_no", sa.String(50), nullable=True, comment="U9任务单号"),
        sa.Column("tf_version", sa.String(30), nullable=True, comment="TF卡版本号"),
        sa.Column("host_version", sa.String(30), nullable=True, comment="上位机版本号"),
        sa.Column("remark", sa.Text(), nullable=True, comment="备注"),
        sa.Column("created_by", sa.String(50), nullable=False, comment="创建人"),
        sa.Column("change_reason", sa.String(255), nullable=True, comment="变更原因"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("shipment_no"),
    )
    op.create_index("ix_shipment_shipment_no", "shipment", ["shipment_no"])
    op.create_index("ix_shipment_sku_id", "shipment", ["sku_id"])


def downgrade():
    op.drop_index("ix_shipment_sku_id", table_name="shipment")
    op.drop_index("ix_shipment_shipment_no", table_name="shipment")
    op.drop_table("shipment")