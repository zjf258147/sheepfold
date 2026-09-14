from datetime import date, datetime

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.rma import RmaDiagnosis, RmaQualityCheck, RmaRepair, RmaReship, RmaReturn, RmaScrap, RmaWarehouseIn
from app.models.inventory import InventoryItem
from app.models.enums import StockStatus, StockCondition, OperationStatus
from app.service.inventory_service import record_history
from app.models.user import User
from app.schemas.rma import (
    RmaAssignCreate,
    RmaDiagnosisCreate,
    RmaQualityCheckCreate,
    RmaRepairCreate,
    RmaReshipCreate,
    RmaReturnCreate,
    RmaScrapApprove,
    RmaScrapCreate,
    RmaTransferRequest,
    RmaWarehouseInCreate,
)
from app.utils.order_no import (
    generate_diag_no,
    generate_fc_no,
    generate_repair_no,
    generate_reship_no,
    generate_scrap_no,
)
from app.utils.audit import write_audit_log
from app.utils.excel_export import build_simple_xlsx
from app.utils.excel_import import build_template_xlsx, parse_import_xlsx


def _return_to_dict(r: RmaReturn) -> dict:
    return {
        "id": r.id,
        "return_no": r.return_no,
        "sku_id": r.sku_id,
        "sku_name": r.sku.name if r.sku else None,
        "sku_code": r.sku.sku_code if r.sku else None,
        "sn": r.sn,
        "quantity": r.quantity,
        "unit": r.unit,
        "customer_name": r.customer_name,
        "return_reason": r.return_reason,
        "return_date": r.return_date,
        "status": r.status,
        "assigned_to": r.assigned_to,
        "assignee_name": r.assignee.nickname or r.assignee.username if r.assignee else None,
        "change_reason": r.change_reason,
        "remark": r.remark,
        "created_at": r.created_at,
        "updated_at": r.updated_at,
    }


