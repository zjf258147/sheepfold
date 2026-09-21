from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class DeviceLedgerResponse(BaseModel):
    id: int
    item_sn: str
    station_id: int
    station_name: Optional[str] = None
    installed_date: date
    removed_date: Optional[date] = None
    warranty_start: Optional[date] = None
    warranty_end: Optional[date] = None
    software_version: Optional[str] = None
    status: str
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class DeviceLedgerCreate(BaseModel):
    item_sn: str = Field(..., max_length=50)
    station_id: int
    installed_date: date
    warranty_start: Optional[date] = None
    warranty_end: Optional[date] = None
    software_version: Optional[str] = Field(None, max_length=50)
    remark: Optional[str] = None


class DeviceLedgerUpdate(BaseModel):
    station_id: Optional[int] = None
    installed_date: Optional[date] = None
    removed_date: Optional[date] = None
    warranty_start: Optional[date] = None
    warranty_end: Optional[date] = None
    software_version: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = None
    remark: Optional[str] = None


class DeviceRemoveRequest(BaseModel):
    removed_date: date


class WarrantyCheckResponse(BaseModel):
    item_sn: str
    in_warranty: bool
    warranty_start: Optional[date] = None
    warranty_end: Optional[date] = None
    days_remaining: Optional[int] = None
    status: Optional[str] = None


class LifecycleEvent(BaseModel):
    timestamp: datetime
    event_type: str
    description: str
    order_no: str | None = None
    detail: dict | None = None


class DeviceLifecycleResponse(BaseModel):
    item_sn: str
    events: list[LifecycleEvent]
    total_events: int