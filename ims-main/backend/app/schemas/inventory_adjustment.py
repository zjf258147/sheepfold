from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class InventoryAdjustmentResponse(BaseModel):
    id: int
    adjustment_no: str
    stocktake_id: int
    stocktake_no: Optional[str] = None
    stocktake_line_id: int
    item_sn: str
    adjustment_type: str
    before_status: str
    after_status: str
    reason: str
    operator_id: int
    operator_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class InventoryAdjustmentCreate(BaseModel):
    stocktake_id: int
    stocktake_line_id: int
    adjustment_type: str = Field(..., max_length=10)
    reason: str = Field(..., max_length=500)


class InventoryAdjustmentConfirmRequest(BaseModel):
    adjustment_ids: list[int] = Field(..., min_length=1)