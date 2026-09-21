from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter, Depends, Query, Request, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.permissions import require_permission
from app.db.database import get_db
from app.models.user import User
from app.schemas.common import PageResult, R
from app.schemas.incoming import (
    IncomingInspectionCreate,
    IncomingInspectionResponse,
    IncomingReceiptConfirm,
    IncomingReceiptCreate,
    IncomingReceiptResponse,
    IncomingReceiptUpdate,
    IncomingReturnCreate,
    IncomingReturnResponse,
)
from app.service import incoming_service
from app.utils.request_ip import get_client_ip

router = APIRouter(prefix="/incoming", tags=["来料管理"])


@router.get("/receipts")
def list_receipts(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    keyword: str | None = None,
    category_id: int | None = None,
    sku_id: int | None = None,
    supplier_id: int | None = None,
    status: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total, items = incoming_service.get_receipts(
        db, page, page_size, keyword, category_id, sku_id, supplier_id, status, start_date, end_date,
    )
    return R.ok(data=PageResult(
        total=total, page=page, page_size=page_size,
        items=[IncomingReceiptResponse.model_validate(item) for item in items],
    ))


@router.get("/receipts/export", summary="导出来料记录 Excel")
def export_receipts(
    keyword: str | None = None,
    category_id: int | None = None,
    sku_id: int | None = None,
    supplier_id: int | None = None,
    status: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    content = incoming_service.export_incoming_xlsx(
        db, keyword=keyword, category_id=category_id,
        sku_id=sku_id, supplier_id=supplier_id,
        status=status, start_date=start_date, end_date=end_date,
    )
    filename = quote("来料管理.xlsx")
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"},
    )


@router.get("/receipts/template", summary="下载来料导入模板")
def download_incoming_template(_: User = Depends(get_current_user)):
    content = incoming_service.export_incoming_template()
    filename = quote("来料导入模板.xlsx")
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"},
    )


@router.post("/receipts/import", summary="导入来料 Excel")
async def import_incoming(
    file: UploadFile,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("incoming.create")),
):
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="请上传 .xlsx 或 .xls 文件")
    content = await file.read()
    result = incoming_service.import_incoming_xlsx(db, content)
    return R.ok(data=result, msg=f"成功 {result['success']} 条，失败 {len(result['errors'])} 条")


@router.get("/receipts/{receipt_id}")
def get_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return incoming_service.get_receipt(db, receipt_id)


@router.post("/receipts", status_code=201)
def create_receipt(
    data: IncomingReceiptCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("incoming.create")),
):
    return incoming_service.create_receipt(db, data, current_user, get_client_ip(request))


@router.post("/receipts/{receipt_id}/confirm")
def confirm_receipt(
    receipt_id: int,
    data: IncomingReceiptConfirm,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("incoming.confirm")),
):
    return incoming_service.confirm_receipt(db, receipt_id, data.change_reason, current_user, get_client_ip(request))


@router.put("/receipts/{receipt_id}")
def update_receipt(
    receipt_id: int,
    data: IncomingReceiptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("incoming.create")),
):
    return incoming_service.update_receipt(db, receipt_id, data)


@router.get("/receipts/{receipt_id}/inspections")
def list_inspections(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return incoming_service.get_inspections(db, receipt_id)


@router.post("/inspections", status_code=201)
def create_inspection(
    data: IncomingInspectionCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("incoming.inspect")),
):
    return incoming_service.create_inspection(db, data, current_user, get_client_ip(request))


@router.post("/returns", status_code=201)
def create_return(
    data: IncomingReturnCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("incoming.return")),
):
    if data.operator_id is None:
        data.operator_id = current_user.id
    return incoming_service.create_return(db, data, current_user, get_client_ip(request))