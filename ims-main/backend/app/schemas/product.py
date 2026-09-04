from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.models.enums import SnMode, SkuType


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("分类名称不能为空")
        return v


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("分类名称不能为空")
        return v


class CategoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class SkuCreate(BaseModel):
    name: str = Field(..., max_length=200)
    category_id: int
    barcode: str = Field(..., max_length=50)
    unit: str | None = Field(None, max_length=20)
    sku_code: str | None = Field(None, max_length=50)
    spec: str | None = Field(None, max_length=100)
    sku_type: SkuType = SkuType.FINISHED_GOODS
    sn_mode: SnMode = SnMode.BOTH
    status: int = 1
    remark: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("商品名称不能为空")
        return v


class SkuUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None
    barcode: str | None = None
    unit: str | None = None
    sku_code: str | None = None
    spec: str | None = None
    sku_type: SkuType | None = None
    sn_mode: SnMode | None = None
    status: int | None = None
    remark: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("商品名称不能为空")
        return v


class SkuResponse(BaseModel):
    id: int
    name: str
    category_id: int
    barcode: str
    unit: str | None
    sku_code: str | None
    spec: str | None
    sku_type: str
    sn_mode: str
    status: int
    remark: str | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}