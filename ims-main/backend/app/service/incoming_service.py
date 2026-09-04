from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.models.audit_log import AuditLog
from app.models.incoming import IncomingInspection, IncomingReceipt, IncomingReturn
from app.models.partner import Partner
from app.models.product import ProductSku
from app.models.user import User
from app.schemas.incoming import (
    IncomingInspectionCreate,
    IncomingReceiptCreate,
    IncomingReceiptUpdate,
    IncomingReturnCreate,
)
from app.utils.order_no import generate_inspection_no, generate_rc_no, generate_return_no


def _receipt_to_response(receipt: IncomingReceipt) -> dict:
    return {
        "id": receipt.id,
        "receipt_no": receipt.receipt_no,
        "supplier_id": receipt.supplier_id,
        "supplier_name": receipt.supplier.name if receipt.supplier else None,
        "sku_id": receipt.sku_id,
        "sku_name": receipt.sku.name if receipt.sku else None,
        "sku_code": receipt.sku.sku_code if receipt.sku else None,
        "spec": receipt.sku.spec if receipt.sku else None,
        "batch_no": receipt.batch_no,
        "quantity": receipt.quantity,
        "unit": receipt.unit,
        "status": receipt.status,
        "delivery_date": receipt.delivery_date,
        "inspector_id": receipt.inspector_id,
        "inspector_name": receipt.inspector.nickname or receipt.inspector.username if receipt.inspector else None,
        "inspection_date": receipt.inspection_date,
        "confirmed_at": receipt.confirmed_at,
        "confirmed_by": receipt.confirmed_by,
        "confirmer_name": receipt.confirmer.nickname or receipt.confirmer.username if receipt.confirmer else None,
        "change_reason": receipt.change_reason,
        "remark": receipt.remark,
        "created_at": receipt.created_at,
        "updated_at": receipt.updated_at,
    }


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
    before_data: dict | None = None,
    after_data: dict | None = None,
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
        before_data=str(before_data) if before_data else None,
        after_data=str(after_data) if after_data else None,
        ip_address=ip_address,
        created_at=datetime.now(),
    ))


def create_receipt(
    db: Session,
    data: IncomingReceiptCreate,
    user: User,
    ip_address: str | None = None,
) -> IncomingReceipt:
    receipt = IncomingReceipt(
        receipt_no=generate_rc_no(db),
        supplier_id=data.supplier_id,
        sku_id=data.sku_id,
        batch_no=data.batch_no,
        quantity=data.quantity,
        unit=data.unit,
        delivery_date=data.delivery_date,
        remark=data.remark,
    )
    db.add(receipt)
    db.flush()

    _write_audit(
        db, user,
        action="CREATE",
        module="incoming",
        resource_type="incoming_receipt",
        resource_id=receipt.receipt_no,
        resource_name=f"到货单 {receipt.receipt_no}",
        summary=f"{user.nickname or user.username} 创建到货单 {receipt.receipt_no}，物料={receipt.sku_id}，数量={receipt.quantity}",
        ip_address=ip_address,
    )

    db.commit()
    db.refresh(receipt)
    return receipt


def update_receipt(db: Session, receipt_id: int, data: IncomingReceiptUpdate) -> IncomingReceipt:
    receipt = db.query(IncomingReceipt).filter(IncomingReceipt.id == receipt_id).first()
    if not receipt:
        raise ValueError(f"到货单不存在：{receipt_id}")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(receipt, field, value)
    db.commit()
    db.refresh(receipt)
    return receipt


