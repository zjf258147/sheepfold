"""
权限矩阵参数化测试 v2
========================
测试逻辑：遍历 PERMISSION_MAP 中所有权限键对应接口，
用 6 个角色 Token 逐一调用，验证 403/非403 与矩阵一致。

运行：
    cd backend && uv run pytest tests/security/test_permission_matrix_v2.py -v

前置条件：
    - 测试使用 SQLite 内存数据库 + seed_data fixture（无需外部 MySQL）
    - 种子用户：admin / warehouse / quality / production / test_eng / staff
    - Token 通过 create_access_token 直接生成，不依赖登录接口
"""

import pytest
from app.core.permissions import PERMISSION_MAP
from app.core.security import create_access_token

ALL_ROLES = ["ADMIN", "WAREHOUSE", "QUALITY", "PRODUCTION", "TEST_ENGINEER", "STAFF"]

# seed_data 键名 → 角色名
SEED_ROLE_MAP = {
    "ADMIN":          "admin",
    "WAREHOUSE":      "warehouse",
    "QUALITY":        "quality",
    "PRODUCTION":     "production",
    "TEST_ENGINEER":  "test_eng",
    "STAFF":          "staff",
}

# 权限键 → HTTP 请求 映射
# 格式：(method, path, body_or_none)
# body=None 表示空请求体（422 也算"能访问"），少量接口传空 body 会 422 但不会是 403
PERMISSION_ENDPOINT_MAP = {
    # ========== 来料管理 ==========
    "incoming.create":      ("POST",  "/api/v1/incoming/receipts",                    None),
    "incoming.inspect":     ("POST",  "/api/v1/incoming/inspections",                 None),
    "incoming.return":      ("POST",  "/api/v1/incoming/returns",                     None),
    "incoming.confirm":     ("POST",  "/api/v1/incoming/receipts/999999/confirm",     None),

    # ========== 入库管理 ==========
    "inbound.create":       ("POST",  "/api/v1/inbound/orders",                       None),
    "inbound.edit":         ("PUT",   "/api/v1/inbound/orders/999999",                None),
    "inbound.submit":       ("POST",  "/api/v1/inbound/orders/999999/submit",         None),
    "inbound.approve":      ("POST",  "/api/v1/inbound/orders/999999/approve",        None),
    "inbound.cancel":       ("POST",  "/api/v1/inbound/orders/999999/cancel",         None),

    # ========== 出库管理 ==========
    "outbound.create":      ("POST",  "/api/v1/outbound/orders",                      None),
    "outbound.edit":        ("PUT",   "/api/v1/outbound/orders/999999",               None),
    "outbound.submit":      ("POST",  "/api/v1/outbound/orders/999999/submit",        None),
    "outbound.approve":     ("POST",  "/api/v1/outbound/orders/999999/approve",       None),

    # ========== 返厂维修 ==========
    "rma.create_return":    ("POST",  "/api/v1/rma/returns",                          None),
    "rma.diagnose":         ("POST",  "/api/v1/rma/diagnoses",                        None),
    "rma.assign":           ("POST",  "/api/v1/rma/returns/999999/assign",            None),
    "rma.repair":           ("POST",  "/api/v1/rma/repairs",                          None),
    "rma.quality_check":    ("POST",  "/api/v1/rma/quality-checks",                   None),
    "rma.warehouse_in":     ("POST",  "/api/v1/rma/warehouse-ins",                    None),
    "rma.reship":           ("POST",  "/api/v1/rma/reships",                          None),
    "rma.request_scrap":    ("POST",  "/api/v1/rma/scraps",                           None),
    "rma.approve_scrap":    ("POST",  "/api/v1/rma/scraps/999999/approve",            None),

    # ========== 出货管理 ==========
    "shipment.create":      ("POST",  "/api/v1/shipment",                             None),
    "shipment.edit":        ("PUT",   "/api/v1/shipment/999999",                      None),

    # ========== BOM ==========
    "bom.create":           ("POST",  "/api/v1/bom",                                  None),
    "bom.edit":             ("PUT",   "/api/v1/bom/999999",                           None),
    "bom.import":           ("POST",  "/api/v1/bom/import",                           None),

    # ========== 生产任务 ==========
    "production_task.create_edit": ("POST",  "/api/v1/production-task/",              None),

    # ========== 库存 ==========
    "inventory.import":     ("POST",  "/api/v1/inventory/items/import",              None),

    # ========== 盘点 ==========
    "stocktake.create":     ("POST",  "/api/v1/stocktakes",                            None),
    "stocktake.scan":       ("POST",  "/api/v1/stocktakes/999999/scan",                None),
    "stocktake.complete":   ("POST",  "/api/v1/stocktakes/999999/complete",            None),
    "stocktake.cancel":     ("POST",  "/api/v1/stocktakes/999999/cancel",              None),

    # ========== 库存调整 ==========
    "adjustment.confirm":   ("POST",  "/api/v1/adjustments",                          None),

    # ========== 场站 ==========
    "station.create_edit":  ("POST",  "/api/v1/stations",                             None),

    # ========== 设备台账 ==========
    "device_ledger.create_edit": ("POST", "/api/v1/device-ledger",                    None),

    # ========== 基础数据 ==========
    "product.manage":       ("POST",  "/api/v1/products/skus",                        None),
    "partner.manage":       ("POST",  "/api/v1/partners",                             None),
    "customer.manage":      ("POST",  "/api/v1/customers",                            None),
}