def get_returns(
    db: Session,
    page: int = 1,
    page_size: int = 15,
    keyword: str | None = None,
    status: str | None = None,
    sku_id: int | None = None,
    assigned_to: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
):
    from app.models.product import ProductSku

    query = db.query(RmaReturn).join(RmaReturn.sku)
    if keyword:
        query = query.filter(
            RmaReturn.return_no.like(f"%{keyword}%")
            | RmaReturn.sn.like(f"%{keyword}%")
            | ProductSku.name.like(f"%{keyword}%")
            | ProductSku.sku_code.like(f"%{keyword}%")
        )
    if status:
        query = query.filter(RmaReturn.status == status)
    if sku_id:
        query = query.filter(RmaReturn.sku_id == sku_id)
    if assigned_to:
        query = query.filter(RmaReturn.assigned_to == assigned_to)
    if start_date:
        query = query.filter(RmaReturn.return_date >= start_date)
    if end_date:
        query = query.filter(RmaReturn.return_date <= end_date)

    total = query.count()
    items = query.order_by(RmaReturn.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return [_return_to_dict(item) for item in items], total


def create_return(
    db: Session,
    data: RmaReturnCreate,
    user: User,
    ip_address: str | None = None,
) -> RmaReturn:
    return_no = generate_fc_no(db)
    receipt = RmaReturn(
        return_no=return_no,
        sku_id=data.sku_id,
        sn=data.sn,
        quantity=data.quantity,
        unit=data.unit,
        customer_name=data.customer_name,
        return_reason=data.return_reason,
        return_date=data.return_date,
        remark=data.remark,
    )
    db.add(receipt)
    db.flush()
    write_audit_log(
        db, user, action="CREATE", module="rma",
        resource_type="rma_return", resource_id=return_no,
        resource_name=f"返厂单 {return_no}", summary=f"创建返厂退货单，SN={data.sn}，原因={data.return_reason}",
        ip_address=ip_address,
    )
    db.commit()
    db.refresh(receipt)
    return receipt


def assign_return(
    db: Session,
    return_id: int,
    data: RmaAssignCreate,
    user: User,
    ip_address: str | None = None,
) -> RmaReturn:
    r = db.query(RmaReturn).filter(RmaReturn.id == return_id).first()
    if not r:
        raise ValueError(f"返厂单不存在：{return_id}")
    if r.status not in ("DIAGNOSED", "REPAIRED"):
        raise ValueError("只能对已诊断或已修复的返厂单进行分配")
    r.assigned_to = data.assigned_to
    r.status = "ASSIGNED"
    r.change_reason = data.change_reason
    db.flush()
    write_audit_log(
        db, user, action="ASSIGN", module="rma",
        resource_type="rma_return", resource_id=r.return_no,
        resource_name=f"返厂单 {r.return_no}",
        summary=f"分配返厂单给用户 {data.assigned_to}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(r)
    return r


def transfer_return(
    db: Session,
    return_id: int,
    data: RmaTransferRequest,
    user: User,
    ip_address: str | None = None,
) -> RmaReturn:
    r = db.query(RmaReturn).filter(RmaReturn.id == return_id).first()
    if not r:
        raise ValueError(f"返厂单不存在：{return_id}")
    r.assigned_to = data.target_assignee
    r.change_reason = data.change_reason
    db.flush()
    write_audit_log(
        db, user, action="TRANSFER", module="rma",
        resource_type="rma_return", resource_id=r.return_no,
        resource_name=f"返厂单 {r.return_no}",
        summary=f"流转返厂单给用户 {data.target_assignee}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(r)
    return r


def create_diagnosis(
    db: Session,
    data: RmaDiagnosisCreate,
    user: User,
    ip_address: str | None = None,
) -> RmaDiagnosis:
    r = db.query(RmaReturn).filter(RmaReturn.id == data.return_id).first()
    if not r:
        raise ValueError(f"返厂单不存在：{data.return_id}")
    if r.status != "PENDING_DIAGNOSIS":
        raise ValueError("只有待诊断的返厂单才能创建诊断报告")

    diagnosis_no = generate_diag_no(db)
    diagnosis = RmaDiagnosis(
        return_id=data.return_id,
        diagnosis_no=diagnosis_no,
        diagnosed_by=data.diagnosed_by,
        diagnosis_date=data.diagnosis_date,
        fault_description=data.fault_description,
        diagnosis_result=data.diagnosis_result,
        change_reason=data.change_reason,
        remark=data.remark,
    )
    db.add(diagnosis)
    r.status = "DIAGNOSED"
    r.diagnosis_result = data.diagnosis_result
    r.change_reason = data.change_reason
    db.flush()
    write_audit_log(
        db, user, action="CREATE", module="rma",
        resource_type="rma_diagnosis", resource_id=diagnosis_no,
        resource_name=f"诊断报告 {diagnosis_no}",
        summary=f"诊断返厂单 {r.return_no}，结果={data.diagnosis_result}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(diagnosis)
    return diagnosis


def get_diagnoses(db: Session, return_id: int):
    return db.query(RmaDiagnosis).filter(RmaDiagnosis.return_id == return_id).order_by(RmaDiagnosis.id.desc()).all()


def create_repair(
    db: Session,
    data: RmaRepairCreate,
    user: User,
    ip_address: str | None = None,
) -> RmaRepair:
    r = db.query(RmaReturn).filter(RmaReturn.id == data.return_id).first()
    if not r:
        raise ValueError(f"返厂单不存在：{data.return_id}")
    if r.status not in ("ASSIGNED", "REPAIRING"):
        raise ValueError("只有已分配或维修中的返厂单才能创建维修工单")

    if data.new_sn:
        existing = db.query(RmaReturn).filter(
            RmaReturn.id != data.return_id, RmaReturn.sn == data.new_sn
        ).first()
        if existing:
            raise ValueError(f"新 SN {data.new_sn} 已存在，不能重复使用")

    repair_no = generate_repair_no(db)
    repair = RmaRepair(
        return_id=data.return_id,
        repair_no=repair_no,
        repair_by=data.repair_by,
        old_sn=data.old_sn,
        new_sn=data.new_sn,
        repair_description=data.repair_description,
        materials_used=data.materials_used,
        fault_code=data.fault_code,
        repair_date=data.repair_date,
        change_reason=data.change_reason,
        remark=data.remark,
    )
    db.add(repair)

    if data.new_sn:
        r.sn = data.new_sn
        r.new_sn = data.new_sn
    r.status = "REPAIRED"
    r.change_reason = data.change_reason
    db.flush()
    write_audit_log(
        db, user, action="CREATE", module="rma",
        resource_type="rma_repair", resource_id=repair_no,
        resource_name=f"维修工单 {repair_no}",
        summary=f"维修返厂单 {r.return_no}，旧SN={data.old_sn}，新SN={data.new_sn or '无'}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(repair)
    return repair


def get_repairs(db: Session, return_id: int):
    return db.query(RmaRepair).filter(RmaRepair.return_id == return_id).order_by(RmaRepair.id.desc()).all()


def create_scrap(
    db: Session,
    data: RmaScrapCreate,
    user: User,
    ip_address: str | None = None,
) -> RmaScrap:
    r = db.query(RmaReturn).filter(RmaReturn.id == data.return_id).first()
    if not r:
        raise ValueError(f"返厂单不存在：{data.return_id}")
    if r.status == "SCRAPPED":
        raise ValueError("该返厂单已报废")

    scrap_no = generate_scrap_no(db)
    scrap = RmaScrap(
        return_id=data.return_id,
        scrap_no=scrap_no,
        requested_by=user.id,
        scrap_reason=data.scrap_reason,
        change_reason=data.change_reason,
        remark=data.remark,
    )
    db.add(scrap)
    db.flush()
    write_audit_log(
        db, user, action="CREATE", module="rma",
        resource_type="rma_scrap", resource_id=scrap_no,
        resource_name=f"报废单 {scrap_no}",
        summary=f"发起报废申请，返厂单={r.return_no}，原因={data.scrap_reason}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(scrap)
    return scrap


def approve_scrap(
    db: Session,
    scrap_id: int,
    data: RmaScrapApprove,
    user: User,
    ip_address: str | None = None,
) -> RmaScrap:
    scrap = db.query(RmaScrap).filter(RmaScrap.id == scrap_id).first()
    if not scrap:
        raise ValueError(f"报废单不存在：{scrap_id}")
    if scrap.status != "PENDING":
        raise ValueError("只能审批待审批的报废单")

    r = db.query(RmaReturn).filter(RmaReturn.id == scrap.return_id).first()
    if not data.reject_reason:
        scrap.status = "APPROVED"
        scrap.approved_by = user.id
        scrap.approved_at = datetime.now()
        r.status = "SCRAPPED"
        r.change_reason = data.change_reason
        summary = f"报废审批通过，返厂单={r.return_no}"
    else:
        scrap.status = "REJECTED"
        scrap.approved_by = user.id
        scrap.approved_at = datetime.now()
        scrap.reject_reason = data.reject_reason
        r.status = "REPAIRED"
        r.change_reason = data.change_reason
        summary = f"报废审批驳回，返厂单={r.return_no}，原因={data.reject_reason}"

    scrap.change_reason = data.change_reason
    db.flush()
    write_audit_log(
        db, user, action="APPROVE", module="rma",
        resource_type="rma_scrap", resource_id=scrap.scrap_no,
        resource_name=f"报废单 {scrap.scrap_no}",
        summary=summary, change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(scrap)
    return scrap


def get_scraps(db: Session, return_id: int):
    return db.query(RmaScrap).filter(RmaScrap.return_id == return_id).order_by(RmaScrap.id.desc()).all()


def create_reship(
    db: Session,
    data: RmaReshipCreate,
    user: User,
    ip_address: str | None = None,
) -> RmaReship:
    r = db.query(RmaReturn).filter(RmaReturn.id == data.return_id).first()
    if not r:
        raise ValueError(f"返厂单不存在：{data.return_id}")
    if r.status not in ("REPAIRED", "QUALITY_CHECK", "WAREHOUSED"):
        raise ValueError("只有已修复、已质检或已入库的返厂单才能再出货")

    reship_no = generate_reship_no(db)
    reship = RmaReship(
        return_id=data.return_id,
        reship_no=reship_no,
        new_sn=data.new_sn,
        software_version=data.software_version,
        ship_date=data.ship_date,
        recipient=data.recipient,
        operator_id=user.id,
        change_reason=data.change_reason,
        remark=data.remark,
    )
    db.add(reship)
    r.status = "RESHIPPED"
    r.change_reason = data.change_reason
    db.flush()
    write_audit_log(
        db, user, action="CREATE", module="rma",
        resource_type="rma_reship", resource_id=reship_no,
        resource_name=f"再出货单 {reship_no}",
        summary=f"再出货返厂单 {r.return_no}，SN={data.new_sn}，版本={data.software_version or '无'}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(reship)
    return reship


def get_reships(db: Session, return_id: int):
    return db.query(RmaReship).filter(RmaReship.return_id == return_id).order_by(RmaReship.id.desc()).all()


def get_quality_checks(db: Session, return_id: int):
    return db.query(RmaQualityCheck).filter(RmaQualityCheck.return_id == return_id).order_by(RmaQualityCheck.id.desc()).all()


def create_quality_check(
    db: Session,
    data: RmaQualityCheckCreate,
    user: User,
    ip_address: str | None = None,
) -> RmaQualityCheck:
    r = db.query(RmaReturn).filter(RmaReturn.id == data.return_id).first()
    if not r:
        raise ValueError("退货单不存在")
    qc = RmaQualityCheck(
        return_id=data.return_id,
        checked_by=data.checked_by,
        check_date=data.check_date,
        check_result=data.check_result,
        check_description=data.check_description,
        change_reason=data.change_reason,
        remark=data.remark,
    )
    db.add(qc)
    r.status = "QUALITY_CHECK"
    r.change_reason = data.change_reason
    db.flush()
    write_audit_log(
        db, user, action="CREATE", module="rma",
        resource_type="rma_quality_check", resource_id=str(qc.id),
        resource_name=f"质量检验 {qc.id}",
        summary=f"创建质量检验，返厂单={r.return_no}，结果={data.check_result}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(qc)
    return qc


def get_warehouse_ins(db: Session, return_id: int):
    return db.query(RmaWarehouseIn).filter(RmaWarehouseIn.return_id == return_id).order_by(RmaWarehouseIn.id.desc()).all()


def create_warehouse_in(
    db: Session,
    data: RmaWarehouseInCreate,
    user: User,
    ip_address: str | None = None,
) -> RmaWarehouseIn:
    r = db.query(RmaReturn).filter(RmaReturn.id == data.return_id).first()
    if not r:
        raise ValueError("退货单不存在")
    wi = RmaWarehouseIn(
        return_id=data.return_id,
        new_sn=data.new_sn,
        warehouse_by=user.id,
        warehouse_date=date.today(),
        repair_count=data.repair_count,
        repair_reason=data.repair_reason,
        warehouse_type=data.warehouse_type,
        change_reason=data.change_reason,
        remark=data.remark,
    )
    db.add(wi)
    r.status = "WAREHOUSED"
    r.change_reason = data.change_reason
    db.flush()

    # 获取最近一次维修记录中的旧SN
    old_sn = None
    latest_repair = db.query(RmaRepair).filter(
        RmaRepair.return_id == data.return_id
    ).order_by(RmaRepair.id.desc()).first()
    if latest_repair:
        old_sn = latest_repair.old_sn

    # 创建新 SN 的库存记录
    inv = InventoryItem(
        item_sn=data.new_sn,
        sku_id=r.sku_id,
        stock_status=StockStatus.IN_STOCK.value,
        stock_condition=StockCondition.RETURNED_FROM_REPAIR.value,
        operation_status=OperationStatus.COMPLETED.value,
        warehouse_type=data.warehouse_type,
        replaced_from_sn=old_sn,
        current_location="库房",
    )
    db.add(inv)
    db.flush()
    record_history(db, inv, "INBOUND", r.return_no, user.id,
                   to_stock=StockStatus.IN_STOCK.value, to_op=OperationStatus.COMPLETED.value)

    # 将旧 SN 的库存记录标记为已替换
    if old_sn:
        old_inv = db.query(InventoryItem).filter(InventoryItem.item_sn == old_sn).first()
        if old_inv:
            old_inv.stock_status = StockStatus.REPLACED.value
            old_inv.replaced_by_sn = data.new_sn
            record_history(db, old_inv, "STATUS_CHANGE", r.return_no, user.id,
                           from_stock=old_inv.stock_status, to_stock=StockStatus.REPLACED.value,
                           remark=f"维修换码，替换为 {data.new_sn}")

    write_audit_log(
        db, user, action="CREATE", module="rma",
        resource_type="rma_warehouse_in", resource_id=str(wi.id),
        resource_name=f"入库审核 {wi.id}",
        summary=f"创建入库审核，返厂单={r.return_no}，SN={data.new_sn}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(wi)
    return wi


def export_rma_xlsx(
    db: Session,
    status: str | None = None,
    keyword: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> bytes:
    from app.models.rma import RmaReturn
    from sqlalchemy import or_
    query = db.query(RmaReturn)
    if status:
        query = query.filter(RmaReturn.status == status)
    if keyword:
        query = query.filter(
            or_(RmaReturn.return_no.contains(keyword), RmaReturn.sn.contains(keyword))
        )
    if start_date:
        query = query.filter(RmaReturn.return_date >= start_date)
    if end_date:
        query = query.filter(RmaReturn.return_date <= end_date)
    returns = query.order_by(RmaReturn.id.desc()).all()
    headers = ["退货单号", "SN", "产品SKU", "客户", "退货原因", "退货日期", "状态", "创建时间"]
    rows = []
    for r in returns:
        rows.append([
            r.return_no, r.sn, str(r.sku_id), r.customer_name or "",
            r.return_reason or "", str(r.return_date), r.status or "",
            str(r.created_at)[:19] if r.created_at else "",
        ])
    return build_simple_xlsx(headers, rows, sheet_title="返修记录")


def export_rma_template() -> bytes:
    headers = ["SN", "产品SKU_ID", "客户名称", "退货原因", "退货日期", "备注"]
    return build_template_xlsx(headers, sheet_title="返修退货导入模板")


def import_rma_xlsx(db: Session, content: bytes, username: str) -> dict:
    rows = parse_import_xlsx(content)
    success = 0
    errors = []
    for i, row in enumerate(rows, start=1):
        try:
            sn = str(row[0]).strip() if row[0] else ""
            sku_id = int(row[1]) if row[1] else None
            customer_name = str(row[2]).strip() if len(row) > 2 and row[2] else ""
            return_reason = str(row[3]).strip() if len(row) > 3 and row[3] else ""
            return_date_str = str(row[4]).strip() if len(row) > 4 and row[4] else ""
            remark = str(row[5]).strip() if len(row) > 5 and row[5] else ""
            if not sn:
                errors.append(f"第{i}行: SN不能为空")
                continue
            return_no = generate_fc_no(db)
            return_date = date.today()
            if return_date_str:
                return_date = date.fromisoformat(return_date_str)
            ret = RmaReturn(
                return_no=return_no,
                sku_id=sku_id or 0,
                sn=sn,
                customer_name=customer_name,
                return_reason=return_reason,
                return_date=return_date,
                status="RECEIVED",
                remark=remark,
            )
            db.add(ret)
            success += 1
        except Exception as e:
            errors.append(f"第{i}行: {str(e)}")
    if success > 0:
        db.commit()
    return {"success": success, "errors": errors}