from datetime import date, datetime

from sqlalchemy import Date, DateTime, DECIMAL, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import BomStatus, MaterialAvailability, TaskStatus


class BomHeader(Base, TimestampMixin):
    """BOM主表（主线D）。"""

    __tablename__ = "bom_header"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bom_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="BOM编号")
    bom_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="BOM名称")
    version: Mapped[str] = mapped_column(String(20), nullable=False, comment="版本号")
    product_sku_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_sku.id"), nullable=False, index=True, comment="成品物料ID"
    )
    product_sku_code: Mapped[str] = mapped_column(String(50), nullable=False, comment="成品物料编码")
    product_sku_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="成品物料名称")
    plan_quantity: Mapped[int] = mapped_column(Integer, nullable=False, comment="计划生产数量")
    status: Mapped[BomStatus] = mapped_column(
        String(20), default=BomStatus.DRAFT, nullable=False, comment="状态：草稿/已发布/已停产"
    )
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")
    created_by: Mapped[str] = mapped_column(String(50), nullable=False, comment="创建人")

    details = relationship("BomDetail", primaryjoin="BomHeader.id == foreign(BomDetail.bom_id)", lazy="selectin")


class BomDetail(Base, TimestampMixin):
    """BOM明细（主线D）—— 支持多级层级（00整机/01子组件/02零件）。"""

    __tablename__ = "bom_detail"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bom_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("bom_header.id"), nullable=False, index=True, comment="关联BOM主表"
    )
    level: Mapped[int] = mapped_column(
        Integer, nullable=False, default=2, comment="层级：0=成品, 1=子组件, 2=零件"
    )
    parent_detail_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("bom_detail.id"), nullable=True, index=True, comment="父级明细行ID（自引用）"
    )
    material_sku_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_sku.id"), nullable=False, comment="原材料物料ID"
    )
    material_sku_code: Mapped[str] = mapped_column(String(50), nullable=False, comment="原材料编码")
    material_sku_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="原材料名称")
    spec: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="规格")
    unit: Mapped[str] = mapped_column(String(10), nullable=False, comment="单位")
    quantity_per_unit: Mapped[float] = mapped_column(DECIMAL(10, 3), nullable=False, comment="单台用量")
    wastage_rate: Mapped[float | None] = mapped_column(DECIMAL(5, 2), nullable=True, comment="损耗率(%)")
    item_version: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="明细行版本（如A00/V1.0.0）")
    process_note: Mapped[str | None] = mapped_column(Text, nullable=True, comment="工艺说明")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注")


class ProductionTask(Base, TimestampMixin):
    """生产任务（主线D）。"""

    __tablename__ = "production_task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="任务编号")
    bom_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("bom_header.id"), nullable=False, index=True, comment="关联BOM"
    )
    plan_quantity: Mapped[int] = mapped_column(Integer, nullable=False, comment="计划生产数量")
    material_availability: Mapped[MaterialAvailability] = mapped_column(
        String(20), default=MaterialAvailability.SHORTAGE, nullable=False, comment="齐套/缺料/已齐套"
    )
    status: Mapped[TaskStatus] = mapped_column(
        String(20), default=TaskStatus.PENDING, nullable=False, comment="待生产/生产中/已完成"
    )
    product_type: Mapped[str] = mapped_column(
        String(30), default="FINISHED_PRODUCT", nullable=False, comment="产出类型：FINISHED_PRODUCT/SEMI_FINISHED"
    )
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="计划开始日期")
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="计划完成日期")
    created_by: Mapped[str] = mapped_column(String(50), nullable=False, comment="创建人")