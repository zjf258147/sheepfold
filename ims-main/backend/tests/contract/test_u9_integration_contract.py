"""
改善点 #5 — U9深度集成 契约测试
验证 Phase1 U9任务单号下拉选择 和 Phase2 数据对接。
Phase1基于现有 Shipment API 可测试，Phase2端点待实现。
"""

import pytest


class TestU9IntegrationContract:
    """U9集成 API 契约测试。"""

    # =========================================================================
    # Phase1 — 现有 u9_task_no 字段验证（已可直接测试）
    # =========================================================================

    def test_shipment_contains_u9_task_no(self, client, auth_headers, seed_data):
        """出货单含 u9_task_no 字段，可存储和读取。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": ["SN-U9-001"],
            "quantity": 1,
            "ship_date": "2026-09-20",
            "address": "测试地址",
            "logistics_provider": "顺丰",
            "tracking_no": "SF-U9-001",
            "u9_task_no": "U9-2026-099",
            "remark": "U9集成测试",
        }
        res = client.post("/api/v1/shipment/", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()["data"]
        assert data["u9_task_no"] == "U9-2026-099"

    def test_shipment_u9_task_no_saved_in_db(self, client, auth_headers, seed_data):
        """u9_task_no 持久化到数据库，GET详情可获取。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": ["SN-U9-002"],
            "quantity": 1,
            "ship_date": "2026-09-20",
            "address": "测试地址",
            "logistics_provider": "德邦",
            "tracking_no": "DB-U9-002",
            "u9_task_no": "U9-2026-047",
            "remark": "U9持久化测试",
        }
        create_res = client.post("/api/v1/shipment/", json=payload, headers=auth_headers)
        ship_id = create_res.json()["data"]["id"]

        detail_res = client.get(f"/api/v1/shipment/{ship_id}", headers=auth_headers)
        assert detail_res.status_code == 200
        assert detail_res.json()["data"]["u9_task_no"] == "U9-2026-047"

    def test_shipment_list_filterable_by_u9(self, client, auth_headers, seed_data):
        """出货单列表可按 u9_task_no 筛选。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id, "sku_code": "202-046",
            "sku_name": "测试成品", "spec": "规格B", "unit": "个",
            "sn_list": ["SN-U9-003"], "quantity": 1,
            "ship_date": "2026-09-20",
            "address": "测试地址",
            "logistics_provider": "圆通",
            "tracking_no": "YT-U9-003",
            "u9_task_no": "U9-FILTER-TEST",
            "remark": "筛选测试",
        }
        client.post("/api/v1/shipment/", json=payload, headers=auth_headers)

        res = client.get("/api/v1/shipment/list?search=U9-FILTER-TEST", headers=auth_headers)
        assert res.status_code == 200
        items = res.json()["data"]["items"]
        assert len(items) >= 1

    def test_shipment_u9_task_no_nullable(self, client, auth_headers, seed_data):
        """u9_task_no 可为空（兼容未集成场景）。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id, "sku_code": "202-046",
            "sku_name": "测试成品", "spec": "规格B", "unit": "个",
            "sn_list": ["SN-U9-NULL"], "quantity": 1,
            "ship_date": "2026-09-20", "address": "测试地址",
            "logistics_provider": "自提",
            "tracking_no": "SELF-U9-NULL",
            "remark": "u9可为空测试",
        }
        res = client.post("/api/v1/shipment/", json=payload, headers=auth_headers)
        assert res.status_code == 201

    # =========================================================================
    # Phase1 U9任务单号下拉选择端点（规格占位 — 待后端实现）
    # =========================================================================

    @pytest.mark.skip(reason="U9历史单号端点尚未实现")
    def test_get_historical_u9_task_nos(self, client, auth_headers):
        """GET /shipment/u9-task-nos 返回去重排序的历史U9单号。"""
        res = client.get("/api/v1/shipment/u9-task-nos", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()["data"]
        assert isinstance(data, list)
        # 应排序
        if len(data) > 1:
            assert data == sorted(data)

    # =========================================================================
    # Phase2 U9对接端点（规格占位 — 待后端实现）
    # =========================================================================

    @pytest.mark.skip(reason="U9健康检查端点尚未实现")
    def test_u9_health_check(self, client, auth_headers):
        """GET /system/u9/health 返回U9接口连通状态。"""
        res = client.get("/api/v1/system/u9/health", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()["data"]
        assert "connected" in data

    @pytest.mark.skip(reason="U9库存对账端点尚未实现")
    def test_u9_inventory_reconciliation(self, client, auth_headers):
        """GET /system/u9/inventory-reconciliation 返回IMS vs U9库存差异。"""
        res = client.get("/api/v1/system/u9/inventory-reconciliation", headers=auth_headers)
        assert res.status_code == 200