"""
库存扣减单元测试。
覆盖：正常扣减、扣减不足、重复扣减。
"""

import pytest
from fastapi.testclient import TestClient


class TestInventoryDeduction:
    """库存扣减相关测试"""

    def test_outbound_deducts_inventory(self, client: TestClient, auth_headers, seed_data):
        """正常出库：入库 → 确认 → 出库 → 库存状态变更。"""
        sku_id = seed_data["sku_fg"].id
        supplier_id = seed_data["supplier"].id

        # Step 1: 创建入库单
        inbound_payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": supplier_id,
            "remark": "库存扣减测试",
            "lines": [
                {
                    "sku_id": sku_id,
                    "quantity": 1,
                    "unit_price": 100,
                    "item_sns": ["SN-DEDUCT-001"],
                }
            ],
        }
        resp = client.post("/api/v1/inbound/orders", json=inbound_payload, headers=auth_headers)
        assert resp.status_code == 201
        inbound_order_id = resp.json()["data"]["id"]

        # Step 2: 提交入库单
        resp = client.post(
            f"/api/v1/inbound/orders/{inbound_order_id}/submit",
            headers=auth_headers,
        )
        assert resp.status_code == 200

        # Step 3: 确认入库
        resp = client.post(
            f"/api/v1/inbound/orders/{inbound_order_id}/approve",
            headers=auth_headers,
        )
        assert resp.status_code == 200

        # Step 4: 验证库存存在
        resp = client.get("/api/v1/inventory/items?keyword=SN-DEDUCT-001", headers=auth_headers)
        assert resp.status_code == 200
        items = resp.json()["data"]["items"]
        in_stock_items = [i for i in items if i["stock_status"] == "IN_STOCK"]
        assert len(in_stock_items) >= 1, f"应有在库单品，实际: {items}"

        # Step 5: 获取库存单品ID，创建出库单
        item_id = in_stock_items[0]["id"]
        outbound_payload = {
            "outbound_type": "SOLD",
            "partner_id": supplier_id,
            "customer_name": "测试客户",
            "remark": "出库扣减测试",
            "item_ids": [item_id],
        }
        resp = client.post("/api/v1/outbound/orders", json=outbound_payload, headers=auth_headers)
        assert resp.status_code == 201
        outbound_data = resp.json()["data"]
        outbound_order_id = outbound_data["id"]

        # Step 6: 提交出库单
        resp = client.post(
            f"/api/v1/outbound/orders/{outbound_order_id}/submit",
            headers=auth_headers,
        )
        assert resp.status_code == 200

        # Step 7: 确认出库
        resp = client.post(
            f"/api/v1/outbound/orders/{outbound_order_id}/approve",
            headers=auth_headers,
        )
        assert resp.status_code == 200

        # Step 8: 验证库存已扣减（状态变为 SOLD）
        resp = client.get("/api/v1/inventory/items?keyword=SN-DEDUCT-001", headers=auth_headers)
        assert resp.status_code == 200
        items = resp.json()["data"]["items"]
        sold_items = [i for i in items if i["stock_status"] == "SOLD"]
        assert len(sold_items) >= 1, f"应有已售出单品，实际: {items}"

    def test_outbound_insufficient_stock(self, client: TestClient, auth_headers, seed_data):
        """出库不存在的库存ID应报错。"""
        supplier_id = seed_data["supplier"].id

        outbound_payload = {
            "outbound_type": "SOLD",
            "partner_id": supplier_id,
            "customer_name": "测试客户",
            "remark": "库存不足测试",
            "item_ids": [99999],
        }
        resp = client.post("/api/v1/outbound/orders", json=outbound_payload, headers=auth_headers)
        # 出库不存在的库存ID应返回错误
        if resp.status_code == 201:
            data = resp.json()
            assert data["code"] != 0, f"应返回错误，实际: {data}"
        else:
            assert resp.status_code in (400, 422)

    def test_concurrent_deduction_same_sn(self, client: TestClient, auth_headers, seed_data):
        """同一库存单品不能重复出库。"""
        sku_id = seed_data["sku_fg"].id
        supplier_id = seed_data["supplier"].id

        # 先入库一个SN
        inbound_payload = {
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": supplier_id,
            "remark": "并发测试",
            "lines": [
                {
                    "sku_id": sku_id,
                    "quantity": 1,
                    "unit_price": 100,
                    "item_sns": ["SN-CONCURRENT-001"],
                }
            ],
        }
        resp = client.post("/api/v1/inbound/orders", json=inbound_payload, headers=auth_headers)
        assert resp.status_code == 201
        inbound_order_id = resp.json()["data"]["id"]

        resp = client.post(
            f"/api/v1/inbound/orders/{inbound_order_id}/submit",
            headers=auth_headers,
        )
        assert resp.status_code == 200

        resp = client.post(
            f"/api/v1/inbound/orders/{inbound_order_id}/approve",
            headers=auth_headers,
        )
        assert resp.status_code == 200

        # 获取库存ID
        resp = client.get("/api/v1/inventory/items?keyword=SN-CONCURRENT-001", headers=auth_headers)
        items = resp.json()["data"]["items"]
        in_stock = [i for i in items if i["stock_status"] == "IN_STOCK"]
        assert len(in_stock) >= 1
        item_id = in_stock[0]["id"]

        # 第一次出库
        outbound_payload = {
            "outbound_type": "SOLD",
            "partner_id": supplier_id,
            "customer_name": "测试客户",
            "remark": "第一次出库",
            "item_ids": [item_id],
        }
        resp = client.post("/api/v1/outbound/orders", json=outbound_payload, headers=auth_headers)
        assert resp.status_code == 201
        outbound_order_id = resp.json()["data"]["id"]

        resp = client.post(
            f"/api/v1/outbound/orders/{outbound_order_id}/submit",
            headers=auth_headers,
        )
        assert resp.status_code == 200

        resp = client.post(
            f"/api/v1/outbound/orders/{outbound_order_id}/approve",
            headers=auth_headers,
        )
        assert resp.status_code == 200

        # 第二次出库同一库存ID应失败
        outbound_payload2 = {
            "outbound_type": "SOLD",
            "partner_id": supplier_id,
            "customer_name": "测试客户",
            "remark": "重复出库",
            "item_ids": [item_id],
        }
        resp = client.post("/api/v1/outbound/orders", json=outbound_payload2, headers=auth_headers)
        if resp.status_code == 201:
            data = resp.json()
            assert data["code"] != 0, f"已经出库的库存不应允许再次出库，实际: {data}"
        else:
            assert resp.status_code in (400, 422)