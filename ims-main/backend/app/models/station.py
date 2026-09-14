from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import StationStatus


class Station(Base, TimestampMixin):
    """场站档案。"""

    __tablename__ = "station"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="场站ID")
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, comment="场站名称")
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customer.id"), nullable=False, comment="关联客户")
    address: Mapped[str | None] = mapped_column(Text, nullable=True, comment="场站地址")
    contact_person: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="联系人")
    contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="联系电话")
    status: Mapped[str] = mapped_column(
        String(20), default=StationStatus.ACTIVE.value, nullable=False, index=True, comment="ACTIVE/INACTIVE"
    )
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    customer: Mapped["Customer"] = relationship(foreign_keys=[customer_id], lazy="select")  # noqa: F821