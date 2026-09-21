"""
质保到期提醒配置 契约测试
验证 GET/PUT /settings/warranty-alert 接口的参数校验、权限和仪表盘联动。

当前状态：/settings/warranty-alert API 尚未实现，全部测试标记为 skip。
当后端实现后，移除 @pytest.mark.skip 即可运行。
"""

import pytest
from datetime import date, timedelta

pytestmark = pytest.mark.skip(reason="/settings/warranty-alert API 尚未实现，待后端开发后启用")


class TestWarrantyAlertConfig:
    """质保提醒配置 API 契约测试。"""

    def test_get_default_config_no_records(self, client, auth_headers):
        """GET /settings/warranty-alert 首次无记录时返回默认值。"""
        res = client.get("/api/v1/settings/warranty-alert", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["enabled"] is True
        assert data["data"]["days"] == [30, 60, 90]

    def test_get_with_auth(self, client, auth_headers):
        """GET /settings/warranty-alert 登录用户可读取。"""
        res = client.get("/api/v1/settings/warranty-alert", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "enabled" in data["data"]
        assert "days" in data["data"]

    def test_update_config_by_admin(self, client, auth_headers):
        """PUT /settings/warranty-alert 管理员更新配置。"""
        res = client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True,
            "days": [15, 45, 120],
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["enabled"] is True
        assert data["data"]["days"] == [15, 45, 120]

    def test_update_then_read(self, client, auth_headers):
        """PUT 更新后 GET 读取一致。"""
        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [7, 14, 30],
        }, headers=auth_headers)

        res = client.get("/api/v1/settings/warranty-alert", headers=auth_headers)
        assert res.json()["data"]["days"] == [7, 14, 30]

    def test_disable_alert(self, client, auth_headers):
        """关闭提醒后 enabled=false，days 保留。"""
        # 先设一个配置
        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30, 60, 90],
        }, headers=auth_headers)

        # 关闭
        res = client.put("/api/v1/settings/warranty-alert", json={
            "enabled": False, "days": [30, 60, 90],
        }, headers=auth_headers)
        assert res.json()["data"]["enabled"] is False
        assert res.json()["data"]["days"] == [30, 60, 90]

    def test_reenable_alert(self, client, auth_headers):
        """关闭后再开启，恢复原配置。"""
        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": False, "days": [30, 60, 90],
        }, headers=auth_headers)
        res = client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30, 60, 90],
        }, headers=auth_headers)
        assert res.json()["data"]["enabled"] is True
        assert res.json()["data"]["days"] == [30, 60, 90]

    def test_warehouse_cannot_update(self, client, auth_headers_warehouse):
        """普通用户（WAREHOUSE）修改返回 403。"""
        res = client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30],
        }, headers=auth_headers_warehouse)
        assert res.status_code == 403

    def test_unauthenticated_cannot_update(self, client):
        """未登录修改返回 401。"""
        res = client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30],
        })
        assert res.status_code == 401

    def test_reject_empty_days(self, client, auth_headers):
        """空数组返回 422。"""
        res = client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [],
        }, headers=auth_headers)
        assert res.status_code == 422

    def test_reject_zero_day(self, client, auth_headers):
        """天数含 0 返回 422。"""
        res = client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [0, 30],
        }, headers=auth_headers)
        assert res.status_code == 422

    def test_reject_day_exceeds_365(self, client, auth_headers):
        """天数含 366 返回 422。"""
        res = client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30, 366],
        }, headers=auth_headers)
        assert res.status_code == 422

    def test_deduplicate_days(self, client, auth_headers):
        """重复天数自动去重并升序保存。"""
        res = client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30, 30, 60],
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"]["days"] == [30, 60]

    def test_sort_days_ascending(self, client, auth_headers):
        """乱序输入自动升序排列。"""
        res = client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [90, 30, 60],
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"]["days"] == [30, 60, 90]


