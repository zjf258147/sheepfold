"""add_missing_columns_customer_inventory_production

Revision ID: bd138515121c
Revises: 9d008cb2ab28
Create Date: 2026-09-14 18:31:30.024863

"""
from alembic import op
import sqlalchemy as sa


revision = 'bd138515121c'
down_revision = '9d008cb2ab28'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('customer', sa.Column('contact_person', sa.String(length=50), nullable=True, comment='联系人'))
    op.add_column('customer', sa.Column('contact_phone', sa.String(length=20), nullable=True, comment='联系电话'))
    op.add_column('customer', sa.Column('contact_email', sa.String(length=100), nullable=True, comment='邮箱'))
    op.add_column('customer', sa.Column('address', sa.Text(), nullable=True, comment='地址'))
    op.add_column('customer', sa.Column('contract_no', sa.String(length=50), nullable=True, comment='合同编号'))
    op.add_column('customer', sa.Column('contract_start', sa.Date(), nullable=True, comment='合同起始日期'))
    op.add_column('customer', sa.Column('contract_end', sa.Date(), nullable=True, comment='合同到期日期'))
    op.add_column('customer', sa.Column('remark', sa.Text(), nullable=True, comment='备注'))

    op.add_column('inventory_item', sa.Column('warehouse_type', sa.String(length=30), nullable=False, server_default='RAW_MATERIAL', comment='仓库类型'))
    op.create_index(op.f('ix_inventory_item_warehouse_type'), 'inventory_item', ['warehouse_type'], unique=False)

    op.add_column('inventory_item_snapshot', sa.Column('warehouse_type', sa.String(length=30), nullable=True, comment='仓库类型'))

    op.add_column('production_task', sa.Column('product_type', sa.String(length=30), nullable=False, server_default='FINISHED_PRODUCT', comment='产出类型：FINISHED_PRODUCT/SEMI_FINISHED'))


def downgrade():
    op.drop_column('production_task', 'product_type')
    op.drop_column('inventory_item_snapshot', 'warehouse_type')
    op.drop_index(op.f('ix_inventory_item_warehouse_type'), table_name='inventory_item')
    op.drop_column('inventory_item', 'warehouse_type')
    op.drop_column('customer', 'remark')
    op.drop_column('customer', 'contract_end')
    op.drop_column('customer', 'contract_start')
    op.drop_column('customer', 'contract_no')
    op.drop_column('customer', 'address')
    op.drop_column('customer', 'contact_email')
    op.drop_column('customer', 'contact_phone')
    op.drop_column('customer', 'contact_person')