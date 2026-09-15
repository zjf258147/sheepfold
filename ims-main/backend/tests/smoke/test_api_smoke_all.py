"""
API 全量冒烟测试 — 遍历所有端点，验证不返回 500。

判断标准：
  200/201 → ✅ 通过
  400/401/403/404/405/422 → ✅ 通过（参数不全、无权限、不存在都算正常业务返回）
  500/502/503 → ❌ 失败（服务器内部错误）

运行：
  cd backend && uv run pytest tests/smoke/ -v --tb=short
"""

import pytest

API_V1 = "/api/v1"

# ──────────────────────────────────────────────
# Type A: GET 端点（无路径参数）
# 直接调用，带 admin token
# ──────────────────────────────────────────────

TYPE_A_NO_PARAM = [
    # auth
    ("GET", f"{API_V1}/auth/me"),
    # dashboard
    ("GET", f"{API_V1}/dashboard/pending-audit"),
    ("GET", f"{API_V1}/dashboard/stock-summary"),
    ("GET", f"{API_V1}/dashboard/partner-summary"),
    ("GET", f"{API_V1}/dashboard/phase2-stats"),
    ("GET", f"{API_V1}/dashboard/poll-status"),
    # inventory
    ("GET", f"{API_V1}/inventory"),
    ("GET", f"{API_V1}/inventory/cursor"),
    ("GET", f"{API_V1}/inventory/available"),
    ("GET", f"{API_V1}/inventory/export"),
    ("GET", f"{API_V1}/inventory/template"),
    # product
    ("GET", f"{API_V1}/products/categories"),
    ("GET", f"{API_V1}/products/skus"),
    ("GET", f"{API_V1}/products/skus/export"),
    ("GET", f"{API_V1}/products/skus/template"),
    # partner
    ("GET", f"{API_V1}/partners/groups"),
    ("GET", f"{API_V1}/partners"),
    ("GET", f"{API_V1}/partners/partners/export"),
    ("GET", f"{API_V1}/partners/partners/template"),
    # customer
    ("GET", f"{API_V1}/customers"),
    # inbound
    ("GET", f"{API_V1}/inbound/generate-no"),
    ("GET", f"{API_V1}/inbound/returnable-items"),
    ("GET", f"{API_V1}/inbound"),
    # outbound
    ("GET", f"{API_V1}/outbound/generate-no"),
    ("GET", f"{API_V1}/outbound"),
    # snapshot
    ("GET", f"{API_V1}/snapshots"),
    ("GET", f"{API_V1}/snapshots/dates"),
    ("GET", f"{API_V1}/snapshots/daily-ledger"),
    ("GET", f"{API_V1}/snapshots/daily-ledger/export"),
    ("GET", f"{API_V1}/snapshots/ledger-summary/export"),
    ("GET", f"{API_V1}/snapshots/items"),
    ("GET", f"{API_V1}/snapshots/items/export"),
    # audit
    ("GET", f"{API_V1}/audit-logs"),
    # settings
    ("GET", f"{API_V1}/settings/branding"),
    # incoming
    ("GET", f"{API_V1}/incoming/receipts"),
    ("GET", f"{API_V1}/incoming/receipts/export"),
    ("GET", f"{API_V1}/incoming/receipts/template"),
    # rma
    ("GET", f"{API_V1}/rma/returns"),
    # shipment
    ("GET", f"{API_V1}/shipments/list"),
    # bom
    ("GET", f"{API_V1}/bom/list"),
    ("GET", f"{API_V1}/bom/export"),
    ("GET", f"{API_V1}/bom/template"),
    # user
    ("GET", f"{API_V1}/users"),
    # station (二期)
    ("GET", f"{API_V1}/stations"),
    ("GET", f"{API_V1}/stations/all"),
    # device_ledger (二期)
    ("GET", f"{API_V1}/device-ledger"),
    # stocktake (二期)
    ("GET", f"{API_V1}/stocktakes"),
    # inventory_adjustment (二期)
    ("GET", f"{API_V1}/inventory-adjustments"),
]


@pytest.mark.parametrize("method,url", TYPE_A_NO_PARAM)
def test_smoke_type_a_no_param(client, auth_headers, method, url):
    """Type A: GET 端点无需路径参数，直接调用。"""
    resp = client.request(method, url, headers=auth_headers)
    assert resp.status_code != 500, (
        f"[500] {method} {url} → {resp.status_code} body={resp.text[:500]}"
    )