def get_receipts(
    db: Session,
    page: int = 1,
    page_size: int = 15,
    keyword: str | None = None,
    category_id: int | None = None,
    sku_id: int | None = None,
    supplier_id: int | None = None,
    status: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> tuple[int, list[dict]]:
    query = db.query(IncomingReceipt).options(
        joinedload(IncomingReceipt.supplier),
        joinedload(IncomingReceipt.sku),
        joinedload(IncomingReceipt.inspector),
        joinedload(IncomingReceipt.confirmer),
    )

    if keyword:
        query = query.join(IncomingReceipt.sku).filter(
            IncomingReceipt.receipt_no.like(f"%{keyword}%")
            | IncomingReceipt.batch_no.like(f"%{keyword}%")
            | ProductSku.name.like(f"%{keyword}%")
            | ProductSku.sku_code.like(f"%{keyword}%")
        )
    if sku_id:
        query = query.filter(IncomingReceipt.sku_id == sku_id)
    if supplier_id:
        query = query.filter(IncomingReceipt.supplier_id == supplier_id)
    if status:
        query = query.filter(IncomingReceipt.status == status)
    if category_id:
        query = query.join(IncomingReceipt.sku).filter(ProductSku.category_id == category_id)
    if start_date:
        query = query.filter(IncomingReceipt.delivery_date >= start_date)
    if end_date:
        query = query.filter(IncomingReceipt.delivery_date <= end_date)

    total = query.count()
    items = (
        query.order_by(IncomingReceipt.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return total, [_receipt_to_response(r) for r in items]


def get_receipt(db: Session, receipt_id: int) -> dict:
    receipt = (
        db.query(IncomingReceipt)
        .options(
            joinedload(IncomingReceipt.supplier),
            joinedload(IncomingReceipt.sku),
            joinedload(IncomingReceipt.inspector),
            joinedload(IncomingReceipt.confirmer),
        )
        .filter(IncomingReceipt.id == receipt_id)
        .first()
    )
    if not receipt:
        raise ValueError(f"到货单不存在：{receipt_id}")
    return _receipt_to_response(receipt)


def create_inspection(
    db: Session,
    data: IncomingInspectionCreate,
    user: User,
    ip_address: str | None = None,
) -> IncomingInspection:
    receipt = db.query(IncomingReceipt).filter(IncomingReceipt.id == data.receipt_id).first()
    if not receipt:
        raise ValueError(f"到货单不存在：{data.receipt_id}")

    inspection = IncomingInspection(
        receipt_id=data.receipt_id,
        inspection_no=generate_inspection_no(db),
        inspector_id=data.inspector_id,
        inspection_date=data.inspection_date,
        result=data.result,
        sample_qty=data.sample_qty,
        defect_qty=data.defect_qty,
        defect_description=data.defect_description,
        change_reason=data.change_reason,
        remark=data.remark,
    )
    receipt.status = "INSPECTED"
    receipt.inspector_id = data.inspector_id
    receipt.inspection_date = data.inspection_date
    receipt.change_reason = data.change_reason

    if data.result == "ACCEPTED" or data.result == "CONCESSION_ACCEPTED":
        receipt.status = "ACCEPTED"
    elif data.result == "REJECTED":
        receipt.status = "REJECTED"

    db.add(inspection)
    db.flush()

    _write_audit(
        db, user,
        action="CREATE",
        module="incoming",
        resource_type="incoming_inspection",
        resource_id=inspection.inspection_no,
        resource_name=f"检验报告 {inspection.inspection_no}",
        summary=f"{user.nickname or user.username} 对到货单 {receipt.receipt_no} 创建检验报告，结果={data.result}",
        change_reason=data.change_reason,
        ip_address=ip_address,
    )

    db.commit()
    db.refresh(inspection)
    return inspection


def create_return(
    db: Session,
    data: IncomingReturnCreate,
    user: User,
    ip_address: str | None = None,
) -> IncomingReturn:
    receipt = db.query(IncomingReceipt).filter(IncomingReceipt.id == data.receipt_id).first()
    if not receipt:
        raise ValueError(f"到货单不存在：{data.receipt_id}")

    rtn = IncomingReturn(
        receipt_id=data.receipt_id,
        return_no=generate_return_no(db),
        return_qty=data.return_qty,
        return_reason=data.return_reason,
        return_date=data.return_date,
        operator_id=data.operator_id,
        change_reason=data.change_reason,
        remark=data.remark,
    )
    receipt.status = "REJECTED"
    receipt.change_reason = data.change_reason

    db.add(rtn)
    db.flush()

    _write_audit(
        db, user,
        action="CREATE",
        module="incoming",
        resource_type="incoming_return",
        resource_id=rtn.return_no,
        resource_name=f"退货单 {rtn.return_no}",
        summary=f"{user.nickname or user.username} 对到货单 {receipt.receipt_no} 创建退货单，退货数量={rtn.return_qty}",
        change_reason=data.change_reason,
        ip_address=ip_address,
    )

    db.commit()
    db.refresh(rtn)
    return rtn


def confirm_receipt(
    db: Session,
    receipt_id: int,
    change_reason: str,
    user: User,
    ip_address: str | None = None,
) -> IncomingReceipt:
    receipt = db.query(IncomingReceipt).filter(IncomingReceipt.id == receipt_id).first()
    if not receipt:
        raise ValueError(f"到货单不存在：{receipt_id}")
    if receipt.status != "ACCEPTED":
        raise ValueError("只有检验合格（ACCEPTED）的到货单才能确认入库")
    if receipt.confirmed_at is not None:
        raise ValueError("该到货单已确认入库，不能重复操作")

    receipt.status = "WAREHOUSED"
    receipt.confirmed_at = datetime.now()
    receipt.confirmed_by = user.id
    receipt.change_reason = change_reason

    db.flush()

    _write_audit(
        db, user,
        action="APPROVE",
        module="incoming",
        resource_type="incoming_receipt",
        resource_id=receipt.receipt_no,
        resource_name=f"到货单 {receipt.receipt_no}",
        summary=f"{user.nickname or user.username} 确认到货单 {receipt.receipt_no} 入库",
        change_reason=change_reason,
        ip_address=ip_address,
    )

    db.commit()
    db.refresh(receipt)
    return receipt


def get_inspections(db: Session, receipt_id: int) -> list[IncomingInspection]:
    return (
        db.query(IncomingInspection)
        .options(joinedload(IncomingInspection.inspector))
        .filter(IncomingInspection.receipt_id == receipt_id)
        .order_by(IncomingInspection.id.desc())
        .all()
    )