"""
库存管理 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestInventoryContract:
    """库存单品 API 契约测试。"""

    def test_list_items_returns_page_result(self, client, auth_headers):
        """GET /inventory/items 返回分页结构。"""
        res = client.get("/api/v1/inventory/items", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert "page" in data["data"]
        assert "page_size" in data["data"]

    def test_list_items_with_filters(self, client, auth_headers, seed_data):
        """GET /inventory/items 支持按 SKU 筛选。"""
        res = client.get(
            f"/api/v1/inventory/items?sku_id={seed_data['sku_fg'].id}",
            headers=auth_headers,
        )
        assert res.status_code == 200

    def test_cursor_pagination(self, client, auth_headers):
        """GET /inventory/items/cursor 游标分页。"""
        res = client.get("/api/v1/inventory/items/cursor", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "has_more" in data["data"]

    def test_available_items(self, client, auth_headers):
        """GET /inventory/items/available 可出库单品。"""
        res = client.get("/api/v1/inventory/items/available", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_export_inventory_xlsx(self, client, auth_headers):
        """GET /inventory/items/export 返回 Excel。"""
        res = client.get("/api/v1/inventory/items/export", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_template_download(self, client, auth_headers):
        """GET /inventory/items/template 返回模板。"""
        res = client.get("/api/v1/inventory/items/template", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_get_item_not_found(self, client, auth_headers):
        """GET /inventory/items/{sn} 单品不存在返回 404。"""
        res = client.get("/api/v1/inventory/items/SN-NOT-EXIST", headers=auth_headers)
        assert res.status_code == 404

    def test_item_history_not_found(self, client, auth_headers):
        """GET /inventory/items/{sn}/history 单品不存在返回 404。"""
        res = client.get("/api/v1/inventory/items/SN-NOT-EXIST/history", headers=auth_headers)
        assert res.status_code == 404