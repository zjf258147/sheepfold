from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.rma import (
    RmaAssignCreate,
    RmaDiagnosisCreate,
    RmaRepairCreate,
    RmaReshipCreate,
    RmaReturnCreate,
    RmaScrapApprove,
    RmaScrapCreate,
    RmaTransferRequest,
)
from app.service import rma_service
from app.utils.request_ip import get_client_ip
from app.schemas.common import PageResult, R

router = APIRouter(prefix="/rma", tags=["RMA 返厂维修"])


@router.get("/returns")
def list_returns(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    keyword: str | None = None,
    status: str | None = None,
    sku_id: int | None = None,
    assigned_to: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = rma_service.get_returns(
        db, page, page_size, keyword, status, sku_id, assigned_to, start_date, end_date
    )
    return R.ok(data=PageResult(items=items, total=total, page=page, page_size=page_size))


@router.get("/returns/{return_id}")
def get_return(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from app.models.rma import RmaReturn
    r = db.query(RmaReturn).filter(RmaReturn.id == return_id).first()
    return R.ok(data=r)


@router.post("/returns", status_code=201)
def create_return(
    data: RmaReturnCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return rma_service.create_return(db, data, current_user, get_client_ip(request))


@router.post("/returns/{return_id}/assign")
def assign_return(
    return_id: int,
    data: RmaAssignCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return rma_service.assign_return(db, return_id, data, current_user, get_client_ip(request))


@router.post("/returns/{return_id}/transfer")
def transfer_return(
    return_id: int,
    data: RmaTransferRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return rma_service.transfer_return(db, return_id, data, current_user, get_client_ip(request))


@router.get("/returns/{return_id}/diagnoses")
def get_diagnoses(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return R.ok(data=rma_service.get_diagnoses(db, return_id))


@router.post("/diagnoses", status_code=201)
def create_diagnosis(
    data: RmaDiagnosisCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return rma_service.create_diagnosis(db, data, current_user, get_client_ip(request))


@router.get("/returns/{return_id}/repairs")
def get_repairs(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return R.ok(data=rma_service.get_repairs(db, return_id))


@router.post("/repairs", status_code=201)
def create_repair(
    data: RmaRepairCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return rma_service.create_repair(db, data, current_user, get_client_ip(request))


@router.get("/returns/{return_id}/scraps")
def get_scraps(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return R.ok(data=rma_service.get_scraps(db, return_id))


@router.post("/scraps", status_code=201)
def create_scrap(
    data: RmaScrapCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return rma_service.create_scrap(db, data, current_user, get_client_ip(request))


@router.post("/scraps/{scrap_id}/approve")
def approve_scrap(
    scrap_id: int,
    data: RmaScrapApprove,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return rma_service.approve_scrap(db, scrap_id, data, current_user, get_client_ip(request))


@router.get("/returns/{return_id}/reships")
def get_reships(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return R.ok(data=rma_service.get_reships(db, return_id))


@router.post("/reships", status_code=201)
def create_reship(
    data: RmaReshipCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return rma_service.create_reship(db, data, current_user, get_client_ip(request))