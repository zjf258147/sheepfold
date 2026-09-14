"""
二期单元专项测试：质保期计算、盘点差异计算、台账关联、盘点锁库存
"""

import pytest
from datetime import date, timedelta

from app.service.device_ledger_service import check_warranty
from app.service.stocktake_service import create_stocktake, scan_items, complete_stocktake, get_stocktake_lines


class TestWarrantyCalculation:
    """质保期计算单元测试"""

    def _setup_device(self, db_session, client, auth_headers, item_sn, w_start, w_end):
        from datetime import date
        cust_res = client.post("/api/v1/customers", json={"name": f"质保客户_{item_sn}"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        st_res = client.post("/api/v1/stations", json={
            "name": f"质保场站_{item_sn}", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = st_res.json()["data"]["id"]
        client.post("/api/v1/device-ledger", json={
            "item_sn": item_sn, "station_id": station_id,
            "installed_date": "2026-09-01",
            "warranty_start": str(w_start) if w_start else None,
            "warranty_end": str(w_end) if w_end else None,
        }, headers=auth_headers)

    def test_in_warranty(self, db_session, client, auth_headers):
        """在保期：warranty_end 在未来。"""
        self._setup_device(db_session, client, auth_headers, "SN-WU01",
                          date.today() - timedelta(days=30), date.today() + timedelta(days=335))
        result = check_warranty(db_session, "SN-WU01")
        assert result.in_warranty is True
        assert result.days_remaining > 0

    def test_expired_warranty(self, db_session, client, auth_headers):
        """过期：warranty_end 在过去。"""
        self._setup_device(db_session, client, auth_headers, "SN-WU02",
                          date.today() - timedelta(days=400), date.today() - timedelta(days=1))
        result = check_warranty(db_session, "SN-WU02")
        assert result.in_warranty is False
        assert result.days_remaining < 0

    def test_warranty_today_expiry(self, db_session, client, auth_headers):
        """当天到期：in_warranty = True。"""
        self._setup_device(db_session, client, auth_headers, "SN-WU03",
                          date.today() - timedelta(days=365), date.today())
        result = check_warranty(db_session, "SN-WU03")
        assert result.in_warranty is True
        assert result.days_remaining >= 0

    def test_no_warranty_info(self, db_session, client, auth_headers):
        """无质保信息：warranty_start 和 warranty_end 都为 NULL。"""
        self._setup_device(db_session, client, auth_headers, "SN-WU04", None, None)
        result = check_warranty(db_session, "SN-WU04")
        assert result.in_warranty is False

    def test_warranty_start_null_end_valid(self, db_session, client, auth_headers):
        """warranty_start=NULL, warranty_end=有值，按end判断。"""
        self._setup_device(db_session, client, auth_headers, "SN-WU05", None,
                          date.today() + timedelta(days=100))
        result = check_warranty(db_session, "SN-WU05")
        assert result.in_warranty is True

    def test_warranty_end_null(self, db_session, client, auth_headers):
        """warranty_end=NULL 当前实现视为不在保。"""
        self._setup_device(db_session, client, auth_headers, "SN-WU06",
                          date.today() - timedelta(days=100), None)
        result = check_warranty(db_session, "SN-WU06")
        assert result.in_warranty is False


class TestStocktakeDiff:
    """盘点差异计算单元测试"""

    def _create_inventory_item(self, client, auth_headers, seed_data, item_sn):
        """创建库存单品。"""
        sku_id = seed_data["sku_fg"].id
        supplier_id = seed_data["supplier"].id
        inbound_payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": supplier_id,
            "lines": [{"sku_id": sku_id, "quantity": 1, "unit_price": 1000,
                       "item_sns": [item_sn]}],
        }
        res = client.post("/api/v1/inbound/orders", json=inbound_payload, headers=auth_headers)
        inbound_id = res.json()["data"]["id"]
        client.post(f"/api/v1/inbound/orders/{inbound_id}/submit", headers=auth_headers)
        client.post(f"/api/v1/inbound/orders/{inbound_id}/approve", headers=auth_headers)

    def test_surplus_diff(self, client, auth_headers, seed_data):
        """盘盈：actual_qty > system_qty，diff_qty > 0。"""
        self._create_inventory_item(client, auth_headers, seed_data, "SN-SURPLUS")
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = create_res.json()["data"]["id"]
        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-SURPLUS", "actual_qty": 2}]
        }, headers=auth_headers)
        lines = client.get(f"/api/v1/stocktakes/{sid}/lines", headers=auth_headers).json()["data"]
        assert lines[0]["diff_qty"] > 0

    def test_shortage_diff(self, client, auth_headers, seed_data):
        """盘亏：actual_qty < system_qty，diff_qty < 0。"""
        self._create_inventory_item(client, auth_headers, seed_data, "SN-SHORTAGE")
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = create_res.json()["data"]["id"]
        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-SHORTAGE", "actual_qty": 0}]
        }, headers=auth_headers)
        lines = client.get(f"/api/v1/stocktakes/{sid}/lines", headers=auth_headers).json()["data"]
        assert lines[0]["diff_qty"] < 0

    def test_balanced_diff(self, client, auth_headers, seed_data):
        """持平：actual_qty == system_qty，diff_qty == 0。"""
        self._create_inventory_item(client, auth_headers, seed_data, "SN-BALANCE")
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = create_res.json()["data"]["id"]
        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-BALANCE", "actual_qty": 1}]
        }, headers=auth_headers)
        lines = client.get(f"/api/v1/stocktakes/{sid}/lines", headers=auth_headers).json()["data"]
        assert lines[0]["diff_qty"] == 0

    def test_batch_scan(self, client, auth_headers):
        """批量扫码：多条记录正确创建。"""
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = create_res.json()["data"]["id"]
        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [
                {"item_sn": "SN-BATCH-1", "actual_qty": 1},
                {"item_sn": "SN-BATCH-2", "actual_qty": 3},
                {"item_sn": "SN-BATCH-3", "actual_qty": 0},
            ]
        }, headers=auth_headers)
        lines = client.get(f"/api/v1/stocktakes/{sid}/lines", headers=auth_headers).json()["data"]
        assert len(lines) == 3

    def test_rescan_updates(self, client, auth_headers):
        """重复扫码：更新已有记录。"""
        create_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = create_res.json()["data"]["id"]
        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-RESCAN", "actual_qty": 1}]
        }, headers=auth_headers)
        client.post(f"/api/v1/stocktakes/{sid}/scan", json={
            "items": [{"item_sn": "SN-RESCAN", "actual_qty": 3}]
        }, headers=auth_headers)
        lines = client.get(f"/api/v1/stocktakes/{sid}/lines", headers=auth_headers).json()["data"]
        assert len(lines) == 1
        assert lines[0]["actual_qty"] == 3


