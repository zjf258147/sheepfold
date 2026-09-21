from fastapi import APIRouter, Depends, Query, Request, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from urllib.parse import quote

from app.core.deps import get_current_user, get_db
from app.core.permissions import require_permission
from app.models.user import User
from app.schemas.bom import BomCreate, BomDetailResponse, BomResponse, BomUpdate, ProductionTaskCreate, ProductionTaskResponse, ProductionTaskUpdate
from app.schemas.common import PageResult, R
from app.service import bom_service
from app.utils.request_ip import get_client_ip

router = APIRouter(prefix="/bom", tags=["主线D BOM管理"])


@router.get("/list")
def list_boms(
    keyword: str | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    items, total = bom_service.get_boms(db, page=page, page_size=page_size, keyword=keyword)
    return R.ok(data=PageResult(items=[BomResponse.model_validate(i) for i in items], total=total, page=page, page_size=page_size))


@router.get("/export", summary="导出BOM列表 Excel")
def export_bom(
    keyword: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    content = bom_service.export_bom_xlsx(db, keyword=keyword)
    filename = quote("BOM列表.xlsx")
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"},
    )


@router.get("/template", summary="下载BOM导入模板")
def download_bom_template(_: User = Depends(get_current_user)):
    content = bom_service.export_bom_template()
    filename = quote("BOM导入模板.xlsx")
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"},
    )


@router.post("/import", summary="导入BOM Excel")
async def import_bom(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("bom.import")),
):
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="请上传 .xlsx 或 .xls 文件")
    content = await file.read()
    result = bom_service.import_bom_xlsx(db, content, current_user.username)
    return R.ok(data=result, msg=f"成功 {result['success']} 条，失败 {len(result['errors'])} 条")


@router.get("/{bom_id}")
def get_bom(bom_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        data = bom_service.get_bom_detail(db, bom_id)
        data["details"] = [BomDetailResponse.model_validate(d) for d in data["details"]]
        return R.ok(data=BomResponse.model_validate(data))
    except ValueError as e:
        return R.fail(msg=str(e))


@router.post("/", status_code=201)
def create_bom(
    data: BomCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("bom.create_edit")),
):
    try:
        bom = bom_service.create_bom(db, data, current_user.username, get_client_ip(request))
        return R.ok(data=BomResponse.model_validate(bom))
    except ValueError as e:
        return R.fail(msg=str(e))


@router.put("/{bom_id}")
def update_bom(
    bom_id: int,
    data: BomUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("bom.create_edit")),
):
    try:
        bom = bom_service.update_bom(db, bom_id, data, current_user.username, get_client_ip(request))
        return R.ok(data=BomResponse.model_validate(bom))
    except ValueError as e:
        return R.fail(msg=str(e))


@router.delete("/{bom_id}")
def delete_bom(
    bom_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("bom.create_edit")),
):
    try:
        bom_service.delete_bom(db, bom_id, current_user.username, get_client_ip(request))
        return R.ok()
    except ValueError as e:
        return R.fail(msg=str(e))


@router.get("/{bom_id}/availability")
def get_bom_availability(
    bom_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        result = bom_service.check_material_availability(db, bom_id)
        return R.ok(data=result)
    except ValueError as e:
        return R.fail(msg=str(e))


router_task = APIRouter(prefix="/production-task", tags=["主线D 生产任务"])


@router_task.get("/list")
def list_tasks(
    keyword: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    items, total = bom_service.get_tasks(db, page=page, page_size=page_size, keyword=keyword, status=status)
    return R.ok(data=PageResult(items=[ProductionTaskResponse.model_validate(i) for i in items], total=total, page=page, page_size=page_size))


@router_task.post("/", status_code=201)
def create_task(
    data: ProductionTaskCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("production_task.create_edit")),
):
    try:
        task = bom_service.create_task(db, data, current_user.username, get_client_ip(request))
        return R.ok(data=ProductionTaskResponse.model_validate(task))
    except ValueError as e:
        return R.fail(msg=str(e))


@router_task.put("/{task_id}")
def update_task(
    task_id: int,
    data: ProductionTaskUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("production_task.create_edit")),
):
    try:
        task = bom_service.update_task(db, task_id, data, current_user.username, get_client_ip(request))
        return R.ok(data=ProductionTaskResponse.model_validate(task))
    except ValueError as e:
        return R.fail(msg=str(e))


@router_task.delete("/{task_id}")
def delete_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("production_task.create_edit")),
):
    try:
        bom_service.delete_task(db, task_id, current_user.username, get_client_ip(request))
        return R.ok()
    except ValueError as e:
        return R.fail(msg=str(e))


@router_task.get("/export", summary="导出生产任务 Excel")
def export_tasks(
    keyword: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    content = bom_service.export_tasks_xlsx(db, keyword=keyword, status=status)
    filename = quote("生产任务列表.xlsx")
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"},
    )


@router_task.get("/template", summary="下载生产任务导入模板")
def download_task_template(_: User = Depends(get_current_user)):
    content = bom_service.export_task_template()
    filename = quote("生产任务导入模板.xlsx")
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"},
    )


@router_task.post("/import", summary="导入生产任务 Excel")
async def import_tasks(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="请上传 .xlsx 或 .xls 文件")
    content = await file.read()
    result = bom_service.import_task_xlsx(db, content, current_user.username)
    return R.ok(data=result, msg=f"成功 {result['success']} 条，失败 {len(result['errors'])} 条")