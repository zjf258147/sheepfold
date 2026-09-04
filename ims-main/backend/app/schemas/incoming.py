from datetime import date, datetime

from pydantic import BaseModel, Field


class IncomingReceiptCreate(BaseModel):
    supplier_id: int
    sku_id: int
    batch_no: str = Field(..., max_length=50)
    quantity: int = Field(..., gt=0)
    unit: str = Field(default="个", max_length=20)
    delivery_date: date
    remark: str | None = None


class IncomingReceiptUpdate(BaseModel):
    supplier_id: int | None = None
    sku_id: int | None = None
    batch_no: str | None = Field(None, max_length=50)
    quantity: int | None = Field(None, gt=0)
    unit: str | None = Field(None, max_length=20)
    delivery_date: date | None = None
    remark: str | None = None


class IncomingReceiptResponse(BaseModel):
    id: int
    receipt_no: str
    supplier_id: int
    supplier_name: str | None = None
    sku_id: int
    sku_name: str | None = None
    sku_code: str | None = None
    spec: str | None = None
    batch_no: str
    quantity: int
    unit: str
    status: str
    delivery_date: date
    inspector_id: int | None = None
    inspector_name: str | None = None
    inspection_date: date | None = None
    change_reason: str | None = None
    remark: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class IncomingInspectionCreate(BaseModel):
    receipt_id: int
    inspector_id: int
    inspection_date: date
    result: str = Field(..., description="ACCEPTED / CONCESSION_ACCEPTED / REJECTED")
    sample_qty: int = Field(default=0, ge=0)
    defect_qty: int = Field(default=0, ge=0)
    defect_description: str | None = None
    change_reason: str | None = None
    remark: str | None = None


class IncomingInspectionResponse(BaseModel):
    id: int
    receipt_id: int
    inspection_no: str
    inspector_id: int
    inspector_name: str | None = None
    inspection_date: date
    result: str
    sample_qty: int
    defect_qty: int
    defect_description: str | None = None
    change_reason: str | None = None
    remark: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class IncomingReturnCreate(BaseModel):
    receipt_id: int
    return_qty: int = Field(..., gt=0)
    return_reason: str = Field(..., max_length=255)
    return_date: date
    operator_id: int | None = None
    change_reason: str | None = None
    remark: str | None = None


class IncomingReturnResponse(BaseModel):
    id: int
    receipt_id: int
    return_no: str
    return_qty: int
    return_reason: str
    return_date: date
    status: str
    operator_id: int
    operator_name: str | None = None
    change_reason: str | None = None
    remark: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}