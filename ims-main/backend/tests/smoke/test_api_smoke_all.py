"""
API 全量冒烟测试 — 四层断言，禁止错误路由和假 404 被计为通过。

四层断言：
  层1 路由存在  → 必须返回 200/201（404 表示路由未注册）
  层2 路径参数  → 允许 404（实体不存在），但禁止 HTML 响应（HTML=路由错误）
  层3 参数校验  → 允许预期 422
  层4 业务逻辑  → 必须返回 200/201/400/422，验证响应 JSON 结构

运行：
  cd backend && uv run pytest tests/smoke/ -v --tb=short
"""

import json

import pytest

API_V1 = "/api/v1"

# ──────────────────────────────────────────────
# 辅助函数
# ──────────────────────────────────────────────

def _is_json_response(resp):
    content_type = resp.headers.get("content-type", "").lower()
    return "application/json" in content_type


def _assert_route_exists(resp, method, url):
    assert resp.status_code in (200, 201), (
        f"[LAYER1] 路由未注册 {method} {url} → {resp.status_code} "
        f"body={resp.text[:300]}"
    )


def _assert_not_server_error(resp, method, url):
    assert resp.status_code < 500, (
        f"[500] {method} {url} → {resp.status_code} body={resp.text[:500]}"
    )
    assert _is_json_response(resp), (
        f"[LAYER2] 响应非 JSON（路由错误或模板渲染） {method} {url} → "
        f"status={resp.status_code} content_type={resp.headers.get('content-type', '?')} "
        f"body={resp.text[:300]}"
    )


def _assert_business_response(resp, method, url):
    assert resp.status_code in (200, 201, 400, 422), (
        f"[LAYER4] 业务异常 {method} {url} → {resp.status_code} body={resp.text[:500]}"
    )
    assert _is_json_response(resp), (
        f"[LAYER4] 响应非 JSON {method} {url} → body={resp.text[:300]}"
    )
    if resp.status_code in (200, 201):
        try:
            data = resp.json()
        except json.JSONDecodeError:
            pytest.fail(f"[LAYER4] 响应体非合法 JSON {method} {url} → {resp.text[:200]}")
        assert isinstance(data, dict), (
            f"[LAYER4] 响应体非 dict {method} {url} → {resp.text[:200]}"
        )


def _assert_file_response(resp, method, url):
    """文件下载端点，允许非 JSON 响应（如 docx 文件流）。"""
    assert resp.status_code in (200, 404, 422), (
        f"[LAYER2-FILE] {method} {url} → {resp.status_code} body={resp.text[:300]}"
    )


# ──────────────────────────────────────────────
# 层1 路由存在: GET 端点（无路径参数，admin 鉴权）
# 必须返回 200。404 = 路由未注册，直接 FAIL。
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
    # inventory (prefix: /inventory/items)
    ("GET", f"{API_V1}/inventory/items"),
    ("GET", f"{API_V1}/inventory/items/cursor"),
    ("GET", f"{API_V1}/inventory/items/available"),
    ("GET", f"{API_V1}/inventory/items/export"),
    ("GET", f"{API_V1}/inventory/items/template"),
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
    # inbound (prefix: /inbound/orders)
    ("GET", f"{API_V1}/inbound/orders/generate-no"),
    ("GET", f"{API_V1}/inbound/orders"),
    # outbound (prefix: /outbound/orders)
    ("GET", f"{API_V1}/outbound/orders/generate-no"),
    ("GET", f"{API_V1}/outbound/orders"),
    # snapshot
    ("GET", f"{API_V1}/snapshots"),
    ("GET", f"{API_V1}/snapshots/dates"),
    # audit
    ("GET", f"{API_V1}/audit-logs"),
    # settings
    ("GET", f"{API_V1}/settings/branding"),
    # docs
    ("GET", f"{API_V1}/docs"),
    # incoming
    ("GET", f"{API_V1}/incoming/receipts"),
    ("GET", f"{API_V1}/incoming/receipts/export"),
    ("GET", f"{API_V1}/incoming/receipts/template"),
    # rma
    ("GET", f"{API_V1}/rma/returns"),
    # shipment (prefix: /shipment)
    ("GET", f"{API_V1}/shipment/list"),
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
    # adjustments (二期, prefix: /adjustments)
    ("GET", f"{API_V1}/adjustments"),
]

# 层1-A2: GET 端点需要 query 参数才能正确响应
TYPE_A1_WITH_QUERY = [
    # snapshot (需要 query 参数)
    ("GET", f"{API_V1}/snapshots/daily-ledger", {"date_from": "2025-01-01", "date_to": "2025-12-31"}),
    ("GET", f"{API_V1}/snapshots/daily-ledger/export", {"date_from": "2025-01-01", "date_to": "2025-12-31"}),
    ("GET", f"{API_V1}/snapshots/ledger-summary/export", {"date_from": "2025-01-01", "date_to": "2025-12-31"}),
    ("GET", f"{API_V1}/snapshots/items", {"snapshot_date": "2025-01-01"}),
    ("GET", f"{API_V1}/snapshots/items/export", {"snapshot_date": "2025-01-01"}),
]


