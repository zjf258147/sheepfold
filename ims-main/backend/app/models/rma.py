from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import AssignType, DiagnosisResult, QualityCheckResult, RmaStatus, ScrapStatus


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
    spec: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="规格")
    customer_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="客户名称")
    return_reason: Mapped[str] = mapped_column(String(255), nullable=False, comment="退货原因")
    return_date: Mapped[date] = mapped_column(Date, nullable=False, comment="退货日期")
    status: Mapped[str] = mapped_column(
        String(30), default=RmaStatus.PENDING_DIAGNOSIS.value, nullable=False, index=True, comment="状态"
    )
    assigned_to: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=True, comment="分配人 ID"
    )
    assign_type: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="分配类型：PRODUCTION/TEST")
    assign_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="分配原因")
    problem_description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="问题描述")
    repair_plan: Mapped[str | None] = mapped_column(Text, nullable=True, comment="维修方案")
    inspection_report_no: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="送检单编号")
    new_sn: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="维修后新SN")
    reship_station: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="维修后发出场站")
    materials_used: Mapped[str | None] = mapped_column(Text, nullable=True, comment="维修用料")
    repair_time_hours: Mapped[float | None] = mapped_column(Float, nullable=True, comment="修复耗时（小时）")
    turnaround_days: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="周转周期（天）")
    repair_count: Mapped[int | None] = mapped_column(Integer, default=1, nullable=True, comment="该SN累计维修次数")
    repair_reason: Mapped[str | None] = mapped_column(Text, nullable=True, comment="维修原因（累计）")
    diagnosis_result: Mapped[str | None] = mapped_column(String(30), nullable=True, comment="诊断结果")
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
        String(30), nullable=False, comment="诊断结果：REPAIRABLE / SCRAP / DIRECT_RESHIP"
    )
    repair_plan: Mapped[str | None] = mapped_column(Text, nullable=True, comment="维修方案")
    inspection_report_no: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="送检单编号")
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
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="维修开始时间")
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="维修结束时间")
    repair_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="维修完成日期")
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    repairer = relationship("User", foreign_keys=[repair_by], lazy="joined")


class RmaQualityCheck(Base, TimestampMixin):
    """质量检验（主线B）。"""

    __tablename__ = "rma_quality_check"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    return_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rma_return.id"), nullable=False, index=True, comment="返厂退货单 ID"
    )
    checked_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=False, comment="检验人 ID"
    )
    check_date: Mapped[date] = mapped_column(Date, nullable=False, comment="检验日期")
    check_result: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="检验结果：PASS / FAIL"
    )
    check_description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="检验描述")
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    checker = relationship("User", foreign_keys=[checked_by], lazy="joined")


class RmaWarehouseIn(Base, TimestampMixin):
    """入库审核（主线B）。"""

    __tablename__ = "rma_warehouse_in"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    return_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rma_return.id"), nullable=False, index=True, comment="返厂退货单 ID"
    )
    new_sn: Mapped[str] = mapped_column(String(50), nullable=False, comment="新SN")
    warehouse_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("sys_user.id"), nullable=False, comment="入库审核人 ID"
    )
    warehouse_date: Mapped[date] = mapped_column(Date, nullable=False, comment="入库日期")
    repair_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="该SN累计维修次数")
    repair_reason: Mapped[str | None] = mapped_column(Text, nullable=True, comment="维修原因（累计）")
    warehouse_type: Mapped[str] = mapped_column(
        String(30), default="ZERO_COST_FINISHED", nullable=False, comment="入库仓库类型：ZERO_COST_FINISHED/ZERO_COST_SEMI"
    )
    change_reason: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="变更原因")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")

    warehouser = relationship("User", foreign_keys=[warehouse_by], lazy="joined")


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