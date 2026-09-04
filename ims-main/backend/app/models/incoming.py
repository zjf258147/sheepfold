from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import IncomingStatus


class IncomingReceipt(Base, TimestampMixin):
    """到货单（主线A）。"""

    __tablename__ = "incoming_receipt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    receipt_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="到货单号")
    supplier_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("partner.id"), nullable=False, index=True, comment="供应商 ID"
    )
    sku_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_sku.id"), nullable=False, index=True, comment="物料 SKU ID"
    )
    batch_no: Mapped[str] = mapped_column(String(50), nullable=False, comment="批次号")
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, comment="到货数量")
    unit: Mapped[str] = mapped_column(String(20), default="个", nullable=False, comment="单位")
    status: Mapped[str] = mapped_column(
        String(30), default=IncomingStatus.PENDING_INSPECTION.value, nullable=False, index=True, comment="状态"
    )
    delivery_date: Mapped[date] = mapped_column(Date, nullable=False, comment="到货日期")
    inspector_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=True, comment="检验人 ID"
    )
    inspection_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="检验日期")
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="入库确认时间")
    confirmed_by: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=True, comment="入库确认人 ID"
    )
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    supplier = relationship("Partner", foreign_keys=[supplier_id], lazy="joined")
    sku = relationship("ProductSku", foreign_keys=[sku_id], lazy="joined")
    inspector = relationship("User", foreign_keys=[inspector_id], lazy="joined")
    confirmer = relationship("User", foreign_keys=[confirmed_by], lazy="joined")


class IncomingInspection(Base, TimestampMixin):
    """来料检验报告（主线A）。"""

    __tablename__ = "incoming_inspection"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    receipt_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("incoming_receipt.id"), nullable=False, index=True, comment="到货单 ID"
    )
    inspection_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="检验编号")
    inspector_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=False, comment="检验人 ID"
    )
    inspection_date: Mapped[date] = mapped_column(Date, nullable=False, comment="检验日期")
    result: Mapped[str] = mapped_column(
        String(30), nullable=False, comment="ACCEPTED / CONCESSION_ACCEPTED / REJECTED"
    )
    sample_qty: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="抽样数量")
    defect_qty: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="不良数量")
    defect_description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="不良描述")
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    inspector = relationship("User", foreign_keys=[inspector_id], lazy="joined")


class IncomingReturn(Base, TimestampMixin):
    """原材料退货单（主线A）。"""

    __tablename__ = "incoming_return"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    receipt_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("incoming_receipt.id"), nullable=False, index=True, comment="到货单 ID"
    )
    return_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="退货单号")
    return_qty: Mapped[int] = mapped_column(Integer, nullable=False, comment="退货数量")
    return_reason: Mapped[str] = mapped_column(String(255), nullable=False, comment="退货原因")
    return_date: Mapped[date] = mapped_column(Date, nullable=False, comment="退货日期")
    status: Mapped[str] = mapped_column(
        String(20), default="PENDING", nullable=False, comment="PENDING / CONFIRMED"
    )
    operator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=False, comment="操作人 ID"
    )
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    operator = relationship("User", foreign_keys=[operator_id], lazy="joined")