"""
JWT 安全测试：篡改、过期、无 Token、伪造签名。

覆盖：
  - JWT 篡改（修改 user_id / role）
  - JWT 过期
  - 无 Token 访问
  - 伪造签名 Token
"""

import time
from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import create_access_token


class TestJwtTampering:
    """JWT 篡改测试：修改 payload 后验证后端拒绝。"""

    def test_tampered_user_id_returns_401(self, client, seed_data):
        """篡改 user_id 为不存在的用户，应返回 401。"""
        token = create_access_token({"user_id": 99999, "username": "fake_user"})
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.get("/api/v1/rma/returns", headers=headers)
        assert resp.status_code == 401, f"预期 401，实际 {resp.status_code}"

    def test_tampered_empty_payload_returns_401(self, client):
        """payload 缺少 user_id，应返回 401。"""
        token = create_access_token({"username": "admin"})
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.get("/api/v1/rma/returns", headers=headers)
        assert resp.status_code == 401, f"预期 401，实际 {resp.status_code}"

    def test_tampered_role_does_not_elevate_privileges(self, client, seed_data):
        """在 payload 中伪造 role=ADMIN 不会提升权限（后端从 DB 查角色）。"""
        test_eng = seed_data["test_eng"]
        token = create_access_token({"user_id": test_eng.id, "username": test_eng.username, "role": "ADMIN"})
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.delete("/api/v1/users/1", headers=headers)
        assert resp.status_code == 403, f"预期 403（测试工程师无权删除用户），实际 {resp.status_code}"

    def test_tampered_user_id_for_disabled_user_returns_403(self, client, seed_data, db_session):
        """已禁用用户的 Token 应返回 403。"""
        admin = seed_data["admin"]
        admin.status = 0
        db_session.flush()
        token = create_access_token({"user_id": admin.id, "username": admin.username})
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.get("/api/v1/rma/returns", headers=headers)
        assert resp.status_code == 403, f"预期 403，实际 {resp.status_code}"


class TestJwtExpiry:
    """JWT 过期测试。"""

    def test_expired_token_returns_401(self, client, seed_data):
        """使用过期 Token 应返回 401。"""
        payload = {"user_id": seed_data["admin"].id, "username": "admin"}
        expire = datetime.now(timezone.utc) - timedelta(minutes=1)
        payload["exp"] = expire
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.get("/api/v1/rma/returns", headers=headers)
        assert resp.status_code == 401, f"预期 401，实际 {resp.status_code}"

    def test_valid_token_returns_200(self, client, auth_headers):
        """有效 Token 应正常返回 200。"""
        resp = client.get("/api/v1/rma/returns", headers=auth_headers)
        assert resp.status_code == 200, f"预期 200，实际 {resp.status_code}"


class TestJwtMissingOrInvalid:
    """无 Token / 伪造签名测试。"""

    def test_no_token_returns_401(self, client):
        """不携带 Token 应返回 401。"""
        resp = client.get("/api/v1/rma/returns")
        assert resp.status_code == 401, f"预期 401，实际 {resp.status_code}"

    def test_forged_signature_token_returns_401(self, client, seed_data):
        """使用错误密钥签名的 Token 应返回 401。"""
        payload = {"user_id": seed_data["admin"].id, "username": "admin"}
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        payload["exp"] = expire
        token = jwt.encode(payload, "wrong-secret-key-12345678", algorithm=settings.JWT_ALGORITHM)
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.get("/api/v1/rma/returns", headers=headers)
        assert resp.status_code == 401, f"预期 401，实际 {resp.status_code}"

    def test_malformed_token_returns_401(self, client):
        """格式错误的 Token 应返回 401。"""
        headers = {"Authorization": "Bearer not.a.valid.jwt.token"}
        resp = client.get("/api/v1/rma/returns", headers=headers)
        assert resp.status_code == 401, f"预期 401，实际 {resp.status_code}"

    def test_empty_bearer_token_returns_401(self, client):
        """空 Bearer Token 应返回 401。"""
        headers = {"Authorization": "Bearer "}
        resp = client.get("/api/v1/rma/returns", headers=headers)
        assert resp.status_code == 401, f"预期 401，实际 {resp.status_code}"