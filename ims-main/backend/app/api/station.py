from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.common import R, PageResult
from app.schemas.station import StationResponse, StationCreate, StationUpdate
from app.service import station_service

router = APIRouter(prefix="/stations", tags=["场站"])


@router.get("", response_model=R[PageResult[StationResponse]], summary="场站列表")
def list_stations(
    page: int = 1,
    page_size: int = 20,
    keyword: str | None = None,
    status: str | None = None,
    customer_id: int | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total, items = station_service.get_station_list(db, page, page_size, keyword, status, customer_id)
    return R.ok(
        data=PageResult(
            total=total,
            page=page,
            page_size=page_size,
            items=[StationResponse.model_validate(s) for s in items],
        )
    )


@router.get("/all", response_model=R[list[StationResponse]], summary="全部启用场站")
def list_all_active(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    items = station_service.get_all_active(db)
    return R.ok(data=[StationResponse.model_validate(s) for s in items])


@router.get("/{station_id}", response_model=R[StationResponse], summary="场站详情")
def get_station(
    station_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    station = station_service.get_station_by_id(db, station_id)
    if not station:
        return R.fail("场站不存在")
    return R.ok(data=StationResponse.model_validate(station))


@router.post("", response_model=R[StationResponse], summary="创建场站")
def create_station(
    body: StationCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        station = station_service.create_station(db, body)
        return R.ok(data=StationResponse.model_validate(station))
    except ValueError as e:
        return R.fail(str(e))


@router.put("/{station_id}", response_model=R[StationResponse], summary="更新场站")
def update_station(
    station_id: int,
    body: StationUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        station = station_service.update_station(db, station_id, body)
        return R.ok(data=StationResponse.model_validate(station))
    except ValueError as e:
        return R.fail(str(e))


@router.delete("/{station_id}", response_model=R[None], summary="删除场站")
def delete_station(
    station_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        station_service.delete_station(db, station_id)
        return R.ok(msg="删除成功")
    except ValueError as e:
        return R.fail(str(e))