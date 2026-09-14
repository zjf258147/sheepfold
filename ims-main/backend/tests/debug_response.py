"""快速调试脚本：查看 API 响应格式。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from sqlalchemy import BigInteger, Integer, create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.database import get_db
from app.core.security import create_access_token, hash_password
from app.models.user import User
from app.models.product import ProductCategory, ProductSku
from app.models.partner import PartnerGroup, Partner
from app.models.enums import UserRole, SnMode, SkuType

# 导入所有模型
import app.models  # noqa
import app.models.incoming  # noqa
import app.models.raw_material  # noqa

# 修复 BigInteger 自增问题
for table in Base.metadata.tables.values():
    for col in table.columns:
        if isinstance(col.type, BigInteger) and col.primary_key:
            col.type = Integer()

eng = create_engine("sqlite:///file::memory:?cache=shared&uri=true", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=eng)

sess = sessionmaker(bind=eng)()

from main import create_app
app = create_app()
app.dependency_overrides[get_db] = lambda: sess

u = User(username="admin", password=hash_password("admin123"), nickname="admin", role=UserRole.ADMIN.value, status=1)
sess.add(u)
cat = ProductCategory(name="cat")
sess.add(cat)
sess.flush()
sku = ProductSku(name="s", category_id=cat.id, barcode="b", sn_mode=SnMode.BOTH.value, unit="u", sku_code="202-018", spec="s", sku_type=SkuType.RAW_MATERIAL.value, status=1)
sess.add(sku)
pg = PartnerGroup(name="g")
sess.add(pg)
sess.flush()
p = Partner(name="p", group_id=pg.id, partner_type=2, status=1)
sess.add(p)
sess.commit()

token = create_access_token({"user_id": u.id, "username": "admin"})
tc = TestClient(app)

payload = {
    "supplier_id": p.id,
    "sku_id": sku.id,
    "batch_no": "BATCH-001",
    "quantity": 100,
    "unit": "个",
    "delivery_date": "2026-09-08",
    "remark": "test",
}
r = tc.post("/api/v1/incoming/receipts", json=payload, headers={"Authorization": f"Bearer {token}"})
print("STATUS:", r.status_code)
import json
print("RESP:", json.dumps(r.json(), indent=2, ensure_ascii=False))