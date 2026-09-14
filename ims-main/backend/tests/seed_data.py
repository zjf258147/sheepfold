"""
测试种子数据模块。

提供所有测试共享的基础数据：用户、分类、SKU、供应商、分组。
每个测试用例使用独立的数据库会话，种子数据在测试结束后自动回滚。
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.product import ProductCategory, ProductSku
from app.models.partner import PartnerGroup, Partner
from app.core.security import hash_password
from app.models.enums import UserRole, SkuType, SnMode


def seed_users(db: Session) -> dict:
    """创建测试用户：管理员、仓库、质量、生产、测试工程师。"""
    admin = User(
        username="admin",
        password=hash_password("admin123"),
        nickname="管理员",
        role=UserRole.ADMIN.value,
        status=1,
    )
    warehouse = User(
        username="warehouse",
        password=hash_password("123456"),
        nickname="仓库管理员",
        role=UserRole.WAREHOUSE.value,
        status=1,
    )
    quality = User(
        username="quality",
        password=hash_password("123456"),
        nickname="质量负责人",
        role=UserRole.QUALITY.value,
        status=1,
    )
    production = User(
        username="production",
        password=hash_password("123456"),
        nickname="生产负责人",
        role=UserRole.PRODUCTION.value,
        status=1,
    )
    test_eng = User(
        username="test_eng",
        password=hash_password("123456"),
        nickname="测试工程师",
        role=UserRole.TEST_ENGINEER.value,
        status=1,
    )
    db.add_all([admin, warehouse, quality, production, test_eng])
    db.flush()
    return {
        "admin": admin,
        "warehouse": warehouse,
        "quality": quality,
        "production": production,
        "test_eng": test_eng,
    }


def seed_products(db: Session) -> dict:
    """创建测试产品分类和 SKU（原材料 + 成品）。"""
    cat = ProductCategory(name="原材料")
    db.add(cat)
    db.flush()

    sku_raw = ProductSku(
        name="测试原材料",
        category_id=cat.id,
        barcode="RAW00001",
        sn_mode=SnMode.BOTH.value,
        unit="个",
        sku_code="202-018",
        spec="规格A",
        sku_type=SkuType.RAW_MATERIAL.value,
        status=1,
    )
    sku_fg = ProductSku(
        name="测试成品",
        category_id=cat.id,
        barcode="FG00001",
        sn_mode=SnMode.BOTH.value,
        unit="个",
        sku_code="202-046",
        spec="规格B",
        sku_type=SkuType.FINISHED_GOODS.value,
        status=1,
    )
    db.add_all([sku_raw, sku_fg])
    db.flush()
    return {
        "category": cat,
        "sku_raw": sku_raw,
        "sku_fg": sku_fg,
    }


def seed_partners(db: Session) -> dict:
    """创建测试往来单位（供应商分组 + 供应商）。"""
    pg = PartnerGroup(name="默认分组")
    db.add(pg)
    db.flush()

    supplier = Partner(
        name="测试供应商",
        group_id=pg.id,
        partner_type=2,
        status=1,
    )
    db.add(supplier)
    db.flush()
    return {
        "partner_group": pg,
        "supplier": supplier,
    }


def create_all_seed_data(db: Session) -> dict:
    """创建全部种子数据，返回字典供测试引用。"""
    users = seed_users(db)
    products = seed_products(db)
    partners = seed_partners(db)
    db.commit()

    return {**users, **products, **partners}