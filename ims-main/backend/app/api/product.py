from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.permissions import require_permission
from app.db.database import get_db
from app.models.product import ProductCategory
from app.models.user import User
from app.schemas.audit import AuditLogCreate
from app.schemas.common import R, PageResult
from app.schemas.product import *
from app.service import audit_service, product_service
from app.utils.request_ip import get_client_ip

router = APIRouter(prefix="/products", tags=["商品SKU"])


@router.get("/categories", response_model=R[list[CategoryResponse]], summary="分类列表")
def list_categories(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return R.ok(data=[CategoryResponse.model_validate(c) for c in product_service.get_categories(db)])


@router.post("/categories", response_model=R[CategoryResponse], status_code=201, summary="新增分类")
def create_category(
    data: CategoryCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("product.manage")),
):
    try:
        cat = product_service.create_category(db, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    audit_service.record(
        db,
        current_user,
        AuditLogCreate(
            action="CREATE",
            module="product",
            resource_type="category",
            resource_id=str(cat.id),
            resource_name=cat.name,
            summary=audit_service.build_summary(current_user, "CREATE", f"商品分类「{cat.name}」"),
            after_data=audit_service.to_audit_data(cat),
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(data=CategoryResponse.model_validate(cat))


@router.put("/categories/{cat_id}", response_model=R[CategoryResponse], summary="修改分类")
def update_category(
    cat_id: int,
    data: CategoryUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("product.manage")),
):
    cat = db.get(ProductCategory, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="分类不存在")
    before = audit_service.to_audit_data(cat)
    try:
        cat = product_service.update_category(db, cat, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    audit_service.record(
        db,
        current_user,
        AuditLogCreate(
            action="UPDATE",
            module="product",
            resource_type="category",
            resource_id=str(cat.id),
            resource_name=cat.name,
            summary=audit_service.build_summary(current_user, "UPDATE", f"商品分类「{cat.name}」"),
            before_data=before,
            after_data=audit_service.to_audit_data(cat),
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(data=CategoryResponse.model_validate(cat))


@router.delete("/categories/{cat_id}", response_model=R, summary="删除分类")
def delete_category(
    cat_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("product.manage")),
):
    cat = db.get(ProductCategory, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="分类不存在")
    before = audit_service.to_audit_data(cat)
    name = cat.name
    try:
        product_service.delete_category(db, cat)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    audit_service.record(
        db,
        current_user,
        AuditLogCreate(
            action="DELETE",
            module="product",
            resource_type="category",
            resource_id=str(cat_id),
            resource_name=name,
            summary=audit_service.build_summary(current_user, "DELETE", f"商品分类「{name}」"),
            before_data=before,
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(msg="删除成功")


@router.get("/skus", response_model=R[PageResult[SkuResponse]], summary="SKU列表")
def list_skus(page: int = 1, page_size: int = 20, category_id: int | None = None, keyword: str | None = None,
              db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    total, items = product_service.get_skus(db, page, page_size, category_id, keyword)
    return R.ok(data=PageResult(total=total, page=page, page_size=page_size,
                                items=[SkuResponse.model_validate(s) for s in items]))


@router.post("/skus", response_model=R[SkuResponse], status_code=201, summary="新增SKU")
def create_sku(
    data: SkuCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("product.manage")),
):
    try:
        sku = product_service.create_sku(db, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    audit_service.record(
        db,
        current_user,
        AuditLogCreate(
            action="CREATE",
            module="product",
            resource_type="sku",
            resource_id=str(sku.id),
            resource_name=sku.name,
            summary=audit_service.build_summary(current_user, "CREATE", f"商品SKU「{sku.name}」", sku.barcode),
            after_data=audit_service.to_audit_data(sku),
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(data=SkuResponse.model_validate(sku))


@router.get("/skus/export", summary="导出SKU列表 Excel")
def export_skus(
    keyword: str | None = None,
    category_id: int | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    content = product_service.export_sku_xlsx(db, keyword=keyword, category_id=category_id)
    filename = quote("SKU列表.xlsx")
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"},
    )


@router.get("/skus/template", summary="下载SKU导入模板")
def download_sku_template(_: User = Depends(get_current_user)):
    content = product_service.export_sku_template()
    filename = quote("SKU导入模板.xlsx")
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"},
    )


@router.post("/skus/import", summary="导入SKU Excel")
async def import_skus(
    file: UploadFile,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("product.manage")),
):
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="请上传 .xlsx 或 .xls 文件")
    content = await file.read()
    result = product_service.import_sku_xlsx(db, content)
    return R.ok(data=result, msg=f"成功 {result['success']} 条，失败 {len(result['errors'])} 条")


@router.get("/skus/{sku_id}", response_model=R[SkuResponse], summary="SKU详情")
def get_sku(sku_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    sku = product_service.get_sku_by_id(db, sku_id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU不存在")
    return R.ok(data=SkuResponse.model_validate(sku))


@router.put("/skus/{sku_id}", response_model=R[SkuResponse], summary="修改SKU")
def update_sku(
    sku_id: int,
    data: SkuUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("product.manage")),
):
    sku = product_service.get_sku_by_id(db, sku_id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU不存在")
    before = audit_service.to_audit_data(sku)
    try:
        sku = product_service.update_sku(db, sku, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    audit_service.record(
        db,
        current_user,
        AuditLogCreate(
            action="UPDATE",
            module="product",
            resource_type="sku",
            resource_id=str(sku.id),
            resource_name=sku.name,
            summary=audit_service.build_summary(current_user, "UPDATE", f"商品SKU「{sku.name}」", sku.barcode),
            before_data=before,
            after_data=audit_service.to_audit_data(sku),
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(data=SkuResponse.model_validate(sku))


@router.delete("/skus/{sku_id}", response_model=R, summary="删除SKU")
def delete_sku(
    sku_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("product.manage")),
):
    sku = product_service.get_sku_by_id(db, sku_id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU不存在")
    before = audit_service.to_audit_data(sku)
    name = sku.name
    code = sku.barcode
    try:
        product_service.delete_sku(db, sku)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    audit_service.record(
        db,
        current_user,
        AuditLogCreate(
            action="DELETE",
            module="product",
            resource_type="sku",
            resource_id=str(sku_id),
            resource_name=name,
            summary=audit_service.build_summary(current_user, "DELETE", f"商品SKU「{name}」", code),
            before_data=before,
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(msg="删除成功")