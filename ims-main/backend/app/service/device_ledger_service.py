from datetime import date

from sqlalchemy.orm import Session

from app.models.device_ledger import DeviceLedger
from app.models.station import Station
from app.models.enums import DeviceLedgerStatus
from app.schemas.device_ledger import DeviceLedgerCreate, DeviceLedgerUpdate, WarrantyCheckResponse


def get_device_ledger_list(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    keyword: str | None = None,
    station_id: int | None = None,
    status: str | None = None,
) -> tuple[int, list[DeviceLedger]]:
    query = db.query(DeviceLedger)
    if keyword and keyword.strip():
        query = query.filter(DeviceLedger.item_sn.like(f"%{keyword.strip()}%"))
    if station_id:
        query = query.filter(DeviceLedger.station_id == station_id)
    if status:
        query = query.filter(DeviceLedger.status == status)
    total = query.count()
    items = (
        query.order_by(DeviceLedger.installed_date.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return total, items


def get_device_by_id(db: Session, ledger_id: int) -> DeviceLedger | None:
    return db.query(DeviceLedger).filter(DeviceLedger.id == ledger_id).first()


def get_device_by_sn_station(db: Session, item_sn: str, station_id: int) -> DeviceLedger | None:
    return (
        db.query(DeviceLedger)
        .filter(DeviceLedger.item_sn == item_sn, DeviceLedger.station_id == station_id)
        .first()
    )


def create_device_ledger(db: Session, data: DeviceLedgerCreate) -> DeviceLedger:
    existing = (
        db.query(DeviceLedger)
        .filter(
            DeviceLedger.item_sn == data.item_sn,
            DeviceLedger.station_id == data.station_id,
            DeviceLedger.removed_date.is_(None),
        )
        .first()
    )
    if existing:
        raise ValueError(f"设备已在场站中存在且未移除: {data.item_sn}")
    ledger = DeviceLedger(
        item_sn=data.item_sn,
        station_id=data.station_id,
        installed_date=data.installed_date,
        warranty_start=data.warranty_start,
        warranty_end=data.warranty_end,
        software_version=data.software_version,
        remark=data.remark,
    )
    db.add(ledger)
    db.flush()
    return ledger


def update_device_ledger(db: Session, ledger_id: int, data: DeviceLedgerUpdate) -> DeviceLedger:
    ledger = db.query(DeviceLedger).filter(DeviceLedger.id == ledger_id).first()
    if not ledger:
        raise ValueError("设备台账记录不存在")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ledger, key, value)
    db.flush()
    return ledger


def remove_device(db: Session, ledger_id: int, removed_date: date) -> DeviceLedger:
    ledger = db.query(DeviceLedger).filter(DeviceLedger.id == ledger_id).first()
    if not ledger:
        raise ValueError("设备台账记录不存在")
    ledger.removed_date = removed_date
    ledger.status = DeviceLedgerStatus.RECOVERED.value
    db.flush()
    return ledger


def check_warranty(db: Session, item_sn: str) -> WarrantyCheckResponse:
    ledger = (
        db.query(DeviceLedger)
        .filter(DeviceLedger.item_sn == item_sn, DeviceLedger.removed_date.is_(None))
        .first()
    )
    if not ledger or not ledger.warranty_end:
        return WarrantyCheckResponse(
            item_sn=item_sn,
            in_warranty=False,
            warranty_start=ledger.warranty_start if ledger else None,
            warranty_end=None,
            days_remaining=None,
            status=ledger.status if ledger else None,
        )
    today = date.today()
    days_remaining = (ledger.warranty_end - today).days
    in_warranty = days_remaining >= 0
    return WarrantyCheckResponse(
        item_sn=item_sn,
        in_warranty=in_warranty,
        warranty_start=ledger.warranty_start,
        warranty_end=ledger.warranty_end,
        days_remaining=days_remaining,
        status=ledger.status,
    )