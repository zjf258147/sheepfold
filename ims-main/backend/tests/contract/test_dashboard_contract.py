"""
仪表盘 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestDashboardContract:
    """仪表盘 API 契约测试。"""

    def test_pending_audit_structure(self, client, auth_headers):
        """GET /dashboard/pending-audit 返回待审核统计。"""
        res = client.get("/api/v1/dashboard/pending-audit", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "inbound_pending" in data["data"]
        assert "outbound_pending" in data["data"]

    def test_stock_summary_structure(self, client, auth_headers):
        """GET /dashboard/stock-summary 返回库存统计。"""
        res = client.get("/api/v1/dashboard/stock-summary", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]

    def test_partner_summary_structure(self, client, auth_headers):
        """GET /dashboard/partner-summary 返回关联单位统计。"""
        res = client.get("/api/v1/dashboard/partner-summary", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]

    def test_partner_summary_with_sku_ids(self, client, auth_headers, seed_data):
        """GET /dashboard/partner-summary 支持按 SKU 筛选。"""
        res = client.get(
            f"/api/v1/dashboard/partner-summary?sku_ids={seed_data['sku_fg'].id}",
            headers=auth_headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]