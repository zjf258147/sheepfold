from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.stocktake import Stocktake, StocktakeLine
from app.models.inventory import InventoryItem
from app.models.enums import StocktakeStatus
from app.schemas.stocktake import StocktakeCreate, ScanItemRequest
from app.utils.order_no import generate_stocktake_no


def _generate_stocktake_no(db: Session) -> str:
    return generate_stocktake_no(db)


def get_stocktake_list(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
) -> tuple[int, list[Stocktake]]:
    query = db.query(Stocktake)
    if status:
        query = query.filter(Stocktake.status == status)
    total = query.count()
    items = (
        query.order_by(Stocktake.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return total, items


def get_stocktake_by_id(db: Session, stocktake_id: int) -> Stocktake | None:
    return db.query(Stocktake).filter(Stocktake.id == stocktake_id).first()


def create_stocktake(db: Session, data: StocktakeCreate, user_id: int) -> Stocktake:
    stocktake = Stocktake(
        stocktake_no=_generate_stocktake_no(db),
        mode=data.mode,
        warehouse=data.warehouse,
        status=StocktakeStatus.IN_PROGRESS.value,
        created_by=user_id,
        started_at=datetime.now(),
        remark=data.remark,
    )
    db.add(stocktake)
    db.flush()
    return stocktake


def get_stocktake_lines(db: Session, stocktake_id: int) -> list[StocktakeLine]:
    return db.query(StocktakeLine).filter(StocktakeLine.stocktake_id == stocktake_id).all()


def scan_items(db: Session, stocktake_id: int, items: list[ScanItemRequest], user_id: int) -> Stocktake:
    stocktake = db.query(Stocktake).filter(Stocktake.id == stocktake_id).first()
    if not stocktake:
        raise ValueError("盘点任务不存在")
    if stocktake.status != StocktakeStatus.IN_PROGRESS.value:
        raise ValueError("盘点任务非进行中状态")

    now = datetime.now()
    for item in items:
        line = (
            db.query(StocktakeLine)
            .filter(
                StocktakeLine.stocktake_id == stocktake_id,
                StocktakeLine.item_sn == item.item_sn,
            )
            .first()
        )
        inventory_item = db.query(InventoryItem).filter(InventoryItem.item_sn == item.item_sn).first()
        sku_id = inventory_item.sku_id if inventory_item else None
        system_qty = 1 if inventory_item else 0

        if line:
            line.actual_qty = item.actual_qty
            line.diff_qty = line.actual_qty - line.system_qty
            line.scanned_at = now
            line.scanned_by = user_id
        else:
            new_line = StocktakeLine(
                stocktake_id=stocktake_id,
                item_sn=item.item_sn,
                sku_id=sku_id,
                system_qty=system_qty,
                actual_qty=item.actual_qty,
                diff_qty=item.actual_qty - system_qty,
                scanned_at=now,
                scanned_by=user_id,
            )
            db.add(new_line)
    db.flush()
    return stocktake


def update_line_reason(db: Session, line_id: int, diff_reason: str) -> StocktakeLine:
    line = db.query(StocktakeLine).filter(StocktakeLine.id == line_id).first()
    if not line:
        raise ValueError("盘点明细不存在")
    line.diff_reason = diff_reason
    db.flush()
    return line


def complete_stocktake(db: Session, stocktake_id: int, remark: str | None) -> Stocktake:
    stocktake = db.query(Stocktake).filter(Stocktake.id == stocktake_id).first()
    if not stocktake:
        raise ValueError("盘点任务不存在")
    if stocktake.status != StocktakeStatus.IN_PROGRESS.value:
        raise ValueError("盘点任务非进行中状态")
    stocktake.status = StocktakeStatus.COMPLETED.value
    stocktake.completed_at = datetime.now()
    if remark:
        stocktake.remark = remark
    db.flush()
    return stocktake


def cancel_stocktake(db: Session, stocktake_id: int) -> Stocktake:
    stocktake = db.query(Stocktake).filter(Stocktake.id == stocktake_id).first()
    if not stocktake:
        raise ValueError("盘点任务不存在")
    if stocktake.status not in (StocktakeStatus.IN_PROGRESS.value, StocktakeStatus.COMPLETED.value):
        raise ValueError("盘点任务状态不允许取消")
    stocktake.status = StocktakeStatus.CANCELLED.value
    db.flush()
    return stocktake