from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.station import Station
from app.models.enums import StationStatus
from app.schemas.station import StationCreate, StationUpdate


def get_station_list(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    keyword: str | None = None,
    status: str | None = None,
    customer_id: int | None = None,
) -> tuple[int, list[Station]]:
    query = db.query(Station)
    if keyword and keyword.strip():
        query = query.filter(Station.name.like(f"%{keyword.strip()}%"))
    if status:
        query = query.filter(Station.status == status)
    if customer_id:
        query = query.filter(Station.customer_id == customer_id)
    total = query.count()
    items = (
        query.order_by(Station.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return total, items


def get_all_active(db: Session) -> list[Station]:
    return db.query(Station).filter(Station.status == StationStatus.ACTIVE.value).order_by(Station.name).all()


def get_station_by_id(db: Session, station_id: int) -> Station | None:
    return db.query(Station).filter(Station.id == station_id).first()


def create_station(db: Session, data: StationCreate) -> Station:
    normalized = data.name.strip()
    existing = db.query(Station).filter(Station.name == normalized).first()
    if existing:
        raise ValueError(f"场站名称已存在: {normalized}")
    station = Station(
        name=normalized,
        customer_id=data.customer_id,
        address=data.address,
        contact_person=data.contact_person,
        contact_phone=data.contact_phone,
        status=data.status or StationStatus.ACTIVE.value,
        remark=data.remark,
    )
    db.add(station)
    db.flush()
    return station


def update_station(db: Session, station_id: int, data: StationUpdate) -> Station:
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station:
        raise ValueError("场站不存在")
    update_data = data.model_dump(exclude_unset=True)
    if "name" in update_data and update_data["name"]:
        normalized = update_data["name"].strip()
        existing = db.query(Station).filter(Station.name == normalized, Station.id != station_id).first()
        if existing:
            raise ValueError(f"场站名称已存在: {normalized}")
        update_data["name"] = normalized
    for key, value in update_data.items():
        setattr(station, key, value)
    db.flush()
    return station


def delete_station(db: Session, station_id: int) -> None:
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station:
        raise ValueError("场站不存在")
    db.delete(station)
    db.flush()