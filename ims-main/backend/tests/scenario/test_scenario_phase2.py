"""
二期场景测试 S007-S010
S007: 设备出库 → 安装到场站
S008: 设备退回 → 质保判断 → 维修 → 再发出
S009: 全面盘点 → 差异 → 调整
S010: 循环盘点 → 差异 → 调整
"""

import pytest
from datetime import date, timedelta


class TestScenarioS007:
    """S007：设备出库 → 安装到场站"""

    def test_device_outbound_and_install(self, client, auth_headers, seed_data):
        """完整流程：出库 → 创建DeviceLedger → 验证台账。"""
        sku_id = seed_data["sku_fg"].id
        supplier_id = seed_data["supplier"].id

        # 创建客户和场站
        cust_res = client.post("/api/v1/customers", json={
            "name": "S007客户", "contact_person": "李四", "address": "S007地址"
        }, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        st_res = client.post("/api/v1/stations", json={
            "name": "S007场站", "customer_id": customer_id, "address": "S007场站地址"
        }, headers=auth_headers)
        station_id = st_res.json()["data"]["id"]

        # 创建入库单
        inbound_payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": supplier_id,
            "lines": [
                {"sku_id": sku_id, "quantity": 1, "unit_price": 5000,
                 "item_sns": ["SN-S007-01"]}
            ],
        }
        res = client.post("/api/v1/inbound/orders", json=inbound_payload, headers=auth_headers)
        inbound_id = res.json()["data"]["id"]
        client.post(f"/api/v1/inbound/orders/{inbound_id}/submit", headers=auth_headers)
        client.post(f"/api/v1/inbound/orders/{inbound_id}/approve", headers=auth_headers)

        # 创建出库单
        inv_res = client.get("/api/v1/inventory/items?keyword=SN-S007-01", headers=auth_headers)
        items = inv_res.json()["data"]["items"]
        in_stock = [i for i in items if i["stock_status"] == "IN_STOCK"]
        assert len(in_stock) >= 1, "应存在在库单品"
        item_id = in_stock[0]["id"]

        outbound_payload = {
            "outbound_type": "SOLD",
            "partner_id": supplier_id,
            "customer_name": "S007客户",
            "item_ids": [item_id],
        }
        res = client.post("/api/v1/outbound/orders", json=outbound_payload, headers=auth_headers)
        outbound_id = res.json()["data"]["id"]
        client.post(f"/api/v1/outbound/orders/{outbound_id}/submit", headers=auth_headers)
        client.post(f"/api/v1/outbound/orders/{outbound_id}/approve", headers=auth_headers)

        # 登记设备到场站
        dl_res = client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-S007-01", "station_id": station_id,
            "installed_date": str(date.today()),
            "warranty_start": str(date.today()),
            "warranty_end": str(date.today() + timedelta(days=365)),
        }, headers=auth_headers)
        assert dl_res.status_code == 200
        assert dl_res.json()["code"] == 0
        assert dl_res.json()["data"]["item_sn"] == "SN-S007-01"
        assert dl_res.json()["data"]["station_id"] == station_id

        # 验证台账中的 station_name
        detail = client.get(f"/api/v1/device-ledger/{dl_res.json()['data']['id']}", headers=auth_headers)
        assert detail.json()["data"]["station_name"] is not None


class TestScenarioS008:
    """S008：设备退回 → 质保判断 → 维修流程"""

    def test_warranty_check_flow(self, client, auth_headers, seed_data):
        """设备退回时查询质保状态。"""
        # 先创建场景数据：客户→场站→设备台账
        cust_res = client.post("/api/v1/customers", json={"name": "S008客户"}, headers=auth_headers)
        customer_id = cust_res.json()["data"]["id"]
        st_res = client.post("/api/v1/stations", json={
            "name": "S008场站", "customer_id": customer_id
        }, headers=auth_headers)
        station_id = st_res.json()["data"]["id"]

        # 创建在保设备
        client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-S008-IN", "station_id": station_id,
            "installed_date": str(date.today() - timedelta(days=30)),
            "warranty_start": str(date.today() - timedelta(days=30)),
            "warranty_end": str(date.today() + timedelta(days=335)),
        }, headers=auth_headers)

        # 创建过期设备
        client.post("/api/v1/device-ledger", json={
            "item_sn": "SN-S008-OUT", "station_id": station_id,
            "installed_date": str(date.today() - timedelta(days=400)),
            "warranty_start": str(date.today() - timedelta(days=400)),
            "warranty_end": str(date.today() - timedelta(days=1)),
        }, headers=auth_headers)

        # 查询在保设备质保
        w1 = client.get("/api/v1/device-ledger/warranty/SN-S008-IN", headers=auth_headers)
        assert w1.json()["code"] == 0
        assert w1.json()["data"]["in_warranty"] is True
        assert w1.json()["data"]["days_remaining"] > 0

        # 查询过期设备质保
        w2 = client.get("/api/v1/device-ledger/warranty/SN-S008-OUT", headers=auth_headers)
        assert w2.json()["code"] == 0
        assert w2.json()["data"]["in_warranty"] is False


