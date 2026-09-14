"""
DeviceLedger API 契约测试
验证设备台账 CRUD、设备移除、质保查询接口。
"""

import pytest
from datetime import date, timedelta


class TestDeviceLedgerContract:
    """设备台账 API 契约测试。"""

    def _setup_station(self, client, auth_headers):
        """创建测试客户和场站，返回 station_id。"""
        cust_res = client.post("/api/v1/customers", json={"name": "台账测试客户"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        res = client.post("/api/v1/stations", json={
            "name": "台账测试场站", "customer_id": customer_id
        }, headers=auth_headers)
        return res.json()["data"]["id"]

    def test_list_devices_returns_page_result(self, client, auth_headers):
        """D01: GET /device-ledger 分页查询返回分页结构。"""
        res = client.get("/api/v1/device-ledger", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_list_devices_filter_by_station(self, client, auth_headers):
        """D02: GET /device-ledger?station_id=1 按场站筛选。"""
        station_id = self._setup_station(client, auth_headers)
        client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-D02", "station_id": station_id,
            "installed_date": str(date.today()),
        }, headers=auth_headers)
        res = client.get(f"/api/v1/device-ledger?station_id={station_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_list_devices_filter_by_status(self, client, auth_headers):
        """D03: GET /device-ledger?status=RUNNING 按状态筛选。"""
        res = client.get("/api/v1/device-ledger?status=RUNNING", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_get_device_detail(self, client, auth_headers):
        """D04: GET /device-ledger/{id} 详情查询。"""
        station_id = self._setup_station(client, auth_headers)
        create_res = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-D04", "station_id": station_id,
            "installed_date": str(date.today()),
        }, headers=auth_headers)
        ledger_id = create_res.json()["data"]["id"]
        res = client.get(f"/api/v1/device-ledger/{ledger_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_get_device_not_found(self, client, auth_headers):
        """GET /device-ledger/{id} 不存在的ID返回失败。"""
        res = client.get("/api/v1/device-ledger/99999", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] != 0

    def test_create_device_ledger(self, client, auth_headers):
        """D07: POST /device-ledger 创建安装记录。"""
        station_id = self._setup_station(client, auth_headers)
        res = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-D07", "station_id": station_id,
            "installed_date": str(date.today()),
            "warranty_start": str(date.today()),
            "warranty_end": str(date.today() + timedelta(days=365)),
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["item_sn"] == "SN-D07"

    def test_create_device_duplicate_in_station(self, client, auth_headers):
        """D08: POST /device-ledger 同一场站重复安装相同SN返回失败。"""
        station_id = self._setup_station(client, auth_headers)
        payload = {"item_sn": "SN-D08", "station_id": station_id, "installed_date": str(date.today())}
        client.post("/api/v1/device-ledger", json=payload, headers=auth_headers)
        res = client.post("/api/v1/device-ledger", json=payload, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] != 0

    def test_update_device_warranty(self, client, auth_headers):
        """D09: PUT /device-ledger/{id} 更新质保期。"""
        station_id = self._setup_station(client, auth_headers)
        create_res = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-D09", "station_id": station_id,
            "installed_date": str(date.today()),
        }, headers=auth_headers)
        ledger_id = create_res.json()["data"]["id"]
        new_end = str(date.today() + timedelta(days=730))
        res = client.put(f"/api/v1/device-ledger/{ledger_id}", json={
            "warranty_start": str(date.today()),
            "warranty_end": new_end,
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_remove_device(self, client, auth_headers):
        """D10: POST /device-ledger/{id}/remove 设备移除。"""
        station_id = self._setup_station(client, auth_headers)
        create_res = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-D10", "station_id": station_id,
            "installed_date": str(date.today()),
        }, headers=auth_headers)
        ledger_id = create_res.json()["data"]["id"]
        res = client.post(f"/api/v1/device-ledger/{ledger_id}/remove", json={
            "removed_date": str(date.today()),
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["status"] == "RECOVERED"

    def test_warranty_check_in_warranty(self, client, auth_headers):
        """D11: GET /device-ledger/warranty/{sn} 质保查询（在保）。"""
        station_id = self._setup_station(client, auth_headers)
        client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-D11", "station_id": station_id,
            "installed_date": str(date.today()),
            "warranty_start": str(date.today()),
            "warranty_end": str(date.today() + timedelta(days=365)),
        }, headers=auth_headers)
        res = client.get("/api/v1/device-ledger/warranty/SN-D11", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["in_warranty"] is True

    def test_warranty_check_expired(self, client, auth_headers):
        """D12: GET /device-ledger/warranty/{sn} 质保查询（过期）。"""
        station_id = self._setup_station(client, auth_headers)
        client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-D12", "station_id": station_id,
            "installed_date": str(date.today() - timedelta(days=400)),
            "warranty_start": str(date.today() - timedelta(days=400)),
            "warranty_end": str(date.today() - timedelta(days=1)),
        }, headers=auth_headers)
        res = client.get("/api/v1/device-ledger/warranty/SN-D12", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["in_warranty"] is False

    def test_warranty_check_sn_not_found(self, client, auth_headers):
        """GET /device-ledger/warranty/{sn} SN无安装记录。"""
        res = client.get("/api/v1/device-ledger/warranty/SN-NOTEXIST", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["in_warranty"] is False