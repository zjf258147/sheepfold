from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from urllib.parse import quote

from app.core.deps import get_current_user
from app.core.permissions import require_permission
from app.db.database import get_db
from app.models.user import User
from app.schemas.audit import AuditLogCreate
from app.schemas.common import R, PageResult
from app.schemas.outbound import *
from app.service import audit_service, outbound_service
from app.utils.order_no import generate_outbound_no
from app.utils.request_ip import get_client_ip

router = APIRouter(prefix="/outbound/orders", tags=["出库"])


def _order_audit_data(db: Session, order) -> dict:
    """将出库单转为审计快照。"""
    return audit_service.to_audit_data(outbound_service.order_to_response(db, order))


@router.get("/generate-no", response_model=R[str], summary="生成出库单号")
def gen_no(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return R.ok(data=generate_outbound_no(db))


@router.get("", response_model=R[PageResult[OutboundOrderResponse]], summary="出库单列表")
def list_orders(
    page: int = 1,
    page_size: int = 20,
    operation_status: str | None = None,
    outbound_type: str | None = None,
    order_no: str | None = None,
    partner_id: int | None = None,
    sku_id: int | None = Query(None, description="商品 SKU ID"),
    item_sn: str | None = Query(None, description="商品 SN 模糊搜索"),
    start_time: datetime | None = Query(None, description="创建时间起"),
    end_time: datetime | None = Query(None, description="创建时间止"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total, items = outbound_service.get_orders(
        db, page, page_size, operation_status, outbound_type, order_no, partner_id,
        sku_id, item_sn, start_time, end_time,
    )
    return R.ok(data=PageResult(total=total, page=page, page_size=page_size,
                                items=[OutboundOrderResponse.model_validate(o) for o in items]))


@router.post("", response_model=R[OutboundOrderResponse], status_code=201, summary="新建出库单")
def create_order(
    data: OutboundOrderCreate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("outbound.create")),
):
    try:
        order = outbound_service.create_order(db, data, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    order = outbound_service.get_order_detail(db, order.id)
    audit_service.record(
        db,
        user,
        AuditLogCreate(
            action="CREATE",
            module="outbound",
            resource_type="outbound_order",
            resource_id=str(order.id),
            resource_name=order.order_no,
            summary=audit_service.build_summary(user, "CREATE", f"出库单「{order.order_no}」"),
            after_data=_order_audit_data(db, order),
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(data=outbound_service.order_to_response(db, order))


@router.get('/export', summary='导出出库单 Excel')
def export_outbound(
    operation_status: str | None = None,
    outbound_type: str | None = None,
    order_no: str | None = None,
    partner_id: int | None = None,
    stock_condition: str | None = None,
    sku_id: int | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    content = outbound_service.export_outbound_xlsx(
        db, operation_status=operation_status, outbound_type=outbound_type,
        order_no=order_no, partner_id=partner_id,
        stock_condition=stock_condition, sku_id=sku_id,
        start_time=start_time, end_time=end_time,
    )
    filename = quote('出库单列表.xlsx')
    return StreamingResponse(
        iter([content]),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f"attachment; filename*=UTF-8''{filename}"},
    )


@router.get('/template', summary='下载出库导入模板')
def download_outbound_template(_: User = Depends(get_current_user)):
    content = outbound_service.export_outbound_template()
    filename = quote('出库导入模板.xlsx')
    return StreamingResponse(
        iter([content]),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f"attachment; filename*=UTF-8''{filename}"},
    )


@router.post('/import', summary='导入出库单 Excel')
async def import_outbound(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("outbound.create")),
):
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail='请上传 .xlsx 或 .xls 文件')
    content = await file.read()
    result = outbound_service.import_outbound_xlsx(db, content, current_user.id)
    return R.ok(data=result, msg=f"成功 {result['success']} 条，失败 {len(result['errors'])} 条")


@router.get("/{order_id}", response_model=R[OutboundOrderResponse], summary="出库单详情")
def get_order(
    order_id: str,
    lookup_by: str = "id",
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if lookup_by == "order_no":
        key = order_id
    elif lookup_by == "id":
        if not order_id.isdigit():
            raise HTTPException(status_code=400, detail="lookup_by=id 时 order_id 必须为整数")
        key = int(order_id)
    else:
        raise HTTPException(status_code=400, detail="lookup_by 仅支持 'id' 或 'order_no'")
    order = outbound_service.get_order_detail(db, key)
    if not order:
        raise HTTPException(status_code=404, detail="出库单不存在")
    return R.ok(data=outbound_service.order_to_response(db, order))


@router.put("/{order_id}", response_model=R[OutboundOrderResponse], summary="修改出库单")
def update_order(
    order_id: int,
    data: OutboundOrderUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("outbound.edit")),
):
    order = outbound_service.get_order_detail(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="出库单不存在")
    before = _order_audit_data(db, order)
    try:
        order = outbound_service.update_order(db, order, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    order = outbound_service.get_order_detail(db, order.id)
    audit_service.record(
        db,
        user,
        AuditLogCreate(
            action="UPDATE",
            module="outbound",
            resource_type="outbound_order",
            resource_id=str(order.id),
            resource_name=order.order_no,
            summary=audit_service.build_summary(user, "UPDATE", f"出库单「{order.order_no}」"),
            before_data=before,
            after_data=_order_audit_data(db, order),
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(data=outbound_service.order_to_response(db, order))


@router.post("/{order_id}/submit", response_model=R[OutboundOrderResponse], summary="提交待审核")
def submit_order(
    order_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("outbound.submit")),
):
    order = outbound_service.get_order_detail(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="出库单不存在")
    before_status = order.operation_status
    try:
        order = outbound_service.submit_order(db, order, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    audit_service.record(
        db,
        user,
        AuditLogCreate(
            action="SUBMIT",
            module="outbound",
            resource_type="outbound_order",
            resource_id=str(order.id),
            resource_name=order.order_no,
            summary=audit_service.build_summary(
                user, "SUBMIT", f"出库单「{order.order_no}」", f"状态 {before_status} → {order.operation_status}"
            ),
            before_data={"operation_status": before_status},
            after_data={"operation_status": order.operation_status},
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(data=outbound_service.order_to_response(db, order), msg="提交成功")


@router.post("/{order_id}/approve", response_model=R[OutboundOrderResponse], summary="审核通过")
def approve_order(
    order_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("outbound.approve")),
):
    order = outbound_service.get_order_detail(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="出库单不存在")
    before = _order_audit_data(db, order)
    try:
        order = outbound_service.approve_order(db, order, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    order = outbound_service.get_order_detail(db, order.id)
    audit_service.record(
        db,
        user,
        AuditLogCreate(
            action="APPROVE",
            module="outbound",
            resource_type="outbound_order",
            resource_id=str(order.id),
            resource_name=order.order_no,
            summary=audit_service.build_summary(user, "APPROVE", f"出库单「{order.order_no}」"),
            before_data=before,
            after_data=_order_audit_data(db, order),
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(data=outbound_service.order_to_response(db, order), msg="审核通过")


@router.post("/{order_id}/cancel", response_model=R[OutboundOrderResponse], summary="取消")
def cancel_order(
    order_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("outbound.cancel")),
):
    order = outbound_service.get_order_detail(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="出库单不存在")
    before_status = order.operation_status
    try:
        order = outbound_service.cancel_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    audit_service.record(
        db,
        user,
        AuditLogCreate(
            action="CANCEL",
            module="outbound",
            resource_type="outbound_order",
            resource_id=str(order.id),
            resource_name=order.order_no,
            summary=audit_service.build_summary(
                user, "CANCEL", f"出库单「{order.order_no}」", f"状态 {before_status} → {order.operation_status}"
            ),
            before_data={"operation_status": before_status},
            after_data={"operation_status": order.operation_status},
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(data=outbound_service.order_to_response(db, order), msg="已取消")


@router.delete("/{order_id}", response_model=R, summary="删除出库单")
def delete_order(
    order_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("outbound.edit")),
):
    order = outbound_service.get_order_detail(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="出库单不存在")
    before = _order_audit_data(db, order)
    order_no = order.order_no
    try:
        outbound_service.delete_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    audit_service.record(
        db,
        user,
        AuditLogCreate(
            action="DELETE",
            module="outbound",
            resource_type="outbound_order",
            resource_id=str(order_id),
            resource_name=order_no,
            summary=audit_service.build_summary(user, "DELETE", f"出库单「{order_no}」"),
            before_data=before,
            ip_address=get_client_ip(request),
        ),
    )
    return R.ok(msg="删除成功")