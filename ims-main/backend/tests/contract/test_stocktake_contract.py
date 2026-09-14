"""
Stocktake API 契约测试
验证盘点任务 CRUD、扫码盘点、完成/取消盘点接口。
"""

import pytest
from datetime import datetime


class TestStocktakeContract:
    """盘点 API 契约测试。"""

    def test_list_stocktakes_returns_page_result(self, client, auth_headers):
        """T01: GET /stocktakes 分页查询返回分页结构。"""
        res = client.get("/api/v1/stocktakes", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_create_cycle_stocktake(self, client, auth_headers):
        """T02: POST /stocktakes 创建循环盘点。"""
        res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["mode"] == "CYCLE"
        assert data["data"]["status"] == "IN_PROGRESS"
        assert data["data"]["stocktake_no"].startswith("PD")

    def test_create_full_stocktake(self, client, auth_headers):
        """T03: POST /stocktakes 创建全面盘点。"""
        res = client.post("/api/v1/stocktakes", json={
            "mode": "FULL", "warehouse": "成品仓"
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["mode"] == "FULL"

    def test_get_stocktake_detail(self, client, auth_headers):
        """GET /stocktakes/{id} 详情查询。"""
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = create_res.json()["data"]["id"]
        res = client.get(f"/api/v1/stocktakes/{stocktake_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_scan_items_matched(self, client, auth_headers):
        """T05: POST /stocktakes/{id}/scan 扫码记录。"""
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = create_res.json()["data"]["id"]
        res = client.post(f"/api/v1/stocktakes/{stocktake_id}/scan", json={
            "items": [{"item_sn": "SN-SCAN-001", "actual_qty": 1}]
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_scan_items_batch(self, client, auth_headers):
        """POST /stocktakes/{id}/scan 批量扫码。"""
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = create_res.json()["data"]["id"]
        res = client.post(f"/api/v1/stocktakes/{stocktake_id}/scan", json={
            "items": [
                {"item_sn": "SN-SCAN-A", "actual_qty": 1},
                {"item_sn": "SN-SCAN-B", "actual_qty": 2},
                {"item_sn": "SN-SCAN-C", "actual_qty": 0},
            ]
        }, headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0

    def test_get_lines(self, client, auth_headers):
        """GET /stocktakes/{id}/lines 盘点明细列表。"""
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = create_res.json()["data"]["id"]
        client.post(f"/api/v1/stocktakes/{stocktake_id}/scan", json={
            "items": [{"item_sn": "SN-LINE-001", "actual_qty": 1}]
        }, headers=auth_headers)
        res = client.get(f"/api/v1/stocktakes/{stocktake_id}/lines", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert len(data["data"]) >= 1

    def test_complete_stocktake(self, client, auth_headers):
        """T07: POST /stocktakes/{id}/complete 完成盘点。"""
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = create_res.json()["data"]["id"]
        client.post(f"/api/v1/stocktakes/{stocktake_id}/scan", json={
            "items": [{"item_sn": "SN-COMPLETE-001", "actual_qty": 1}]
        }, headers=auth_headers)
        res = client.post(f"/api/v1/stocktakes/{stocktake_id}/complete", json={
            "remark": "盘点完成"
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["status"] == "COMPLETED"

    def test_cancel_stocktake(self, client, auth_headers):
        """T08: POST /stocktakes/{id}/cancel 取消盘点。"""
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = create_res.json()["data"]["id"]
        res = client.post(f"/api/v1/stocktakes/{stocktake_id}/cancel", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["status"] == "CANCELLED"

    def test_cancel_completed_stocktake(self, client, auth_headers):
        """T09: POST /stocktakes/{id}/cancel 取消已完成盘点（当前允许取消已完成）。"""
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = create_res.json()["data"]["id"]
        client.post(f"/api/v1/stocktakes/{stocktake_id}/complete", headers=auth_headers)
        res = client.post(f"/api/v1/stocktakes/{stocktake_id}/cancel", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] == 0
        assert res.json()["data"]["status"] == "CANCELLED"

    def test_get_stocktake_not_found(self, client, auth_headers):
        """GET /stocktakes/{id} 不存在的ID返回失败。"""
        res = client.get("/api/v1/stocktakes/99999", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["code"] != 0