"""
读接口权限测试
==============
验证两类读接口的权限控制：
1. ADMIN 专用读接口（如用户管理、审计日志）— 仅 ADMIN 可访问
2. 全员可读接口（如库存、BOM 等业务数据）— 所有角色不返回 403

运行：
    cd backend && uv run pytest tests/security/test_read_all_roles.py -v

前置条件：
    - 数据库已 seeded
"""

import pytest
from fastapi.testclient import TestClient

ALL_ROLES = ["ADMIN", "WAREHOUSE", "QUALITY", "PRODUCTION", "TEST_ENGINEER"]
NON_ADMIN_ROLES = ["WAREHOUSE", "QUALITY", "PRODUCTION", "TEST_ENGINEER"]

ROLE_LOGIN_MAP = {
    "ADMIN":          ("admin",       "admin123"),
    "WAREHOUSE":      ("warehouse",   "123456"),
    "QUALITY":        ("quality",     "123456"),
    "PRODUCTION":     ("production",  "123456"),
    "TEST_ENGINEER":  ("test_eng",    "123456"),
}

# ============================================================
# ADMIN 专用读端点（仅 ADMIN 可访问，其他角色 403）
# ============================================================
ADMIN_READ_ENDPOINTS = [
    ("GET", "/api/v1/users",                 "用户列表"),
    ("GET", "/api/v1/audit-logs",            "审计日志"),
]

# ============================================================
# 全员可读端点（所有角色均不返回 403）
# ============================================================
PUBLIC_READ_ENDPOINTS = [
    ("GET", "/api/v1/dashboard/stats",            "首页统计"),
    ("GET", "/api/v1/inventory/items",             "库存列表"),
    ("GET", "/api/v1/inventory/items/export",      "库存导出"),
    ("GET", "/api/v1/inventory/items/template",    "库存导入模板"),
    ("GET", "/api/v1/products/skus",               "SKU列表"),
    ("GET", "/api/v1/products/categories",         "产品分类"),
    ("GET", "/api/v1/partners",                    "往来单位"),
    ("GET", "/api/v1/partners/groups",             "往来单位分组"),
    ("GET", "/api/v1/customers",                   "客户列表"),
    ("GET", "/api/v1/incoming/receipts",           "来料收货列表"),
    ("GET", "/api/v1/incoming/inspections",        "来料检验列表"),
    ("GET", "/api/v1/incoming/returns",            "来料退货列表"),
    ("GET", "/api/v1/inbound/orders",              "入库单列表"),
    ("GET", "/api/v1/outbound/orders",             "出库单列表"),
    ("GET", "/api/v1/shipment",                    "出货列表"),
    ("GET", "/api/v1/rma/returns",                 "返厂退货列表"),
    ("GET", "/api/v1/rma/diagnoses",               "诊断列表"),
    ("GET", "/api/v1/rma/repairs",                 "维修列表"),
    ("GET", "/api/v1/rma/quality-checks",          "质检列表"),
    ("GET", "/api/v1/rma/warehouse-ins",           "入库列表"),
    ("GET", "/api/v1/rma/reships",                 "重发列表"),
    ("GET", "/api/v1/rma/scraps",                  "报废列表"),
    ("GET", "/api/v1/bom",                         "BOM列表"),
    ("GET", "/api/v1/bom/template",                "BOM导入模板"),
    ("GET", "/api/v1/production-task/list",        "生产任务列表"),
    ("GET", "/api/v1/production-task/export",      "生产任务导出"),
    ("GET", "/api/v1/production-task/template",    "生产任务导入模板"),
    ("GET", "/api/v1/stocktakes",                  "盘点列表"),
    ("GET", "/api/v1/adjustments",                 "库存调整列表"),
    ("GET", "/api/v1/stations",                    "场站列表"),
    ("GET", "/api/v1/device-ledger",               "设备台账列表"),
    ("GET", "/api/v1/snapshots",                   "库存快照"),
    ("GET", "/api/v1/settings/branding",           "品牌设置"),
    ("GET", "/api/v1/print/stocktakes/template",   "盘点打印模板"),
    ("GET", "/api/v1/docs",                        "文档下载"),
]


@pytest.fixture(scope="function")
def role_tokens(client: TestClient, seed_data):
    tokens = {}
    for role, (username, pwd) in ROLE_LOGIN_MAP.items():
        resp = client.post(
            "/api/v1/auth/login",
            json={"username": username, "password": pwd},
        )
        if resp.status_code == 200 and "access_token" in resp.json().get("data", {}):
            tokens[role] = resp.json()["data"]["access_token"]
        else:
            tokens[role] = None
    return tokens


# ============================================================
# 测试：ADMIN 专用端点
# ============================================================

_ADMIN_COMBOS = [
    (role, method, path, desc)
    for role in ALL_ROLES
    for (method, path, desc) in ADMIN_READ_ENDPOINTS
]


@pytest.mark.parametrize("role,method,path,desc", _ADMIN_COMBOS)
def test_admin_endpoints_require_admin(client, role_tokens, role, method, path, desc):
    """ADMIN 专用端点：ADMIN 可访问，其他角色 403"""
    token = role_tokens.get(role)
    if token is None:
        pytest.skip(f"{role} Token 获取失败")

    headers = {"Authorization": f"Bearer {token}"}
    resp = client.request(method, path, headers=headers)

    if role == "ADMIN":
        assert resp.status_code != 403, (
            f"ADMIN 访问 {desc} ({method} {path}) 不应返回 403，实际 {resp.status_code}"
        )
    else:
        assert resp.status_code == 403, (
            f"{role} 访问 {desc} ({method} {path}) 应返回 403，实际 {resp.status_code}"
        )


# ============================================================
# 测试：全员可读端点
# ============================================================

_PUBLIC_COMBOS = [
    (role, method, path, desc)
    for role in ALL_ROLES
    for (method, path, desc) in PUBLIC_READ_ENDPOINTS
]


@pytest.mark.parametrize("role,method,path,desc", _PUBLIC_COMBOS)
def test_public_read_accessible(client, role_tokens, role, method, path, desc):
    """全员可读端点：所有角色均不返回 403"""
    token = role_tokens.get(role)
    if token is None:
        pytest.skip(f"{role} Token 获取失败")

    headers = {"Authorization": f"Bearer {token}"}
    resp = client.request(method, path, headers=headers)

    assert resp.status_code != 403, (
        f"{role} 访问 {desc} ({method} {path}) 返回 403，预期全员可读。实际 {resp.status_code}"
    )