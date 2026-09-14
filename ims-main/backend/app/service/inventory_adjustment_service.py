from datetime import datetime

from sqlalchemy.orm import Session

from app.models.inventory_adjustment import InventoryAdjustment
from app.models.stocktake import StocktakeLine
from app.models.inventory import InventoryItem, InventoryItemHistory
from app.models.enums import AdjustmentType, StockStatus
from app.schemas.inventory_adjustment import InventoryAdjustmentCreate
from app.utils.order_no import generate_adjustment_no


def _generate_adjustment_no(db: Session) -> str:
    return generate_adjustment_no(db)


def get_adjustment_list(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    stocktake_id: int | None = None,
    adjustment_type: str | None = None,
) -> tuple[int, list[InventoryAdjustment]]:
    query = db.query(InventoryAdjustment)
    if stocktake_id:
        query = query.filter(InventoryAdjustment.stocktake_id == stocktake_id)
    if adjustment_type:
        query = query.filter(InventoryAdjustment.adjustment_type == adjustment_type)
    total = query.count()
    items = (
        query.order_by(InventoryAdjustment.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return total, items


def get_adjustment_by_id(db: Session, adjustment_id: int) -> InventoryAdjustment | None:
    return db.query(InventoryAdjustment).filter(InventoryAdjustment.id == adjustment_id).first()


def create_adjustment(db: Session, data: InventoryAdjustmentCreate, user_id: int) -> InventoryAdjustment:
    line = db.query(StocktakeLine).filter(StocktakeLine.id == data.stocktake_line_id).first()
    if not line:
        raise ValueError("盘点明细不存在")
    if line.diff_qty == 0:
        raise ValueError("盘点差异为0，无需调整")

    if data.adjustment_type == AdjustmentType.SURPLUS.value:
        before_status = StockStatus.IN_STOCK.value
        after_status = StockStatus.IN_STOCK.value
    else:
        inventory_item = db.query(InventoryItem).filter(InventoryItem.item_sn == line.item_sn).first()
        before_status = inventory_item.stock_status if inventory_item else StockStatus.IN_STOCK.value
        after_status = StockStatus.SCRAPPED.value

    adjustment = InventoryAdjustment(
        adjustment_no=_generate_adjustment_no(db),
        stocktake_id=data.stocktake_id,
        stocktake_line_id=data.stocktake_line_id,
        item_sn=line.item_sn,
        adjustment_type=data.adjustment_type,
        before_status=before_status,
        after_status=after_status,
        reason=data.reason,
        operator_id=user_id,
    )
    db.add(adjustment)
    db.flush()
    return adjustment


def confirm_adjustments(db: Session, adjustment_ids: list[int], user_id: int) -> list[InventoryAdjustment]:
    confirmed: list[InventoryAdjustment] = []
    now = datetime.now()
    for adj_id in adjustment_ids:
        adj = db.query(InventoryAdjustment).filter(InventoryAdjustment.id == adj_id).first()
        if not adj:
            raise ValueError(f"调整记录不存在: {adj_id}")

        inventory_item = db.query(InventoryItem).filter(InventoryItem.item_sn == adj.item_sn).first()

        if adj.adjustment_type == AdjustmentType.SURPLUS.value:
            if inventory_item:
                inventory_item.stock_status = StockStatus.IN_STOCK.value
            else:
                raise ValueError(f"库存单品不存在: {adj.item_sn}")
        elif adj.adjustment_type == AdjustmentType.SHORTAGE.value:
            if inventory_item:
                inventory_item.stock_status = StockStatus.SCRAPPED.value
        else:
            raise ValueError(f"未知调整类型: {adj.adjustment_type}")

        history = InventoryItemHistory(
            item_id=inventory_item.id if inventory_item else 0,
            event_type="STOCKTAKE_ADJUST",
            order_no=adj.adjustment_no,
            from_stock_status=adj.before_status,
            to_stock_status=adj.after_status,
            operator_id=user_id,
            remark=adj.reason,
            created_at=now,
        )
        db.add(history)
        confirmed.append(adj)
    db.flush()
    return confirmed