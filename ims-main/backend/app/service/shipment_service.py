from datetime import datetime

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.shipment import Shipment
from app.models.user import User
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.utils.order_no import generate_shipment_no


def _write_audit(
    db: Session,
    user: User,
    action: str,
    module: str,
    resource_type: str,
    resource_id: str,
    resource_name: str,
    summary: str,
    change_reason: str | None = None,
    ip_address: str | None = None,
):
    db.add(AuditLog(
        operator_id=user.id,
        operator_name=f"{user.nickname or user.username}（{user.username}）",
        action=action,
        module=module,
        resource_type=resource_type,
        resource_id=resource_id,
        resource_name=resource_name,
        summary=summary,
        change_reason=change_reason,
        ip_address=ip_address,
        created_at=datetime.now(),
    ))


def get_shipments(
    db: Session,
    page: int = 1,
    page_size: int = 15,
    keyword: str | None = None,
    sku_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
):
    query = db.query(Shipment)

    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(
            Shipment.shipment_no.like(kw)
            | Shipment.sku_name.like(kw)
            | Shipment.sku_code.like(kw)
            | Shipment.tracking_no.like(kw)
            | Shipment.u9_task_no.like(kw)
        )
    if sku_id:
        query = query.filter(Shipment.sku_id == sku_id)
    if start_date:
        query = query.filter(Shipment.ship_date >= start_date)
    if end_date:
        query = query.filter(Shipment.ship_date <= end_date)

    total = query.count()
    items = query.order_by(Shipment.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def create_shipment(
    db: Session,
    data: ShipmentCreate,
    username: str,
    ip_address: str | None = None,
) -> Shipment:
    shipment_no = generate_shipment_no(db)

    from app.models.inventory import InventoryItem
    from app.models.outbound import OutboundOrder, OutboundOrderItem
    from app.utils.sn_generator import sn_timestamp

    sn_list = data.sn_list if isinstance(data.sn_list, list) else []

    inventory_items = []
    not_found_sns = []
    for sn in sn_list:
        inv = db.query(InventoryItem).filter(
            InventoryItem.item_sn == sn,
            InventoryItem.stock_status == "IN_STOCK",
        ).first()
        if inv:
            inventory_items.append(inv)
        else:
            not_found_sns.append(sn)

    shipment = Shipment(
        shipment_no=shipment_no,
        sku_id=data.sku_id,
        sku_code=data.sku_code,
        sku_name=data.sku_name,
        spec=data.spec,
        unit=data.unit or "个",
        sn_list=sn_list,
        quantity=data.quantity,
        ship_date=data.ship_date,
        address=data.address,
        logistics_provider=data.logistics_provider,
        tracking_no=data.tracking_no,
        u9_task_no=data.u9_task_no,
        tf_version=data.tf_version,
        host_version=data.host_version,
        remark=data.remark,
        created_by=username,
        change_reason=data.change_reason,
    )
    db.add(shipment)
    db.flush()

    if inventory_items:
        from app.utils.order_no import generate_outbound_no
        outbound_no = generate_outbound_no(db)
        outbound = OutboundOrder(
            order_no=outbound_no,
            outbound_type="SOLD",
            partner_id=1,
            customer_name=data.address,
            remark=f"出货单 {shipment_no} 自动创建",
            operation_status="INITIATED",
            submitted_by=1,
        )
        db.add(outbound)
        db.flush()

        for inv in inventory_items:
            db.add(OutboundOrderItem(
                outbound_order_id=outbound.id,
                item_id=inv.id,
                sku_id=inv.sku_id,
            ))
            inv.operation_status = "PICKING"
            inv.last_order_no = outbound_no

        outbound.operation_status = "COMPLETED"
        for inv in inventory_items:
            inv.stock_status = "SOLD"
            inv.operation_status = "COMPLETED"

    user = db.query(User).filter(User.username == username).first()
    summary_parts = [f"出货登记，物料={data.sku_name}，数量={data.quantity}，SN数={len(sn_list)}"]
    if not_found_sns:
        summary_parts.append(f"未找到库存SN: {not_found_sns}")
    if inventory_items:
        summary_parts.append(f"已自动扣减库存 {len(inventory_items)} 件")

    _write_audit(
        db, user, action="CREATE", module="shipment",
        resource_type="shipment", resource_id=shipment_no,
        resource_name=f"出货单 {shipment_no}",
        summary="，".join(summary_parts),
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(shipment)
    return shipment


def update_shipment(
    db: Session,
    shipment_id: int,
    data: ShipmentUpdate,
    username: str,
    ip_address: str | None = None,
) -> Shipment:
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise ValueError(f"出货单不存在：{shipment_id}")

    update_fields = data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(shipment, field, value)

    db.flush()
    user = db.query(User).filter(User.username == username).first()
    _write_audit(
        db, user, action="UPDATE", module="shipment",
        resource_type="shipment", resource_id=shipment.shipment_no,
        resource_name=f"出货单 {shipment.shipment_no}",
        summary=f"更新出货单，修改字段={list(update_fields.keys())}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(shipment)
    return shipment


def delete_shipment(
    db: Session,
    shipment_id: int,
    username: str,
    ip_address: str | None = None,
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise ValueError(f"出货单不存在：{shipment_id}")

    shipment_no = shipment.shipment_no
    db.delete(shipment)
    user = db.query(User).filter(User.username == username).first()
    _write_audit(
        db, user, action="DELETE", module="shipment",
        resource_type="shipment", resource_id=shipment_no,
        resource_name=f"出货单 {shipment_no}",
        summary=f"删除出货单 {shipment_no}",
        change_reason=None, ip_address=ip_address,
    )
    db.commit()