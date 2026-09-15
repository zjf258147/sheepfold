from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.incoming import IncomingInspection, IncomingReceipt, IncomingReturn
from app.models.rma import RmaRepair, RmaReturn
from app.models.bom import BomHeader, BomDetail
from app.models.shipment import Shipment
from app.models.user import User
from app.schemas.common import R
from app.schemas.print import (
    PrintBomData,
    PrintBomDetailItem,
    PrintBomResponse,
    PrintIncomingInspectionData,
    PrintIncomingInspectionResponse,
    PrintIncomingReceiptData,
    PrintIncomingReceiptResponse,
    PrintIncomingReturnData,
    PrintIncomingReturnResponse,
    PrintRmaRepairData,
    PrintRmaRepairResponse,
    PrintShipmentData,
    PrintShipmentItem,
    PrintShipmentResponse,
)

router = APIRouter(prefix="/print", tags=["打印"])


@router.get("/incoming_receipt/{receipt_id}")
def get_incoming_receipt_print_data(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    receipt = db.query(IncomingReceipt).filter(IncomingReceipt.id == receipt_id).first()
    if not receipt:
        return R.fail(msg=f"到货单不存在：{receipt_id}")

    data = PrintIncomingReceiptData(
        receipt_no=receipt.receipt_no,
        receipt_date=receipt.delivery_date,
        supplier_name=receipt.supplier.name if receipt.supplier else "",
        batch_no=receipt.batch_no,
        sku_code=receipt.sku.sku_code if receipt.sku else "",
        sku_name=receipt.sku.name if receipt.sku else "",
        spec=receipt.sku.spec if receipt.sku else None,
        quantity=receipt.quantity,
        unit=receipt.unit,
        status=receipt.status,
        remark=receipt.remark,
        created_at=receipt.created_at,
    )
    return R.ok(data=PrintIncomingReceiptResponse(data=data))


@router.get("/shipment/{shipment_id}")
def get_shipment_print_data(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        return R.fail(msg=f"出货单不存在：{shipment_id}")

    sn_list = shipment.sn_list if isinstance(shipment.sn_list, list) else []
    items = []
    for i, sn in enumerate(sn_list):
        items.append(PrintShipmentItem(
            row_no=i + 1,
            sku_code=shipment.sku_code,
            sku_name=shipment.sku_name,
            spec=shipment.spec,
            quantity=1,
            unit=shipment.unit,
            sn=sn,
            remark=None,
        ))

    if not items:
        items.append(PrintShipmentItem(
            row_no=1,
            sku_code=shipment.sku_code,
            sku_name=shipment.sku_name,
            spec=shipment.spec,
            quantity=shipment.quantity,
            unit=shipment.unit,
            sn=None,
            remark=shipment.remark,
        ))

    data = PrintShipmentData(
        shipment_no=shipment.shipment_no,
        ship_date=shipment.ship_date,
        customer_name=None,
        address=shipment.address,
        logistics_provider=shipment.logistics_provider,
        tracking_no=shipment.tracking_no,
        u9_task_no=shipment.u9_task_no,
        tf_version=shipment.tf_version,
        host_version=shipment.host_version,
        total_amount=0,
        remark=shipment.remark,
        created_by=shipment.created_by,
    )
    return R.ok(data=PrintShipmentResponse(data=data, items=items))


RESULT_MAP = {
    "ACCEPTED": "合格",
    "CONCESSION_ACCEPTED": "特采",
    "REJECTED": "不合格",
}


@router.get("/incoming_inspection/{inspection_id}")
def get_incoming_inspection_print_data(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    insp = db.query(IncomingInspection).filter(IncomingInspection.id == inspection_id).first()
    if not insp:
        return R.fail(msg=f"检验报告不存在：{inspection_id}")

    receipt = db.query(IncomingReceipt).filter(IncomingReceipt.id == insp.receipt_id).first()
    supplier_name = receipt.supplier.name if receipt and receipt.supplier else ""
    receipt_no = receipt.receipt_no if receipt else ""
    batch_no = receipt.batch_no if receipt else ""
    sku_code = receipt.sku.sku_code if receipt and receipt.sku else ""
    sku_name = receipt.sku.name if receipt and receipt.sku else ""
    spec = receipt.sku.spec if receipt and receipt.sku else None
    quantity = receipt.quantity if receipt else 0
    unit = receipt.unit if receipt else "个"

    data = PrintIncomingInspectionData(
        inspection_no=insp.inspection_no,
        inspection_date=insp.inspection_date,
        supplier_name=supplier_name,
        receipt_no=receipt_no,
        batch_no=batch_no,
        sku_code=sku_code,
        sku_name=sku_name,
        spec=spec,
        quantity=quantity,
        unit=unit,
        sample_qty=insp.sample_qty,
        defect_qty=insp.defect_qty,
        result=insp.result,
        result_cn=RESULT_MAP.get(insp.result, insp.result),
        defect_description=insp.defect_description,
        inspector_name=insp.inspector.username if insp.inspector else "",
        remark=insp.remark,
    )
    return R.ok(data=PrintIncomingInspectionResponse(data=data))


@router.get("/incoming_return/{return_id}")
def get_incoming_return_print_data(
    return_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ret = db.query(IncomingReturn).filter(IncomingReturn.id == return_id).first()
    if not ret:
        return R.fail(msg=f"退货单不存在：{return_id}")

    receipt = db.query(IncomingReceipt).filter(IncomingReceipt.id == ret.receipt_id).first()
    supplier_name = receipt.supplier.name if receipt and receipt.supplier else ""
    receipt_no = receipt.receipt_no if receipt else ""
    batch_no = receipt.batch_no if receipt else ""
    sku_code = receipt.sku.sku_code if receipt and receipt.sku else ""
    sku_name = receipt.sku.name if receipt and receipt.sku else ""
    spec = receipt.sku.spec if receipt and receipt.sku else None
    quantity = receipt.quantity if receipt else 0
    unit = receipt.unit if receipt else "个"

    data = PrintIncomingReturnData(
        return_no=ret.return_no,
        return_date=ret.return_date,
        supplier_name=supplier_name,
        receipt_no=receipt_no,
        batch_no=batch_no,
        sku_code=sku_code,
        sku_name=sku_name,
        spec=spec,
        quantity=quantity,
        return_qty=ret.return_qty,
        unit=unit,
        return_reason=ret.return_reason,
        status=ret.status,
        remark=ret.remark,
    )
    return R.ok(data=PrintIncomingReturnResponse(data=data))


@router.get("/rma_repair/{repair_id}")
def get_rma_repair_print_data(
    repair_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repair = db.query(RmaRepair).filter(RmaRepair.id == repair_id).first()
    if not repair:
        return R.fail(msg=f"维修工单不存在：{repair_id}")

    rma = db.query(RmaReturn).filter(RmaReturn.id == repair.return_id).first()
    customer_name = rma.customer_name if rma else None
    return_no = rma.return_no if rma else ""
    sku_code = rma.sku.sku_code if rma and rma.sku else ""
    sku_name = rma.sku.name if rma and rma.sku else ""
    spec = rma.sku.spec if rma and rma.sku else None
    problem_description = rma.problem_description if rma else None
    diagnosis_result = rma.diagnosis_result if rma else None

    data = PrintRmaRepairData(
        repair_no=repair.repair_no,
        return_no=return_no,
        customer_name=customer_name,
        sku_code=sku_code,
        sku_name=sku_name,
        spec=spec,
        old_sn=repair.old_sn,
        new_sn=repair.new_sn,
        problem_description=problem_description,
        diagnosis_result=diagnosis_result,
        repair_description=repair.repair_description,
        materials_used=repair.materials_used,
        repair_date=repair.repair_date,
        repairer_name=repair.repairer.username if repair.repairer else "",
        remark=repair.remark,
    )
    return R.ok(data=PrintRmaRepairResponse(data=data))


@router.get("/bom/{bom_id}")
def get_bom_print_data(
    bom_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bom = db.query(BomHeader).filter(BomHeader.id == bom_id).first()
    if not bom:
        return R.fail(msg=f"BOM不存在：{bom_id}")

    details = db.query(BomDetail).filter(BomDetail.bom_id == bom_id).order_by(BomDetail.id).all()
    items = []
    for i, d in enumerate(details):
        items.append(PrintBomDetailItem(
            row_no=i + 1,
            level=d.level,
            material_sku_code=d.material_sku_code,
            material_sku_name=d.material_sku_name,
            spec=d.spec,
            unit=d.unit,
            quantity_per_unit=float(d.quantity_per_unit),
            wastage_rate=float(d.wastage_rate) if d.wastage_rate else None,
            remark=d.remark,
        ))

    data = PrintBomData(
        bom_no=bom.bom_no,
        bom_name=bom.bom_name,
        version=bom.version,
        product_sku_code=bom.product_sku_code,
        product_sku_name=bom.product_sku_name,
        plan_quantity=bom.plan_quantity,
        status=bom.status.value if hasattr(bom.status, 'value') else str(bom.status),
        created_by=bom.created_by,
        remark=bom.remark,
    )
    return R.ok(data=PrintBomResponse(data=data, items=items))