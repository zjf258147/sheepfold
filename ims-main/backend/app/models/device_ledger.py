from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import DeviceLedgerStatus


class DeviceLedger(Base, TimestampMixin):
    """设备安装记录（台账）。"""

    __tablename__ = "device_ledger"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="台账ID")
    item_sn: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, comment="设备SN，关联inventory_item.item_sn"
    )
    station_id: Mapped[int] = mapped_column(Integer, ForeignKey("station.id"), nullable=False, comment="场站")
    installed_date: Mapped[date] = mapped_column(Date, nullable=False, comment="安装到场站日期")
    removed_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="移除日期，NULL=当前在场站")
    warranty_start: Mapped[date | None] = mapped_column(Date, nullable=True, comment="质保起始日期")
    warranty_end: Mapped[date | None] = mapped_column(Date, nullable=True, comment="质保到期日期")
    software_version: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="软件版本号")
    status: Mapped[str] = mapped_column(
        String(20), default=DeviceLedgerStatus.RUNNING.value, nullable=False, index=True, comment="运行中/故障/已回收"
    )
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    station: Mapped["Station"] = relationship(foreign_keys=[station_id], lazy="select")  # noqa: F821