@pytest.mark.parametrize("method,url", TYPE_A_NO_PARAM)
def test_layer1_route_exists(client, auth_headers, method, url):
    """层1 路由存在: GET 端点无需路径参数，admin 鉴权后必须返回 200。"""
    resp = client.request(method, url, headers=auth_headers)
    _assert_route_exists(resp, method, url)


@pytest.mark.parametrize("method,url,params", TYPE_A1_WITH_QUERY)
def test_layer1a_query_params(client, auth_headers, method, url, params):
    """层1-A2: GET 端点需要 query 参数。"""
    resp = client.request(method, url, headers=auth_headers, params=params)
    _assert_route_exists(resp, method, url)


# ──────────────────────────────────────────────
# 层2 路径参数: GET 端点（有路径参数，使用虚假 ID）
# 允许 404（实体不存在），但响应必须是 JSON。
# HTML 响应 = 路由未注册，直接 FAIL。
# ──────────────────────────────────────────────

TYPE_B_PATH_PARAM = [
    # inventory
    ("GET", f"{API_V1}/inventory/items/FAKE_SN_99999"),
    ("GET", f"{API_V1}/inventory/items/FAKE_SN_99999/history"),
    # product
    ("GET", f"{API_V1}/products/categories/99999"),
    ("GET", f"{API_V1}/products/skus/99999"),
    # partner
    ("GET", f"{API_V1}/partners/groups/99999"),
    ("GET", f"{API_V1}/partners/99999"),
    # customer
    ("GET", f"{API_V1}/customers/99999"),
    # inbound
    ("GET", f"{API_V1}/inbound/orders/99999"),
    # outbound
    ("GET", f"{API_V1}/outbound/orders/99999"),
    # shipment
    ("GET", f"{API_V1}/shipment/99999"),
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
    # adjustments (二期)
    ("GET", f"{API_V1}/adjustments/99999"),
    # print
    ("GET", f"{API_V1}/print/incoming_receipt/99999"),
    ("GET", f"{API_V1}/print/shipment/99999"),
    ("GET", f"{API_V1}/print/incoming_inspection/99999"),
    ("GET", f"{API_V1}/print/incoming_return/99999"),
    ("GET", f"{API_V1}/print/rma_repair/99999"),
    ("GET", f"{API_V1}/print/bom/99999"),
]

# 层2-B2: 路径参数端点返回文件（非 JSON），如文档下载
TYPE_B_FILE_DOWNLOAD = [
    ("GET", f"{API_V1}/docs/download/spec"),
]

# 层2-B3: GET 端点需要 query 参数且依赖实体存在（允许 400 业务错误）
TYPE_B_QUERY_PARAM = [
    ("GET", f"{API_V1}/inbound/orders/returnable-items", {"outbound_order_id": 1, "stock_condition": "良品"}),
]


@pytest.mark.parametrize("method,url", TYPE_B_PATH_PARAM)
def test_layer2_path_param(client, auth_headers, method, url):
    """层2 路径参数: GET 端点有路径参数（用虚假 ID，允许 404），但禁止非 JSON 响应。"""
    resp = client.request(method, url, headers=auth_headers)
    _assert_not_server_error(resp, method, url)


@pytest.mark.parametrize("method,url", TYPE_B_FILE_DOWNLOAD)
def test_layer2b_file_download(client, auth_headers, method, url):
    """层2-B2: 文件下载端点，允许非 JSON 响应（二进制流）。"""
    resp = client.request(method, url, headers=auth_headers)
    _assert_file_response(resp, method, url)


@pytest.mark.parametrize("method,url,params", TYPE_B_QUERY_PARAM)
def test_layer2c_query_deps(client, auth_headers, method, url, params):
    """层2-B3: GET 端点需 query 参数且依赖实体存在（允许 400 业务错误）。"""
    resp = client.request(method, url, headers=auth_headers, params=params)
    _assert_not_server_error(resp, method, url)


# ──────────────────────────────────────────────
# 层3 参数校验: POST 端点（需要 body，用最小参数或空 body）
# 允许 422，但禁止 500 和非 JSON 响应。
# ──────────────────────────────────────────────

