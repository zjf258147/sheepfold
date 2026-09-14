from sqlalchemy.orm import Session

from app.core.cache import get_cache, invalidate_cache
from app.models.partner import Partner, PartnerGroup
from app.schemas.partner import GroupCreate, GroupUpdate, PartnerCreate, PartnerUpdate
from app.utils.excel_export import build_simple_xlsx
from app.utils.excel_import import build_template_xlsx, parse_import_xlsx
import json


GROUP_CACHE_KEY = "ims:partner_groups:all"
GROUP_CACHE_TTL = 600


def get_groups(db: Session) -> list[PartnerGroup]:
    cache = get_cache()
    cached = cache.get(GROUP_CACHE_KEY)
    if cached is not None:
        return [PartnerGroup(**item) for item in json.loads(cached)]
    result = db.query(PartnerGroup).order_by(PartnerGroup.id).all()
    cache.set(GROUP_CACHE_KEY, json.dumps([{
        "id": g.id, "name": g.name, "created_at": str(g.created_at), "updated_at": str(g.updated_at),
    } for g in result], default=str), ttl=GROUP_CACHE_TTL)
    return result


def create_group(db: Session, data: GroupCreate) -> PartnerGroup:
    if db.query(PartnerGroup).filter(PartnerGroup.name == data.name).first():
        raise ValueError(f"分组名称已存在：{data.name}")
    group = PartnerGroup(name=data.name)
    db.add(group)
    db.commit()
    db.refresh(group)
    invalidate_cache(GROUP_CACHE_KEY)
    return group


def update_group(db: Session, group: PartnerGroup, data: GroupUpdate) -> PartnerGroup:
    if data.name and data.name != group.name:
        if db.query(PartnerGroup).filter(PartnerGroup.name == data.name).first():
            raise ValueError(f"分组名称已存在：{data.name}")
        group.name = data.name
    db.commit()
    db.refresh(group)
    invalidate_cache(GROUP_CACHE_KEY)
    return group


def delete_group(db: Session, group: PartnerGroup) -> None:
    if db.query(Partner).filter(Partner.group_id == group.id).first():
        raise ValueError("分组下存在往来单位，无法删除")
    db.delete(group)
    db.commit()
    invalidate_cache(GROUP_CACHE_KEY)


def get_partners(db: Session, page: int = 1, page_size: int = 20, group_id: int | None = None, partner_type: int | None = None, keyword: str | None = None):
    query = db.query(Partner)
    if group_id:
        query = query.filter(Partner.group_id == group_id)
    if partner_type is not None:
        query = query.filter(Partner.partner_type == partner_type)
    if keyword:
        query = query.filter(Partner.name.like(f"%{keyword}%"))
    total = query.count()
    items = query.order_by(Partner.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return total, items


def get_partner_by_id(db: Session, partner_id: int) -> Partner | None:
    return db.get(Partner, partner_id)


def validate_partner(db: Session, partner_id: int | None) -> Partner:
    """校验关联往来单位是否存在且已启用（不限制单位类型）。"""
    if partner_id is None:
        raise ValueError("请选择关联单位")
    partner = db.get(Partner, partner_id)
    if not partner:
        raise ValueError(f"往来单位不存在：{partner_id}")
    if partner.status != 1:
        raise ValueError(f"往来单位 [{partner.name}] 已停用")
    return partner


def create_partner(db: Session, data: PartnerCreate) -> Partner:
    partner = Partner(**data.model_dump())
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner


def update_partner(db: Session, partner: Partner, data: PartnerUpdate) -> Partner:
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(partner, k, v)
    db.commit()
    db.refresh(partner)
    return partner


def delete_partner(db: Session, partner: Partner) -> None:
    db.delete(partner)
    db.commit()


PARTNER_IMPORT_HEADERS = ["单位名称", "分组名称", "类型", "备注"]
PARTNER_IMPORT_COL_WIDTHS = [24, 16, 12, 20]


def export_partner_template() -> bytes:
    return build_template_xlsx(
        PARTNER_IMPORT_HEADERS,
        example_row=["示例供应商", "供应商分组", "供应商", "备注示例"],
        sheet_title="往来单位导入模板",
        col_widths=PARTNER_IMPORT_COL_WIDTHS,
    )


def export_partner_xlsx(db: Session, keyword: str | None = None, group_id: int | None = None, partner_type: int | None = None) -> bytes:
    total, items = get_partners(db, page=1, page_size=99999, keyword=keyword, group_id=group_id, partner_type=partner_type)
    type_map = {0: "供应商&客户", 1: "客户", 2: "供应商"}
    headers = PARTNER_IMPORT_HEADERS
    rows = []
    for p in items:
        rows.append([
            p.name or "", (p.group.name if p.group else ""),
            type_map.get(p.partner_type, ""),
            p.remark or "",
        ])
    return build_simple_xlsx(headers, rows, sheet_title="往来单位列表", col_widths=PARTNER_IMPORT_COL_WIDTHS)


def import_partner_xlsx(db: Session, content: bytes) -> dict:
    rows = parse_import_xlsx(content)
    success, errors = 0, []
    type_map_rev = {"供应商": 2, "客户": 1, "供应商&客户": 0, "0": 0, "1": 1, "2": 2}
    for i, row in enumerate(rows, 1):
        try:
            if len(row) < 2:
                errors.append(f"第{i}行：列数不足")
                continue
            name, group_name, ptype, remark = row[0], row[1], row[2] if len(row) > 2 else "", row[3] if len(row) > 3 else ""
            if not name.strip():
                errors.append(f"第{i}行：单位名称为空")
                continue
            group = db.query(PartnerGroup).filter(PartnerGroup.name == group_name.strip()).first()
            if not group:
                group = PartnerGroup(name=group_name.strip() or "未分组")
                db.add(group)
                db.flush()
            partner_type = type_map_rev.get(ptype.strip(), 0) if ptype.strip() else 0
            partner = Partner(
                name=name.strip(), group_id=group.id,
                partner_type=partner_type, remark=remark.strip() or None,
            )
            db.add(partner)
            db.flush()
            success += 1
        except Exception as e:
            errors.append(f"第{i}行：{str(e)}")
    db.commit()
    return {"success": success, "errors": errors}