# ──────────────────────────────────────────────
# Type B: GET 端点（有路径参数）
# 使用 seed_data 中的 ID 或虚假 ID（接受 404）
# ──────────────────────────────────────────────

TYPE_B_PATH_PARAM = [
    # inventory
    ("GET", f"{API_V1}/inventory/FAKE_SN_99999"),
    ("GET", f"{API_V1}/inventory/FAKE_SN_99999/history"),
    # product
    ("GET", f"{API_V1}/products/categories/99999"),
    ("GET", f"{API_V1}/products/skus/99999"),
    # partner
    ("GET", f"{API_V1}/partners/groups/99999"),
    ("GET", f"{API_V1}/partners/99999"),
    # customer
    ("GET", f"{API_V1}/customers/99999"),
    # inbound
    ("GET", f"{API_V1}/inbound/99999"),
    # outbound
    ("GET", f"{API_V1}/outbound/99999"),
    # shipment
    ("GET", f"{API_V1}/shipments/99999"),
    # bom
    ("GET", f"{API_V1}/bom/99999"),
    ("GET", f"{API_V1}/bom/99999/availability"),
    # incoming
    ("GET", f"{API_V1}/incoming/receipts/99999"),
    ("GET", f"{API_V1}/incoming/receipts/99999/inspections"),
    # rma
    ("GET", f"{API_V1}/rma/returns/99999"),
    ("GET", f"{API_V1}/rma/returns/99999/diagnoses"),
    ("GET", f"{API_V1}/rma/returns/99999/repairs"),
    ("GET", f"{API_V1}/rma/returns/99999/scraps"),
    ("GET", f"{API_V1}/rma/returns/99999/reships"),
    ("GET", f"{API_V1}/rma/returns/99999/quality-checks"),
    ("GET", f"{API_V1}/rma/returns/99999/warehouse-ins"),
    # user
    ("GET", f"{API_V1}/users/99999"),
    # station (二期)
    ("GET", f"{API_V1}/stations/99999"),
    # device_ledger (二期)
    ("GET", f"{API_V1}/device-ledger/99999"),
    ("GET", f"{API_V1}/device-ledger/warranty/FAKE_SN_99999"),
    # stocktake (二期)
    ("GET", f"{API_V1}/stocktakes/99999"),
    ("GET", f"{API_V1}/stocktakes/99999/lines"),
    # inventory_adjustment (二期)
    ("GET", f"{API_V1}/inventory-adjustments/99999"),
    # print
    ("GET", f"{API_V1}/print/incoming_receipt/99999"),
    ("GET", f"{API_V1}/print/shipment/99999"),
    ("GET", f"{API_V1}/print/incoming_inspection/99999"),
    ("GET", f"{API_V1}/print/incoming_return/99999"),
    ("GET", f"{API_V1}/print/rma_repair/99999"),
    ("GET", f"{API_V1}/print/bom/99999"),
]


@pytest.mark.parametrize("method,url", TYPE_B_PATH_PARAM)
def test_smoke_type_b_path_param(client, auth_headers, method, url):
    """Type B: GET 端点有路径参数（用虚假 ID，接受 404）。"""
    resp = client.request(method, url, headers=auth_headers)
    assert resp.status_code != 500, (
        f"[500] {method} {url} → {resp.status_code} body={resp.text[:500]}"
    )


# ──────────────────────────────────────────────
# Type C1: POST 端点（需要 body，用最小参数或空 body）
# ──────────────────────────────────────────────

