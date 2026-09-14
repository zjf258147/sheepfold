from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.common import R, PageResult
from app.schemas.stocktake import (
    StocktakeResponse,
    StocktakeCreate,
    StocktakeScanRequest,
    StocktakeLineResponse,
    StocktakeLineUpdateRequest,
    StocktakeCompleteRequest,
)
from app.service import stocktake_service

router = APIRouter(prefix="/stocktakes", tags=["盘点"])


@router.get("", response_model=R[PageResult[StocktakeResponse]], summary="盘点任务列表")
def list_stocktakes(
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total, items = stocktake_service.get_stocktake_list(db, page, page_size, status)
    return R.ok(
        data=PageResult(
            total=total,
            page=page,
            page_size=page_size,
            items=[StocktakeResponse.model_validate(s) for s in items],
        )
    )


@router.get("/{stocktake_id}", response_model=R[StocktakeResponse], summary="盘点任务详情")
def get_stocktake(
    stocktake_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    stocktake = stocktake_service.get_stocktake_by_id(db, stocktake_id)
    if not stocktake:
        return R.fail("盘点任务不存在")
    return R.ok(data=StocktakeResponse.model_validate(stocktake))


@router.get("/{stocktake_id}/lines", response_model=R[list[StocktakeLineResponse]], summary="盘点明细列表")
def list_lines(
    stocktake_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    lines = stocktake_service.get_stocktake_lines(db, stocktake_id)
    return R.ok(data=[StocktakeLineResponse.model_validate(l) for l in lines])


@router.post("", response_model=R[StocktakeResponse], summary="创建盘点任务")
def create_stocktake(
    body: StocktakeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stocktake = stocktake_service.create_stocktake(db, body, current_user.id)
    return R.ok(data=StocktakeResponse.model_validate(stocktake))


@router.post("/{stocktake_id}/scan", response_model=R[StocktakeResponse], summary="扫码盘点")
def scan_items(
    stocktake_id: int,
    body: StocktakeScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        stocktake = stocktake_service.scan_items(db, stocktake_id, body.items, current_user.id)
        return R.ok(data=StocktakeResponse.model_validate(stocktake))
    except ValueError as e:
        return R.fail(str(e))


@router.put("/lines/{line_id}", response_model=R[StocktakeLineResponse], summary="更新盘点明细差异原因")
def update_line(
    line_id: int,
    body: StocktakeLineUpdateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        line = stocktake_service.update_line_reason(db, line_id, body.diff_reason)
        return R.ok(data=StocktakeLineResponse.model_validate(line))
    except ValueError as e:
        return R.fail(str(e))


@router.post("/{stocktake_id}/complete", response_model=R[StocktakeResponse], summary="完成盘点")
def complete_stocktake(
    stocktake_id: int,
    body: StocktakeCompleteRequest = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        stocktake = stocktake_service.complete_stocktake(db, stocktake_id, body.remark if body else None)
        return R.ok(data=StocktakeResponse.model_validate(stocktake))
    except ValueError as e:
        return R.fail(str(e))


@router.post("/{stocktake_id}/cancel", response_model=R[StocktakeResponse], summary="取消盘点")
def cancel_stocktake(
    stocktake_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        stocktake = stocktake_service.cancel_stocktake(db, stocktake_id)
        return R.ok(data=StocktakeResponse.model_validate(stocktake))
    except ValueError as e:
        return R.fail(str(e))