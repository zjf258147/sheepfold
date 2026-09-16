from datetime import datetime

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.bom import BomHeader, BomDetail, ProductionTask
from app.models.raw_material import RawMaterialInventory
from app.models.user import User
from app.schemas.bom import BomCreate, BomUpdate, MaterialCheckItem, ProductionTaskCreate, ProductionTaskUpdate
from app.utils.excel_export import build_simple_xlsx
from app.utils.excel_import import build_template_xlsx, parse_import_xlsx
from app.utils.order_no import generate_bom_no, generate_task_no


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


def get_boms(
    db: Session,
    page: int = 1,
    page_size: int = 15,
    keyword: str | None = None,
    status: str | None = None,
) -> tuple[list[BomHeader], int]:
    query = db.query(BomHeader)
    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(
            BomHeader.bom_no.like(kw)
            | BomHeader.bom_name.like(kw)
            | BomHeader.product_sku_name.like(kw)
        )
    if status:
        query = query.filter(BomHeader.status == status)
    total = query.count()
    items = query.order_by(BomHeader.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def get_bom_detail(db: Session, bom_id: int) -> dict:
    bom = db.query(BomHeader).filter(BomHeader.id == bom_id).first()
    if not bom:
        raise ValueError(f"BOM不存在：{bom_id}")
    details = db.query(BomDetail).filter(BomDetail.bom_id == bom_id).all()
    result = {k: v for k, v in bom.__dict__.items() if not k.startswith("_")}
    result["details"] = details
    return result


def create_bom(
db: Session,
data: BomCreate,
username: str,
ip_address: str | None = None,
) -> BomHeader:
    bom_no = generate_bom_no(db)
    bom = BomHeader(
        bom_no=bom_no,
        bom_name=data.bom_name,
        version=data.version,
        product_sku_id=data.product_sku_id,
        product_sku_code=data.product_sku_code,
        product_sku_name=data.product_sku_name,
        plan_quantity=data.plan_quantity,
        status=data.status,
        remark=data.remark,
        created_by=username,
    )
    db.add(bom)
    db.flush()

    for item in data.details:
        detail = BomDetail(
            bom_id=bom.id,
            material_sku_id=item.material_sku_id,
            material_sku_code=item.material_sku_code,
            material_sku_name=item.material_sku_name,
            spec=item.spec,
            unit=item.unit,
            quantity_per_unit=item.quantity_per_unit,
            wastage_rate=item.wastage_rate,
            level=item.level,
            parent_detail_id=item.parent_detail_id,
            item_version=item.item_version,
            process_note=item.process_note,
            remark=item.remark,
        )
        db.add(detail)

    user = db.query(User).filter(User.username == username).first()
    _write_audit(
        db, user, action="CREATE", module="bom",
        resource_type="bom_header", resource_id=bom_no,
        resource_name=f"BOM {bom_no}",
        summary=f"创建BOM {data.bom_name}，成品={data.product_sku_name}，明细数={len(data.details)}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(bom)
    return bom


def update_bom(
db: Session,
bom_id: int,
data: BomUpdate,
username: str,
ip_address: str | None = None,
) -> BomHeader:
    bom = db.query(BomHeader).filter(BomHeader.id == bom_id).first()
    if not bom:
        raise ValueError(f"BOM不存在：{bom_id}")

    header_fields = {k: v for k, v in data.model_dump(exclude_unset=True).items()
                     if k not in ("details", "change_reason")}
    for field, value in header_fields.items():
        setattr(bom, field, value)

    if data.details is not None:
        db.query(BomDetail).filter(BomDetail.bom_id == bom_id).delete()
        for item in data.details:
            detail = BomDetail(
                bom_id=bom.id,
                material_sku_id=item.material_sku_id,
                material_sku_code=item.material_sku_code,
                material_sku_name=item.material_sku_name,
                spec=item.spec,
                unit=item.unit,
                quantity_per_unit=item.quantity_per_unit,
                wastage_rate=item.wastage_rate,
                level=item.level,
                parent_detail_id=item.parent_detail_id,
                item_version=item.item_version,
                process_note=item.process_note,
                remark=item.remark,
            )
            db.add(detail)

    db.flush()
    user = db.query(User).filter(User.username == username).first()
    _write_audit(
        db, user, action="UPDATE", module="bom",
        resource_type="bom_header", resource_id=bom.bom_no,
        resource_name=f"BOM {bom.bom_no}",
        summary=f"更新BOM {bom.bom_name}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(bom)
    return bom


def delete_bom(
db: Session,
bom_id: int,
username: str,
ip_address: str | None = None,
) -> None:
    bom = db.query(BomHeader).filter(BomHeader.id == bom_id).first()
    if not bom:
        raise ValueError(f"BOM不存在：{bom_id}")

    bom_no = bom.bom_no
    bom_name = bom.bom_name
    db.query(BomDetail).filter(BomDetail.bom_id == bom_id).delete()
    db.delete(bom)

    user = db.query(User).filter(User.username == username).first()
    _write_audit(
        db, user, action="DELETE", module="bom",
        resource_type="bom_header", resource_id=bom_no,
        resource_name=f"BOM {bom_no}",
        summary=f"删除BOM {bom_name}",
        change_reason=None, ip_address=ip_address,
    )
    db.commit()


def check_material_availability(db: Session, bom_id: int) -> dict:
    bom = db.query(BomHeader).filter(BomHeader.id == bom_id).first()
    if not bom:
        raise ValueError(f"BOM不存在：{bom_id}")

    details = db.query(BomDetail).filter(BomDetail.bom_id == bom_id).all()
    items = []
    for d in details:
        stock = db.query(RawMaterialInventory).filter(
            RawMaterialInventory.sku_id == d.material_sku_id,
            RawMaterialInventory.status == "IN_STOCK",
        ).all()
        stock_qty = sum(s.quantity for s in stock)
        required = d.quantity_per_unit * bom.plan_quantity
        shortage = max(0, required - stock_qty)
        items.append(MaterialCheckItem(
            material_sku_id=d.material_sku_id,
            material_sku_code=d.material_sku_code,
            material_sku_name=d.material_sku_name,
            spec=d.spec,
            unit=d.unit,
            quantity_per_unit=d.quantity_per_unit,
            required_qty=required,
            stock_qty=stock_qty,
            shortage_qty=shortage,
            is_sufficient=shortage == 0,
        ))

    return {
        "bom_id": bom_id,
        "bom_no": bom.bom_no,
        "bom_name": bom.bom_name,
        "plan_quantity": bom.plan_quantity,
        "overall_sufficient": all(item.is_sufficient for item in items),
        "items": items,
    }


def get_tasks(
    db: Session,
    page: int = 1,
    page_size: int = 15,
    keyword: str | None = None,
    status: str | None = None,
) -> tuple[list[ProductionTask], int]:
    query = db.query(ProductionTask)
    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(ProductionTask.task_no.like(kw))
    if status:
        query = query.filter(ProductionTask.status == status)
    total = query.count()
    items = query.order_by(ProductionTask.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    bom_ids = list({item.bom_id for item in items if item.bom_id})
    if bom_ids:
        bom_map = {b.id: b for b in db.query(BomHeader).filter(BomHeader.id.in_(bom_ids)).all()}
        for item in items:
            bom = bom_map.get(item.bom_id)
            if bom:
                item.bom_no = bom.bom_no
                item.bom_name = bom.bom_name
    return items, total


def export_bom_xlsx(db: Session, keyword: str | None = None) -> bytes:
    """导出 BOM 列表为 Excel。"""
    query = db.query(BomHeader)
    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(
            (BomHeader.bom_no.like(kw)) | (BomHeader.bom_name.like(kw))
        )
    items = query.order_by(BomHeader.id.desc()).all()

    headers = ["BOM编号", "BOM名称", "版本", "成品编码", "成品名称", "计划数量", "状态", "创建人", "备注"]
    rows = []
    for b in items:
        rows.append([
            b.bom_no, b.bom_name, b.version, b.product_sku_code,
            b.product_sku_name, b.plan_quantity, b.status, b.created_by, b.remark or "",
        ])
    return build_simple_xlsx(headers, rows, sheet_title="BOM列表", col_widths=[18, 30, 10, 16, 24, 12, 10, 12, 20])


def export_tasks_xlsx(db: Session, keyword: str | None = None, status: str | None = None) -> bytes:
    """导出生产任务列表为 Excel。"""
    query = db.query(ProductionTask)
    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(ProductionTask.task_no.like(kw))
    if status:
        query = query.filter(ProductionTask.status == status)
    items = query.order_by(ProductionTask.id.desc()).all()

    bom_ids = list({t.bom_id for t in items if t.bom_id})
    bom_map = {b.id: b for b in db.query(BomHeader).filter(BomHeader.id.in_(bom_ids)).all()} if bom_ids else {}

    headers = ["任务编号", "BOM编号", "BOM名称", "计划数量", "物料齐套", "状态", "开始日期", "结束日期", "创建人"]
    rows = []
    for t in items:
        bom = bom_map.get(t.bom_id)
        rows.append([
            t.task_no, bom.bom_no if bom else "", bom.bom_name if bom else "",
            t.plan_quantity, t.material_availability, t.status,
            str(t.start_date) if t.start_date else "", str(t.end_date) if t.end_date else "",
            t.created_by,
        ])
    return build_simple_xlsx(headers, rows, sheet_title="生产任务", col_widths=[18, 18, 30, 12, 12, 10, 14, 14, 12])


def create_task(
db: Session,
data: ProductionTaskCreate,
username: str,
ip_address: str | None = None,
) -> ProductionTask:
    bom = db.query(BomHeader).filter(BomHeader.id == data.bom_id).first()
    if not bom:
        raise ValueError(f"BOM不存在：{data.bom_id}")

    task_no = generate_task_no(db)
    availability = check_material_availability(db, data.bom_id)
    material_availability = "COMPLETE" if availability["overall_sufficient"] else "SHORTAGE"

    task = ProductionTask(
        task_no=task_no,
        bom_id=data.bom_id,
        plan_quantity=data.plan_quantity,
        material_availability=material_availability,
        status="PENDING",
        product_type=data.product_type,
        start_date=data.start_date,
        end_date=data.end_date,
        created_by=username,
    )
    db.add(task)
    db.flush()

    user = db.query(User).filter(User.username == username).first()
    _write_audit(
        db, user, action="CREATE", module="production",
        resource_type="production_task", resource_id=task_no,
        resource_name=f"生产任务 {task_no}",
        summary=f"创建生产任务，BOM={bom.bom_no}，计划数量={data.plan_quantity}，齐套状态={material_availability}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(task)
    task.bom_no = bom.bom_no
    task.bom_name = bom.bom_name
    return task


def update_task(
db: Session,
task_id: int,
data: ProductionTaskUpdate,
username: str,
ip_address: str | None = None,
) -> ProductionTask:
    task = db.query(ProductionTask).filter(ProductionTask.id == task_id).first()
    if not task:
        raise ValueError(f"生产任务不存在：{task_id}")

    old_status = task.status
    update_fields = {k: v for k, v in data.model_dump(exclude_unset=True).items()
                     if k != "change_reason"}
    for field, value in update_fields.items():
        setattr(task, field, value)

    new_status = task.status

    if old_status != "COMPLETED" and new_status == "COMPLETED":
        bom = db.query(BomHeader).filter(BomHeader.id == task.bom_id).first()
        if not bom:
            raise ValueError(f"关联BOM不存在：{task.bom_id}")

        from app.models.inventory import InventoryItem
        from app.utils.sn_generator import generate_sn, sn_timestamp
        import uuid

        warehouse_type = "FINISHED" if task.product_type == "FINISHED_PRODUCT" else "SEMI_FINISHED"

        for i in range(task.plan_quantity):
            timestamp = sn_timestamp()
            item_sn = generate_sn(bom.product_sku_id, timestamp, i + 1)
            db.add(InventoryItem(
                item_sn=item_sn,
                sku_id=bom.product_sku_id,
                stock_status="IN_STOCK",
                stock_condition="NEW",
                operation_status="COMPLETED",
                warehouse_type=warehouse_type,
                last_order_no=task.task_no,
                current_location="库房",
                quantity=1,
            ))

        from app.models.raw_material import RawMaterialInventory
        details = db.query(BomDetail).filter(BomDetail.bom_id == task.bom_id).all()
        for d in details:
            materials = db.query(RawMaterialInventory).filter(
                RawMaterialInventory.sku_id == d.material_sku_id,
                RawMaterialInventory.status == "IN_STOCK",
            ).order_by(RawMaterialInventory.id.asc()).limit(
                int(d.quantity_per_unit * task.plan_quantity)
            ).all()
            for m in materials:
                m.status = "CONSUMED"

    db.flush()
    user = db.query(User).filter(User.username == username).first()
    _write_audit(
        db, user, action="UPDATE", module="production",
        resource_type="production_task", resource_id=task.task_no,
        resource_name=f"生产任务 {task.task_no}",
        summary=f"更新生产任务，修改字段={list(update_fields.keys())}",
        change_reason=data.change_reason, ip_address=ip_address,
    )
    db.commit()
    db.refresh(task)
    return task


def delete_task(
    db: Session,
    task_id: int,
    username: str,
    ip_address: str | None = None,
):
    task = db.query(ProductionTask).filter(ProductionTask.id == task_id).first()
    if not task:
        raise ValueError(f"生产任务不存在：{task_id}")

    task_no = task.task_no
    db.delete(task)

    user = db.query(User).filter(User.username == username).first()
    _write_audit(
        db, user, action="DELETE", module="production",
        resource_type="production_task",
        resource_id=task_no,
        resource_name=f"生产任务 {task_no}",
        summary=f"删除生产任务 {task_no}",
        change_reason=None, ip_address=ip_address,
    )
    db.commit()


BOM_IMPORT_HEADERS = ["BOM名称", "版本号", "成品物料编码", "成品物料名称", "计划数量", "备注"]
BOM_IMPORT_COL_WIDTHS = [20, 12, 16, 20, 12, 16]


def export_bom_template() -> bytes:
    return build_template_xlsx(
        BOM_IMPORT_HEADERS,
        example_row=["示例BOM", "V1.0", "SKU001", "示例成品", "100", "备注示例"],
        sheet_title="BOM导入模板",
        col_widths=BOM_IMPORT_COL_WIDTHS,
    )


def import_bom_xlsx(db: Session, content: bytes, username: str) -> dict:
    rows = parse_import_xlsx(content)
    success, errors = 0, []
    for i, row in enumerate(rows, 1):
        try:
            if len(row) < 4:
                errors.append(f"第{i}行：列数不足（需要BOM名称、版本号、物料编码、物料名称）")
                continue
            bom_name, version, sku_code, sku_name, plan_qty, remark = row[0], row[1], row[2], row[3], row[4] if len(row) > 4 else "1", row[5] if len(row) > 5 else ""
            if not bom_name.strip():
                errors.append(f"第{i}行：BOM名称为空")
                continue
            from app.models.product import ProductSku
            sku = db.query(ProductSku).filter(ProductSku.sku_code == sku_code.strip()).first()
            if not sku:
                errors.append(f"第{i}行：物料编码 {sku_code.strip()} 不存在")
                continue
            import uuid
            bom_no = "BOM" + uuid.uuid4().hex[:8].upper()
            try:
                plan_qty_val = int(plan_qty) if plan_qty and str(plan_qty).strip() else 1
            except ValueError:
                plan_qty_val = 1
            bom = BomHeader(
                bom_no=bom_no, bom_name=bom_name.strip(), version=version.strip(),
                product_sku_id=sku.id, product_sku_code=sku.sku_code or "",
                product_sku_name=sku.name, plan_quantity=plan_qty_val,
                status="DRAFT", remark=remark.strip() or None, created_by=username,
            )
            db.add(bom)
            db.flush()
            success += 1
        except Exception as e:
            errors.append(f"第{i}行：{str(e)}")
    db.commit()
    return {"success": success, "errors": errors}


TASK_IMPORT_HEADERS = ["BOM编号", "计划数量", "计划开始日期", "计划完成日期"]
TASK_IMPORT_COL_WIDTHS = [16, 12, 16, 16]


def export_task_template() -> bytes:
    return build_template_xlsx(
        TASK_IMPORT_HEADERS,
        example_row=["BOM00000001", "50", "2026-01-01", "2026-01-31"],
        sheet_title="生产任务导入模板",
        col_widths=TASK_IMPORT_COL_WIDTHS,
    )


def import_task_xlsx(db: Session, content: bytes, username: str) -> dict:
    rows = parse_import_xlsx(content)
    success, errors = 0, []
    for i, row in enumerate(rows, 1):
        try:
            if len(row) < 2:
                errors.append(f"第{i}行：列数不足")
                continue
            bom_no, plan_qty, start_date, end_date = row[0], row[1], row[2] if len(row) > 2 else "", row[3] if len(row) > 3 else ""
            bom = db.query(BomHeader).filter(BomHeader.bom_no == bom_no.strip()).first()
            if not bom:
                errors.append(f"第{i}行：BOM编号 {bom_no.strip()} 不存在")
                continue
            try:
                plan_qty_val = int(plan_qty) if plan_qty and str(plan_qty).strip() else 1
            except ValueError:
                plan_qty_val = 1
            import uuid
            task_no = "TASK" + uuid.uuid4().hex[:8].upper()
            from datetime import date
            s_date = date.fromisoformat(start_date.strip()) if start_date and start_date.strip() else None
            e_date = date.fromisoformat(end_date.strip()) if end_date and end_date.strip() else None
            task = ProductionTask(
                task_no=task_no, bom_id=bom.id, plan_quantity=plan_qty_val,
                status="PENDING", start_date=s_date, end_date=e_date,
                created_by=username,
            )
            db.add(task)
            db.flush()
            success += 1
        except Exception as e:
            errors.append(f"第{i}行：{str(e)}")
    db.commit()
    return {"success": success, "errors": errors}