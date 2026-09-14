"""
库存快照 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest
from datetime import date, timedelta


class TestSnapshotContract:
    """库存快照 API 契约测试。"""

    @property
    def today(self):
        return date.today().isoformat()

    @property
    def yesterday(self):
        return (date.today() - timedelta(days=1)).isoformat()

    def test_list_snapshots(self, client, auth_headers):
        """GET /snapshots 返回快照批次列表。"""
        res = client.get("/api/v1/snapshots", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert isinstance(data["data"], list)

    def test_snapshot_dates(self, client, auth_headers):
        """GET /snapshots/dates 返回快照日期列表。"""
        res = client.get(
            f"/api/v1/snapshots/dates?date_from={self.yesterday}&date_to={self.today}",
            headers=auth_headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert isinstance(data["data"], list)

    def test_daily_ledger_requires_dates(self, client, auth_headers):
        """GET /snapshots/daily-ledger 缺少日期参数返回 422。"""
        res = client.get("/api/v1/snapshots/daily-ledger", headers=auth_headers)
        assert res.status_code == 422

    def test_daily_ledger_valid(self, client, auth_headers):
        """GET /snapshots/daily-ledger 返回日流水。"""
        res = client.get(
            f"/api/v1/snapshots/daily-ledger?date_from={self.yesterday}&date_to={self.today}",
            headers=auth_headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert isinstance(data["data"], list)

    def test_daily_ledger_breakdown(self, client, auth_headers):
        """GET /snapshots/daily-ledger/{date}/breakdown 返回流水明细。"""
        res = client.get(
            f"/api/v1/snapshots/daily-ledger/{self.today}/breakdown?dimension=sku",
            headers=auth_headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]

    def test_daily_ledger_export(self, client, auth_headers):
        """GET /snapshots/daily-ledger/export 返回 Excel。"""
        res = client.get(
            f"/api/v1/snapshots/daily-ledger/export?date_from={self.yesterday}&date_to={self.today}",
            headers=auth_headers,
        )
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_ledger_summary_requires_dates(self, client, auth_headers):
        """GET /snapshots/ledger-summary 缺少日期参数返回 422。"""
        res = client.get("/api/v1/snapshots/ledger-summary", headers=auth_headers)
        assert res.status_code == 422

    def test_ledger_summary_valid(self, client, auth_headers):
        """GET /snapshots/ledger-summary 返回快照汇总。"""
        res = client.get(
            f"/api/v1/snapshots/ledger-summary?date_from={self.yesterday}&date_to={self.today}",
            headers=auth_headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert isinstance(data["data"], list)

    def test_ledger_summary_export(self, client, auth_headers):
        """GET /snapshots/ledger-summary/export 返回 Excel。"""
        res = client.get(
            f"/api/v1/snapshots/ledger-summary/export?date_from={self.yesterday}&date_to={self.today}",
            headers=auth_headers,
        )
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_snapshot_items(self, client, auth_headers):
        """GET /snapshots/items 返回快照明细。"""
        res = client.get(
            f"/api/v1/snapshots/items?snapshot_date={self.today}",
            headers=auth_headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]

    def test_snapshot_items_export(self, client, auth_headers):
        """GET /snapshots/items/export 返回 Excel。"""
        res = client.get(
            f"/api/v1/snapshots/items/export?snapshot_date={self.today}",
            headers=auth_headers,
        )
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_trigger_snapshot(self, client, auth_headers):
        """POST /snapshots/trigger 手动触发日快照。"""
        res = client.post("/api/v1/snapshots/trigger", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0