"""add rma tables

Revision ID: bdbe653a2582
Revises: r1s2t3u4v5w6
Create Date: 2026-09-04 15:59:27.580430

"""
from alembic import op
import sqlalchemy as sa

revision = 'bdbe653a2582'
down_revision = 'r1s2t3u4v5w6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'rma_return',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('return_no', sa.String(50), nullable=False, comment='返厂单号 FC'),
        sa.Column('sku_id', sa.Integer(), nullable=False, comment='物料 SKU ID'),
        sa.Column('sn', sa.String(50), nullable=False, comment='设备SN'),
        sa.Column('quantity', sa.Integer(), server_default=sa.text('1'), nullable=False, comment='退货数量'),
        sa.Column('unit', sa.String(20), server_default=sa.text("'个'"), nullable=False, comment='单位'),
        sa.Column('customer_name', sa.String(100), nullable=True, comment='客户名称'),
        sa.Column('return_reason', sa.String(255), nullable=False, comment='退货原因'),
        sa.Column('return_date', sa.Date(), nullable=False, comment='退货日期'),
        sa.Column('status', sa.String(30), server_default=sa.text("'PENDING_DIAGNOSIS'"), nullable=False, comment='状态'),
        sa.Column('assigned_to', sa.Integer(), nullable=True, comment='分配人 ID'),
        sa.Column('change_reason', sa.String(255), nullable=True, comment='变更原因'),
        sa.Column('remark', sa.Text(), nullable=True, comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['sku_id'], ['product_sku.id'], name='fk_rma_return_sku_id'),
        sa.ForeignKeyConstraint(['assigned_to'], ['sys_user.id'], name='fk_rma_return_assigned_to'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_rma_return_return_no', 'rma_return', ['return_no'], unique=True)
    op.create_index('ix_rma_return_sn', 'rma_return', ['sn'], unique=False)
    op.create_index('ix_rma_return_sku_id', 'rma_return', ['sku_id'], unique=False)
    op.create_index('ix_rma_return_status', 'rma_return', ['status'], unique=False)

    op.create_table(
        'rma_diagnosis',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('return_id', sa.Integer(), nullable=False, comment='返厂退货单 ID'),
        sa.Column('diagnosis_no', sa.String(50), nullable=False, comment='诊断编号 DG'),
        sa.Column('diagnosed_by', sa.Integer(), nullable=False, comment='诊断人 ID'),
        sa.Column('diagnosis_date', sa.Date(), nullable=False, comment='诊断日期'),
        sa.Column('fault_description', sa.Text(), nullable=False, comment='故障描述'),
        sa.Column('diagnosis_result', sa.String(30), nullable=False, comment='诊断结果'),
        sa.Column('change_reason', sa.String(255), nullable=True, comment='变更原因'),
        sa.Column('remark', sa.Text(), nullable=True, comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['return_id'], ['rma_return.id'], name='fk_rma_diagnosis_return_id'),
        sa.ForeignKeyConstraint(['diagnosed_by'], ['sys_user.id'], name='fk_rma_diagnosis_diagnosed_by'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_rma_diagnosis_return_id', 'rma_diagnosis', ['return_id'], unique=False)
    op.create_index('ix_rma_diagnosis_diagnosis_no', 'rma_diagnosis', ['diagnosis_no'], unique=True)

    op.create_table(
        'rma_repair',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('return_id', sa.Integer(), nullable=False, comment='返厂退货单 ID'),
        sa.Column('repair_no', sa.String(50), nullable=False, comment='维修工单号 WX'),
        sa.Column('repair_by', sa.Integer(), nullable=False, comment='维修人 ID'),
        sa.Column('old_sn', sa.String(50), nullable=False, comment='原设备 SN'),
        sa.Column('new_sn', sa.String(50), nullable=True, comment='新设备 SN'),
        sa.Column('repair_description', sa.Text(), nullable=True, comment='维修描述'),
        sa.Column('materials_used', sa.Text(), nullable=True, comment='维修用料'),
        sa.Column('fault_code', sa.String(50), nullable=True, comment='故障码'),
        sa.Column('repair_date', sa.Date(), nullable=True, comment='维修完成日期'),
        sa.Column('change_reason', sa.String(255), nullable=True, comment='变更原因'),
        sa.Column('remark', sa.Text(), nullable=True, comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['return_id'], ['rma_return.id'], name='fk_rma_repair_return_id'),
        sa.ForeignKeyConstraint(['repair_by'], ['sys_user.id'], name='fk_rma_repair_repair_by'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_rma_repair_return_id', 'rma_repair', ['return_id'], unique=False)
    op.create_index('ix_rma_repair_repair_no', 'rma_repair', ['repair_no'], unique=True)

    op.create_table(
        'rma_scrap',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('return_id', sa.Integer(), nullable=False, comment='返厂退货单 ID'),
        sa.Column('scrap_no', sa.String(50), nullable=False, comment='报废单号 BF'),
        sa.Column('requested_by', sa.Integer(), nullable=False, comment='申请人 ID'),
        sa.Column('scrap_reason', sa.Text(), nullable=False, comment='报废原因'),
        sa.Column('status', sa.String(20), server_default=sa.text("'PENDING'"), nullable=False, comment='审批状态'),
        sa.Column('approved_by', sa.Integer(), nullable=True, comment='审批人 ID'),
        sa.Column('approved_at', sa.DateTime(), nullable=True, comment='审批时间'),
        sa.Column('reject_reason', sa.String(255), nullable=True, comment='驳回原因'),
        sa.Column('change_reason', sa.String(255), nullable=True, comment='变更原因'),
        sa.Column('remark', sa.Text(), nullable=True, comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['return_id'], ['rma_return.id'], name='fk_rma_scrap_return_id'),
        sa.ForeignKeyConstraint(['requested_by'], ['sys_user.id'], name='fk_rma_scrap_requested_by'),
        sa.ForeignKeyConstraint(['approved_by'], ['sys_user.id'], name='fk_rma_scrap_approved_by'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_rma_scrap_return_id', 'rma_scrap', ['return_id'], unique=False)
    op.create_index('ix_rma_scrap_scrap_no', 'rma_scrap', ['scrap_no'], unique=True)
    op.create_index('ix_rma_scrap_status', 'rma_scrap', ['status'], unique=False)

    op.create_table(
        'rma_reship',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('return_id', sa.Integer(), nullable=False, comment='返厂退货单 ID'),
        sa.Column('reship_no', sa.String(50), nullable=False, comment='再出货单号 RH'),
        sa.Column('new_sn', sa.String(50), nullable=False, comment='出货 SN'),
        sa.Column('software_version', sa.String(50), nullable=True, comment='软件版本号'),
        sa.Column('ship_date', sa.Date(), nullable=False, comment='出货日期'),
        sa.Column('recipient', sa.String(100), nullable=True, comment='收货人/客户'),
        sa.Column('operator_id', sa.Integer(), nullable=False, comment='操作人 ID'),
        sa.Column('change_reason', sa.String(255), nullable=True, comment='变更原因'),
        sa.Column('remark', sa.Text(), nullable=True, comment='备注'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['return_id'], ['rma_return.id'], name='fk_rma_reship_return_id'),
        sa.ForeignKeyConstraint(['operator_id'], ['sys_user.id'], name='fk_rma_reship_operator_id'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_rma_reship_return_id', 'rma_reship', ['return_id'], unique=False)
    op.create_index('ix_rma_reship_reship_no', 'rma_reship', ['reship_no'], unique=True)


def downgrade():
    op.drop_index('ix_rma_reship_reship_no', table_name='rma_reship')
    op.drop_index('ix_rma_reship_return_id', table_name='rma_reship')
    op.drop_table('rma_reship')
    op.drop_index('ix_rma_scrap_status', table_name='rma_scrap')
    op.drop_index('ix_rma_scrap_scrap_no', table_name='rma_scrap')
    op.drop_index('ix_rma_scrap_return_id', table_name='rma_scrap')
    op.drop_table('rma_scrap')
    op.drop_index('ix_rma_repair_repair_no', table_name='rma_repair')
    op.drop_index('ix_rma_repair_return_id', table_name='rma_repair')
    op.drop_table('rma_repair')
    op.drop_index('ix_rma_diagnosis_diagnosis_no', table_name='rma_diagnosis')
    op.drop_index('ix_rma_diagnosis_return_id', table_name='rma_diagnosis')
    op.drop_table('rma_diagnosis')
    op.drop_index('ix_rma_return_status', table_name='rma_return')
    op.drop_index('ix_rma_return_sku_id', table_name='rma_return')
    op.drop_index('ix_rma_return_sn', table_name='rma_return')
    op.drop_index('ix_rma_return_return_no', table_name='rma_return')
    op.drop_table('rma_return')