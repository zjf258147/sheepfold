"""
客户 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestCustomerContract:
    """客户 API 契约测试。"""

    def test_list_customers_returns_page_result(self, client, auth_headers):
        """GET /customers 返回分页结构。"""
        res = client.get("/api/v1/customers", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_list_customers_with_keyword(self, client, auth_headers):
        """GET /customers 支持关键字搜索。"""
        res = client.get("/api/v1/customers?keyword=测试", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0

    def test_list_customers_pagination(self, client, auth_headers):
        """GET /customers 分页参数生效。"""
        res = client.get("/api/v1/customers?page=1&page_size=5", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["data"]["page"] == 1
        assert data["data"]["page_size"] == 5
        assert len(data["data"]["items"]) <= 5