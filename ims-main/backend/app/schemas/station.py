from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class StationResponse(BaseModel):
    id: int
    name: str
    customer_id: int
    customer_name: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    status: str
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class StationCreate(BaseModel):
    name: str = Field(..., max_length=200)
    customer_id: int
    address: Optional[str] = None
    contact_person: Optional[str] = Field(None, max_length=50)
    contact_phone: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = None
    remark: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("场站名称不能为空")
        return v


class StationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    customer_id: Optional[int] = None
    address: Optional[str] = None
    contact_person: Optional[str] = Field(None, max_length=50)
    contact_phone: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = None
    remark: Optional[str] = None