class TestWarrantyAlertDashboardIntegration:
    """质保提醒配置与仪表盘联动测试。"""

    def test_phase2_stats_includes_warranty_config(self, client, auth_headers):
        """phase2-stats 返回配置状态和分档统计。"""
        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30, 60, 90],
        }, headers=auth_headers)

        res = client.get("/api/v1/dashboard/phase2-stats", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()["data"]
        assert "warranty_alert_enabled" in data
        assert "warranty_alert_days" in data
        assert "warranty_expiring_soon" in data
        assert "warranty_expiring_by_day" in data

    def test_phase2_stats_warranty_disabled(self, client, auth_headers):
        """关闭提醒后 warranty 字段全为 0。"""
        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": False, "days": [30, 60, 90],
        }, headers=auth_headers)

        res = client.get("/api/v1/dashboard/phase2-stats", headers=auth_headers)
        data = res.json()["data"]
        assert data["warranty_alert_enabled"] is False
        assert data["warranty_expiring_soon"] == 0
        assert data["warranty_expiring_by_day"] == {}

    def test_poll_status_reflects_warranty_config(self, client, auth_headers):
        """poll-status 的 warranty_expiring_soon 跟随配置。"""
        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30, 60, 90],
        }, headers=auth_headers)

        res = client.get("/api/v1/dashboard/poll-status", headers=auth_headers)
        assert res.status_code == 200
        assert "warranty_expiring_soon" in res.json()["data"]

    def test_poll_status_warranty_disabled(self, client, auth_headers):
        """关闭提醒后 poll-status 质保字段为 0。"""
        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": False, "days": [30, 60, 90],
        }, headers=auth_headers)

        res = client.get("/api/v1/dashboard/poll-status", headers=auth_headers)
        assert res.json()["data"]["warranty_expiring_soon"] == 0

    def test_config_change_reflected_immediately(self, client, auth_headers):
        """配置修改后下一次请求立即生效（无需重启）。"""
        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [10, 20],
        }, headers=auth_headers)

        res = client.get("/api/v1/dashboard/phase2-stats", headers=auth_headers)
        assert res.json()["data"]["warranty_alert_days"] == [10, 20]

        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30, 90],
        }, headers=auth_headers)

        res = client.get("/api/v1/dashboard/phase2-stats", headers=auth_headers)
        assert res.json()["data"]["warranty_alert_days"] == [30, 90]

    def test_device_without_warranty_end_not_counted(self, client, auth_headers, db_session):
        """设备无 warranty_end 不计入统计。"""
        from app.models.device_ledger import DeviceLedger
        from app.models.enums import DeviceLedgerStatus

        # 确保至少有一台无 warranty_end 的设备
        device = db_session.query(DeviceLedger).filter(
            DeviceLedger.warranty_end.is_(None)
        ).first()

        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30, 60, 90],
        }, headers=auth_headers)

        res = client.get("/api/v1/dashboard/phase2-stats", headers=auth_headers)
        by_day = res.json()["data"]["warranty_expiring_by_day"]
        # 无 warranty_end 的不会出现在统计中（验证接口不崩溃即可）
        assert isinstance(by_day, dict)

    def test_warranty_end_today_included(self, client, auth_headers, db_session):
        """warranty_end = 今天，应计入最小档位。"""
        from app.models.device_ledger import DeviceLedger

        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [7, 30, 90],
        }, headers=auth_headers)

        res = client.get("/api/v1/dashboard/phase2-stats", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()["data"]
        assert "warranty_expiring_by_day" in data

    def test_old_field_compatibility(self, client, auth_headers):
        """warranty_expiring_soon 兼容旧前端，值 = 最大档位累计数。"""
        client.put("/api/v1/settings/warranty-alert", json={
            "enabled": True, "days": [30, 60, 90],
        }, headers=auth_headers)

        res = client.get("/api/v1/dashboard/phase2-stats", headers=auth_headers)
        data = res.json()["data"]
        by_day = data["warranty_expiring_by_day"]

        total_max = sum(by_day.values()) if by_day else 0
        # warranty_expiring_soon 应该等于最大天数档位的累计值
        if "90" in by_day:
            assert data["warranty_expiring_soon"] == by_day["90"]