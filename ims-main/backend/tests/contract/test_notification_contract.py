"""
改善点 #12 — 消息通知与待办推送 契约测试
验证 DingTalk/企微 webhook 通知和 BackgroundTasks 机制。
"""

import pytest


class TestNotificationContract:
    """消息通知 API 契约测试。"""

    # =========================================================================
    # 现有Dashboard轮询机制验证（通知的前置条件）
    # =========================================================================

    def test_dashboard_poll_status_returns_pending_count(self, client, auth_headers):
        """poll-status 返回待办数量（通知触发依据）。"""
        res = client.get("/api/v1/dashboard/poll-status", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()["data"]
        assert "inbound_pending" in data
        assert "warranty_expiring_soon" in data
        assert isinstance(data["inbound_pending"], int)

    def test_phase2_stats_returns_data(self, client, auth_headers):
        """phase2-stats 返回仪表盘数据（包含质保到期信息）。"""
        res = client.get("/api/v1/dashboard/phase2-stats", headers=auth_headers)
        assert res.status_code == 200

    def test_settings_branding_exists(self, client, auth_headers):
        """系统设置有品牌配置（可扩展通知配置区域）。"""
        res = client.get("/api/v1/settings/branding", headers=auth_headers)
        assert res.status_code == 200

    # =========================================================================
    # 消息通知端点（规格占位 — 待后端实现）
    # =========================================================================

    @pytest.mark.skip(reason="通知配置端点尚未实现")
    def test_get_notification_config(self, client, auth_headers):
        """GET /settings/notification 返回通知配置。"""
        res = client.get("/api/v1/settings/notification", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()["data"]
        assert "dingtalk_enabled" in data
        assert "wechat_enabled" in data
        assert "warranty_alert_enabled" in data

    @pytest.mark.skip(reason="通知配置端点尚未实现")
    def test_update_notification_config(self, client, auth_headers):
        """PUT /settings/notification 更新通知配置。"""
        res = client.put("/api/v1/settings/notification", json={
            "dingtalk_enabled": True,
            "dingtalk_webhook": "https://oapi.dingtalk.com/robot/send?access_token=test",
            "dingtalk_secret": "SECtest",
        }, headers=auth_headers)
        assert res.status_code == 200

    @pytest.mark.skip(reason="通知配置端点尚未实现")
    def test_unauthorized_cannot_update(self, client):
        """未登录不可修改通知配置。"""
        res = client.put("/api/v1/settings/notification", json={
            "dingtalk_enabled": True,
        })
        assert res.status_code == 401

    @pytest.mark.skip(reason="通知推送端点尚未实现")
    def test_dingtalk_webhook_test(self, client, auth_headers):
        """POST /settings/notification/test-dingtalk 测试DingTalk连通性。"""
        res = client.post("/api/v1/settings/notification/test-dingtalk", headers=auth_headers)
        assert res.status_code in [200, 502]

    @pytest.mark.skip(reason="通知模板端点尚未实现")
    def test_notification_templates_available(self, client, auth_headers):
        """GET /settings/notification/templates 返回通知模板列表。"""
        res = client.get("/api/v1/settings/notification/templates", headers=auth_headers)
        assert res.status_code == 200
        templates = res.json()["data"]
        template_codes = [t["code"] for t in templates]
        assert "PENDING_AUDIT" in template_codes
        assert "WARRANTY_EXPIRING" in template_codes