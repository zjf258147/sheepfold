from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.incoming import (
    IncomingInspectionCreate,
    IncomingInspectionResponse,
    IncomingReceiptCreate,
    IncomingReceiptResponse,
    IncomingReceiptUpdate,
    IncomingReturnCreate,
    IncomingReturnResponse,
)
from app.service import incoming_service

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
    return {"total": total, "items": items}


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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return incoming_service.create_receipt(db, data)


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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return incoming_service.create_inspection(db, data)


@router.post("/returns", status_code=201)
def create_return(
    data: IncomingReturnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return incoming_service.create_return(db, data)