from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StocktakeLineResponse(BaseModel):
    id: int
    stocktake_id: int
    item_sn: str
    sku_id: Optional[int] = None
    sku_name: Optional[str] = None
    system_qty: int
    actual_qty: int
    diff_qty: int
    diff_reason: Optional[str] = None
    scanned_at: Optional[datetime] = None
    scanned_by: Optional[int] = None
    scanned_by_name: Optional[str] = None
    model_config = {"from_attributes": True}


class StocktakeResponse(BaseModel):
    id: int
    stocktake_no: str
    mode: str
    status: str
    warehouse: str
    created_by: int
    created_by_name: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    lines: Optional[list[StocktakeLineResponse]] = None
    model_config = {"from_attributes": True}


class StocktakeCreate(BaseModel):
    mode: str = Field(default="CYCLE", max_length=10)
    warehouse: str = Field(..., max_length=30)
    remark: Optional[str] = Field(None, max_length=500)


class ScanItemRequest(BaseModel):
    item_sn: str = Field(..., max_length=50)
    actual_qty: int = Field(..., ge=0)


class StocktakeScanRequest(BaseModel):
    items: list[ScanItemRequest] = Field(..., min_length=1)


class StocktakeLineUpdateRequest(BaseModel):
    diff_reason: Optional[str] = Field(None, max_length=255)


class StocktakeCompleteRequest(BaseModel):
    remark: Optional[str] = Field(None, max_length=500)