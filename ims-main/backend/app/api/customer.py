from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.permissions import require_permission
from app.db.database import get_db
from app.models.user import User
from app.schemas.common import R, PageResult
from app.schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate
from app.service import customer_service

router = APIRouter(prefix="/customers", tags=["客户"])


@router.get("", response_model=R[PageResult[CustomerResponse]], summary="客户列表")
def list_customers(
    page: int = 1,
    page_size: int = 20,
    keyword: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    total, items = customer_service.get_customers(db, page, page_size, keyword)
    return R.ok(
        data=PageResult(
            total=total,
            page=page,
            page_size=page_size,
            items=[CustomerResponse.model_validate(c) for c in items],
        )
    )


@router.post("", response_model=R[CustomerResponse], summary="创建客户")
def create_customer(
    body: CustomerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("customer.manage")),
):
    customer = customer_service.get_or_create(db, body.name)
    for key, value in body.model_dump(exclude={"name"}).items():
        if value is not None:
            setattr(customer, key, value)
    db.flush()
    return R.ok(data=CustomerResponse.model_validate(customer))


@router.put("/{customer_id}", response_model=R[CustomerResponse], summary="更新客户")
def update_customer(
    customer_id: int,
    body: CustomerUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_permission("customer.manage")),
):
    customer = db.query(customer_service.Customer).filter(customer_service.Customer.id == customer_id).first()
    if not customer:
        return R.fail("客户不存在")
    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(customer, key, value)
    db.flush()
    return R.ok(data=CustomerResponse.model_validate(customer))