"""
主线C - 出货管理 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestShipmentContract:
    """出货登记 API 契约测试。"""

    def test_create_shipment_success(self, client, auth_headers, seed_data):
        """POST /shipment/ 创建出货单成功。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": ["SN-SHIP-001", "SN-SHIP-002", "SN-SHIP-003"],
            "quantity": 3,
            "ship_date": "2026-09-08",
            "address": "北京市朝阳区测试路100号",
            "logistics_provider": "顺丰速运",
            "tracking_no": "SF1234567890",
            "u9_task_no": "U9-2026-001",
            "tf_version": "V1.2.3",
            "host_version": "V3.0.1",
            "remark": "契约测试",
            "change_reason": "出货",
        }
        res = client.post("/api/v1/shipment/", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["data"]["shipment_no"] is not None
        assert data["data"]["shipment_no"].startswith("SH")
        assert data["data"]["sn_list"] == ["SN-SHIP-001", "SN-SHIP-002", "SN-SHIP-003"]
        assert data["data"]["u9_task_no"] == "U9-2026-001"

    def test_list_shipments_returns_page_result(self, client, auth_headers, seed_data):
        """GET /shipment/list 返回分页结构。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": ["SN-SHIP-004"],
            "quantity": 1,
            "ship_date": "2026-09-08",
            "address": "测试地址",
            "logistics_provider": "顺丰速运",
            "tracking_no": "SF0000000001",
            "change_reason": "出货",
        }
        client.post("/api/v1/shipment/", json=payload, headers=auth_headers)

        res = client.get("/api/v1/shipment/list", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert "page" in data["data"]

    def test_get_shipment_detail(self, client, auth_headers, seed_data):
        """GET /shipment/{id} 返回出货单详情。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": ["SN-SHIP-005"],
            "quantity": 1,
            "ship_date": "2026-09-08",
            "address": "测试地址",
            "logistics_provider": "顺丰速运",
            "tracking_no": "SF0000000002",
            "change_reason": "出货",
        }
        create_res = client.post("/api/v1/shipment/", json=payload, headers=auth_headers)
        shipment_id = create_res.json()["data"]["id"]

        res = client.get(f"/api/v1/shipment/{shipment_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"]["id"] == shipment_id

    def test_update_shipment(self, client, auth_headers, seed_data):
        """PUT /shipment/{id} 更新出货单。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": ["SN-SHIP-006"],
            "quantity": 1,
            "ship_date": "2026-09-08",
            "address": "测试地址",
            "logistics_provider": "顺丰速运",
            "tracking_no": "SF0000000003",
            "change_reason": "出货",
        }
        create_res = client.post("/api/v1/shipment/", json=payload, headers=auth_headers)
        shipment_id = create_res.json()["data"]["id"]

        update_res = client.put(
            f"/api/v1/shipment/{shipment_id}",
            json={"tracking_no": "SF9999999999", "remark": "已更新物流单号"},
            headers=auth_headers,
        )
        assert update_res.status_code == 200

    def test_delete_shipment(self, client, auth_headers, seed_data):
        """DELETE /shipment/{id} 删除出货单。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": ["SN-SHIP-007"],
            "quantity": 1,
            "ship_date": "2026-09-08",
            "address": "测试地址",
            "logistics_provider": "顺丰速运",
            "tracking_no": "SF0000000004",
            "change_reason": "出货",
        }
        create_res = client.post("/api/v1/shipment/", json=payload, headers=auth_headers)
        shipment_id = create_res.json()["data"]["id"]

        delete_res = client.delete(f"/api/v1/shipment/{shipment_id}", headers=auth_headers)
        assert delete_res.status_code == 200

        get_res = client.get(f"/api/v1/shipment/{shipment_id}", headers=auth_headers)
        assert get_res.json()["code"] != 0

    def test_create_shipment_validates_required_fields(self, client, auth_headers):
        """POST /shipment/ 缺少必填字段返回 422。"""
        res = client.post("/api/v1/shipment/", json={}, headers=auth_headers)
        assert res.status_code == 422

    def test_shipment_fields_completeness(self, client, auth_headers, seed_data):
        """创建出货单后验证所有字段完整性。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": ["SN-CMPL-001"],
            "quantity": 1,
            "ship_date": "2026-09-08",
            "address": "北京市朝阳区",
            "logistics_provider": "顺丰速运",
            "tracking_no": "SF0000000005",
            "u9_task_no": "U9-TEST-001",
            "tf_version": "V1.0.0",
            "host_version": "V2.0.0",
            "remark": "完整字段测试",
            "change_reason": "出货",
        }
        res = client.post("/api/v1/shipment/", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()["data"]
        assert data["shipment_no"] is not None
        assert data["sku_id"] == seed_data["sku_fg"].id
        assert data["sku_code"] == "202-046"
        assert data["sku_name"] == "测试成品"
        assert data["spec"] == "规格B"
        assert data["unit"] == "个"
        assert data["quantity"] == 1
        assert data["address"] == "北京市朝阳区"
        assert data["logistics_provider"] == "顺丰速运"
        assert data["tracking_no"] == "SF0000000005"
        assert data["u9_task_no"] == "U9-TEST-001"
        assert data["tf_version"] == "V1.0.0"
        assert data["host_version"] == "V2.0.0"
        assert data["created_by"] is not None
        assert data["created_at"] is not None