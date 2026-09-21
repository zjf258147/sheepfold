from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from urllib.parse import quote

from app.core.deps import get_current_user, get_db
from app.core.permissions import require_permission
from app.models.user import User
from app.schemas.rma import (
    RmaAssignCreate,
    RmaDiagnosisCreate,
    RmaDiagnosisResponse,
    RmaKnowledgeBaseCreate,
    RmaQualityCheckCreate,
    RmaQualityCheckResponse,
    RmaRepairCreate,
    RmaRepairResponse,
    RmaReshipCreate,
    RmaReshipResponse,
    RmaReturnCreate,
    RmaReturnResponse,
    RmaScrapApprove,
    RmaScrapCreate,
    RmaScrapResponse,
    RmaTransferRequest,
    RmaWarehouseInCreate,
    RmaWarehouseInResponse,
)
from app.service import rma_service
from app.utils.request_ip import get_client_ip
from app.schemas.common import PageResult, R

router = APIRouter(prefix="/rma", tags=["RMA 返厂维修"])


@router.get("/returns")
def list_returns(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    keyword: str | None = None,
    status: str | None = None,
    sku_id: int | None = None,
    assigned_to: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = rma_service.get_returns(
        db, page, page_size, keyword, status, sku_id, assigned_to, start_date, end_date
    )
    return R.ok(data=PageResult(items=[RmaReturnResponse.model_validate(item) for item in items], total=total, page=page, page_size=page_size))


@router.get("/returns/{return_id}")
def get_return(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from app.models.rma import RmaReturn
    r = db.query(RmaReturn).filter(RmaReturn.id == return_id).first()
    if not r:
        return R.fail(msg="退货单不存在")
    return R.ok(data=RmaReturnResponse.model_validate(r))


@router.post("/returns", status_code=201)
def create_return(
    data: RmaReturnCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.create_return")),
):
    return rma_service.create_return(db, data, current_user, get_client_ip(request))


@router.post("/returns/{return_id}/assign")
def assign_return(
    return_id: int,
    data: RmaAssignCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.assign")),
):
    return rma_service.assign_return(db, return_id, data, current_user, get_client_ip(request))


@router.post("/returns/{return_id}/transfer")
def transfer_return(
    return_id: int,
    data: RmaTransferRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.warehouse_in")),
):
    return rma_service.transfer_return(db, return_id, data, current_user, get_client_ip(request))


@router.get("/returns/{return_id}/diagnoses")
def get_diagnoses(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return R.ok(data=[RmaDiagnosisResponse.model_validate(i) for i in rma_service.get_diagnoses(db, return_id)])


@router.post("/diagnoses", status_code=201)
def create_diagnosis(
    data: RmaDiagnosisCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.diagnose")),
):
    return rma_service.create_diagnosis(db, data, current_user, get_client_ip(request))


@router.get("/returns/{return_id}/repairs")
def get_repairs(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return R.ok(data=[RmaRepairResponse.model_validate(i) for i in rma_service.get_repairs(db, return_id)])


@router.post("/repairs", status_code=201)
def create_repair(
    data: RmaRepairCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.repair")),
):
    return rma_service.create_repair(db, data, current_user, get_client_ip(request))


@router.get("/returns/{return_id}/scraps")
def get_scraps(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return R.ok(data=[RmaScrapResponse.model_validate(i) for i in rma_service.get_scraps(db, return_id)])


@router.post("/scraps", status_code=201)
def create_scrap(
    data: RmaScrapCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.request_scrap")),
):
    return rma_service.create_scrap(db, data, current_user, get_client_ip(request))


@router.post("/scraps/{scrap_id}/approve")
def approve_scrap(
    scrap_id: int,
    data: RmaScrapApprove,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.approve_scrap")),
):
    return rma_service.approve_scrap(db, scrap_id, data, current_user, get_client_ip(request))


@router.get("/returns/{return_id}/reships")
def get_reships(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return R.ok(data=[RmaReshipResponse.model_validate(i) for i in rma_service.get_reships(db, return_id)])


@router.post("/reships", status_code=201)
def create_reship(
    data: RmaReshipCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.reship")),
):
    return rma_service.create_reship(db, data, current_user, get_client_ip(request))


@router.get("/returns/{return_id}/quality-checks")
def get_quality_checks(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return R.ok(data=[RmaQualityCheckResponse.model_validate(i) for i in rma_service.get_quality_checks(db, return_id)])


@router.post("/quality-checks", status_code=201)
def create_quality_check(
    data: RmaQualityCheckCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.quality_check")),
):
    return rma_service.create_quality_check(db, data, current_user, get_client_ip(request))


@router.get("/returns/{return_id}/warehouse-ins")
def get_warehouse_ins(return_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return R.ok(data=[RmaWarehouseInResponse.model_validate(i) for i in rma_service.get_warehouse_ins(db, return_id)])


@router.post("/warehouse-ins", status_code=201)
def create_warehouse_in(
    data: RmaWarehouseInCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.warehouse_in")),
):
    return rma_service.create_warehouse_in(db, data, current_user, get_client_ip(request))


@router.get('/export', summary='导出返修记录 Excel')
def export_rma(
    status: str | None = None,
    keyword: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    content = rma_service.export_rma_xlsx(
        db, status=status, keyword=keyword,
        start_date=start_date, end_date=end_date,
    )
    filename = quote('返修记录.xlsx')
    return StreamingResponse(
        iter([content]),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f"attachment; filename*=UTF-8''{filename}"},
    )


@router.get('/template', summary='下载返修退货导入模板')
def download_rma_template(_: User = Depends(get_current_user)):
    content = rma_service.export_rma_template()
    filename = quote('返修退货导入模板.xlsx')
    return StreamingResponse(
        iter([content]),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f"attachment; filename*=UTF-8''{filename}"},
    )


@router.post('/import', summary='导入返修退货 Excel')
async def import_rma(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.create_return")),
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail='请上传 .xlsx 或 .xls 文件')
    content = await file.read()
    result = rma_service.import_rma_xlsx(db, content, current_user.username)
    return R.ok(data=result, msg=f"成功 {result['success']} 条，失败 {len(result['errors'])} 条")


# ============================================================
# 知识库
# ============================================================


@router.post("/knowledge-base", status_code=201, summary="创建知识库条目")
def create_knowledge_base(
    data: RmaKnowledgeBaseCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.knowledge_base")),
):
    entry = rma_service.create_knowledge_base_entry(
        db=db,
        title=data.title,
        fault_code=data.fault_code,
        fault_symptom=data.fault_symptom,
        solution=data.solution,
        user=current_user,
        tags=data.tags,
        ip_address=get_client_ip(request),
    )
    return R.ok(data=rma_service._kb_entry_to_dict(entry))


@router.get("/knowledge-base/search", summary="搜索知识库")
def search_knowledge_base(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    fault_code: str | None = Query(None, description="故障码精确匹配"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = rma_service.search_knowledge_base(
        db, keyword=keyword, fault_code=fault_code, page=page, page_size=page_size
    )
    return R.ok(data=[rma_service._kb_entry_to_dict(item) for item in items])


@router.post("/knowledge-base/from-repair/{repair_id}", status_code=201, summary="从维修工单沉淀知识")
def create_knowledge_base_from_repair(
    repair_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.knowledge_base")),
):
    entry = rma_service.create_knowledge_base_from_repair(
        db=db,
        repair_id=repair_id,
        user=current_user,
        ip_address=get_client_ip(request),
    )
    return R.ok(data=rma_service._kb_entry_to_dict(entry))


@router.post("/knowledge-base/{entry_id}/publish", summary="发布知识库条目")
def publish_knowledge_base(
    entry_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("rma.knowledge_base")),
):
    entry = rma_service.publish_knowledge_base_entry(
        db=db,
        entry_id=entry_id,
        user=current_user,
        ip_address=get_client_ip(request),
    )
    return R.ok(data=rma_service._kb_entry_to_dict(entry))