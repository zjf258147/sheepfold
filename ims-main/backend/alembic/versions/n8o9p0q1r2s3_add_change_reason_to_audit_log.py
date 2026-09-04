"""add change_reason to sys_audit_log

Revision ID: n8o9p0q1r2s3
Revises: m7n8o9p0q1r2
Create Date: 2026-09-04 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "n8o9p0q1r2s3"
down_revision = "m7n8o9p0q1r2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("sys_audit_log", sa.Column("change_reason", sa.String(length=255), nullable=True, comment="变更原因"))


def downgrade():
    op.drop_column("sys_audit_log", "change_reason")