from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import RmaStatus, ScrapStatus


class RmaReturn(Base, TimestampMixin):
    """返厂退货单（主线B）。"""

    __tablename__ = "rma_return"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    return_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="返厂单号 FC")
    sku_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_sku.id"), nullable=False, index=True, comment="物料 SKU ID"
    )
    sn: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment="设备SN")
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="退货数量")
    unit: Mapped[str] = mapped_column(String(20), default="个", nullable=False, comment="单位")
    customer_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="客户名称")
    return_reason: Mapped[str] = mapped_column(String(255), nullable=False, comment="退货原因")
    return_date: Mapped[date] = mapped_column(Date, nullable=False, comment="退货日期")
    status: Mapped[str] = mapped_column(
        String(30), default=RmaStatus.PENDING_DIAGNOSIS.value, nullable=False, index=True, comment="状态"
    )
    assigned_to: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=True, comment="分配人 ID"
    )
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    sku = relationship("ProductSku", foreign_keys=[sku_id], lazy="joined")
    assignee = relationship("User", foreign_keys=[assigned_to], lazy="joined")


class RmaDiagnosis(Base, TimestampMixin):
    """诊断报告（主线B）。"""

    __tablename__ = "rma_diagnosis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    return_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rma_return.id"), nullable=False, index=True, comment="返厂退货单 ID"
    )
    diagnosis_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="诊断编号 DG")
    diagnosed_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=False, comment="诊断人 ID"
    )
    diagnosis_date: Mapped[date] = mapped_column(Date, nullable=False, comment="诊断日期")
    fault_description: Mapped[str] = mapped_column(Text, nullable=False, comment="故障描述")
    diagnosis_result: Mapped[str] = mapped_column(
        String(30), nullable=False, comment="诊断结果：REPAIRABLE / SCRAP"
    )
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    diagnoser = relationship("User", foreign_keys=[diagnosed_by], lazy="joined")


class RmaRepair(Base, TimestampMixin):
    """维修工单（主线B）。"""

    __tablename__ = "rma_repair"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    return_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rma_return.id"), nullable=False, index=True, comment="返厂退货单 ID"
    )
    repair_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="维修工单号 WX")
    repair_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=False, comment="维修人 ID"
    )
    old_sn: Mapped[str] = mapped_column(String(50), nullable=False, comment="原设备 SN")
    new_sn: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="新设备 SN（换码时填写）")
    repair_description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="维修描述")
    materials_used: Mapped[str | None] = mapped_column(Text, nullable=True, comment="维修用料")
    fault_code: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="故障码")
    repair_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="维修完成日期")
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    repairer = relationship("User", foreign_keys=[repair_by], lazy="joined")


class RmaScrap(Base, TimestampMixin):
    """报废申请审批单（主线B）。"""

    __tablename__ = "rma_scrap"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    return_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rma_return.id"), nullable=False, index=True, comment="返厂退货单 ID"
    )
    scrap_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="报废单号 BF")
    requested_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=False, comment="申请人 ID"
    )
    scrap_reason: Mapped[str] = mapped_column(Text, nullable=False, comment="报废原因")
    status: Mapped[str] = mapped_column(
        String(20), default=ScrapStatus.PENDING.value, nullable=False, index=True, comment="审批状态"
    )
    approved_by: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=True, comment="审批人 ID"
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="审批时间")
    reject_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="驳回原因")
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    requester = relationship("User", foreign_keys=[requested_by], lazy="joined")
    approver = relationship("User", foreign_keys=[approved_by], lazy="joined")


class RmaReship(Base, TimestampMixin):
    """再出货单（主线B）。"""

    __tablename__ = "rma_reship"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    return_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rma_return.id"), nullable=False, index=True, comment="返厂退货单 ID"
    )
    reship_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="再出货单号 RH")
    new_sn: Mapped[str] = mapped_column(String(50), nullable=False, comment="出货 SN")
    software_version: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="软件版本号")
    ship_date: Mapped[date] = mapped_column(Date, nullable=False, comment="出货日期")
    recipient: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="收货人/客户")
    operator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=False, comment="操作人 ID"
    )
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    operator = relationship("User", foreign_keys=[operator_id], lazy="joined")