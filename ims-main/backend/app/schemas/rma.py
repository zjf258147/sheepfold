from datetime import date, datetime

from pydantic import BaseModel, Field


class RmaReturnCreate(BaseModel):
    sku_id: int = Field(..., description="物料 SKU ID")
    sn: str = Field(..., min_length=1, max_length=50, description="设备 SN")
    quantity: int = Field(default=1, ge=1, description="退货数量")
    unit: str = Field(default="个", description="单位")
    customer_name: str | None = Field(None, max_length=100, description="客户名称")
    return_reason: str = Field(..., min_length=1, max_length=255, description="退货原因（必填）")
    return_date: date = Field(..., description="退货日期")
    remark: str | None = Field(None, description="备注")


class RmaReturnResponse(BaseModel):
    id: int
    return_no: str
    sku_id: int
    sku_name: str | None = None
    sku_code: str | None = None
    sn: str
    quantity: int
    unit: str
    spec: str | None = None
    customer_name: str | None = None
    return_reason: str
    return_date: date
    status: str
    assigned_to: int | None = None
    assignee_name: str | None = None
    assign_type: str | None = None
    assign_reason: str | None = None
    problem_description: str | None = None
    repair_plan: str | None = None
    inspection_report_no: str | None = None
    new_sn: str | None = None
    reship_station: str | None = None
    materials_used: str | None = None
    repair_time_hours: float | None = None
    turnaround_days: int | None = None
    repair_count: int | None = None
    repair_reason: str | None = None
    repair_id: int | None = None
    diagnosis_result: str | None = None
    change_reason: str | None = None
    remark: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class RmaDiagnosisCreate(BaseModel):
    return_id: int = Field(..., description="返厂退货单 ID")
    diagnosed_by: int = Field(..., description="诊断人 ID")
    diagnosis_date: date = Field(..., description="诊断日期")
    fault_description: str = Field(..., min_length=1, description="故障描述")
    diagnosis_result: str = Field(..., description="诊断结果：REPAIRABLE（可维修）")
    repair_plan: str | None = Field(None, description="维修方案")
    inspection_report_no: str | None = Field(None, max_length=100, description="送检单编号")
    change_reason: str | None = Field(None, max_length=255, description="变更原因")
    remark: str | None = Field(None, description="备注")


class RmaDiagnosisResponse(BaseModel):
    id: int
    return_id: int
    diagnosis_no: str
    diagnosed_by: int
    diagnoser_name: str | None = None
    diagnosis_date: date
    fault_description: str
    diagnosis_result: str
    repair_plan: str | None = None
    inspection_report_no: str | None = None
    change_reason: str | None = None
    remark: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class RmaRepairCreate(BaseModel):
    return_id: int = Field(..., description="返厂退货单 ID")
    repair_by: int = Field(..., description="维修人 ID")
    old_sn: str = Field(..., min_length=1, max_length=50, description="原设备 SN")
    new_sn: str | None = Field(None, max_length=50, description="新设备 SN（换码时填写）")
    repair_description: str | None = Field(None, description="维修描述")
    materials_used: str | None = Field(None, description="维修用料")
    fault_code: str | None = Field(None, max_length=50, description="故障码")
    start_time: datetime | None = Field(None, description="维修开始时间")
    end_time: datetime | None = Field(None, description="维修结束时间")
    repair_date: date | None = Field(None, description="维修完成日期")
    change_reason: str | None = Field(None, max_length=255, description="变更原因")
    remark: str | None = Field(None, description="备注")


class RmaRepairResponse(BaseModel):
    id: int
    return_id: int
    repair_no: str
    repair_by: int
    repairer_name: str | None = None
    old_sn: str
    new_sn: str | None = None
    repair_description: str | None = None
    materials_used: str | None = None
    fault_code: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    repair_date: date | None = None
    change_reason: str | None = None
    remark: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class RmaQualityCheckCreate(BaseModel):
    return_id: int = Field(..., description="返厂退货单 ID")
    checked_by: int = Field(..., description="检验人 ID")
    check_date: date = Field(..., description="检验日期")
    check_result: str = Field(..., description="PASS / FAIL")
    check_description: str | None = Field(None, description="检验描述")
    change_reason: str | None = Field(None, max_length=255, description="变更原因")
    remark: str | None = Field(None, description="备注")