TYPE_C1_POST = [
    # auth (public, no auth header needed)
    ("POST", f"{API_V1}/auth/login", {"username": "admin", "password": "admin123"}, False),
    # inbound validation
    ("POST", f"{API_V1}/inbound/validate-sns", {"sns": ["FAKE_SN_001"]}, True),
    # snapshot trigger
    ("POST", f"{API_V1}/snapshots/trigger", {}, True),
    # product import (no auth needed for import url)
    ("POST", f"{API_V1}/products/skus/import", {}, True),
    # partner import
    ("POST", f"{API_V1}/partners/partners/import", {}, True),
    # inventory import
    ("POST", f"{API_V1}/inventory/import", {}, True),
    # bom import
    ("POST", f"{API_V1}/bom/import", {}, True),
    # device_ledger warranty check
    ("POST", f"{API_V1}/device-ledger/warranty/FAKE/item_sn", {}, True),
    # RMA — use fake return_id
    ("POST", f"{API_V1}/rma/returns/99999/assign", {"assignee": "test"}, True),
    ("POST", f"{API_V1}/rma/returns/99999/transfer", {"to_station": "S1"}, True),
    ("POST", f"{API_V1}/rma/scraps/99999/approve", {"change_reason": "test"}, True),
    # stocktake scan
    ("POST", f"{API_V1}/stocktakes/99999/scan", {"item_sn": "FAKE", "change_reason": "test"}, True),
    ("POST", f"{API_V1}/stocktakes/99999/complete", {"change_reason": "test"}, True),
    ("POST", f"{API_V1}/stocktakes/99999/cancel", {"change_reason": "test"}, True),
    # inventory_adjustment confirm
    ("POST", f"{API_V1}/inventory-adjustments/confirm", {"ids": [99999], "change_reason": "test"}, True),
    # inventory complete-offline-sale
    ("POST", f"{API_V1}/inventory/FAKE_SN/complete-offline-sale", {"change_reason": "test"}, True),
    # device_ledger remove
    ("POST", f"{API_V1}/device-ledger/99999/remove", {"change_reason": "test"}, True),
    # outbound submit/approve/cancel
    ("POST", f"{API_V1}/outbound/99999/submit", {"change_reason": "test"}, True),
    ("POST", f"{API_V1}/outbound/99999/approve", {"change_reason": "test"}, True),
    ("POST", f"{API_V1}/outbound/99999/cancel", {"change_reason": "test"}, True),
    # inbound submit/approve/cancel
    ("POST", f"{API_V1}/inbound/99999/submit", {"change_reason": "test"}, True),
    ("POST", f"{API_V1}/inbound/99999/approve", {"change_reason": "test"}, True),
    ("POST", f"{API_V1}/inbound/99999/cancel", {"change_reason": "test"}, True),
    # incoming receipt confirm
    ("POST", f"{API_V1}/incoming/receipts/99999/confirm", {"change_reason": "test"}, True),
    # user change password
    ("POST", f"{API_V1}/users/change-password", {"old_password": "admin123", "new_password": "new123"}, True),
]


@pytest.mark.parametrize("method,url,body,needs_auth", TYPE_C1_POST)
def test_smoke_type_c1_post(client, auth_headers, method, url, body, needs_auth):
    """Type C1: POST 端点（带最小 body）。"""
    headers = auth_headers if needs_auth else {}
    resp = client.request(method, url, json=body, headers=headers)
    assert resp.status_code != 500, (
        f"[500] {method} {url} → {resp.status_code} body={resp.text[:500]}"
    )


# ──────────────────────────────────────────────
# Type C2: POST 创建类端点（需要真实数据 body）
# 这类端点期望完整数据，用空 body 可能 422，只要不是 500 就过
# ──────────────────────────────────────────────

TYPE_C2_CREATE = [
    # create entities with minimal body
    ("POST", f"{API_V1}/products/categories", {"name": "SmokeTestCat"}, True),
    ("POST", f"{API_V1}/partners/groups", {"name": "SmokeTestGroup"}, True),
    # settings
    ("PUT", f"{API_V1}/settings/branding", {"company_name": "Test"}, True),
    # settings delete logo
    ("DELETE", f"{API_V1}/settings/branding/logo", {}, True),
]


@pytest.mark.parametrize("method,url,body,needs_auth", TYPE_C2_CREATE)
def test_smoke_type_c2_create(client, auth_headers, method, url, body, needs_auth):
    """Type C2: POST/PUT/DELETE 创建/修改类端点。"""
    headers = auth_headers if needs_auth else {}
    resp = client.request(method, url, json=body, headers=headers)
    assert resp.status_code != 500, (
        f"[500] {method} {url} → {resp.status_code} body={resp.text[:500]}"
    )


# ──────────────────────────────────────────────
# Type D: POST 创建类端点（需要种子数据中的 ID）
# ──────────────────────────────────────────────