# ============================================================
# Helpers
# ============================================================

def _make_headers(seed_data: dict, role: str) -> dict:
    seed_key = SEED_ROLE_MAP.get(role)
    if not seed_key:
        return {}
    user = seed_data.get(seed_key)
    if not user:
        return {}
    token = create_access_token({"user_id": user.id, "username": user.username})
    return {"Authorization": f"Bearer {token}"}


def _has_permission(role: str, permission_key: str) -> bool:
    """判断角色对某权限键是否有权限。ADMIN 始终有。"""
    if role == "ADMIN":
        return True
    allowed = PERMISSION_MAP.get(permission_key, ["ADMIN"])
    return role in allowed


# ============================================================
# 参数化测试
# ============================================================

# 生成 (role, permission_key) 所有组合
_COMBOS = [
    (role, perm_key)
    for perm_key in PERMISSION_ENDPOINT_MAP
    for role in ALL_ROLES
]


@pytest.mark.parametrize("role,perm_key", _COMBOS)
def test_write_permission_matrix(client, seed_data, role, perm_key):
    """
    矩阵参数化测试：
    对每个角色 × 每个权限键，调用对应写接口，
    验证有权限者不返回 403，无权限者返回 403。
    """
    headers = _make_headers(seed_data, role)
    if not headers:
        pytest.skip(f"{role} 用户不存在，跳过")

    method, path, body = PERMISSION_ENDPOINT_MAP[perm_key]

    if body is not None:
        resp = client.request(method, path, headers=headers, json=body)
    else:
        resp = client.request(method, path, headers=headers)

    has_perm = _has_permission(role, perm_key)

    if has_perm:
        assert resp.status_code != 403, (
            f"{role} 应有权访问 {perm_key} ({method} {path})，"
            f"实际返回 {resp.status_code}"
        )
        # 404 可接受：submit/approve/cancel 类端点检查资源存在性，
        # 测试用 ID=999999 的资源不存在，但权限校验已通过
        assert resp.status_code != 500, (
            f"{role} 访问 {perm_key} ({method} {path}) 服务端异常 500"
        )
    else:
        assert resp.status_code == 403, (
            f"{role} 不应有权访问 {perm_key} ({method} {path})，"
            f"实际返回 {resp.status_code}"
        )


# ============================================================
# 单角色快速检查
# ============================================================

@pytest.mark.parametrize("perm_key", list(PERMISSION_ENDPOINT_MAP.keys()))
def test_admin_always_passes(client, seed_data, perm_key):
    """ADMIN 任意操作都不应返回 403"""
    headers = _make_headers(seed_data, "ADMIN")
    if not headers:
        pytest.skip("ADMIN 用户不存在")
    method, path, body = PERMISSION_ENDPOINT_MAP[perm_key]
    resp = client.request(method, path, headers=headers, json=body) if body else client.request(method, path, headers=headers)
    assert resp.status_code != 403, f"ADMIN 访问 {perm_key} 返回 403"
    # 404 可接受（资源不存在但权限已通过）
    assert resp.status_code != 500, f"ADMIN 访问 {perm_key} ({method} {path}) 服务端异常 500"


@pytest.mark.parametrize("perm_key", list(PERMISSION_ENDPOINT_MAP.keys()))
def test_staff_always_denied(client, seed_data, perm_key):
    """STAFF 任意写操作都应返回 403（STAFF 不在任何 PERMISSION_MAP 中）"""
    headers = _make_headers(seed_data, "STAFF")
    if not headers:
        pytest.skip("STAFF 用户不存在")
    method, path, body = PERMISSION_ENDPOINT_MAP[perm_key]
    resp = client.request(method, path, headers=headers, json=body) if body else client.request(method, path, headers=headers)
    assert resp.status_code == 403, f"STAFF 访问 {perm_key}，期望 403，实际 {resp.status_code}"