TYPE_C1_POST = [
    # auth (public, no auth header needed)
    ("POST", f"{API_V1}/auth/login", {"username": "admin", "password": "admin123"}, False),
    # inbound validation
    ("POST", f"{API_V1}/inbound/orders/validate-sns", {"sns": ["FAKE_SN_001"]}, True),
    # snapshot trigger
    ("POST", f"{API_V1}/snapshots/trigger", {}, True),
    # product import
    ("POST", f"{API_V1}/products/skus/import", {}, True),
    # partner import
    ("POST", f"{API_V1}/partners/partners/import", {}, True),
    # inventory import
    ("POST", f"{API_V1}/inventory/items/import", {}, True),
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
    # adjustments confirm
    ("POST", f"{API_V1}/adjustments/confirm", {"ids": [99999], "change_reason": "test"}, True),
    # inventory complete-offline-sale
    ("POST", f"{API_V1}/inventory/items/FAKE_SN/complete-offline-sale", {"change_reason": "test"}, True),
    # device_ledger remove
    ("POST", f"{API_V1}/device-ledger/99999/remove", {"change_reason": "test"}, True),
    # outbound submit/approve/cancel
    ("POST", f"{API_V1}/outbound/orders/99999/submit", {"change_reason": "test"}, True),
    ("POST", f"{API_V1}/outbound/orders/99999/approve", {"change_reason": "test"}, True),
    ("POST", f"{API_V1}/outbound/orders/99999/cancel", {"change_reason": "test"}, True),
    # inbound submit/approve/cancel
    ("POST", f"{API_V1}/inbound/orders/99999/submit", {"change_reason": "test"}, True),
    ("POST", f"{API_V1}/inbound/orders/99999/approve", {"change_reason": "test"}, True),
    ("POST", f"{API_V1}/inbound/orders/99999/cancel", {"change_reason": "test"}, True),
    # incoming receipt confirm
    ("POST", f"{API_V1}/incoming/receipts/99999/confirm", {"change_reason": "test"}, True),
    # user change password
    ("POST", f"{API_V1}/users/change-password", {"old_password": "admin123", "new_password": "new123"}, True),
    # settings test-connection
    ("POST", f"{API_V1}/settings/test-connection", {"url": "http://127.0.0.1:9999"}, True),
]


@pytest.mark.parametrize("method,url,body,needs_auth", TYPE_C1_POST)
def test_layer3_param_check(client, auth_headers, method, url, body, needs_auth):
    """层3 参数校验: POST 端点（带最小 body），允许 422，禁止 500 和 HTML 响应。"""
    headers = auth_headers if needs_auth else {}
    resp = client.request(method, url, json=body, headers=headers)
    _assert_not_server_error(resp, method, url)


# ──────────────────────────────────────────────
# 层4 业务逻辑: POST/PUT/DELETE 端点
# 必须返回 200/201/400/422，验证响应为合法 JSON dict。
# ──────────────────────────────────────────────

TYPE_C2_CREATE = [
    ("POST", f"{API_V1}/products/categories", {"name": "SmokeTestCat"}, True),
    ("POST", f"{API_V1}/partners/groups", {"name": "SmokeTestGroup"}, True),
    ("PUT", f"{API_V1}/settings/branding", {"company_name": "Test"}, True),
    ("DELETE", f"{API_V1}/settings/branding/logo", {}, True),
]


@pytest.mark.parametrize("method,url,body,needs_auth", TYPE_C2_CREATE)
def test_layer4_create_modify(client, auth_headers, method, url, body, needs_auth):
    """层4 业务逻辑: POST/PUT/DELETE 端点，验证 JSON 响应结构。"""
    headers = auth_headers if needs_auth else {}
    resp = client.request(method, url, json=body, headers=headers)
    _assert_business_response(resp, method, url)


# ──────────────────────────────────────────────
# 层4 业务逻辑: 创建类端点（依赖种子数据）
# ──────────────────────────────────────────────

def test_smoke_create_inbound_with_seed(client, auth_headers, seed_data):
    """最小参数创建入库单。"""
    body = {
        "supplier_id": seed_data["supplier"].id,
        "items": [{"sku_id": seed_data["sku_raw"].id, "quantity": 1}],
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/inbound/orders", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/inbound/orders")


def test_smoke_create_incoming_receipt_with_seed(client, auth_headers, seed_data):
    """最小参数创建来料记录。"""
    body = {
        "supplier_id": seed_data["supplier"].id,
        "sku_id": seed_data["sku_raw"].id,
        "quantity": 1,
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/incoming/receipts", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/incoming/receipts")


def test_smoke_create_rma_return_with_seed(client, auth_headers, seed_data):
    """最小参数创建RMA退货单。"""
    body = {
        "item_sn": "FAKE_RMA_SN_001",
        "sku_id": seed_data["sku_fg"].id,
        "return_reason": "smoke test",
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/rma/returns", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/rma/returns")


def test_smoke_create_shipment_with_seed(client, auth_headers, seed_data):
    """最小参数创建出货单。"""
    body = {
        "customer_name": "Smoke Test Customer",
        "items": [{"item_sn": "FAKE_SHIP_SN_001", "sku_id": seed_data["sku_fg"].id}],
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/shipment/", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/shipment/")


