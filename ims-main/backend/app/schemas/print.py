from datetime import date, datetime

from pydantic import BaseModel


class PrintCompanyInfo(BaseModel):
    full_name: str = "西安敦临计量检测有限公司"
    short_name: str = "敦临计量"


class PrintIncomingReceiptData(BaseModel):
    receipt_no: str
    receipt_date: date
    supplier_name: str
    batch_no: str
    sku_code: str
    sku_name: str
    spec: str | None = None
    quantity: int
    unit: str
    status: str
    remark: str | None = None
    created_at: datetime | None = None


class PrintIncomingReceiptResponse(BaseModel):
    company: PrintCompanyInfo = PrintCompanyInfo()
    doc_type: str = "incoming_receipt"
    doc_title: str = "采购收货单"
    data: PrintIncomingReceiptData


class PrintShipmentItem(BaseModel):
    row_no: int
    sku_code: str
    sku_name: str
    spec: str | None = None
    quantity: int
    unit: str
    sn: str | None = None
    remark: str | None = None


class PrintShipmentData(BaseModel):
    shipment_no: str
    ship_date: date
    customer_name: str | None = None
    address: str
    logistics_provider: str
    tracking_no: str
    u9_task_no: str | None = None
    tf_version: str | None = None
    host_version: str | None = None
    total_amount: float | None = 0
    remark: str | None = None
    created_by: str


class PrintShipmentResponse(BaseModel):
    company: PrintCompanyInfo = PrintCompanyInfo()
    doc_type: str = "shipment"
    doc_title: str = "出货单"
    data: PrintShipmentData
    items: list[PrintShipmentItem]


class PrintIncomingInspectionData(BaseModel):
    inspection_no: str
    inspection_date: date
    supplier_name: str
    receipt_no: str
    batch_no: str
    sku_code: str
    sku_name: str
    spec: str | None = None
    quantity: int
    unit: str
    sample_qty: int
    defect_qty: int
    result: str
    result_cn: str
    defect_description: str | None = None
    inspector_name: str
    remark: str | None = None


class PrintIncomingInspectionResponse(BaseModel):
    company: PrintCompanyInfo = PrintCompanyInfo()
    doc_type: str = "incoming_inspection"
    doc_title: str = "来料检验报告"
    data: PrintIncomingInspectionData


class PrintIncomingReturnData(BaseModel):
    return_no: str
    return_date: date
    supplier_name: str
    receipt_no: str
    batch_no: str
    sku_code: str
    sku_name: str
    spec: str | None = None
    quantity: int
    return_qty: int
    unit: str
    return_reason: str
    status: str
    remark: str | None = None


class PrintIncomingReturnResponse(BaseModel):
    company: PrintCompanyInfo = PrintCompanyInfo()
    doc_type: str = "incoming_return"
    doc_title: str = "退货单"
    data: PrintIncomingReturnData


class PrintRmaRepairData(BaseModel):
    repair_no: str
    return_no: str
    customer_name: str | None = None
    sku_code: str
    sku_name: str
    spec: str | None = None
    old_sn: str
    new_sn: str | None = None
    problem_description: str | None = None
    diagnosis_result: str | None = None
    repair_description: str | None = None
    materials_used: str | None = None
    repair_date: date | None = None
    repairer_name: str
    remark: str | None = None


class PrintRmaRepairResponse(BaseModel):
    company: PrintCompanyInfo = PrintCompanyInfo()
    doc_type: str = "rma_repair"
    doc_title: str = "维修工单"
    data: PrintRmaRepairData


class PrintBomDetailItem(BaseModel):
    row_no: int
    level: int
    material_sku_code: str
    material_sku_name: str
    spec: str | None = None
    unit: str
    quantity_per_unit: float
    wastage_rate: float | None = None
    remark: str | None = None


class PrintBomData(BaseModel):
    bom_no: str
    bom_name: str
    version: str
    product_sku_code: str
    product_sku_name: str
    plan_quantity: int
    status: str
    created_by: str
    remark: str | None = None


class PrintBomResponse(BaseModel):
    company: PrintCompanyInfo = PrintCompanyInfo()
    doc_type: str = "bom"
    doc_title: str = "BOM清单"
    data: PrintBomData
    items: list[PrintBomDetailItem]