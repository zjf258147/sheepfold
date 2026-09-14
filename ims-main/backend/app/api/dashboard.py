from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.common import R
from app.schemas.dashboard import (
    DashboardPartnerSummary,
    DashboardStockSummary,
    PartnerStockSummaryItem,
    PendingAuditResponse,
    Phase2StatsResponse,
    PollStatusResponse,
)
from app.schemas.inventory import StockSummaryItem
from app.service import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["首页"])


@router.get("/pending-audit", response_model=R[PendingAuditResponse], summary="待审核统计")
def pending_audit(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    data = dashboard_service.get_pending_audit(db)
    return R.ok(data=PendingAuditResponse(**data))


@router.get("/stock-summary", response_model=R[DashboardStockSummary], summary="按SKU库存统计")
def stock_summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    items = dashboard_service.get_stock_summary(db)
    return R.ok(data=DashboardStockSummary(items=[StockSummaryItem(**i) for i in items]))


@router.get("/partner-summary", response_model=R[DashboardPartnerSummary], summary="按关联单位统计不在库单品")
def partner_summary(
    sku_ids: list[int] | None = Query(None, description="商品 SKU ID 列表"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    items = dashboard_service.get_partner_summary(db, sku_ids=sku_ids)
    return R.ok(data=DashboardPartnerSummary(items=[PartnerStockSummaryItem(**i) for i in items]))


@router.get("/phase2-stats", response_model=R[Phase2StatsResponse], summary="二期看板统计")
def phase2_stats(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    data = dashboard_service.get_phase2_stats(db)
    return R.ok(data=Phase2StatsResponse(**data))


@router.get("/poll-status", response_model=R[PollStatusResponse], summary="轮询轻量状态")
def poll_status(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    data = dashboard_service.get_poll_status(db)
    return R.ok(data=PollStatusResponse(**data))