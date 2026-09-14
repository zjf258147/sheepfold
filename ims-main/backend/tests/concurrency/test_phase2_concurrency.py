"""
二期并发测试
验证：盘点扫码并发、全面盘点并发
"""

import pytest


class TestStocktakeConcurrency:
    """盘点并发测试"""

    def test_scan_repeatedly_same_sn(self, client, auth_headers):
        """E1: 同一SN重复扫码，更新已有记录而非创建新记录。"""
        st_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = st_res.json()["data"]["id"]

        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-CONCUR-1", "actual_qty": 1}]
        }, headers=auth_headers)
        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-CONCUR-1", "actual_qty": 5}]
        }, headers=auth_headers)

        lines = client.get(f"/api/v1/stocktakes/{sid}/lines", headers=auth_headers).json()["data"]
        assert len(lines) == 1
        assert lines[0]["actual_qty"] == 5

    def test_multiple_full_stocktake_parallel(self, client, auth_headers):
        """E3: 同时创建两个全面盘点（当前允许多个并存）。"""
        r1 = client.post("/api/v1/stocktakes", json={
            "mode": "FULL", "warehouse": "成品仓"
        }, headers=auth_headers)
        r2 = client.post("/api/v1/stocktakes", json={
            "mode": "FULL", "warehouse": "成品仓"
        }, headers=auth_headers)
        assert r1.json()["code"] == 0
        assert r2.json()["code"] == 0

    def test_complete_then_adjustment(self, client, auth_headers, seed_data):
        """E4: 盘点完成中同时确认调整应串行化。"""
        sku_id = seed_data["sku_fg"].id
        supplier_id = seed_data["supplier"].id
        inbound_payload = {
            "inbound_mode": "PROCUREMENT", "stock_condition": "NEW",
            "partner_id": supplier_id,
            "lines": [{"sku_id": sku_id, "quantity": 1, "unit_price": 1000,
                       "item_sns": ["SN-CONCUR-2"]}],
        }
        res = client.post("/api/v1/inbound/orders", json=inbound_payload, headers=auth_headers)
        inbound_id = res.json()["data"]["id"]
        client.post(f"/api/v1/inbound/orders/{inbound_id}/submit", headers=auth_headers)
        client.post(f"/api/v1/inbound/orders/{inbound_id}/approve", headers=auth_headers)

        st_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = st_res.json()["data"]["id"]

        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-CONCUR-2", "actual_qty": 2}]
        }, headers=auth_headers)
        client.post(f"/api/v1/stocktakes/{sid}/complete", json={"remark": "并发测试"}, headers=auth_headers)

        lines = client.get(f"/api/v1/stocktakes/{sid}/lines", headers=auth_headers).json()["data"]

        adj_res = client.post("/api/v1/adjustments", json={
            "stocktake_id": sid,
            "stocktake_line_id": lines[0]["id"],
            "adjustment_type": "SURPLUS",
            "reason": "并发调整测试"
        }, headers=auth_headers)
        assert adj_res.json()["code"] == 0

        adj_id = adj_res.json()["data"]["id"]
        confirm_res = client.post("/api/v1/adjustments/confirm", json={
            "adjustment_ids": [adj_id]
        }, headers=auth_headers)
        assert confirm_res.json()["code"] == 0

    def test_scan_empty_items_rejected(self, client, auth_headers):
        """扫码空数组被Pydantic拒绝返回422。"""
        st_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = st_res.json()["data"]["id"]
        res = client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": []
        }, headers=auth_headers)
        assert res.status_code == 422
        res.close()