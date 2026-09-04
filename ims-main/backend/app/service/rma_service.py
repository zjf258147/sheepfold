from datetime import datetime

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.rma import RmaDiagnosis, RmaRepair, RmaReship, RmaReturn, RmaScrap
from app.models.user import User
from app.schemas.rma import (
    RmaAssignCreate,
    RmaDiagnosisCreate,
    RmaRepairCreate,
    RmaReshipCreate,
    RmaReturnCreate,
    RmaScrapApprove,
    RmaScrapCreate,
    RmaTransferRequest,
)
from app.utils.order_no import (
    generate_diag_no,
    generate_fc_no,
    generate_repair_no,
    generate_reship_no,
    generate_scrap_no,
)


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
    from app.models.product_sku import ProductSku

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
    return items, total


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
    _write_audit(
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
    _write_audit(
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
    _write_audit(
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
    r.change_reason = data.change_reason
    db.flush()
    _write_audit(
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
    r.status = "REPAIRED"
    r.change_reason = data.change_reason
    db.flush()
    _write_audit(
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
    _write_audit(
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
    _write_audit(
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
    if r.status != "REPAIRED":
        raise ValueError("只有已修复的返厂单才能再出货")

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
    _write_audit(
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