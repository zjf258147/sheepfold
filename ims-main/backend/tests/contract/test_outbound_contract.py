"""
出库管理 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestOutboundOrderContract:
    """出库单 API 契约测试。"""

    def test_generate_order_no(self, client, auth_headers):
        """GET /outbound/orders/generate-no 返回出库单号。"""
        res = client.get("/api/v1/outbound/orders/generate-no", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0
        assert res.json()["data"] is not None

    def test_list_outbound_orders(self, client, auth_headers):
        """GET /outbound/orders 返回分页结构。"""
        res = client.get("/api/v1/outbound/orders", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_create_outbound_order_validates_fields(self, client, auth_headers):
        """POST /outbound/orders 缺少必填字段返回 422。"""
        res = client.post("/api/v1/outbound/orders", json={}, headers=auth_headers)
        assert res.status_code == 422

    def test_export_outbound_xlsx(self, client, auth_headers):
        """GET /outbound/orders/export 返回 Excel。"""
        res = client.get("/api/v1/outbound/orders/export", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_template_download(self, client, auth_headers):
        """GET /outbound/orders/template 返回模板。"""
        res = client.get("/api/v1/outbound/orders/template", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")