"""add rma missing fields and tables

Revision ID: c1d2e3f4g5h6
Revises: bdbe653a2582
Create Date: 2026-09-04 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'c1d2e3f4g5h6'
down_revision = 'bdbe653a2582'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('rma_return', sa.Column('spec', sa.String(50), nullable=True, comment='规格'))
    op.add_column('rma_return', sa.Column('assign_type', sa.String(20), nullable=True, comment='分配类型：PRODUCTION/TEST'))
    op.add_column('rma_return', sa.Column('assign_reason', sa.String(255), nullable=True, comment='分配原因'))
    op.add_column('rma_return', sa.Column('problem_description', sa.Text(), nullable=True, comment='问题描述'))
    op.add_column('rma_return', sa.Column('repair_plan', sa.Text(), nullable=True, comment='维修方案'))
    op.add_column('rma_return', sa.Column('inspection_report_no', sa.String(100), nullable=True, comment='送检单编号'))
    op.add_column('rma_return', sa.Column('new_sn', sa.String(50), nullable=True, comment='维修后新SN'))
    op.add_column('rma_return', sa.Column('reship_station', sa.String(100), nullable=True, comment='维修后发出场站'))
    op.add_column('rma_return', sa.Column('materials_used', sa.Text(), nullable=True, comment='维修用料'))
    op.add_column('rma_return', sa.Column('repair_time_hours', sa.Float(), nullable=True, comment='修复耗时（小时）'))
    op.add_column('rma_return', sa.Column('turnaround_days', sa.Integer(), nullable=True, comment='周转周期（天）'))
    op.add_column('rma_return', sa.Column('repair_count', sa.Integer(), server_default=sa.text('1'), nullable=True, comment='该SN累计维修次数'))
    op.add_column('rma_return', sa.Column('repair_reason', sa.Text(), nullable=True, comment='维修原因（累计）'))
    op.add_column('rma_return', sa.Column('diagnosis_result', sa.String(30), nullable=True, comment='诊断结果'))

    op.add_column('rma_diagnosis', sa.Column('repair_plan', sa.Text(), nullable=True, comment='维修方案'))
    op.add_column('rma_diagnosis', sa.Column('inspection_report_no', sa.String(100), nullable=True, comment='送检单编号'))

    op.add_column('rma_repair', sa.Column('start_time', sa.DateTime(), nullable=True, comment='维修开始时间'))
    op.add_column('rma_repair', sa.Column('end_time', sa.DateTime(), nullable=True, comment='维修结束时间'))

    op.create_table(
        'rma_quality_check',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('return_id', sa.Integer(), nullable=False, comment='返厂退货单 ID'),
        sa.Column('checked_by', sa.Integer(), nullable=False, comment='检验人 ID'),
        sa.Column('check_date', sa.Date(), nullable=False, comment='检验日期'),
        sa.Column('check_result', sa.String(20), nullable=False, comment='检验结果：PASS / FAIL'),
        sa.Column('check_description', sa.Text(), nullable=True, comment='检验描述'),
        sa.Column('change_reason', sa.String(255), nullable=True, comment='变更原因'),
        sa.Column('remark', sa.Text(), nullable=True, comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['return_id'], ['rma_return.id'], name='fk_rma_quality_check_return_id'),
        sa.ForeignKeyConstraint(['checked_by'], ['sys_user.id'], name='fk_rma_quality_check_checked_by'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_rma_quality_check_return_id', 'rma_quality_check', ['return_id'], unique=False)

    op.create_table(
        'rma_warehouse_in',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('return_id', sa.Integer(), nullable=False, comment='返厂退货单 ID'),
        sa.Column('new_sn', sa.String(50), nullable=False, comment='新SN'),
        sa.Column('warehouse_by', sa.Integer(), nullable=False, comment='入库审核人 ID'),
        sa.Column('warehouse_date', sa.Date(), nullable=False, comment='入库日期'),
        sa.Column('repair_count', sa.Integer(), server_default=sa.text('1'), nullable=False, comment='该SN累计维修次数'),
        sa.Column('repair_reason', sa.Text(), nullable=True, comment='维修原因（累计）'),
        sa.Column('change_reason', sa.String(255), nullable=True, comment='变更原因'),
        sa.Column('remark', sa.Text(), nullable=True, comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['return_id'], ['rma_return.id'], name='fk_rma_warehouse_in_return_id'),
        sa.ForeignKeyConstraint(['warehouse_by'], ['sys_user.id'], name='fk_rma_warehouse_in_warehouse_by'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_rma_warehouse_in_return_id', 'rma_warehouse_in', ['return_id'], unique=False)


def downgrade():
    op.drop_index('ix_rma_warehouse_in_return_id', table_name='rma_warehouse_in')
    op.drop_table('rma_warehouse_in')
    op.drop_index('ix_rma_quality_check_return_id', table_name='rma_quality_check')
    op.drop_table('rma_quality_check')

    op.drop_column('rma_repair', 'end_time')
    op.drop_column('rma_repair', 'start_time')

    op.drop_column('rma_diagnosis', 'inspection_report_no')
    op.drop_column('rma_diagnosis', 'repair_plan')

    op.drop_column('rma_return', 'repair_reason')
    op.drop_column('rma_return', 'repair_count')
    op.drop_column('rma_return', 'diagnosis_result')
    op.drop_column('rma_return', 'turnaround_days')
    op.drop_column('rma_return', 'repair_time_hours')
    op.drop_column('rma_return', 'materials_used')
    op.drop_column('rma_return', 'reship_station')
    op.drop_column('rma_return', 'new_sn')
    op.drop_column('rma_return', 'inspection_report_no')
    op.drop_column('rma_return', 'repair_plan')
    op.drop_column('rma_return', 'problem_description')
    op.drop_column('rma_return', 'assign_reason')
    op.drop_column('rma_return', 'assign_type')
    op.drop_column('rma_return', 'spec')