class TestDeviceLedgerAssociation:
    """DeviceLedger 关联测试"""

    def _setup_station(self, client, auth_headers, name):
        cust_res = client.post("/api/v1/customers", json={"name": f"台账客户_{name}"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        st_res = client.post("/api/v1/stations", json={
            "name": f"台账场站_{name}", "customer_id": customer_id
        }, headers=auth_headers)
        return st_res.json()["data"]["id"]

    def test_one_to_many_sn_history(self, client, auth_headers):
        """一对多：同一SN可安装到不同场站（先移除再安装）。"""
        st1 = self._setup_station(client, auth_headers, "ST1")
        st2 = self._setup_station(client, auth_headers, "ST2")
        r1 = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-1TOM", "station_id": st1, "installed_date": "2026-01-01"
        }, headers=auth_headers)
        assert r1.json()["code"] == 0
        lid = r1.json()["data"]["id"]
        client.post(f"/api/v1/device-ledger/{lid}/remove", json={
            "removed_date": "2026-06-01"
        }, headers=auth_headers)
        r2 = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-1TOM", "station_id": st2, "installed_date": "2026-06-02"
        }, headers=auth_headers)
        assert r2.json()["code"] == 0

    def test_current_devices_by_station(self, client, auth_headers):
        """当前场站在用设备：按 station_id + status 筛选。"""
        st = self._setup_station(client, auth_headers, "CUR")
        client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-CUR-1", "station_id": st, "installed_date": "2026-01-01"
        }, headers=auth_headers)
        client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-CUR-2", "station_id": st, "installed_date": "2026-02-01"
        }, headers=auth_headers)
        res = client.get(f"/api/v1/device-ledger?station_id={st}&status=RUNNING", headers=auth_headers)
        assert res.json()["code"] == 0
        assert res.json()["data"]["total"] >= 2

    def test_remove_and_reinstall(self, client, auth_headers):
        """移除后再安装到新场站。"""
        st1 = self._setup_station(client, auth_headers, "R1")
        st2 = self._setup_station(client, auth_headers, "R2")
        r = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-REINST", "station_id": st1, "installed_date": "2026-03-01"
        }, headers=auth_headers)
        lid = r.json()["data"]["id"]
        client.post(f"/api/v1/device-ledger/{lid}/remove", json={
            "removed_date": "2026-08-01"
        }, headers=auth_headers)
        r2 = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-REINST", "station_id": st2, "installed_date": "2026-08-15"
        }, headers=auth_headers)
        assert r2.json()["code"] == 0
        assert r2.json()["data"]["station_id"] == st2


class TestStocktakeLock:
    """盘点锁库存测试"""

    def test_create_full_stocktake(self, client, auth_headers):
        """全面盘点创建成功。"""
        res = client.post("/api/v1/stocktakes", json={
            "mode": "FULL", "warehouse": "成品仓"
        }, headers=auth_headers)
        assert res.json()["code"] == 0

    def test_cycle_stocktake_no_lock(self, client, auth_headers):
        """循环盘点不锁库存：多个循环盘点可并存。"""
        r1 = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        assert r1.json()["code"] == 0
        r2 = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "原材料仓"
        }, headers=auth_headers)
        assert r2.json()["code"] == 0

    def test_multiple_full_stocktake(self, client, auth_headers):
        """多个全面盘点可并存（当前不锁）。"""
        r1 = client.post("/api/v1/stocktakes", json={
            "mode": "FULL", "warehouse": "成品仓"
        }, headers=auth_headers)
        assert r1.json()["code"] == 0
        r2 = client.post("/api/v1/stocktakes", json={
            "mode": "FULL", "warehouse": "成品仓"
        }, headers=auth_headers)
        assert r2.json()["code"] == 0

    def test_cancel_releases(self, client, auth_headers):
        """取消盘点后状态变为CANCELLED。"""
        r = client.post("/api/v1/stocktakes", json={
            "mode": "FULL", "warehouse": "成品仓"
        }, headers=auth_headers)
        sid = r.json()["data"]["id"]
        cancel = client.post(f"/api/v1/stocktakes/{sid}/cancel", headers=auth_headers)
        assert cancel.json()["data"]["status"] == "CANCELLED"