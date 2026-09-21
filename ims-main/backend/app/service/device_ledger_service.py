from datetime import date

from sqlalchemy.orm import Session, joinedload

from app.models.device_ledger import DeviceLedger
from app.models.enums import DeviceLedgerStatus
from app.models.user import User
from app.schemas.device_ledger import DeviceLedgerCreate, DeviceLedgerUpdate, WarrantyCheckResponse


def get_device_ledger_list(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    keyword: str | None = None,
    station_id: int | None = None,
    status: str | None = None,
) -> tuple[int, list[DeviceLedger]]:
    query = db.query(DeviceLedger).options(joinedload(DeviceLedger.station))
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
    return (
        db.query(DeviceLedger)
        .options(joinedload(DeviceLedger.station))
        .filter(DeviceLedger.id == ledger_id)
        .first()
    )


def get_device_by_sn_station(db: Session, item_sn: str, station_id: int) -> DeviceLedger | None:
    return (
        db.query(DeviceLedger)
        .filter(DeviceLedger.item_sn == item_sn, DeviceLedger.station_id == station_id)
        .first()
    )


def create_device_ledger(db: Session, data: DeviceLedgerCreate, user: User | None = None) -> DeviceLedger:
    from app.service.rma_service import write_audit_log

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

    if user:
        from app.models.station import Station
        st = db.query(Station).filter(Station.id == data.station_id).first()
        write_audit_log(
            db, user, action="CREATE", module="device",
            resource_type="device_ledger", resource_id=str(ledger.id),
            resource_name=f"{data.item_sn} 安装",
            summary=f"设备 {data.item_sn} 安装到场站 {st.name if st else data.station_id}",
            change_reason=data.remark,
        )

    db.refresh(ledger)
    return ledger


def update_device_ledger(db: Session, ledger_id: int, data: DeviceLedgerUpdate, user: User | None = None) -> DeviceLedger:
    from app.service.rma_service import write_audit_log

    ledger = db.query(DeviceLedger).options(joinedload(DeviceLedger.station)).filter(DeviceLedger.id == ledger_id).first()
    if not ledger:
        raise ValueError("设备台账记录不存在")
    old_station_id = ledger.station_id
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ledger, key, value)
    db.flush()

    new_station_id = update_data.get("station_id")
    if new_station_id is not None and new_station_id != old_station_id:
        from app.models.station import Station
        old_s = db.query(Station).filter(Station.id == old_station_id).first()
        new_s = db.query(Station).filter(Station.id == new_station_id).first()
        if user:
            write_audit_log(
                db, user, action="STATION_CHANGE", module="device",
                resource_type="device_ledger", resource_id=str(ledger.id),
                resource_name=f"{ledger.item_sn} 站址变更",
                summary=f"设备 {ledger.item_sn} 从 {old_s.name if old_s else old_station_id} 变更为 {new_s.name if new_s else new_station_id}",
                change_reason=getattr(data, 'remark', None),
            )

    return ledger


def remove_device(db: Session, ledger_id: int, removed_date: date, user: User | None = None) -> DeviceLedger:
    from app.service.rma_service import write_audit_log

    ledger = db.query(DeviceLedger).options(joinedload(DeviceLedger.station)).filter(DeviceLedger.id == ledger_id).first()
    if not ledger:
        raise ValueError("设备台账记录不存在")
    ledger.removed_date = removed_date
    ledger.status = DeviceLedgerStatus.RECOVERED.value
    db.flush()

    if user:
        station_name = ledger.station.name if ledger.station else None
        write_audit_log(
            db, user, action="REMOVE", module="device",
            resource_type="device_ledger", resource_id=str(ledger.id),
            resource_name=f"{ledger.item_sn} 移除",
            summary=f"设备 {ledger.item_sn} 从场站 {station_name or ledger.station_id} 移除",
        )

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


