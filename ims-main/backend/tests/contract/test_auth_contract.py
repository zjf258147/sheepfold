"""
认证 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestAuthContract:
    """认证 API 契约测试。"""

    def test_login_success_returns_token(self, client, seed_data):
        """POST /auth/login 成功返回 token。"""
        res = client.post("/api/v1/auth/login", json={
            "username": "admin",
            "password": "admin123",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "access_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"
        assert data["data"]["access_token"] is not None

    def test_login_wrong_password(self, client, seed_data):
        """POST /auth/login 密码错误返回 401。"""
        res = client.post("/api/v1/auth/login", json={
            "username": "admin",
            "password": "wrongpassword",
        })
        assert res.status_code == 401

    def test_login_user_not_exist(self, client):
        """POST /auth/login 用户不存在返回 401。"""
        res = client.post("/api/v1/auth/login", json={
            "username": "nonexistent_user",
            "password": "test123456",
        })
        assert res.status_code == 401

    def test_login_disabled_user(self, client, auth_headers, db_session):
        """POST /auth/login 禁用用户返回 403。"""
        from app.models.user import User
        from app.core.security import hash_password

        disabled_user = User(
            username="disabled_test",
            password=hash_password("test123456"),
            nickname="已禁用用户",
            role="WAREHOUSE",
            status=0,
        )
        db_session.add(disabled_user)
        db_session.commit()

        res = client.post("/api/v1/auth/login", json={
            "username": "disabled_test",
            "password": "test123456",
        })
        assert res.status_code == 403

    def test_login_validates_fields(self, client):
        """POST /auth/login 缺少必填字段返回 422。"""
        res = client.post("/api/v1/auth/login", json={})
        assert res.status_code == 422

    def test_get_me_returns_current_user(self, client, auth_headers):
        """GET /auth/me 返回当前登录用户信息。"""
        res = client.get("/api/v1/auth/me", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["username"] == "admin"
        assert "password" not in data["data"]

    def test_get_me_without_token(self, client):
        """GET /auth/me 无 token 返回 401。"""
        res = client.get("/api/v1/auth/me")
        assert res.status_code == 401