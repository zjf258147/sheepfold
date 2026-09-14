from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CustomerResponse(BaseModel):
    id: int
    name: str
    weight: int
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    contract_no: Optional[str] = None
    contract_start: Optional[date] = None
    contract_end: Optional[date] = None
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class CustomerCreate(BaseModel):
    name: str = Field(..., max_length=200)
    weight: int = 0
    contact_person: Optional[str] = Field(None, max_length=50)
    contact_phone: Optional[str] = Field(None, max_length=20)
    contact_email: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    contract_no: Optional[str] = Field(None, max_length=50)
    contract_start: Optional[date] = None
    contract_end: Optional[date] = None
    remark: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("客户名称不能为空")
        return v


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    weight: Optional[int] = None
    contact_person: Optional[str] = Field(None, max_length=50)
    contact_phone: Optional[str] = Field(None, max_length=20)
    contact_email: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    contract_no: Optional[str] = Field(None, max_length=50)
    contract_start: Optional[date] = None
    contract_end: Optional[date] = None
    remark: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("客户名称不能为空")
        return v