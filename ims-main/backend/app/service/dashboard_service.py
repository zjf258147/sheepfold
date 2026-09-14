from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.device_ledger import DeviceLedger
from app.models.enums import DeviceLedgerStatus, OperationStatus, StationStatus, StocktakeStatus
from app.models.inbound import InboundOrder
from app.models.inventory_adjustment import InventoryAdjustment
from app.models.outbound import OutboundOrder
from app.models.station import Station
from app.models.stocktake import Stocktake
from app.service.inventory_service import get_stock_summary_by_partner, get_stock_summary_by_sku


def get_pending_audit(db: Session) -> dict:
    """待审核统计：已提交且状态为 INITIATED 的单据数。"""
    inbound_count = (
        db.query(InboundOrder)
        .filter(
            InboundOrder.operation_status == OperationStatus.INITIATED.value,
            InboundOrder.submitted_at.isnot(None),
        )
        .count()
    )
    outbound_count = (
        db.query(OutboundOrder)
        .filter(
            OutboundOrder.operation_status == OperationStatus.INITIATED.value,
            OutboundOrder.submitted_at.isnot(None),
        )
        .count()
    )
    return {"inbound_pending": inbound_count, "outbound_pending": outbound_count}


def get_poll_status(db: Session) -> dict:
    """轮询轻量状态，合并待办+设备故障+盘点提醒，单次<50ms。"""
    inbound_pending = (
        db.query(InboundOrder)
        .filter(
            InboundOrder.operation_status == OperationStatus.INITIATED.value,
            InboundOrder.submitted_at.isnot(None),
        )
        .count()
    )
    outbound_pending = (
        db.query(OutboundOrder)
        .filter(
            OutboundOrder.operation_status == OperationStatus.INITIATED.value,
            OutboundOrder.submitted_at.isnot(None),
        )
        .count()
    )
    device_fault = (
        db.query(DeviceLedger)
        .filter(DeviceLedger.status == DeviceLedgerStatus.FAULT.value)
        .count()
    )
    stocktake_in_progress = (
        db.query(Stocktake)
        .filter(Stocktake.status == StocktakeStatus.IN_PROGRESS.value)
        .count()
    )
    pending_adjustments = db.query(InventoryAdjustment).count()
    warranty_expiring_soon = (
        db.query(DeviceLedger)
        .filter(
            DeviceLedger.warranty_end.isnot(None),
            DeviceLedger.warranty_end >= date.today(),
            DeviceLedger.warranty_end <= date.today() + timedelta(days=30),
        )
        .count()
    )
    return {
        "inbound_pending": inbound_pending,
        "outbound_pending": outbound_pending,
        "device_fault": device_fault,
        "stocktake_in_progress": stocktake_in_progress,
        "pending_adjustments": pending_adjustments,
        "warranty_expiring_soon": warranty_expiring_soon,
    }


def get_phase2_stats(db: Session) -> dict:
    """二期统计卡片数据。"""
    station_total = db.query(Station).count()
    station_active = db.query(Station).filter(Station.status == StationStatus.ACTIVE.value).count()

    device_total = db.query(DeviceLedger).count()
    device_running = db.query(DeviceLedger).filter(DeviceLedger.status == DeviceLedgerStatus.RUNNING.value).count()
    device_fault = db.query(DeviceLedger).filter(DeviceLedger.status == DeviceLedgerStatus.FAULT.value).count()
    device_recycled = db.query(DeviceLedger).filter(DeviceLedger.status == DeviceLedgerStatus.RECOVERED.value).count()

    stocktake_in_progress = db.query(Stocktake).filter(
        Stocktake.status == StocktakeStatus.IN_PROGRESS.value
    ).count()
    stocktake_completed = db.query(Stocktake).filter(
        Stocktake.status == StocktakeStatus.COMPLETED.value
    ).count()

    pending_adjustments = db.query(InventoryAdjustment).count()

    warranty_expiring_soon = db.query(DeviceLedger).filter(
        DeviceLedger.warranty_end.isnot(None),
        DeviceLedger.warranty_end >= date.today(),
        DeviceLedger.warranty_end <= date.today() + timedelta(days=30),
    ).count()

    return {
        "station_total": station_total,
        "station_active": station_active,
        "device_total": device_total,
        "device_running": device_running,
        "device_fault": device_fault,
        "device_recycled": device_recycled,
        "stocktake_in_progress": stocktake_in_progress,
        "stocktake_completed": stocktake_completed,
        "pending_adjustments": pending_adjustments,
        "warranty_expiring_soon": warranty_expiring_soon,
    }


def get_stock_summary(db: Session) -> list[dict]:
    """按 SKU 库存统计表。"""
    return get_stock_summary_by_sku(db)


def get_partner_summary(db: Session, sku_ids: list[int] | None = None) -> list[dict]:
    """按关联单位统计不在库单品各状态数量。"""
    return get_stock_summary_by_partner(db, sku_ids=sku_ids)