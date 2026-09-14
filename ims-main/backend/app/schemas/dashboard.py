from pydantic import BaseModel
from app.schemas.inventory import StockSummaryItem


class PendingAuditResponse(BaseModel):
    inbound_pending: int
    outbound_pending: int


class PollStatusResponse(BaseModel):
    """轮询轻量状态，单次查询<50ms。"""
    inbound_pending: int = 0
    outbound_pending: int = 0
    device_fault: int = 0
    stocktake_in_progress: int = 0
    pending_adjustments: int = 0
    warranty_expiring_soon: int = 0


class DashboardStockSummary(BaseModel):
    items: list[StockSummaryItem]


class PartnerStockSummaryItem(BaseModel):
    partner_id: int | None = None
    partner_name: str
    partner_group_name: str | None = None
    sold: int = 0
    presold: int = 0
    sold_offline: int = 0
    borrowed: int = 0
    gifted: int = 0
    scrapped: int = 0
    rnd: int = 0
    sample: int = 0
    trial: int = 0
    repair: int = 0
    dept_procurement: int = 0


class DashboardPartnerSummary(BaseModel):
    items: list[PartnerStockSummaryItem]


class Phase2StatsResponse(BaseModel):
    """二期看板统计。"""
    station_total: int = 0
    station_active: int = 0
    device_total: int = 0
    device_running: int = 0
    device_fault: int = 0
    device_recycled: int = 0
    stocktake_in_progress: int = 0
    stocktake_completed: int = 0
    pending_adjustments: int = 0
    warranty_expiring_soon: int = 0