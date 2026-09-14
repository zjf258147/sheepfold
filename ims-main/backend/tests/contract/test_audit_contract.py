"""
审计日志 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
需要管理员权限。
"""

import pytest


class TestAuditLogContract:
    """审计日志 API 契约测试。"""

    def test_list_audit_logs_returns_page_result(self, client, auth_headers):
        """GET /audit-logs 返回分页结构。"""
        res = client.get("/api/v1/audit-logs", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_list_audit_logs_with_module_filter(self, client, auth_headers):
        """GET /audit-logs 支持按模块筛选。"""
        res = client.get("/api/v1/audit-logs?module=auth", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0

    def test_list_audit_logs_with_action_filter(self, client, auth_headers):
        """GET /audit-logs 支持按操作筛选。"""
        res = client.get("/api/v1/audit-logs?action=LOGIN", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0

    def test_list_audit_logs_with_keyword(self, client, auth_headers):
        """GET /audit-logs 支持关键字搜索。"""
        res = client.get("/api/v1/audit-logs?keyword=admin", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0

    def test_list_audit_logs_with_time_range(self, client, auth_headers):
        """GET /audit-logs 支持时间范围筛选。"""
        res = client.get(
            "/api/v1/audit-logs?start_time=2026-01-01T00:00:00&end_time=2026-12-31T23:59:59",
            headers=auth_headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0

    def test_list_audit_logs_pagination(self, client, auth_headers):
        """GET /audit-logs 分页参数生效。"""
        res = client.get("/api/v1/audit-logs?page=1&page_size=5", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["data"]["page"] == 1
        assert data["data"]["page_size"] == 5
        assert len(data["data"]["items"]) <= 5