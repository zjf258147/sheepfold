from sqlalchemy import ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import SnMode, SkuType


class ProductCategory(Base, TimestampMixin):
    """商品分类。"""

    __tablename__ = "product_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment="分类名称")

    skus: Mapped[list["ProductSku"]] = relationship(back_populates="category")


class ProductSku(Base, TimestampMixin):
    """商品 SKU。"""

    __tablename__ = "product_sku"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="商品ID")
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="商品名称")
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_category.id"), nullable=False, index=True, comment="分类ID"
    )
    barcode: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="条码编码，如 NO00001")
    sn_mode: Mapped[SnMode] = mapped_column(
        String(10), default=SnMode.BOTH, nullable=False, comment="SN模式：MANUAL/AUTO/BOTH"
    )
    unit: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="计量单位，如 个/张/份/副")
    sku_code: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True, comment="物料编码（U9编码）")
    spec: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="规格型号")
    sku_type: Mapped[SkuType] = mapped_column(
        String(20), default=SkuType.FINISHED_GOODS, nullable=False, comment="物料类型：RAW_MATERIAL/FINISHED_GOODS"
    )
    status: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False, comment="1=启用 0=停用")
    remark: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="备注")

    category: Mapped["ProductCategory"] = relationship(back_populates="skus")