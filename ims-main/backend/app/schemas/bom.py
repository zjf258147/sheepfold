from datetime import date, datetime

from pydantic import BaseModel, Field


class BomDetailItem(BaseModel):
    """BOM明细项。"""

    material_sku_id: int
    material_sku_code: str = ""
    material_sku_name: str = ""
    spec: str | None = None
    unit: str = "个"
    quantity_per_unit: float = Field(..., gt=0, description="单台用量")
    wastage_rate: float | None = None
    level: int = Field(default=2, ge=0, le=2, description="层级：0=成品, 1=子组件, 2=零件")
    parent_detail_id: int | None = None
    item_version: str | None = None
    process_note: str | None = None
    remark: str | None = None


class BomCreate(BaseModel):
    """创建BOM。"""

    bom_name: str
    version: str
    product_sku_id: int
    product_sku_code: str
    product_sku_name: str
    plan_quantity: int = Field(..., gt=0)
    status: str = "DRAFT"
    remark: str | None = None
    change_reason: str | None = None
    details: list[BomDetailItem] = Field(..., min_length=1, description="BOM明细")


class BomUpdate(BaseModel):
    """更新BOM。"""

    bom_name: str | None = None
    version: str | None = None
    product_sku_id: int | None = None
    product_sku_code: str | None = None
    product_sku_name: str | None = None
    plan_quantity: int | None = None
    status: str | None = None
    remark: str | None = None
    change_reason: str | None = None
    details: list[BomDetailItem] | None = None


class BomDetailResponse(BaseModel):
    """BOM明细响应。"""

    id: int
    material_sku_id: int
    material_sku_code: str
    material_sku_name: str
    spec: str | None = None
    unit: str
    quantity_per_unit: float
    wastage_rate: float | None = None
    level: int = 2
    parent_detail_id: int | None = None
    item_version: str | None = None
    process_note: str | None = None
    remark: str | None = None

    model_config = {"from_attributes": True}


class BomResponse(BaseModel):
    """BOM响应。"""

    id: int
    bom_no: str
    bom_name: str
    version: str
    product_sku_id: int
    product_sku_code: str
    product_sku_name: str
    plan_quantity: int
    status: str
    remark: str | None = None
    created_by: str
    created_at: datetime
    updated_at: datetime
    details: list[BomDetailResponse] = []

    model_config = {"from_attributes": True}


class ProductionTaskCreate(BaseModel):
    """创建生产任务。"""

    bom_id: int
    plan_quantity: int = Field(..., gt=0)
    product_type: str = "FINISHED_PRODUCT"
    start_date: date | None = None
    end_date: date | None = None
    change_reason: str | None = None


class ProductionTaskUpdate(BaseModel):
    """更新生产任务。"""

    plan_quantity: int | None = None
    status: str | None = None
    product_type: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    change_reason: str | None = None


class ProductionTaskResponse(BaseModel):
    """生产任务响应。"""

    id: int
    task_no: str
    bom_id: int
    bom_no: str | None = None
    bom_name: str | None = None
    plan_quantity: int
    material_availability: str
    status: str
    product_type: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MaterialCheckItem(BaseModel):
    """齐套分析物料项。"""

    material_sku_id: int
    material_sku_code: str
    material_sku_name: str
    spec: str | None = None
    unit: str
    quantity_per_unit: float
    required_qty: float
    stock_qty: float
    shortage_qty: float
    is_sufficient: bool


class MaterialCheckResult(BaseModel):
    """齐套分析结果。"""

    bom_id: int
    bom_no: str
    bom_name: str
    plan_quantity: int
    overall_sufficient: bool
    items: list[MaterialCheckItem] = []