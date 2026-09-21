"""add rma knowledge base

Revision ID: k8b9c0d1e2f3
Revises: 08770d6c4ebf
Create Date: 2026-09-20 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'k8b9c0d1e2f3'
down_revision = '08770d6c4ebf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'rma_knowledge_base',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(200), nullable=False, comment='知识标题'),
        sa.Column('fault_code', sa.String(50), nullable=True, comment='故障码'),
        sa.Column('fault_symptom', sa.Text(), nullable=False, comment='故障现象'),
        sa.Column('solution', sa.Text(), nullable=False, comment='解决方案'),
        sa.Column('tags', sa.String(500), nullable=True, comment='标签 JSON 数组'),
        sa.Column('source_type', sa.String(20), server_default=sa.text("'MANUAL'"), nullable=False, comment='来源: MANUAL/FROM_REPAIR'),
        sa.Column('source_repair_id', sa.Integer(), nullable=True, comment='来源维修工单ID'),
        sa.Column('usage_count', sa.Integer(), server_default=sa.text('0'), nullable=False, comment='引用次数'),
        sa.Column('status', sa.String(20), server_default=sa.text("'DRAFT'"), nullable=False, comment='状态: DRAFT/PUBLISHED'),
        sa.Column('created_by', sa.Integer(), nullable=False, comment='创建人'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['source_repair_id'], ['rma_repair.id'], name='fk_kb_source_repair_id'),
        sa.ForeignKeyConstraint(['created_by'], ['sys_user.id'], name='fk_kb_created_by'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_kb_fault_code', 'rma_knowledge_base', ['fault_code'], unique=False)
    op.create_index('ix_kb_status', 'rma_knowledge_base', ['status'], unique=False)


def downgrade():
    op.drop_index('ix_kb_status', table_name='rma_knowledge_base')
    op.drop_index('ix_kb_fault_code', table_name='rma_knowledge_base')
    op.drop_table('rma_knowledge_base')