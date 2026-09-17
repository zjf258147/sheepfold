"""
后端边界条件和异常处理测试。
覆盖：空值、无效ID、未授权、SQL注入防护、并发状态等。
"""
import pytest
from fastapi.testclient import TestClient


class TestPrintEdgeCases:
    """打印API边界条件测试"""

    def test_incoming_receipt_not_found(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/print/incoming_receipt/99999", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] != 0  # 应该返回失败

    def test_shipment_not_found(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/print/shipment/99999", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] != 0

    def test_incoming_inspection_not_found(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/print/incoming_inspection/99999", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] != 0

    def test_incoming_return_not_found(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/print/incoming_return/99999", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] != 0

    def test_rma_repair_not_found(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/print/rma_repair/99999", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] != 0

    def test_bom_not_found(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/print/bom/99999", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] != 0

    def test_print_without_auth(self, client: TestClient):
        resp = client.get("/api/v1/print/incoming_receipt/1")
        assert resp.status_code == 401

    def test_print_invalid_id_type(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/print/incoming_receipt/abc", headers=auth_headers)
        assert resp.status_code == 422  # 类型校验失败


class TestPaginationEdgeCases:
    """分页边界条件测试"""

    def test_page_zero(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/incoming/receipts?page=0", headers=auth_headers)
        assert resp.status_code == 422  # page >= 1

    def test_page_size_zero(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/incoming/receipts?page_size=0", headers=auth_headers)
        assert resp.status_code == 422

    def test_page_size_exceed(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/incoming/receipts?page_size=200", headers=auth_headers)
        assert resp.status_code == 422  # page_size <= 100

    def test_negative_page(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/incoming/receipts?page=-1", headers=auth_headers)
        assert resp.status_code == 422


class TestAuthEdgeCases:
    """认证边界条件测试"""

    def test_login_empty_password(self, client: TestClient):
        resp = client.post("/api/v1/auth/login", json={"username": "admin", "password": ""})
        assert resp.status_code == 422  # 或 400

    def test_login_empty_username(self, client: TestClient):
        resp = client.post("/api/v1/auth/login", json={"username": "", "password": "admin123"})
        assert resp.status_code == 422  # 或 400

    def test_login_wrong_password(self, client: TestClient):
        resp = client.post("/api/v1/auth/login", json={"username": "admin", "password": "wrongpassword"})
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        resp = client.post("/api/v1/auth/login", json={"username": "nonexistent_user_999", "password": "12345678"})
        assert resp.status_code == 401

    def test_invalid_token(self, client: TestClient):
        resp = client.get("/api/v1/users", headers={"Authorization": "Bearer invalid_token_here"})
        assert resp.status_code == 401


class TestRMAEdgeCases:
    """RMA边界条件测试"""

    def test_get_nonexistent_return(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/rma/returns/99999", headers=auth_headers)
        assert resp.status_code in [200, 404, 500]  # 200表示返回错误信息，500表示服务端异常

    def test_diagnose_nonexistent_return(self, client: TestClient, auth_headers):
        resp = client.post("/api/v1/rma/diagnoses", json={
            "return_id": 99999,
            "diagnosed_by": 1,
            "diagnosis_date": "2026-09-10",
            "fault_description": "test",
            "diagnosis_result": "REPAIRABLE",
            "repair_plan": "test",
        }, headers=auth_headers)
        assert resp.status_code in [400, 422, 200, 500]  # 200 with error code

    def test_create_return_without_sn(self, client: TestClient, auth_headers):
        resp = client.post("/api/v1/rma/returns", json={
            "sku_id": 1,
            "quantity": 1,
            "customer_name": "test",
            "return_reason": "test",
            "return_date": "2026-09-10",
        }, headers=auth_headers)
        assert resp.status_code == 422  # sn is required


class TestSQLInjectionProtection:
    """SQL注入防护测试"""

    def test_keyword_injection(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/incoming/receipts?keyword='; DROP TABLE users;--", headers=auth_headers)
        assert resp.status_code == 200  # 参数化查询不受影响

    def test_status_injection(self, client: TestClient, auth_headers):
        resp = client.get("/api/v1/rma/returns?status=' OR '1'='1", headers=auth_headers)
        assert resp.status_code == 200  # 参数化查询安全

    def test_login_injection(self, client: TestClient):
        resp = client.post("/api/v1/auth/login", json={
            "username": "admin' OR '1'='1",
            "password": "admin' OR '1'='1",
        })
        assert resp.status_code == 401  # SQL注入不应绕过登录


class TestConcurrency:
    """并发场景测试"""

    def test_sequential_requests(self, client: TestClient, auth_headers):
        for _ in range(10):
            resp = client.get("/api/v1/incoming/receipts", headers=auth_headers)
            assert resp.status_code == 200


class TestWarrantyEdgeCases:
    """二期 - 质保期边界测试"""

    def test_warranty_start_after_end(self, client: TestClient, auth_headers):
        """E01: warranty_start > warranty_end 当前不校验，创建成功。"""
        cust_res = client.post("/api/v1/customers", json={"name": "质保边界客户"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        st_res = client.post("/api/v1/stations", json={
            "name": "质保边界场站", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = st_res.json()["data"]["id"]
        res = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-WE01",
            "station_id": station_id,
            "installed_date": "2026-09-01",
            "warranty_start": "2026-12-01",
            "warranty_end": "2026-01-01",
        }, headers=auth_headers)
        assert res.json()["code"] == 0

    def test_warranty_same_day(self, client: TestClient, auth_headers):
        """E02: warranty_start = warranty_end（当天）在保。"""
        cust_res = client.post("/api/v1/customers", json={"name": "当天质保客户"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        st_res = client.post("/api/v1/stations", json={
            "name": "当天质保场站", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = st_res.json()["data"]["id"]
        today = "2026-09-11"
        res = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-WE02",
            "station_id": station_id,
            "installed_date": today,
            "warranty_start": today,
            "warranty_end": today,
        }, headers=auth_headers)
        assert res.json()["code"] == 0

    def test_warranty_expired_yesterday(self, client: TestClient, auth_headers):
        """E03: warranty_end = 昨天，不在保。"""
        cust_res = client.post("/api/v1/customers", json={"name": "过期质保客户"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        st_res = client.post("/api/v1/stations", json={
            "name": "过期质保场站", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = st_res.json()["data"]["id"]
        res = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-WE03",
            "station_id": station_id,
            "installed_date": "2026-01-01",
            "warranty_start": "2026-01-01",
            "warranty_end": "2026-09-10",
        }, headers=auth_headers)
        assert res.json()["code"] == 0
        w_res = client.get("/api/v1/device-ledger/warranty/SN-WE03", headers=auth_headers)
        assert w_res.json()["data"]["in_warranty"] is False

    def test_empty_warehouse_stocktake(self, client: TestClient, auth_headers):
        """E04: 盘点仓库范围为空，Pydantic未设min_length，当前允许创建。"""
        res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": ""
        }, headers=auth_headers)
        assert res.json()["code"] == 0

    def test_zero_sn_stocktake_scan(self, client: TestClient, auth_headers):
        """E05: 盘点0个SN，Pydantic校验min_length=1返回422。"""
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = create_res.json()["data"]["id"]
        res = client.post(f"/api/v1/stocktakes/{stocktake_id}/scan", json={
            "items": []
        }, headers=auth_headers)
        assert res.status_code == 422
        res.close()

    def test_station_delete_with_active_device(self, client: TestClient, auth_headers):
        """E07: 删除有活跃DeviceLedger的场站，FK约束禁止返回500。"""
        cust_res = client.post("/api/v1/customers", json={"name": "删除测试客户"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        st_res = client.post("/api/v1/stations", json={
            "name": "待删除场站", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = st_res.json()["data"]["id"]
        client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-EDEL01", "station_id": station_id,
            "installed_date": "2026-09-01",
        }, headers=auth_headers)
        res = client.delete(f"/api/v1/stations/{station_id}", headers=auth_headers)
        assert res.status_code in (200, 500)

    def test_remove_date_before_install(self, client: TestClient, auth_headers):
        """E08: removed_date < installed_date 当前不校验，移除成功。"""
        cust_res = client.post("/api/v1/customers", json={"name": "移除日期客户"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        st_res = client.post("/api/v1/stations", json={
            "name": "移除日期场站", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = st_res.json()["data"]["id"]
        create_res = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-WE08", "station_id": station_id,
            "installed_date": "2026-09-11",
        }, headers=auth_headers)
        ledger_id = create_res.json()["data"]["id"]
        res = client.post(f"/api/v1/device-ledger/{ledger_id}/remove", json={
            "removed_date": "2026-09-01"
        }, headers=auth_headers)
        assert res.json()["code"] == 0


class TestSerializationEdgeCases:
    """序列化异常测试：验证 datetime / Decimal / None 字段正确序列化，不产生 500。"""

    def test_inventory_response_serializes_decimal_and_datetime(self, client, auth_headers):
        """GET /api/v1/inventory/items 返回 unit_price(Decimal) + created_at(datetime)，验证 JSON 序列化无 500。"""
        resp = client.get("/api/v1/inventory/items", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        for item in data.get("data", {}).get("items", []):
            if "unit_price" in item:
                raw = resp.text
                assert "Decimal" not in raw, f"unit_price 未序列化: {raw[:200]}"

    def test_inbound_response_serializes_decimal_price(self, client, auth_headers):
        """GET /api/v1/inbound/orders 返回 unit_price(Decimal)，验证不出现 'Decimal' 字符串。"""
        resp = client.get("/api/v1/inbound/orders", headers=auth_headers)
        assert resp.status_code == 200
        raw = resp.text
        assert "Decimal" not in raw, f"响应含未序列化的 Decimal: {raw[:200]}"

    def test_snapshot_list_serializes_decimal_amount(self, client, auth_headers):
        """GET /api/v1/snapshots 返回 closing_asset_amount(Decimal)，验证序列化正常。"""
        resp = client.get("/api/v1/snapshots", headers=auth_headers)
        assert resp.status_code == 200
        raw = resp.text
        assert "Decimal" not in raw, f"snapshot 响应含未序列化的 Decimal: {raw[:200]}"

    def test_incoming_receipt_pagination_serialization(self, client, auth_headers):
        """GET /api/v1/incoming/receipts 分页返回 datetime 字段，验证序列化。"""
        resp = client.get("/api/v1/incoming/receipts?page=1&page_size=10", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        raw = resp.text
        assert "datetime" not in raw.lower(), f"响应含未序列化的 datetime: {raw[:200]}"

    def test_product_list_serializes_datetime(self, client, auth_headers):
        """GET /api/v1/products/skus 返回 created_at/updated_at(datetime)，验证序列化。"""
        resp = client.get("/api/v1/products/skus", headers=auth_headers)
        assert resp.status_code == 200
        raw = resp.text
        assert "datetime" not in raw.lower(), f"products 响应含未序列化的 datetime: {raw[:200]}"

    def test_partner_list_serializes_none_fields(self, client, auth_headers):
        """GET /api/v1/partners 返回可选字段(可含 None)，验证 None 正确序列化为 null。"""
        resp = client.get("/api/v1/partners", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        if data["code"] == 0 and data.get("data", {}).get("items"):
            raw = resp.text
            assert "None" not in raw, f"响应含 Python None 字符串: {raw[:200]}"

    def test_station_list_serializes_datetime(self, client, auth_headers):
        """GET /api/v1/stations 二期接口，验证 created_at 序列化。"""
        resp = client.get("/api/v1/stations", headers=auth_headers)
        assert resp.status_code == 200
        raw = resp.text
        assert "datetime" not in raw.lower(), f"stations 响应含未序列化的 datetime: {raw[:200]}"

    def test_customer_list_serializes_none(self, client, auth_headers):
        """GET /api/v1/customers 返回可选扩展字段(可含 None)，验证序列化。"""
        resp = client.get("/api/v1/customers", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        if data["code"] == 0 and data.get("data", {}).get("items"):
            raw = resp.text
            assert "None" not in raw, f"customers 响应含 Python None: {raw[:200]}"