def test_smoke_create_bom_with_seed(client, auth_headers, seed_data):
    """最小参数创建BOM。"""
    body = {
        "product_sku_id": seed_data["sku_fg"].id,
        "name": "SmokeTest BOM",
        "items": [{"sku_id": seed_data["sku_raw"].id, "quantity": 1}],
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/bom/", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/bom/")


def test_smoke_create_station_with_seed(client, auth_headers):
    """最小参数创建场站。"""
    body = {"name": "SmokeTest_Station", "code": "SMK001", "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/stations", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/stations")


def test_smoke_create_stocktake_with_seed(client, auth_headers, seed_data):
    """最小参数创建盘点任务。"""
    body = {"sku_id": seed_data["sku_raw"].id, "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/stocktakes", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/stocktakes")


def test_smoke_create_adjustment_with_seed(client, auth_headers, seed_data):
    """最小参数创建库存调整（prefix: /adjustments）。"""
    body = {
        "item_sn": "FAKE_ADJ_SN_001",
        "adjustment_type": "quantity",
        "new_quantity": 10,
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/adjustments", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/adjustments")


def test_smoke_create_device_ledger_with_seed(client, auth_headers, seed_data):
    """最小参数登记设备到场站。"""
    body = {
        "item_sn": "FAKE_DEV_SN_001",
        "station_id": 99999,
        "sku_id": seed_data["sku_fg"].id,
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/device-ledger", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/device-ledger")


def test_smoke_create_user_with_seed(client, auth_headers):
    """最小参数创建用户。"""
    body = {"username": "smoke_test_user", "password": "test123", "nickname": "Smoke", "role": "WAREHOUSE"}
    resp = client.post(f"{API_V1}/users", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/users")


def test_smoke_create_incoming_inspection_with_seed(client, auth_headers, seed_data):
    """创建来料检验记录。"""
    body = {
        "receipt_id": 99999,
        "inspection_result": "PASS",
        "inspector": "SmokeTester",
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/incoming/inspections", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/incoming/inspections")


def test_smoke_create_incoming_return_with_seed(client, auth_headers, seed_data):
    """创建来料退货记录。"""
    body = {
        "receipt_id": 99999,
        "return_quantity": 1,
        "return_reason": "smoke test",
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/incoming/returns", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/incoming/returns")


def test_smoke_create_rma_diagnosis_with_seed(client, auth_headers, seed_data):
    """创建RMA诊断记录。"""
    body = {"return_id": 99999, "diagnosis_result": "REPAIRABLE", "diagnosed_by": "Smoke", "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/rma/diagnoses", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/rma/diagnoses")


def test_smoke_create_rma_repair_with_seed(client, auth_headers, seed_data):
    """创建RMA维修记录。"""
    body = {"return_id": 99999, "repair_description": "smoke test", "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/rma/repairs", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/rma/repairs")


def test_smoke_create_rma_scrap_with_seed(client, auth_headers, seed_data):
    """创建RMA报废记录。"""
    body = {"return_id": 99999, "scrap_reason": "smoke test", "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/rma/scraps", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/rma/scraps")


def test_smoke_create_rma_reship_with_seed(client, auth_headers, seed_data):
    """创建RMA再出货记录。"""
    body = {
        "return_id": 99999,
        "new_item_sn": "FAKE_RESHIP_SN_001",
        "sku_id": seed_data["sku_fg"].id,
        "change_reason": "smoke test",
    }
    resp = client.post(f"{API_V1}/rma/reships", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/rma/reships")


def test_smoke_create_rma_quality_check_with_seed(client, auth_headers, seed_data):
    """创建RMA质检记录。"""
    body = {"return_id": 99999, "check_result": "PASS", "checker": "Smoke", "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/rma/quality-checks", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/rma/quality-checks")


def test_smoke_create_rma_warehouse_in_with_seed(client, auth_headers, seed_data):
    """创建RMA入库记录。"""
    body = {"return_id": 99999, "change_reason": "smoke test"}
    resp = client.post(f"{API_V1}/rma/warehouse-ins", json=body, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/rma/warehouse-ins")


# ──────────────────────────────────────────────
# 层4 业务逻辑: Logo 上传（multipart）
# ──────────────────────────────────────────────

def test_smoke_upload_logo(client, auth_headers):
    """上传 Logo 图片，验证返回 200 且响应为合法 JSON。"""
    import io

    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00'
        b'\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    files = {"file": ("test-logo.png", io.BytesIO(png_bytes), "image/png")}
    resp = client.post(f"{API_V1}/settings/branding/logo", files=files, headers=auth_headers)
    _assert_business_response(resp, "POST", f"{API_V1}/settings/branding/logo")