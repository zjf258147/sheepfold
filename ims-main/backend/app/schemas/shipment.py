from datetime import date, datetime

from pydantic import BaseModel, Field


class ShipmentCreate(BaseModel):
    """创建出货单。"""

    sku_id: int
    sku_code: str
    sku_name: str
    spec: str | None = None
    unit: str = "个"
    sn_list: list[str] = Field(..., min_length=1, description="出货SN列表")
    quantity: int
    ship_date: date
    address: str
    logistics_provider: str
    tracking_no: str
    u9_task_no: str | None = None
    tf_version: str | None = None
    host_version: str | None = None
    remark: str | None = None
    change_reason: str | None = None


class ShipmentUpdate(BaseModel):
    """更新出货单。"""

    sku_id: int | None = None
    sku_code: str | None = None
    sku_name: str | None = None
    spec: str | None = None
    unit: str | None = None
    sn_list: list[str] | None = None
    quantity: int | None = None
    ship_date: date | None = None
    address: str | None = None
    logistics_provider: str | None = None
    tracking_no: str | None = None
    u9_task_no: str | None = None
    tf_version: str | None = None
    host_version: str | None = None
    remark: str | None = None
    change_reason: str | None = None


class ShipmentResponse(BaseModel):
    """出货单响应。"""

    id: int
    shipment_no: str
    sku_id: int
    sku_code: str
    sku_name: str
    spec: str | None = None
    unit: str
    sn_list: list[str]
    quantity: int
    ship_date: date
    address: str
    logistics_provider: str
    tracking_no: str
    u9_task_no: str | None = None
    tf_version: str | None = None
    host_version: str | None = None
    remark: str | None = None
    created_by: str
    change_reason: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}