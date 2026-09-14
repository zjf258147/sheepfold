from datetime import date

from sqlalchemy import Date, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Shipment(Base, TimestampMixin):
    """出货单（主线C）。"""

    __tablename__ = "shipment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    shipment_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="出货单号 SH")
    sku_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, comment="物料ID"
    )
    sku_code: Mapped[str] = mapped_column(String(50), nullable=False, comment="物料编码（U9编码）")
    sku_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="物料名称")
    spec: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="规格型号")
    unit: Mapped[str] = mapped_column(String(10), nullable=False, default="个", comment="单位")
    sn_list: Mapped[list] = mapped_column(JSON, nullable=False, comment="出货SN列表")
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, comment="数量")
    ship_date: Mapped[date] = mapped_column(Date, nullable=False, comment="发货日期")
    address: Mapped[str] = mapped_column(Text, nullable=False, comment="收货地址")
    logistics_provider: Mapped[str] = mapped_column(String(50), nullable=False, comment="物流供应商")
    tracking_no: Mapped[str] = mapped_column(String(50), nullable=False, comment="快递单号")
    u9_task_no: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="U9任务单号")
    tf_version: Mapped[str | None] = mapped_column(String(30), nullable=True, comment="TF卡版本号")
    host_version: Mapped[str | None] = mapped_column(String(30), nullable=True, comment="上位机版本号")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
    created_by: Mapped[str] = mapped_column(String(50), nullable=False, comment="创建人")
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")