"""add confirmed_at, confirmed_by to incoming_receipt

Revision ID: r1s2t3u4v5w6
Revises: q1r2s3t4u5v6
Create Date: 2026-09-04 14:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "r1s2t3u4v5w6"
down_revision = "q1r2s3t4u5v6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "incoming_receipt",
        sa.Column("confirmed_at", sa.DateTime(), nullable=True, comment="入库确认时间"),
    )
    op.add_column(
        "incoming_receipt",
        sa.Column("confirmed_by", sa.Integer(), nullable=True, comment="入库确认人 ID"),
    )
    op.create_foreign_key("fk_incoming_receipt_confirmed_by", "incoming_receipt", "sys_user", ["confirmed_by"], ["id"])


def downgrade():
    op.drop_constraint("fk_incoming_receipt_confirmed_by", "incoming_receipt", type_="foreignkey")
    op.drop_column("incoming_receipt", "confirmed_by")
    op.drop_column("incoming_receipt", "confirmed_at")