"""
场景测试 S003：成品出货 → 关联U9任务单（主线C完整流程）
"""

import pytest


class TestScenarioS003:
    """S003：成品出货 → 关联U9任务单（主线C完整流程）。"""

    def test_full_shipment_flow(self, client, auth_headers, seed_data):
        """完整出货流程：创建出货单 → 查询 → 更新物流信息 → 查询详情。"""
        sku_id = seed_data["sku_fg"].id

        # Step 1: 创建出货单
        shipment_payload = {
            "sku_id": sku_id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": ["SN-S003-001", "SN-S003-002", "SN-S003-003"],
            "quantity": 3,
            "ship_date": "2026-09-08",
            "address": "上海市浦东新区张江高科技园区",
            "logistics_provider": "顺丰速运",
            "tracking_no": "SF8888888888",
            "u9_task_no": "U9-2026-00888",
            "tf_version": "V1.5.2",
            "host_version": "V3.2.0",
            "remark": "S003场景测试",
            "change_reason": "S003出货",
        }
        res = client.post("/api/v1/shipment/", json=shipment_payload, headers=auth_headers)
        assert res.status_code == 201
        shipment = res.json()["data"]
        assert shipment["shipment_no"].startswith("SH")
        assert shipment["u9_task_no"] == "U9-2026-00888"
        assert shipment["sn_list"] == ["SN-S003-001", "SN-S003-002", "SN-S003-003"]
        assert shipment["tf_version"] == "V1.5.2"
        assert shipment["host_version"] == "V3.2.0"
        shipment_id = shipment["id"]

        # Step 2: 查询出货单列表
        res = client.get("/api/v1/shipment/list", headers=auth_headers)
        assert res.status_code == 200
        list_data = res.json()["data"]
        assert list_data["total"] >= 1
        sns = [s["shipment_no"] for s in list_data["items"]]
        assert shipment["shipment_no"] in sns

        # Step 3: 查询出货单详情
        res = client.get(f"/api/v1/shipment/{shipment_id}", headers=auth_headers)
        assert res.status_code == 200
        detail = res.json()["data"]
        assert detail["id"] == shipment_id
        assert detail["shipment_no"] == shipment["shipment_no"]
        assert detail["u9_task_no"] == "U9-2026-00888"

        # Step 4: 更新物流信息
        update_payload = {
            "tracking_no": "SF9999999999",
            "logistics_provider": "京东物流",
            "remark": "S003物流信息已更新",
        }
        res = client.put(f"/api/v1/shipment/{shipment_id}", json=update_payload, headers=auth_headers)
        assert res.status_code == 200

        # Step 5: 验证更新后的数据
        res = client.get(f"/api/v1/shipment/{shipment_id}", headers=auth_headers)
        detail = res.json()["data"]
        assert detail["tracking_no"] == "SF9999999999"
        assert detail["logistics_provider"] == "京东物流"

        # Step 6: 删除出货单
        res = client.delete(f"/api/v1/shipment/{shipment_id}", headers=auth_headers)
        assert res.status_code == 200

        # Step 7: 验证删除后不再可查
        res = client.get(f"/api/v1/shipment/{shipment_id}", headers=auth_headers)
        assert res.json()["code"] != 0

    def test_shipment_with_multiple_sns(self, client, auth_headers, seed_data):
        """多SN出货场景。"""
        sku_id = seed_data["sku_fg"].id
        sns = [f"SN-S003-MULTI-{i:03d}" for i in range(1, 11)]

        shipment_payload = {
            "sku_id": sku_id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": sns,
            "quantity": 10,
            "ship_date": "2026-09-08",
            "address": "广州市天河区",
            "logistics_provider": "德邦物流",
            "tracking_no": "DB0000000001",
            "change_reason": "多SN出货",
        }
        res = client.post("/api/v1/shipment/", json=shipment_payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()["data"]
        assert data["sn_list"] == sns
        assert data["quantity"] == 10

    def test_shipment_without_u9_task(self, client, auth_headers, seed_data):
        """不关联U9任务单的出货场景。"""
        sku_id = seed_data["sku_fg"].id

        shipment_payload = {
            "sku_id": sku_id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": ["SN-S003-NOU9"],
            "quantity": 1,
            "ship_date": "2026-09-08",
            "address": "测试地址",
            "logistics_provider": "测试物流",
            "tracking_no": "TEST000000001",
            "change_reason": "无U9出货",
        }
        res = client.post("/api/v1/shipment/", json=shipment_payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()["data"]
        assert data["u9_task_no"] is None

    def test_shipment_deducts_inventory(self, client, auth_headers, seed_data, db_session):
        """出货登记 → 自动扣减成品库存。"""
        from app.models.inventory import InventoryItem

        sku_id = seed_data["sku_fg"].id

        # 先创建 2 个在库成品
        sns = []
        for i in range(2):
            import uuid
            item_sn = f"SN-C-{uuid.uuid4().hex[:8].upper()}"
            item = InventoryItem(
                item_sn=item_sn,
                sku_id=sku_id,
                stock_status="IN_STOCK",
                stock_condition="NEW",
                operation_status="COMPLETED",
                warehouse_type="FINISHED",
                current_location="库房",
                quantity=1,
            )
            db_session.add(item)
            sns.append(item_sn)
        db_session.flush()

        # 出货
        shipment_payload = {
            "sku_id": sku_id,
            "sku_code": "202-046",
            "sku_name": "测试成品",
            "spec": "规格B",
            "unit": "个",
            "sn_list": sns,
            "quantity": 2,
            "ship_date": "2026-09-08",
            "address": "北京市朝阳区",
            "logistics_provider": "顺丰速运",
            "tracking_no": "SF1234567890",
            "change_reason": "库存扣减测试",
        }
        res = client.post("/api/v1/shipment/", json=shipment_payload, headers=auth_headers)
        assert res.status_code == 201

        # 验证库存已扣减
        for sn in sns:
            item = db_session.query(InventoryItem).filter(InventoryItem.item_sn == sn).first()
            assert item is not None
            assert item.stock_status == "SOLD", f"SN {sn} 应为 SOLD 状态，实际为 {item.stock_status}"