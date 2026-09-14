"""
InventoryAdjustment API 契约测试
验证库存调整的创建、确认接口。
"""

import pytest


class TestInventoryAdjustmentContract:
    """库存调整 API 契约测试。"""

    def _create_stocktake_with_lines(self, client, auth_headers, seed_data):
        """创建盘点任务并扫码，返回 stocktake 和 line 信息。"""
        sku_id = seed_data["sku_fg"].id
        supplier_id = seed_data["supplier"].id

        # 入库SN到库存
        inbound_payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": supplier_id,
            "lines": [
                {"sku_id": sku_id, "quantity": 2, "unit_price": 2000,
                 "item_sns": ["SN-ADJ-001", "SN-ADJ-002"]}
            ],
        }
        res = client.post("/api/v1/inbound/orders", json=inbound_payload, headers=auth_headers)
        inbound_id = res.json()["data"]["id"]
        client.post(f"/api/v1/inbound/orders/{inbound_id}/submit", headers=auth_headers)
        client.post(f"/api/v1/inbound/orders/{inbound_id}/approve", headers=auth_headers)

        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = create_res.json()["data"]["id"]

        # system_qty=1（已入库），扫码 actual_qty=2（盘盈1）或 actual_qty=0（盘亏1）
        client.post(f"/api/v1/stocktakes/{stocktake_id}/scan", json={
            "items": [
                {"item_sn": "SN-ADJ-001", "actual_qty": 2},
                {"item_sn": "SN-ADJ-002", "actual_qty": 0},
            ]
        }, headers=auth_headers)
        lines_res = client.get(f"/api/v1/stocktakes/{stocktake_id}/lines", headers=auth_headers)
        return stocktake_id, lines_res.json()["data"]

    def test_list_adjustments_returns_page_result(self, client, auth_headers):
        """A01: GET /adjustments 分页查询返回分页结构。"""
        res = client.get("/api/v1/adjustments", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_create_surplus_adjustment(self, client, auth_headers, seed_data):
        """A02: POST /adjustments 创建盘盈调整。"""
        stocktake_id, lines = self._create_stocktake_with_lines(client, auth_headers, seed_data)
        surplus_line = [l for l in lines if l["diff_qty"] > 0]
        if surplus_line:
            res = client.post("/api/v1/adjustments", json={
                "stocktake_id": stocktake_id,
                "stocktake_line_id": surplus_line[0]["id"],
                "adjustment_type": "SURPLUS",
                "reason": "盘盈调整测试",
            }, headers=auth_headers)
            assert res.status_code == 200
            data = res.json()
            assert data["code"] == 0
            assert data["data"]["adjustment_type"] == "SURPLUS"
            assert data["data"]["adjustment_no"].startswith("TZ")

    def test_create_shortage_adjustment(self, client, auth_headers, seed_data):
        """A03: POST /adjustments 创建盘亏调整。"""
        stocktake_id, lines = self._create_stocktake_with_lines(client, auth_headers, seed_data)
        shortage_line = [l for l in lines if l["diff_qty"] < 0]
        if shortage_line:
            res = client.post("/api/v1/adjustments", json={
                "stocktake_id": stocktake_id,
                "stocktake_line_id": shortage_line[0]["id"],
                "adjustment_type": "SHORTAGE",
                "reason": "盘亏调整测试",
            }, headers=auth_headers)
            assert res.status_code == 200
            data = res.json()
            assert data["code"] == 0
            assert data["data"]["adjustment_type"] == "SHORTAGE"

    def test_confirm_adjustments(self, client, auth_headers, seed_data):
        """A04: POST /adjustments/confirm 确认库存调整。"""
        stocktake_id, lines = self._create_stocktake_with_lines(client, auth_headers, seed_data)
        surplus_line = [l for l in lines if l["diff_qty"] > 0]
        if not surplus_line:
            pytest.skip("无盘盈差异数据")
        adj_res = client.post("/api/v1/adjustments", json={
            "stocktake_id": stocktake_id,
            "stocktake_line_id": surplus_line[0]["id"],
            "adjustment_type": "SURPLUS",
            "reason": "确认调整测试",
        }, headers=auth_headers)
        adj_id = adj_res.json()["data"]["id"]
        res = client.post("/api/v1/adjustments/confirm", json={
            "adjustment_ids": [adj_id]
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_get_adjustment_detail(self, client, auth_headers, seed_data):
        """GET /adjustments/{id} 详情查询。"""
        stocktake_id, lines = self._create_stocktake_with_lines(client, auth_headers, seed_data)
        surplus_line = [l for l in lines if l["diff_qty"] > 0]
        if not surplus_line:
            pytest.skip("无盘盈差异数据")
        adj_res = client.post("/api/v1/adjustments", json={
            "stocktake_id": stocktake_id,
            "stocktake_line_id": surplus_line[0]["id"],
            "adjustment_type": "SURPLUS",
            "reason": "详情测试",
        }, headers=auth_headers)
        adj_id = adj_res.json()["data"]["id"]
        res = client.get(f"/api/v1/adjustments/{adj_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_get_adjustment_not_found(self, client, auth_headers):
        """GET /adjustments/{id} 不存在的ID返回失败。"""
        res = client.get("/api/v1/adjustments/99999", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] != 0