class RmaQualityCheckResponse(BaseModel):
    id: int
    return_id: int
    checked_by: int
    checker_name: str | None = None
    check_date: date
    check_result: str
    check_description: str | None = None
    change_reason: str | None = None
    remark: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class RmaWarehouseInCreate(BaseModel):
    return_id: int = Field(..., description="返厂退货单 ID")
    new_sn: str = Field(..., min_length=1, max_length=50, description="新SN")
    repair_count: int = Field(default=1, ge=1, description="该SN累计维修次数")
    repair_reason: str | None = Field(None, description="维修原因（累计）")
    warehouse_type: str = Field(default="ZERO_COST_FINISHED", description="入库仓库类型：ZERO_COST_FINISHED（零成本成品）/ ZERO_COST_SEMI（零成本半成品）")
    change_reason: str | None = Field(None, max_length=255, description="变更原因")
    remark: str | None = Field(None, description="备注")


class RmaWarehouseInResponse(BaseModel):
    id: int
    return_id: int
    new_sn: str
    warehouse_by: int
    warehouser_name: str | None = None
    warehouse_date: date
    repair_count: int
    repair_reason: str | None = None
    warehouse_type: str | None = None
    change_reason: str | None = None
    remark: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class RmaScrapCreate(BaseModel):
    return_id: int = Field(..., description="返厂退货单 ID")
    scrap_reason: str = Field(..., min_length=1, description="报废原因")
    change_reason: str | None = Field(None, max_length=255, description="变更原因")
    remark: str | None = Field(None, description="备注")


class RmaScrapApprove(BaseModel):
    change_reason: str = Field(..., min_length=1, max_length=255, description="审批意见（必填）")
    reject_reason: str | None = Field(None, max_length=255, description="驳回原因（驳回时填写）")


class RmaScrapResponse(BaseModel):
    id: int
    return_id: int
    scrap_no: str
    requested_by: int
    requester_name: str | None = None
    scrap_reason: str
    status: str
    approved_by: int | None = None
    approver_name: str | None = None
    approved_at: datetime | None = None
    reject_reason: str | None = None
    change_reason: str | None = None
    remark: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class RmaReshipCreate(BaseModel):
    return_id: int = Field(..., description="返厂退货单 ID")
    new_sn: str = Field(..., min_length=1, max_length=50, description="出货 SN")
    software_version: str | None = Field(None, max_length=50, description="软件版本号")
    ship_date: date = Field(..., description="出货日期")
    recipient: str | None = Field(None, max_length=100, description="收货人/客户")
    change_reason: str | None = Field(None, max_length=255, description="变更原因")
    remark: str | None = Field(None, description="备注")


class RmaReshipResponse(BaseModel):
    id: int
    return_id: int
    reship_no: str
    new_sn: str
    software_version: str | None = None
    ship_date: date
    recipient: str | None = None
    operator_id: int
    operator_name: str | None = None
    change_reason: str | None = None
    remark: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class RmaAssignCreate(BaseModel):
    assigned_to: int | None = Field(None, description="分配人 ID（判定报废时可不填）")
    assign_type: str = Field(..., description="分配类型：PRODUCTION（外观问题）/ TEST（功能问题）/ SCRAP（判定报废）")
    assign_reason: str = Field(..., min_length=1, max_length=255, description="分配原因/报废原因（必填）")
    scrap_reason: str | None = Field(None, max_length=500, description="报废原因（判定报废时填写）")
    change_reason: str = Field(..., min_length=1, max_length=255, description="变更原因（必填）")


class RmaTransferRequest(BaseModel):
    change_reason: str = Field(..., min_length=1, max_length=255, description="流转原因（必填）")
    target_assignee: int = Field(..., description="目标人 ID")


class RmasResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int


class RmaKnowledgeBaseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="知识标题")
    fault_code: str | None = Field(None, max_length=50, description="故障码")
    fault_symptom: str = Field(..., min_length=1, description="故障现象")
    solution: str = Field(..., min_length=1, description="解决方案")
    tags: list[str] | None = Field(None, description="标签列表")


class RmaKnowledgeBaseResponse(BaseModel):
    id: int
    title: str
    fault_code: str | None = None
    fault_symptom: str
    solution: str
    tags: list[str] | None = None
    source_type: str
    source_repair_id: int | None = None
    usage_count: int
    status: str
    created_by: int
    creator_name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class RmaKnowledgeBaseSearchResult(BaseModel):
    items: list[RmaKnowledgeBaseResponse]
    total: int
    keyword: str