"""create incoming_receipt, incoming_inspection, incoming_return

Revision ID: q1r2s3t4u5v6
Revises: p0q1r2s3t4u5
Create Date: 2026-09-04 11:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "q1r2s3t4u5v6"
down_revision = "p0q1r2s3t4u5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "incoming_receipt",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("receipt_no", sa.String(length=50), nullable=False, comment="到货单号"),
        sa.Column("supplier_id", sa.Integer(), nullable=False, comment="供应商 ID"),
        sa.Column("sku_id", sa.Integer(), nullable=False, comment="物料 SKU ID"),
        sa.Column("batch_no", sa.String(length=50), nullable=False, comment="批次号"),
        sa.Column("quantity", sa.Integer(), nullable=False, comment="到货数量"),
        sa.Column("unit", sa.String(length=20), nullable=False, server_default="个", comment="单位"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="PENDING_INSPECTION", comment="状态"),
        sa.Column("delivery_date", sa.Date(), nullable=False, comment="到货日期"),
        sa.Column("inspector_id", sa.Integer(), nullable=True, comment="检验人 ID"),
        sa.Column("inspection_date", sa.Date(), nullable=True, comment="检验日期"),
        sa.Column("change_reason", sa.String(length=255), nullable=True, comment="变更原因"),
        sa.Column("remark", sa.Text(), nullable=True, comment="备注"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["supplier_id"], ["partner.id"]),
        sa.ForeignKeyConstraint(["sku_id"], ["product_sku.id"]),
        sa.ForeignKeyConstraint(["inspector_id"], ["sys_user.id"]),
    )
    op.create_index("ix_incoming_receipt_receipt_no", "incoming_receipt", ["receipt_no"], unique=True)
    op.create_index("ix_incoming_receipt_supplier_id", "incoming_receipt", ["supplier_id"])
    op.create_index("ix_incoming_receipt_sku_id", "incoming_receipt", ["sku_id"])
    op.create_index("ix_incoming_receipt_status", "incoming_receipt", ["status"])

    op.create_table(
        "incoming_inspection",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("receipt_id", sa.Integer(), nullable=False, comment="到货单 ID"),
        sa.Column("inspection_no", sa.String(length=50), nullable=False, comment="检验编号"),
        sa.Column("inspector_id", sa.Integer(), nullable=False, comment="检验人 ID"),
        sa.Column("inspection_date", sa.Date(), nullable=False, comment="检验日期"),
        sa.Column("result", sa.String(length=30), nullable=False, comment="ACCEPTED / CONCESSION_ACCEPTED / REJECTED"),
        sa.Column("sample_qty", sa.Integer(), nullable=False, server_default="0", comment="抽样数量"),
        sa.Column("defect_qty", sa.Integer(), nullable=False, server_default="0", comment="不良数量"),
        sa.Column("defect_description", sa.Text(), nullable=True, comment="不良描述"),
        sa.Column("change_reason", sa.String(length=255), nullable=True, comment="变更原因"),
        sa.Column("remark", sa.Text(), nullable=True, comment="备注"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["receipt_id"], ["incoming_receipt.id"]),
        sa.ForeignKeyConstraint(["inspector_id"], ["sys_user.id"]),
    )
    op.create_index("ix_incoming_inspection_receipt_id", "incoming_inspection", ["receipt_id"])
    op.create_index("ix_incoming_inspection_inspection_no", "incoming_inspection", ["inspection_no"], unique=True)

    op.create_table(
        "incoming_return",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("receipt_id", sa.Integer(), nullable=False, comment="到货单 ID"),
        sa.Column("return_no", sa.String(length=50), nullable=False, comment="退货单号"),
        sa.Column("return_qty", sa.Integer(), nullable=False, comment="退货数量"),
        sa.Column("return_reason", sa.String(length=255), nullable=False, comment="退货原因"),
        sa.Column("return_date", sa.Date(), nullable=False, comment="退货日期"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="PENDING", comment="PENDING / CONFIRMED"),
        sa.Column("operator_id", sa.Integer(), nullable=False, comment="操作人 ID"),
        sa.Column("change_reason", sa.String(length=255), nullable=True, comment="变更原因"),
        sa.Column("remark", sa.Text(), nullable=True, comment="备注"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["receipt_id"], ["incoming_receipt.id"]),
        sa.ForeignKeyConstraint(["operator_id"], ["sys_user.id"]),
    )
    op.create_index("ix_incoming_return_receipt_id", "incoming_return", ["receipt_id"])
    op.create_index("ix_incoming_return_return_no", "incoming_return", ["return_no"], unique=True)


def downgrade():
    op.drop_table("incoming_return")
    op.drop_table("incoming_inspection")
    op.drop_table("incoming_receipt")