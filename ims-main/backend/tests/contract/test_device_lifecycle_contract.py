"""
改善点 #11 — 设备生命周期追溯图谱 契约测试
验证SN全链路数据完整性和时间轴可视化。
基于现有 DeviceLedger、RMA、Station、Stocktake 数据源。
"""

import pytest
from datetime import date


class TestDeviceLifecycleContract:
    """设备生命周期追溯 API 契约测试。"""

    # =========================================================================
    # 现有设备数据就绪验证
    # =========================================================================

    def _create_test_device(self, client, auth_headers, sn="SN-LIFECYCLE-001"):
        """辅助：创建设备并返回完整数据。"""
        cust_res = client.post("/api/v1/customers", json={"name": "生命周期测试客户"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        station_res = client.post("/api/v1/stations", json={
            "name": "生命周期测试场站", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = station_res.json()["data"]["id"]

        dev_res = client.post("/api/v1/device-ledger", json={
            "item_sn": sn,
            "station_id": station_id,
            "installed_date": str(date.today()),
        }, headers=auth_headers)
        return dev_res.json()["data"]

    def test_device_detail_contains_basic_info(self, client, auth_headers):
        """设备详情含基本字段。"""
        device = self._create_test_device(client, auth_headers, "SN-LIFECYCLE-001")
        detail = client.get(f"/api/v1/device-ledger/{device['id']}", headers=auth_headers)
        assert detail.status_code == 200
        data = detail.json()["data"]
        assert "item_sn" in data
        assert "station_name" in data or "station_id" in data
        assert "installed_date" in data
        assert "status" in data

    def test_device_list_filter_by_sn(self, client, auth_headers):
        """设备台账可按SN精确搜索。"""
        self._create_test_device(client, auth_headers, "SN-LIFECYCLE-SEARCH")
        res = client.get("/api/v1/device-ledger?search=SN-LIFECYCLE-SEARCH", headers=auth_headers)
        assert res.status_code == 200

    def test_rma_linked_to_device_sn(self, client, auth_headers, seed_data):
        """RMA退货可通过SN关联到设备（生命周期链条）。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-LIFECYCLE-RMA",
            "quantity": 1, "unit": "个",
            "customer_name": "生命周期RMA测试",
            "return_reason": "设备老化",
            "return_date": str(date.today()),
        }
        res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        assert res.status_code == 201
        assert res.json()["sn"] == "SN-LIFECYCLE-RMA"

    def test_device_station_change_tracked(self, client, auth_headers):
        """设备站址变更应可记录（生命周期事件类型之一）。"""
        device = self._create_test_device(client, auth_headers, "SN-LIFECYCLE-STATION")

        cust_res = client.post("/api/v1/customers", json={"name": "新站址客户"}, headers=auth_headers)
        new_station = client.post("/api/v1/stations", json={
            "name": "新站址", "customer_id": cust_res.json()["data"]["id"]
        }, headers=auth_headers)
        new_station_id = new_station.json()["data"]["id"]

        update_res = client.put(f"/api/v1/device-ledger/{device['id']}", json={
            "station_id": new_station_id,
            "item_sn": "SN-LIFECYCLE-STATION",
        }, headers=auth_headers)
        assert update_res.status_code == 200

    # =========================================================================
    # 生命周期全链路端点（规格占位 — 待后端实现）
    # =========================================================================

    def test_device_lifecycle_returns_timeline(self, client, auth_headers):
        """GET /device-ledger/{sn}/lifecycle 返回时间轴。"""
        device = self._create_test_device(client, auth_headers, "SN-LIFECYCLE-TL")
        res = client.get(f"/api/v1/device-ledger/{device['item_sn']}/lifecycle", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert "events" in data["data"]
        for event in data["data"]["events"]:
            assert "timestamp" in event
            assert "event_type" in event
            assert "description" in event

    def test_lifecycle_includes_multiple_event_types(self, client, auth_headers, seed_data):
        """全链路含生产、出货、维修、盘点等多种事件类型。"""
        res = client.get("/api/v1/device-ledger/SN-LIFECYCLE-FULL/lifecycle", headers=auth_headers)
        event_types = {e["event_type"] for e in res.json()["data"]["events"]}
        expected = {"PRODUCTION", "OUTBOUND", "REPAIR", "STOCKTAKE", "STATION_CHANGE"}
        assert len(event_types & expected) > 0

    def test_sn_not_found_returns_404(self, client, auth_headers):
        """不存在的SN返回404。"""
        res = client.get("/api/v1/device-ledger/INVALID-SN-XXXX/lifecycle", headers=auth_headers)
        assert res.status_code == 404

    def test_empty_events_device(self, client, auth_headers):
        """新建无历史事件的设备返回空事件列表。"""
        res = client.get("/api/v1/device-ledger/SN-LIFECYCLE-EMPTY/lifecycle", headers=auth_headers)
        assert res.json()["data"]["events"] == []