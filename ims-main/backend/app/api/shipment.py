from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.core.permissions import require_permission
from app.models.user import User
from app.models.shipment import Shipment
from app.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentUpdate
from app.schemas.common import PageResult, R
from app.service import shipment_service
from app.utils.request_ip import get_client_ip

router = APIRouter(prefix="/shipment", tags=["主线C 出货管理"])


@router.get("/list")
def list_shipments(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    keyword: str | None = None,
    sku_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = shipment_service.get_shipments(
        db, page, page_size, keyword, sku_id, start_date, end_date
    )
    items = [ShipmentResponse.model_validate(item) for item in items]
    return R.ok(data=PageResult(items=items, total=total, page=page, page_size=page_size))


@router.get("/{shipment_id}")
def get_shipment(shipment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        return R.fail(msg=f"出货单不存在：{shipment_id}")
    return R.ok(data=ShipmentResponse.model_validate(shipment))


@router.post("/", status_code=201)
def create_shipment(
    data: ShipmentCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipment.create")),
):
    try:
        shipment = shipment_service.create_shipment(
            db, data, current_user.username, get_client_ip(request)
        )
        return R.ok(data=ShipmentResponse.model_validate(shipment))
    except ValueError as e:
        return R.fail(msg=str(e))


@router.put("/{shipment_id}")
def update_shipment(
    shipment_id: int,
    data: ShipmentUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipment.edit")),
):
    try:
        shipment = shipment_service.update_shipment(
            db, shipment_id, data, current_user.username, get_client_ip(request)
        )
        return R.ok(data=ShipmentResponse.model_validate(shipment))
    except ValueError as e:
        return R.fail(msg=str(e))


@router.delete("/{shipment_id}")
def delete_shipment(
    shipment_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipment.edit")),
):
    try:
        shipment_service.delete_shipment(
            db, shipment_id, current_user.username, get_client_ip(request)
        )
        return R.ok()
    except ValueError as e:
        return R.fail(msg=str(e))