"""add_bom_detail_level_version

Revision ID: 061337f81d29
Revises: t3u4v5w6x7y8
Create Date: 2026-09-07 17:55:13.899077

"""
from alembic import op
import sqlalchemy as sa


revision = '061337f81d29'
down_revision = 't3u4v5w6x7y8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('bom_detail', sa.Column('level', sa.Integer(), nullable=False, server_default='2', comment='层级：0=成品, 1=子组件, 2=零件'))
    op.add_column('bom_detail', sa.Column('parent_detail_id', sa.Integer(), nullable=True, comment='父级明细行ID（自引用）'))
    op.add_column('bom_detail', sa.Column('item_version', sa.String(length=20), nullable=True, comment='明细行版本（如A00/V1.0.0）'))
    op.add_column('bom_detail', sa.Column('process_note', sa.Text(), nullable=True, comment='工艺说明'))
    op.create_index(op.f('ix_bom_detail_parent_detail_id'), 'bom_detail', ['parent_detail_id'], unique=False)
    op.create_foreign_key('fk_bom_detail_parent', 'bom_detail', 'bom_detail', ['parent_detail_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_bom_detail_parent', 'bom_detail', type_='foreignkey')
    op.drop_index(op.f('ix_bom_detail_parent_detail_id'), table_name='bom_detail')
    op.drop_column('bom_detail', 'process_note')
    op.drop_column('bom_detail', 'item_version')
    op.drop_column('bom_detail', 'parent_detail_id')
    op.drop_column('bom_detail', 'level')