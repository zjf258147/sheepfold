from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.permissions import require_permission
from app.db.database import get_db
from app.models.user import User
from app.schemas.common import R, PageResult
from app.schemas.inventory_adjustment import (
    InventoryAdjustmentResponse,
    InventoryAdjustmentCreate,
    InventoryAdjustmentConfirmRequest,
)
from app.service import inventory_adjustment_service

router = APIRouter(prefix="/adjustments", tags=["库存调整"])


@router.get("", response_model=R[PageResult[InventoryAdjustmentResponse]], summary="库存调整列表")
def list_adjustments(
    page: int = 1,
    page_size: int = 20,
    stocktake_id: int | None = None,
    adjustment_type: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total, items = inventory_adjustment_service.get_adjustment_list(
        db, page, page_size, stocktake_id, adjustment_type
    )
    return R.ok(
        data=PageResult(
            total=total,
            page=page,
            page_size=page_size,
            items=[InventoryAdjustmentResponse.model_validate(a) for a in items],
        )
    )


@router.get("/{adjustment_id}", response_model=R[InventoryAdjustmentResponse], summary="库存调整详情")
def get_adjustment(
    adjustment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    adj = inventory_adjustment_service.get_adjustment_by_id(db, adjustment_id)
    if not adj:
        return R.fail("调整记录不存在")
    return R.ok(data=InventoryAdjustmentResponse.model_validate(adj))


@router.post("", response_model=R[InventoryAdjustmentResponse], summary="创建库存调整")
def create_adjustment(
    body: InventoryAdjustmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("adjustment.confirm")),
):
    try:
        adj = inventory_adjustment_service.create_adjustment(db, body, current_user.id)
        return R.ok(data=InventoryAdjustmentResponse.model_validate(adj))
    except ValueError as e:
        return R.fail(str(e))


@router.post("/confirm", response_model=R[list[InventoryAdjustmentResponse]], summary="确认库存调整")
def confirm_adjustments(
    body: InventoryAdjustmentConfirmRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("adjustment.confirm")),
):
    try:
        items = inventory_adjustment_service.confirm_adjustments(db, body.adjustment_ids, current_user.id)
        return R.ok(data=[InventoryAdjustmentResponse.model_validate(a) for a in items])
    except ValueError as e:
        return R.fail(str(e))