class TestScenarioS009:
    """S009：全面盘点 → 差异 → 调整"""

    def test_full_stocktake_with_adjustment(self, client, auth_headers, seed_data):
        """全面盘点完整流程。"""
        sku_id = seed_data["sku_fg"].id
        supplier_id = seed_data["supplier"].id

        # 入库一个SN
        inbound_payload = {
            "inbound_mode": "PROCUREMENT", "stock_condition": "NEW",
            "partner_id": supplier_id,
            "lines": [{"sku_id": sku_id, "quantity": 1, "unit_price": 3000,
                       "item_sns": ["SN-S009-01"]}],
        }
        res = client.post("/api/v1/inbound/orders", json=inbound_payload, headers=auth_headers)
        inbound_id = res.json()["data"]["id"]
        client.post(f"/api/v1/inbound/orders/{inbound_id}/submit", headers=auth_headers)
        client.post(f"/api/v1/inbound/orders/{inbound_id}/approve", headers=auth_headers)

        # 创建全面盘点
        st_res = client.post("/api/v1/stocktakes", json={
            "mode": "FULL", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = st_res.json()["data"]["id"]

        # 扫码盘点（模拟盘盈：system_qty=1，actual_qty=2）
        client.post(f"/api/v1/stocktakes/{stocktake_id}/scan", json={
            "items": [{"item_sn": "SN-S009-01", "actual_qty": 2}]
        }, headers=auth_headers)

        # 验证差异
        lines = client.get(f"/api/v1/stocktakes/{stocktake_id}/lines", headers=auth_headers).json()["data"]
        assert lines[0]["diff_qty"] == 1

        # 完成盘点
        client.post(f"/api/v1/stocktakes/{stocktake_id}/complete", json={"remark": "S009完成"}, headers=auth_headers)

        # 创建盘盈调整
        adj_res = client.post("/api/v1/adjustments", json={
            "stocktake_id": stocktake_id,
            "stocktake_line_id": lines[0]["id"],
            "adjustment_type": "SURPLUS",
            "reason": "S009盘盈调整"
        }, headers=auth_headers)
        assert adj_res.json()["code"] == 0
        assert adj_res.json()["data"]["adjustment_no"].startswith("TZ")


class TestScenarioS010:
    """S010：循环盘点 → 差异 → 调整"""

    def test_cycle_stocktake_with_adjustment(self, client, auth_headers, seed_data):
        """循环盘点完整流程。"""
        sku_id = seed_data["sku_fg"].id
        supplier_id = seed_data["supplier"].id

        # 入库
        inbound_payload = {
            "inbound_mode": "PROCUREMENT", "stock_condition": "NEW",
            "partner_id": supplier_id,
            "lines": [{"sku_id": sku_id, "quantity": 1, "unit_price": 2000,
                       "item_sns": ["SN-S010-01"]}],
        }
        res = client.post("/api/v1/inbound/orders", json=inbound_payload, headers=auth_headers)
        inbound_id = res.json()["data"]["id"]
        client.post(f"/api/v1/inbound/orders/{inbound_id}/submit", headers=auth_headers)
        client.post(f"/api/v1/inbound/orders/{inbound_id}/approve", headers=auth_headers)

        # 循环盘点不锁库存
        st_res = client.post("/api/v1/stocktakes", json={
            "mode": "CYCLE", "warehouse": "成品仓"
        }, headers=auth_headers)
        stocktake_id = st_res.json()["data"]["id"]

        # 扫码盘点（模拟盘亏：system_qty=1，actual_qty=0）
        client.post(f"/api/v1/stocktakes/{stocktake_id}/scan", json={
            "items": [{"item_sn": "SN-S010-01", "actual_qty": 0}]
        }, headers=auth_headers)

        lines = client.get(f"/api/v1/stocktakes/{stocktake_id}/lines", headers=auth_headers).json()["data"]
        assert lines[0]["diff_qty"] == -1

        # 完成盘点
        client.post(f"/api/v1/stocktakes/{stocktake_id}/complete", json={"remark": "S010完成"}, headers=auth_headers)

        # 创建盘亏调整
        adj_res = client.post("/api/v1/adjustments", json={
            "stocktake_id": stocktake_id,
            "stocktake_line_id": lines[0]["id"],
            "adjustment_type": "SHORTAGE",
            "reason": "S010盘亏调整"
        }, headers=auth_headers)
        assert adj_res.json()["code"] == 0