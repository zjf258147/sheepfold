"""
品牌配置 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
需要管理员权限。
"""

import pytest


class TestBrandingContract:
    """品牌配置 API 契约测试。"""

    def test_get_branding_public(self, client):
        """GET /settings/branding 无需鉴权也可访问。"""
        res = client.get("/api/v1/settings/branding")
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "app_name" in data["data"]

    def test_get_branding_with_auth(self, client, auth_headers):
        """GET /settings/branding 带鉴权也正常。"""
        res = client.get("/api/v1/settings/branding", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "app_name" in data["data"]
        assert "app_subtitle" in data["data"]

    def test_update_branding(self, client, auth_headers):
        """PUT /settings/branding 更新品牌文案。"""
        res = client.put("/api/v1/settings/branding", json={
            "app_name": "IMS测试系统",
            "app_subtitle": "契约测试副标题",
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["app_name"] == "IMS测试系统"

    def test_update_branding_validates_fields(self, client, auth_headers):
        """PUT /settings/branding 缺少字段返回 422。"""
        res = client.put("/api/v1/settings/branding", json={}, headers=auth_headers)
        assert res.status_code == 422