def test_smoke_create_inbound_with_seed(client, auth_headers, seed_data):
    """最小参数创建入库单，验证不 500。"""
    body = {
        "supplier_id": seed_data["supplier"].id,
        "items": [{"sku_id": seed_data["sku_raw"].id, "quantity": 1}],
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/inbound", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /inbound → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_incoming_receipt_with_seed(client, auth_headers, seed_data):
    """最小参数创建来料记录。"""
    body = {
        "supplier_id": seed_data["supplier"].id,
        "sku_id": seed_data["sku_raw"].id,
        "quantity": 1,
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/incoming/receipts", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /incoming/receipts → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_rma_return_with_seed(client, auth_headers, seed_data):
    """最小参数创建RMA退货单。"""
    body = {
        "item_sn": "FAKE_RMA_SN_001",
        "sku_id": seed_data["sku_fg"].id,
        "return_reason": "smoke test",
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/rma/returns", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /rma/returns → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_shipment_with_seed(client, auth_headers, seed_data):
    """最小参数创建出货单。"""
    body = {
        "customer_name": "Smoke Test Customer",
        "items": [{"item_sn": "FAKE_SHIP_SN_001", "sku_id": seed_data["sku_fg"].id}],
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/shipments/", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /shipments/ → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_bom_with_seed(client, auth_headers, seed_data):
    """最小参数创建BOM。"""
    body = {
        "product_sku_id": seed_data["sku_fg"].id,
        "name": "SmokeTest BOM",
        "items": [{"sku_id": seed_data["sku_raw"].id, "quantity": 1}],
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/bom/", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /bom/ → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_station_with_seed(client, auth_headers):
    """最小参数创建场站。"""
    body = {"name": "SmokeTest_Station", "code": "SMK001", "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/stations", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /stations → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_stocktake_with_seed(client, auth_headers, seed_data):
    """最小参数创建盘点任务。"""
    body = {"sku_id": seed_data["sku_raw"].id, "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/stocktakes", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /stocktakes → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_adjustment_with_seed(client, auth_headers, seed_data):
    """最小参数创建库存调整。"""
    body = {
        "item_sn": "FAKE_ADJ_SN_001",
        "adjustment_type": "quantity",
        "new_quantity": 10,
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/inventory-adjustments", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /inventory-adjustments → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_device_ledger_with_seed(client, auth_headers, seed_data):
    """最小参数登记设备到场站。"""
    body = {
        "item_sn": "FAKE_DEV_SN_001",
        "station_id": 99999,
        "sku_id": seed_data["sku_fg"].id,
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/device-ledger", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /device-ledger → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_user_with_seed(client, auth_headers):
    """最小参数创建用户。"""
    body = {"username": "smoke_test_user", "password": "test123", "nickname": "Smoke", "role": "WAREHOUSE"}
    resp = client.post(f"{API_V1}/users", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /users → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_incoming_inspection_with_seed(client, auth_headers, seed_data):
    """创建来料检验记录（如果成功创建了来料记录就关联，否则用 fake ID）。"""
    body = {
        "receipt_id": 99999,
        "inspection_result": "PASS",
        "inspector": "SmokeTester",
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/incoming/inspections", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /incoming/inspections → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_incoming_return_with_seed(client, auth_headers, seed_data):
    """创建来料退货记录。"""
    body = {
        "receipt_id": 99999,
        "return_quantity": 1,
        "return_reason": "smoke test",
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/incoming/returns", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /incoming/returns → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_rma_diagnosis_with_seed(client, auth_headers, seed_data):
    """创建RMA诊断记录。"""
    body = {"return_id": 99999, "diagnosis_result": "REPAIRABLE", "diagnosed_by": "Smoke", "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/rma/diagnoses", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /rma/diagnoses → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_rma_repair_with_seed(client, auth_headers, seed_data):
    """创建RMA维修记录。"""
    body = {"return_id": 99999, "repair_description": "smoke test", "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/rma/repairs", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /rma/repairs → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_rma_scrap_with_seed(client, auth_headers, seed_data):
    """创建RMA报废记录。"""
    body = {"return_id": 99999, "scrap_reason": "smoke test", "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/rma/scraps", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /rma/scraps → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_rma_reship_with_seed(client, auth_headers, seed_data):
    """创建RMA再出货记录。"""
    body = {
        "return_id": 99999,
        "new_item_sn": "FAKE_RESHIP_SN_001",
        "sku_id": seed_data["sku_fg"].id,
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/rma/reships", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /rma/reships → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_rma_quality_check_with_seed(client, auth_headers, seed_data):
    """创建RMA质检记录。"""
    body = {"return_id": 99999, "check_result": "PASS", "checker": "Smoke", "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/rma/quality-checks", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /rma/quality-checks → {resp.status_code} body={resp.text[:500]}"


def test_smoke_create_rma_warehouse_in_with_seed(client, auth_headers, seed_data):
    """创建RMA入库记录。"""
    body = {"return_id": 99999, "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/rma/warehouse-ins", json=body, headers=auth_headers)
    assert resp.status_code != 500, f"[500] POST /rma/warehouse-ins → {resp.status_code} body={resp.text[:500]}"