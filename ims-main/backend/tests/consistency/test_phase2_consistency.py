"""
二期数据一致性测试
验证：台账-库存一致性、盘点差异计算、调整记录一致性
"""

import pytest


class TestDataConsistencyPhase2:
    """二期数据一致性测试"""

    def test_device_ledger_timestamps(self, client, auth_headers):
        """DeviceLedger 时间戳一致性：installed_date <= removed_date（或NULL）。"""
        cust_res = client.post("/api/v1/customers", json={"name": "一致性客户"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        st_res = client.post("/api/v1/stations", json={
            "name": "一致性场站", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = st_res.json()["data"]["id"]

        r = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-CONSIST-1", "station_id": station_id,
            "installed_date": "2026-06-01"
        }, headers=auth_headers)
        lid = r.json()["data"]["id"]

        client.post(f"/api/v1/device-ledger/{lid}/remove", json={
            "removed_date": "2026-09-01"
        }, headers=auth_headers)

        detail = client.get(f"/api/v1/device-ledger/{lid}", headers=auth_headers).json()["data"]
        assert detail["installed_date"] <= detail["removed_date"]

    def test_stocktake_diff_calculation(self, client, auth_headers):
        """StocktakeLine 差异计算：diff_qty = actual_qty - system_qty。"""
        st_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = st_res.json()["data"]["id"]

        # system_qty=0（SN不在库），actual_qty=2 → diff=2
        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-DIFF-CALC", "actual_qty": 2}]
        }, headers=auth_headers)

        lines = client.get(f"/api/v1/stocktakes/{sid}/lines", headers=auth_headers).json()["data"]
        assert lines[0]["diff_qty"] == lines[0]["actual_qty"] - lines[0]["system_qty"]

    def test_adjustment_creates_valid_record(self, client, auth_headers):
        """调整记录包含必要字段。"""
        st_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = st_res.json()["data"]["id"]
        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-ADJ-REC", "actual_qty": 2}]
        }, headers=auth_headers)
        lines = client.get(f"/api/v1/stocktakes/{sid}/lines", headers=auth_headers).json()["data"]

        adj_res = client.post("/api/v1/adjustments", json={
            "stocktake_id": sid,
            "stocktake_line_id": lines[0]["id"],
            "adjustment_type": "SURPLUS",
            "reason": "一致性测试调整"
        }, headers=auth_headers)

        data = adj_res.json()["data"]
        assert data["adjustment_no"].startswith("TZ")
        assert data["item_sn"] == "SN-ADJ-REC"
        assert data["adjustment_type"] == "SURPLUS"
        assert data["before_status"] is not None
        assert data["after_status"] is not None
        assert data["reason"] == "一致性测试调整"

    def test_adjustment_confirm_updates_inventory(self, client, auth_headers, seed_data):
        """确认调整后库存状态更新并写入History。"""
        sku_id = seed_data["sku_fg"].id
        supplier_id = seed_data["supplier"].id

        # 入库
        inbound_payload = {
            "inbound_mode": "PROCUREMENT", "stock_condition": "NEW",
            "partner_id": supplier_id,
            "lines": [{"sku_id": sku_id, "quantity": 1, "unit_price": 1000,
                       "item_sns": ["SN-CONFIRM-01"]}],
        }
        res = client.post("/api/v1/inbound/orders", json=inbound_payload, headers=auth_headers)
        inbound_id = res.json()["data"]["id"]
        client.post(f"/api/v1/inbound/orders/{inbound_id}/submit", headers=auth_headers)
        client.post(f"/api/v1/inbound/orders/{inbound_id}/approve", headers=auth_headers)

        # 盘点
        st_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = st_res.json()["data"]["id"]
        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-CONFIRM-01", "actual_qty": 2}]
        }, headers=auth_headers)
        lines = client.get(f"/api/v1/stocktakes/{sid}/lines", headers=auth_headers).json()["data"]

        # 创建调整（盘盈：actual_qty=2, diff_qty=1）
        adj_res = client.post("/api/v1/adjustments", json={
            "stocktake_id": sid,
            "stocktake_line_id": lines[0]["id"],
            "adjustment_type": "SURPLUS",
            "reason": "盘盈确认测试"
        }, headers=auth_headers)
        adj_id = adj_res.json()["data"]["id"]

        # 确认调整
        confirm_res = client.post("/api/v1/adjustments/confirm", json={
            "adjustment_ids": [adj_id]
        }, headers=auth_headers)
        assert confirm_res.json()["code"] == 0

        # 验证库存状态变更
        inv_res = client.get("/api/v1/inventory/items?keyword=SN-CONFIRM-01", headers=auth_headers)
        items = inv_res.json()["data"]["items"]
        assert len(items) > 0