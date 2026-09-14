from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.models.enums import AdjustmentType


class InventoryAdjustment(Base, TimestampMixin):
    """库存调整记录。"""

    __tablename__ = "inventory_adjustment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="调整ID")
    adjustment_no: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, index=True, comment="TZ前缀调整单号"
    )
    stocktake_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("stocktake.id"), nullable=False, comment="盘点任务ID"
    )
    stocktake_line_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("stocktake_line.id"), nullable=False, comment="盘点明细ID"
    )
    item_sn: Mapped[str] = mapped_column(String(50), nullable=False, comment="设备SN")
    adjustment_type: Mapped[str] = mapped_column(
        String(10), nullable=False, comment="SURPLUS/SHORTAGE"
    )
    before_status: Mapped[str] = mapped_column(String(30), nullable=False, comment="调整前库存状态")
    after_status: Mapped[str] = mapped_column(String(30), nullable=False, comment="调整后库存状态")
    reason: Mapped[str] = mapped_column(Text, nullable=False, comment="调整原因")
    operator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=False, comment="操作人"
    )