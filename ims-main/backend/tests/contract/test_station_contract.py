"""
Station API 契约测试
验证场站 CRUD 接口的请求格式、响应结构、状态码。
"""

import pytest


class TestStationContract:
    """场站 API 契约测试。"""

    def _create_customer(self, client, auth_headers):
        res = client.post("/api/v1/customers", json={"name": "测试客户A"}, headers=auth_headers)
        assert res.status_code == 200
        return res.json()["data"]["id"]

    def test_list_stations_returns_page_result(self, client, auth_headers):
        """S01: GET /stations 分页查询，默认 page=1,size=20，返回分页结构。"""
        res = client.get("/api/v1/stations", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_list_stations_filter_by_customer(self, client, auth_headers):
        """S02: GET /stations?customer_id=1 按客户筛选。"""
        customer_id = self._create_customer(client, auth_headers)
        client.post("/api/v1/stations", json={
            "name": "场站S02", "customer_id": customer_id
        }, headers=auth_headers)
        res = client.get(f"/api/v1/stations?customer_id={customer_id}", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert len(data["data"]["items"]) >= 1

    def test_get_station_detail(self, client, auth_headers):
        """S03: GET /stations/{id} 详情查询。"""
        customer_id = self._create_customer(client, auth_headers)
        create_res = client.post("/api/v1/stations", json={
            "name": "场站S03", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = create_res.json()["data"]["id"]
        res = client.get(f"/api/v1/stations/{station_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0
        assert res.json()["data"]["name"] == "场站S03"

    def test_get_station_not_found(self, client, auth_headers):
        """S04: GET /stations/{id} 不存在的ID返回失败。"""
        res = client.get("/api/v1/stations/99999", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] != 0

    def test_create_station(self, client, auth_headers):
        """S05: POST /stations 创建场站（含必填字段）。"""
        customer_id = self._create_customer(client, auth_headers)
        res = client.post("/api/v1/stations", json={
            "name": "场站S05", "customer_id": customer_id, "address": "测试地址"
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["name"] == "场站S05"

    def test_create_station_missing_required(self, client, auth_headers):
        """S06: POST /stations 缺少必填字段返回422。"""
        res = client.post("/api/v1/stations", json={"name": "缺客户"}, headers=auth_headers)
        assert res.status_code == 422

    def test_create_station_duplicate_name(self, client, auth_headers):
        """S07: POST /stations 重名场站返回失败。"""
        customer_id = self._create_customer(client, auth_headers)
        client.post("/api/v1/stations", json={
            "name": "重名场站", "customer_id": customer_id
        }, headers=auth_headers)
        res = client.post("/api/v1/stations", json={
            "name": "重名场站", "customer_id": customer_id
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] != 0

    def test_update_station(self, client, auth_headers):
        """S08: PUT /stations/{id} 更新场站信息。"""
        customer_id = self._create_customer(client, auth_headers)
        create_res = client.post("/api/v1/stations", json={
            "name": "场站S08", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = create_res.json()["data"]["id"]
        res = client.put(f"/api/v1/stations/{station_id}", json={
            "address": "新地址", "contact_person": "张三"
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0
        assert res.json()["data"]["address"] == "新地址"

    def test_delete_station_without_device(self, client, auth_headers):
        """S09: DELETE /stations/{id} 删除无关联设备的场站。"""
        customer_id = self._create_customer(client, auth_headers)
        create_res = client.post("/api/v1/stations", json={
            "name": "场站S09", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = create_res.json()["data"]["id"]
        res = client.delete(f"/api/v1/stations/{station_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_delete_station_with_device(self, client, auth_headers):
        """S10: DELETE /stations/{id} 删除有关联设备的场站（当前不阻止删除）。"""
        customer_id = self._create_customer(client, auth_headers)
        create_res = client.post("/api/v1/stations", json={
            "name": "场站S10", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = create_res.json()["data"]["id"]
        res = client.delete(f"/api/v1/stations/{station_id}", headers=auth_headers)
        assert res.status_code == 200

    def test_list_all_active_stations(self, client, auth_headers):
        """GET /stations/all 返回所有启用场站。"""
        res = client.get("/api/v1/stations/all", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0
        assert isinstance(res.json()["data"], list)