"""
权限矩阵测试。
覆盖：DELETE/APPROVE/EXPORT 操作 × 5角色，以及越权测试。
"""

import pytest
from fastapi.testclient import TestClient

from app.core.security import create_access_token


def _make_headers(seed_data, role_key: str) -> dict:
    """生成指定角色的认证头。"""
    user = seed_data.get(role_key)
    if not user:
        return {}
    token = create_access_token({"user_id": user.id, "username": user.username})
    return {"Authorization": f"Bearer {token}"}


class TestPermissionMatrix:
    """权限矩阵：DELETE / AUDIT / SETTINGS × 5角色"""

    # =========== DELETE 操作 ===========

    def test_admin_can_access_delete_user(self, client: TestClient, seed_data):
        """ADMIN 可访问删除用户端点（即使ID不存在，也不应返回403）。"""
        headers = _make_headers(seed_data, "admin")
        resp = client.delete("/api/v1/users/99999", headers=headers)
        # ADMIN 不应返回403，应返回404（用户不存在）或200（业务错误）
        assert resp.status_code != 403, f"ADMIN 应可访问删除用户，实际: {resp.status_code}"

    def test_warehouse_cannot_delete_user(self, client: TestClient, seed_data):
        """仓库管理员 不能删除用户。"""
        headers = _make_headers(seed_data, "warehouse")
        resp = client.delete("/api/v1/users/1", headers=headers)
        assert resp.status_code == 403

    def test_quality_cannot_delete_user(self, client: TestClient, seed_data):
        """质量负责人 不能删除用户。"""
        headers = _make_headers(seed_data, "quality")
        resp = client.delete("/api/v1/users/1", headers=headers)
        assert resp.status_code == 403

    def test_production_cannot_delete_user(self, client: TestClient, seed_data):
        """生产负责人 不能删除用户。"""
        headers = _make_headers(seed_data, "production")
        resp = client.delete("/api/v1/users/1", headers=headers)
        assert resp.status_code == 403

    def test_test_engineer_cannot_delete_user(self, client: TestClient, seed_data):
        """测试工程师 不能删除用户。"""
        headers = _make_headers(seed_data, "test_eng")
        resp = client.delete("/api/v1/users/1", headers=headers)
        assert resp.status_code == 403

    # =========== AUDIT 操作（仅 ADMIN） ===========

    def test_admin_can_access_audit_logs(self, client: TestClient, seed_data):
        """ADMIN 可访问审计日志。"""
        headers = _make_headers(seed_data, "admin")
        resp = client.get("/api/v1/audit-logs", headers=headers)
        assert resp.status_code == 200

    def test_warehouse_cannot_access_audit_logs(self, client: TestClient, seed_data):
        """仓库管理员 不能访问审计日志。"""
        headers = _make_headers(seed_data, "warehouse")
        resp = client.get("/api/v1/audit-logs", headers=headers)
        assert resp.status_code == 403

    def test_quality_cannot_access_audit_logs(self, client: TestClient, seed_data):
        """质量负责人 不能访问审计日志。"""
        headers = _make_headers(seed_data, "quality")
        resp = client.get("/api/v1/audit-logs", headers=headers)
        assert resp.status_code == 403

    def test_production_cannot_access_audit_logs(self, client: TestClient, seed_data):
        """生产负责人 不能访问审计日志。"""
        headers = _make_headers(seed_data, "production")
        resp = client.get("/api/v1/audit-logs", headers=headers)
        assert resp.status_code == 403

    def test_test_engineer_cannot_access_audit_logs(self, client: TestClient, seed_data):
        """测试工程师 不能访问审计日志。"""
        headers = _make_headers(seed_data, "test_eng")
        resp = client.get("/api/v1/audit-logs", headers=headers)
        assert resp.status_code == 403

    # =========== SETTINGS 操作（仅 ADMIN） ===========

    def test_admin_can_access_settings(self, client: TestClient, seed_data):
        """ADMIN 可更新系统设置。"""
        headers = _make_headers(seed_data, "admin")
        resp = client.put("/api/v1/settings/branding", json={
            "app_name": "IMS", "app_subtitle": "测试",
        }, headers=headers)
        # ADMIN 可以更新设置
        assert resp.status_code == 200

    def test_warehouse_cannot_access_settings(self, client: TestClient, seed_data):
        """仓库管理员 不能更新系统设置。"""
        headers = _make_headers(seed_data, "warehouse")
        resp = client.put("/api/v1/settings/branding", json={
            "app_name": "IMS", "app_subtitle": "测试",
        }, headers=headers)
        assert resp.status_code == 403

    def test_test_engineer_cannot_access_settings(self, client: TestClient, seed_data):
        """测试工程师 不能更新系统设置。"""
        headers = _make_headers(seed_data, "test_eng")
        resp = client.put("/api/v1/settings/branding", json={
            "app_name": "IMS", "app_subtitle": "测试",
        }, headers=headers)
        assert resp.status_code == 403


class TestUnauthorizedAccess:
    """越权测试：低权限角色访问高权限接口"""

    def test_test_engineer_delete_user_403(self, client: TestClient, seed_data):
        """测试工程师 → DELETE 用户 → 403。"""
        headers = _make_headers(seed_data, "test_eng")
        resp = client.delete("/api/v1/users/1", headers=headers)
        assert resp.status_code == 403

    def test_warehouse_access_audit_logs_403(self, client: TestClient, seed_data):
        """仓库管理员 → GET 审计日志 → 403。"""
        headers = _make_headers(seed_data, "warehouse")
        resp = client.get("/api/v1/audit-logs", headers=headers)
        assert resp.status_code == 403

    def test_production_access_settings_403(self, client: TestClient, seed_data):
        """生产主管 → PUT 系统设置 → 403。"""
        headers = _make_headers(seed_data, "production")
        resp = client.put("/api/v1/settings/branding", json={
            "app_name": "IMS", "app_subtitle": "测试",
        }, headers=headers)
        assert resp.status_code == 403