def get_device_lifecycle(db: Session, sn: str) -> dict:
    from datetime import datetime

    from app.models.audit_log import AuditLog
    from app.models.inventory import InventoryItem
    from app.models.rma import RmaRepair
    from app.models.shipment import Shipment
    from app.models.stocktake import Stocktake

    # 检查 SN 是否存在于任何源表中
    sn_exists = (
        db.query(DeviceLedger.id).filter(DeviceLedger.item_sn == sn).limit(1).scalar()
        or db.query(InventoryItem.id).filter(InventoryItem.item_sn == sn).limit(1).scalar()
        or db.query(Shipment.id).filter(Shipment.sn_list.like(f"%{sn}%")).limit(1).scalar()
        or db.query(RmaRepair.id).filter(RmaRepair.old_sn == sn).limit(1).scalar()
        or db.query(Stocktake.id).filter(Stocktake.item_sn == sn).limit(1).scalar()
    )
    if not sn_exists:
        raise ValueError(f"设备 SN 不存在：{sn}")

    events: list[dict] = []

    # 1. 生产事件 (PRODUCTION)
    inv = db.query(InventoryItem).filter(InventoryItem.item_sn == sn).first()
    if inv:
        events.append({
            "timestamp": inv.created_at,
            "event_type": "PRODUCTION",
            "description": f"设备 {sn} 生产入库",
            "order_no": None,
            "detail": {
                "sku_id": inv.sku_id,
                "stock_status": inv.stock_status,
                "warehouse_type": inv.warehouse_type,
            },
        })

    # 2. 站址变更 (STATION_CHANGE) - AuditLog
    station_logs = db.query(AuditLog).filter(
        AuditLog.resource_type == "device_ledger",
        AuditLog.action == "STATION_CHANGE",
        AuditLog.resource_name.like(f"%{sn}%"),
    ).order_by(AuditLog.created_at).all()
    for log in station_logs:
        events.append({
            "timestamp": log.created_at,
            "event_type": "STATION_CHANGE",
            "description": log.summary or f"设备 {sn} 站址变更",
            "order_no": None,
            "detail": {
                "operator": log.operator_name,
                "change_reason": log.change_reason,
            },
        })

    # 3. 设备安装/移除 (INSTALL/REMOVE)
    devices = db.query(DeviceLedger).filter(DeviceLedger.item_sn == sn).order_by(DeviceLedger.id).all()
    for dev in devices:
        station_name = dev.station.name if dev.station else None
        events.append({
            "timestamp": dev.created_at,
            "event_type": "INSTALL",
            "description": f"设备安装到场站 {station_name or dev.station_id}",
            "order_no": None,
            "detail": {
                "station_id": dev.station_id,
                "station_name": station_name,
                "installed_date": str(dev.installed_date),
            },
        })
        if dev.removed_date:
            events.append({
                "timestamp": datetime(dev.removed_date.year, dev.removed_date.month, dev.removed_date.day, 0, 0, 0),
                "event_type": "REMOVE",
                "description": f"设备从场站 {station_name or dev.station_id} 移除",
                "order_no": None,
                "detail": {
                    "station_id": dev.station_id,
                    "station_name": station_name,
                    "removed_date": str(dev.removed_date),
                },
            })

    # 4. 维修事件 (REPAIR)
    from app.models.rma import RmaRepair, RmaDiagnosis
    repairs = db.query(RmaRepair).filter(RmaRepair.old_sn == sn).order_by(RmaRepair.id).all()
    for rp in repairs:
        diag = db.query(RmaDiagnosis).filter(RmaDiagnosis.return_id == rp.return_id).order_by(
            RmaDiagnosis.id.desc()
        ).first()
        events.append({
            "timestamp": rp.created_at,
            "event_type": "REPAIR",
            "description": f"设备 {sn} 维修：{rp.repair_description or '无描述'}",
            "order_no": rp.repair_no,
            "detail": {
                "repair_no": rp.repair_no,
                "fault_code": rp.fault_code,
                "new_sn": rp.new_sn,
                "diagnosis": diag.diagnosis_result if diag else None,
            },
        })

    # 5. 出货事件 (OUTBOUND)
    shipments = db.query(Shipment).filter(Shipment.sn_list.like(f"%{sn}%")).order_by(Shipment.id).all()
    for sh in shipments:
        events.append({
            "timestamp": sh.created_at,
            "event_type": "OUTBOUND",
            "description": f"设备 {sn} 出货：{sh.shipment_no}",
            "order_no": sh.shipment_no,
            "detail": {
                "shipment_no": sh.shipment_no,
                "recipient": sh.recipient,
                "status": sh.status,
            },
        })

    # 6. 盘点事件 (STOCKTAKE)
    stocktakes = db.query(Stocktake).filter(Stocktake.item_sn == sn).order_by(Stocktake.id).all()
    for st in stocktakes:
        events.append({
            "timestamp": st.created_at,
            "event_type": "STOCKTAKE",
            "description": f"设备 {sn} 盘点：{st.remark or ''}",
            "order_no": st.task_no,
            "detail": {
                "task_no": st.task_no,
                "difference": st.difference_qty,
            },
        })

    events.sort(key=lambda e: e["timestamp"] if isinstance(e["timestamp"], datetime) else datetime.min)

    return {
        "item_sn": sn,
        "events": events,
        "total_events": len(events),
    }