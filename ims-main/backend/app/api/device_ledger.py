from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.permissions import require_permission
from app.db.database import get_db
from app.models.user import User
from app.models.station import Station
from app.schemas.common import R, PageResult
from app.schemas.device_ledger import (
    DeviceLedgerResponse,
    DeviceLedgerCreate,
    DeviceLedgerUpdate,
    DeviceRemoveRequest,
    WarrantyCheckResponse,
    DeviceLifecycleResponse,
)
from app.service import device_ledger_service

router = APIRouter(prefix="/device-ledger", tags=["设备台账"])


@router.get("", response_model=R[PageResult[DeviceLedgerResponse]], summary="设备台账列表")
def list_devices(
    page: int = 1,
    page_size: int = 20,
    keyword: str | None = None,
    station_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total, items = device_ledger_service.get_device_ledger_list(db, page, page_size, keyword, station_id, status)
    def to_response(d):
        r = DeviceLedgerResponse.model_validate(d)
        if d.station:
            r.station_name = d.station.name
        return r
    return R.ok(
        data=PageResult(
            total=total,
            page=page,
            page_size=page_size,
            items=[to_response(d) for d in items],
        )
    )


@router.get("/{ledger_id}", response_model=R[DeviceLedgerResponse], summary="设备台账详情")
def get_device(
    ledger_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    ledger = device_ledger_service.get_device_by_id(db, ledger_id)
    if not ledger:
        return R.fail("设备台账记录不存在")
    r = DeviceLedgerResponse.model_validate(ledger)
    if ledger.station:
        r.station_name = ledger.station.name
    return R.ok(data=r)


@router.post("", response_model=R[DeviceLedgerResponse], summary="登记设备到场站")
def create_device(
    body: DeviceLedgerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("device_ledger.create_edit")),
):
    try:
        ledger = device_ledger_service.create_device_ledger(db, body, current_user)
        r = DeviceLedgerResponse.model_validate(ledger)
        if ledger.station:
            r.station_name = ledger.station.name
        return R.ok(data=r)
    except ValueError as e:
        return R.fail(str(e))


@router.put("/{ledger_id}", response_model=R[DeviceLedgerResponse], summary="更新设备台账")
def update_device(
    ledger_id: int,
    body: DeviceLedgerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("device_ledger.create_edit")),
):
    try:
        ledger = device_ledger_service.update_device_ledger(db, ledger_id, body, current_user)
        r = DeviceLedgerResponse.model_validate(ledger)
        if ledger.station:
            r.station_name = ledger.station.name
        return R.ok(data=r)
    except ValueError as e:
        return R.fail(str(e))


@router.post("/{ledger_id}/remove", response_model=R[DeviceLedgerResponse], summary="设备回收/移出")
def remove_device(
    ledger_id: int,
    body: DeviceRemoveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("device_ledger.create_edit")),
):
    try:
        ledger = device_ledger_service.remove_device(db, ledger_id, body.removed_date, current_user)
        r = DeviceLedgerResponse.model_validate(ledger)
        if ledger.station:
            r.station_name = ledger.station.name
        return R.ok(data=r)
    except ValueError as e:
        return R.fail(str(e))


@router.get("/warranty/{item_sn}", response_model=R[WarrantyCheckResponse], summary="设备质保检查")
def check_warranty(
    item_sn: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = device_ledger_service.check_warranty(db, item_sn)
    return R.ok(data=result)


@router.get("/{sn}/lifecycle", response_model=R[DeviceLifecycleResponse], summary="设备生命周期追溯")
def get_device_lifecycle(
    sn: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        result = device_ledger_service.get_device_lifecycle(db, sn)
        return R.ok(data=DeviceLifecycleResponse(**result))
    except ValueError:
        raise HTTPException(status_code=404, detail=f"设备 SN 不存在：{sn}")