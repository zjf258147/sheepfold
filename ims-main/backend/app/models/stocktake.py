from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import StocktakeMode, StocktakeStatus


class Stocktake(Base, TimestampMixin):
    """盘点任务。"""

    __tablename__ = "stocktake"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="盘点ID")
    stocktake_no: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, index=True, comment="PD前缀盘点单号"
    )
    mode: Mapped[str] = mapped_column(
        String(10), default=StocktakeMode.CYCLE.value, nullable=False, comment="CYCLE/FULL"
    )
    status: Mapped[str] = mapped_column(
        String(20), default=StocktakeStatus.IN_PROGRESS.value, nullable=False, index=True, comment="进行中/已完成/已取消"
    )
    warehouse: Mapped[str] = mapped_column(String(30), nullable=False, comment="盘点仓库范围")
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="创建人")
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="开始时间")
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="完成时间")
    remark: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="备注")

    lines: Mapped[list["StocktakeLine"]] = relationship(back_populates="stocktake", cascade="all, delete-orphan")


class StocktakeLine(Base):
    """盘点明细行。"""

    __tablename__ = "stocktake_line"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="明细ID")
    stocktake_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("stocktake.id"), nullable=False, index=True, comment="盘点任务ID"
    )
    item_sn: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment="设备SN")
    sku_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("product_sku.id"), nullable=True, comment="SKU ID")
    system_qty: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="系统数量")
    actual_qty: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="实盘数量")
    diff_qty: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="差异数量")
    diff_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="差异原因")
    scanned_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="扫码时间")
    scanned_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("sys_user.id"), nullable=True, comment="扫码人")

    stocktake: Mapped["Stocktake"] = relationship(back_populates="lines")