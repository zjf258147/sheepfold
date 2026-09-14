from sqlalchemy.orm import Session

from app.core.cache import get_cache, invalidate_cache
from app.db.database import get_db
from app.models.product import ProductCategory, ProductSku
from app.schemas.product import CategoryCreate, CategoryUpdate, SkuCreate, SkuUpdate
from app.utils.excel_export import build_simple_xlsx
from app.utils.excel_import import build_template_xlsx, parse_import_xlsx
import json


CATEGORY_CACHE_KEY = "ims:categories:all"
CATEGORY_CACHE_TTL = 600


def get_categories(db: Session) -> list[ProductCategory]:
    cache = get_cache()
    cached = cache.get(CATEGORY_CACHE_KEY)
    if cached is not None:
        return [ProductCategory(**item) for item in json.loads(cached)]
    result = db.query(ProductCategory).order_by(ProductCategory.id).all()
    cache.set(CATEGORY_CACHE_KEY, json.dumps([{
        "id": c.id, "name": c.name, "created_at": str(c.created_at), "updated_at": str(c.updated_at),
    } for c in result], default=str), ttl=CATEGORY_CACHE_TTL)
    return result


def create_category(db: Session, data: CategoryCreate) -> ProductCategory:
    if db.query(ProductCategory).filter(ProductCategory.name == data.name).first():
        raise ValueError(f"分类名称已存在：{data.name}")
    cat = ProductCategory(name=data.name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    invalidate_cache(CATEGORY_CACHE_KEY)
    return cat


def update_category(db: Session, cat: ProductCategory, data: CategoryUpdate) -> ProductCategory:
    if data.name and data.name != cat.name:
        if db.query(ProductCategory).filter(ProductCategory.name == data.name).first():
            raise ValueError(f"分类名称已存在：{data.name}")
        cat.name = data.name
    db.commit()
    db.refresh(cat)
    invalidate_cache(CATEGORY_CACHE_KEY)
    return cat


def delete_category(db: Session, cat: ProductCategory) -> None:
    if db.query(ProductSku).filter(ProductSku.category_id == cat.id).first():
        raise ValueError("分类下存在商品，无法删除")
    db.delete(cat)
    db.commit()
    invalidate_cache(CATEGORY_CACHE_KEY)


def get_skus(db: Session, page: int = 1, page_size: int = 20, category_id: int | None = None, keyword: str | None = None):
    query = db.query(ProductSku)
    if category_id:
        query = query.filter(ProductSku.category_id == category_id)
    if keyword:
        query = query.filter(
            ProductSku.name.like(f"%{keyword}%")
            | ProductSku.barcode.like(f"%{keyword}%")
            | ProductSku.sku_code.like(f"%{keyword}%")
        )
    total = query.count()
    items = query.order_by(ProductSku.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return total, items


def get_sku_by_id(db: Session, sku_id: int) -> ProductSku | None:
    return db.get(ProductSku, sku_id)


def create_sku(db: Session, data: SkuCreate) -> ProductSku:
    if db.query(ProductSku).filter(ProductSku.barcode == data.barcode).first():
        raise ValueError(f"条码已存在：{data.barcode}")
    sku = ProductSku(**data.model_dump())
    db.add(sku)
    db.commit()
    db.refresh(sku)
    return sku


def update_sku(db: Session, sku: ProductSku, data: SkuUpdate) -> ProductSku:
    update_data = data.model_dump(exclude_none=True)
    if "barcode" in update_data and update_data["barcode"] != sku.barcode:
        if db.query(ProductSku).filter(ProductSku.barcode == update_data["barcode"]).first():
            raise ValueError(f"条码已存在：{update_data['barcode']}")
    for k, v in update_data.items():
        setattr(sku, k, v)
    db.commit()
    db.refresh(sku)
    return sku


def delete_sku(db: Session, sku: ProductSku) -> None:
    from app.models.inventory import InventoryItem
    if db.query(InventoryItem).filter(InventoryItem.sku_id == sku.id).first():
        raise ValueError("该 SKU 已有库存记录，无法删除")
    db.delete(sku)
    db.commit()


SKU_IMPORT_HEADERS = ["物料名称", "分类名称", "物料编码", "规格型号", "条码", "单位", "SN模式", "物料类型", "备注"]
SKU_IMPORT_COL_WIDTHS = [20, 16, 16, 14, 16, 8, 10, 12, 20]


def export_sku_template() -> bytes:
    return build_template_xlsx(
        SKU_IMPORT_HEADERS,
        example_row=["示例物料", "成品", "SKU001", "规格A", "BAR001", "个", "BOTH", "成品", "备注示例"],
        sheet_title="SKU导入模板",
        col_widths=SKU_IMPORT_COL_WIDTHS,
    )


def export_sku_xlsx(db: Session, keyword: str | None = None, category_id: int | None = None) -> bytes:
    total, items = get_skus(db, page=1, page_size=99999, keyword=keyword, category_id=category_id)
    headers = SKU_IMPORT_HEADERS
    rows = []
    for s in items:
        rows.append([
            s.name or "", (s.category.name if s.category else ""),
            s.sku_code or "", s.spec or "",
            s.barcode or "", s.unit or "",
            s.sn_mode or "", s.sku_type or "",
            s.remark or "",
        ])
    return build_simple_xlsx(headers, rows, sheet_title="SKU列表", col_widths=SKU_IMPORT_COL_WIDTHS)


def import_sku_xlsx(db: Session, content: bytes) -> dict:
    rows = parse_import_xlsx(content)
    success, errors = 0, []
    for i, row in enumerate(rows, 1):
        try:
            if len(row) < 4:
                errors.append(f"第{i}行：列数不足")
                continue
            name, cat_name, sku_code, spec, barcode, unit, sn_mode, sku_type, remark = row[0], row[1], row[2], row[3], row[4] if len(row) > 4 else "", row[5] if len(row) > 5 else "", row[6] if len(row) > 6 else "BOTH", row[7] if len(row) > 7 else "成品", row[8] if len(row) > 8 else ""
            if not name.strip():
                errors.append(f"第{i}行：物料名称为空")
                continue
            cat = db.query(ProductCategory).filter(ProductCategory.name == cat_name.strip()).first()
            if not cat:
                cat = ProductCategory(name=cat_name.strip() or "未分类")
                db.add(cat)
                db.flush()
            if not barcode.strip():
                import uuid
                barcode = "BAR" + uuid.uuid4().hex[:8].upper()
            existing = db.query(ProductSku).filter(ProductSku.barcode == barcode.strip()).first()
            if existing:
                errors.append(f"第{i}行：条码 {barcode.strip()} 已存在")
                continue
            sn_map = {"BOTH": "BOTH", "MANUAL": "MANUAL", "AUTO": "AUTO", "手动": "MANUAL", "自动": "AUTO", "手动+自动": "BOTH"}
            sn = sn_map.get(sn_mode.strip(), "BOTH") if sn_mode and sn_mode.strip() else "BOTH"
            type_map = {"成品": "FINISHED_GOODS", "原材料": "RAW_MATERIAL", "半成品": "FINISHED_GOODS", "FINISHED_GOODS": "FINISHED_GOODS", "RAW_MATERIAL": "RAW_MATERIAL"}
            st = type_map.get(sku_type.strip(), "FINISHED_GOODS") if sku_type and sku_type.strip() else "FINISHED_GOODS"
            sku = ProductSku(
                name=name.strip(), category_id=cat.id, sku_code=sku_code.strip() or None,
                spec=spec.strip() or None, barcode=barcode.strip(), unit=unit.strip() or None,
                sn_mode=sn, sku_type=st, remark=remark.strip() or None,
            )
            db.add(sku)
            db.flush()
            success += 1
        except Exception as e:
            errors.append(f"第{i}行：{str(e)}")
    db.commit()
    return {"success": success, "errors": errors}