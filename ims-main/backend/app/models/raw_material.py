from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.enums import RawMaterialSnStatus


class RawMaterialInventory(Base, TimestampMixin):
    """原材料库存（批次管理）。"""

    __tablename__ = "raw_material_inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_sku.id"), nullable=False, index=True, comment="物料 SKU ID"
    )
    batch_no: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment="批次号")
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="库存数量")
    unit: Mapped[str] = mapped_column(String(20), default="个", nullable=False, comment="单位")
    status: Mapped[str] = mapped_column(
        String(20), default=RawMaterialSnStatus.IN_STOCK.value, nullable=False, comment="库存状态"
    )
    supplier_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("partner.id"), nullable=True, index=True, comment="供应商 ID"
    )
    receipt_no: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="关联到货单号")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")


class RawMaterialSn(Base, TimestampMixin):
    """原材料 SN 明细（可选 SN 管理）。"""

    __tablename__ = "raw_material_sn"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inventory_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("raw_material_inventory.id"), nullable=False, index=True, comment="库存批次 ID"
    )
    sn: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="原材料 SN 号")
    status: Mapped[str] = mapped_column(
        String(20), default=RawMaterialSnStatus.IN_STOCK.value, nullable=False, comment="SN 状态"
    )
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")


class RawMaterialInventoryLog(Base):
    """原材料库存流水。"""

    __tablename__ = "raw_material_inventory_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inventory_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("raw_material_inventory.id"), nullable=False, index=True, comment="库存批次 ID"
    )
    sn_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("raw_material_sn.id"), nullable=True, comment="SN ID（按 SN 扣减时记录）"
    )
    change_type: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="INCREASE / DECREASE"
    )
    change_qty: Mapped[int] = mapped_column(Integer, nullable=False, comment="变更数量")
    before_qty: Mapped[int] = mapped_column(Integer, nullable=False, comment="变更前数量")
    after_qty: Mapped[int] = mapped_column(Integer, nullable=False, comment="变更后数量")
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    related_order_no: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="关联单号")
    operator_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=True, comment="操作人 ID"
    )
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="操作时间")