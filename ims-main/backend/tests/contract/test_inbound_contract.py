"""
入库管理 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestInboundOrderContract:
    """入库单 API 契约测试。"""

    def test_generate_order_no(self, client, auth_headers):
        """GET /inbound/orders/generate-no 返回入库单号。"""
        res = client.get("/api/v1/inbound/orders/generate-no", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0
        assert res.json()["data"] is not None

    def test_validate_sns(self, client, auth_headers):
        """POST /inbound/orders/validate-sns SN 唯一性校验。"""
        res = client.post("/api/v1/inbound/orders/validate-sns", json={
            "sns": ["SN-UNIQUE-001", "SN-UNIQUE-002"],
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_create_inbound_order_success(self, client, auth_headers, seed_data):
        """POST /inbound/orders 创建采购入库单成功。"""
        payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": seed_data["supplier"].id,
            "remark": "契约测试",
            "lines": [
                {
                    "sku_id": seed_data["sku_raw"].id,
                    "quantity": 10,
                    "unit_price": 150.00,
                }
            ],
        }
        res = client.post("/api/v1/inbound/orders", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["order_no"] is not None
        assert data["data"]["order_no"].startswith("JIN")

    def test_list_inbound_orders(self, client, auth_headers, seed_data):
        """GET /inbound/orders 返回分页结构。"""
        payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": seed_data["supplier"].id,
            "lines": [{"sku_id": seed_data["sku_raw"].id, "quantity": 5, "unit_price": 100.00}],
        }
        client.post("/api/v1/inbound/orders", json=payload, headers=auth_headers)

        res = client.get("/api/v1/inbound/orders", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_get_inbound_order_detail(self, client, auth_headers, seed_data):
        """GET /inbound/orders/{id} 返回入库单详情。"""
        payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": seed_data["supplier"].id,
            "lines": [{"sku_id": seed_data["sku_raw"].id, "quantity": 3, "unit_price": 100.00}],
        }
        create_res = client.post("/api/v1/inbound/orders", json=payload, headers=auth_headers)
        order_id = create_res.json()["data"]["id"]

        res = client.get(f"/api/v1/inbound/orders/{order_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"]["id"] == order_id

    def test_update_inbound_order(self, client, auth_headers, seed_data):
        """PUT /inbound/orders/{id} 更新入库单。"""
        payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": seed_data["supplier"].id,
            "lines": [{"sku_id": seed_data["sku_raw"].id, "quantity": 5, "unit_price": 100.00}],
        }
        create_res = client.post("/api/v1/inbound/orders", json=payload, headers=auth_headers)
        order_id = create_res.json()["data"]["id"]

        update_res = client.put(
            f"/api/v1/inbound/orders/{order_id}",
            json={"remark": "已更新备注"},
            headers=auth_headers,
        )
        assert update_res.status_code == 200

    def test_submit_inbound_order(self, client, auth_headers, seed_data):
        """POST /inbound/orders/{id}/submit 提交待审核。"""
        payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": seed_data["supplier"].id,
            "lines": [{"sku_id": seed_data["sku_raw"].id, "quantity": 5, "unit_price": 100.00}],
        }
        create_res = client.post("/api/v1/inbound/orders", json=payload, headers=auth_headers)
        order_id = create_res.json()["data"]["id"]

        res = client.post(f"/api/v1/inbound/orders/{order_id}/submit", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_approve_inbound_order(self, client, auth_headers, seed_data):
        """POST /inbound/orders/{id}/approve 审核通过。"""
        payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": seed_data["supplier"].id,
            "lines": [{"sku_id": seed_data["sku_raw"].id, "quantity": 5, "unit_price": 100.00}],
        }
        create_res = client.post("/api/v1/inbound/orders", json=payload, headers=auth_headers)
        order_id = create_res.json()["data"]["id"]

        client.post(f"/api/v1/inbound/orders/{order_id}/submit", headers=auth_headers)
        res = client.post(f"/api/v1/inbound/orders/{order_id}/approve", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_cancel_inbound_order(self, client, auth_headers, seed_data):
        """POST /inbound/orders/{id}/cancel 取消入库单。"""
        payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": seed_data["supplier"].id,
            "lines": [{"sku_id": seed_data["sku_raw"].id, "quantity": 5, "unit_price": 100.00}],
        }
        create_res = client.post("/api/v1/inbound/orders", json=payload, headers=auth_headers)
        order_id = create_res.json()["data"]["id"]

        res = client.post(f"/api/v1/inbound/orders/{order_id}/cancel", headers=auth_headers)
        assert res.status_code == 200

    def test_delete_inbound_order(self, client, auth_headers, seed_data):
        """DELETE /inbound/orders/{id} 删除入库单。"""
        payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": seed_data["supplier"].id,
            "lines": [{"sku_id": seed_data["sku_raw"].id, "quantity": 5, "unit_price": 100.00}],
        }
        create_res = client.post("/api/v1/inbound/orders", json=payload, headers=auth_headers)
        order_id = create_res.json()["data"]["id"]

        delete_res = client.delete(f"/api/v1/inbound/orders/{order_id}", headers=auth_headers)
        assert delete_res.status_code == 200

    def test_create_inbound_order_validates_fields(self, client, auth_headers):
        """POST /inbound/orders 缺少必填字段返回 422。"""
        res = client.post("/api/v1/inbound/orders", json={}, headers=auth_headers)
        assert res.status_code == 422

    def test_export_inbound_xlsx(self, client, auth_headers):
        """GET /inbound/orders/export 返回 Excel。"""
        res = client.get("/api/v1/inbound/orders/export", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_template_download(self, client, auth_headers):
        """GET /inbound/orders/template 返回模板。"""
        res = client.get("/api/v1/inbound/orders/template", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")