from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
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
    current_user: User = Depends(get_current_user),
):
    return incoming_service.create_receipt(db, data, current_user, get_client_ip(request))


@router.post("/receipts/{receipt_id}/confirm")
def confirm_receipt(
    receipt_id: int,
    data: IncomingReceiptConfirm,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return incoming_service.confirm_receipt(db, receipt_id, data.change_reason, current_user, get_client_ip(request))


@router.put("/receipts/{receipt_id}")
def update_receipt(
    receipt_id: int,
    data: IncomingReceiptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
):
    return incoming_service.create_inspection(db, data, current_user, get_client_ip(request))


@router.post("/returns", status_code=201)
def create_return(
    data: IncomingReturnCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.operator_id is None:
        data.operator_id = current_user.id
    return incoming_service.create_return(db, data, current_user, get_client_ip(request))