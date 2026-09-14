from datetime import date

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Customer(Base, TimestampMixin):
    """客户。"""

    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="客户ID")
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, comment="客户名称")
    weight: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="权重，越高越靠前")
    contact_person: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="联系人")
    contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="联系电话")
    contact_email: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="邮箱")
    address: Mapped[str | None] = mapped_column(Text, nullable=True, comment="地址")
    contract_no: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="合同编号")
    contract_start: Mapped[date | None] = mapped_column(Date, nullable=True, comment="合同起始日期")
    contract_end: Mapped[date | None] = mapped_column(Date, nullable=True, comment="合同到期日期")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")