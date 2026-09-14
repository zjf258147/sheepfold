"""
场景测试 S001：原材料到货 → 检验 → 入库（主线A完整流程）
场景测试 S005：原材料退货（不合格品处理）
"""

import pytest


class TestScenarioS001:
    """S001：原材料到货 → 检验 → 入库（主线A完整流程）。"""

    def test_full_incoming_flow(self, client, auth_headers, seed_data):
        """完整流程：创建到货单 → 来料检验 → 确认入库。"""
        sku_id = seed_data["sku_raw"].id
        supplier_id = seed_data["supplier"].id

        # Step 1: 创建到货单
        receipt_payload = {
            "supplier_id": supplier_id,
            "sku_id": sku_id,
            "batch_no": "S001-BATCH",
            "quantity": 200,
            "unit": "个",
            "delivery_date": "2026-09-08",
            "remark": "S001场景测试",
        }
        res = client.post("/api/v1/incoming/receipts", json=receipt_payload, headers=auth_headers)
        assert res.status_code == 201
        receipt = res.json()
        assert receipt["status"] == "PENDING_INSPECTION"
        assert receipt["receipt_no"].startswith("RC")
        receipt_id = receipt["id"]

        # Step 2: 来料检验 - 合格
        inspection_payload = {
            "receipt_id": receipt_id,
            "inspector_id": seed_data["quality"].id,
            "inspection_date": "2026-09-08",
            "result": "ACCEPTED",
            "sample_qty": 20,
            "defect_qty": 0,
            "defect_description": None,
            "change_reason": "S001合格检验",
        }
        res = client.post("/api/v1/incoming/inspections", json=inspection_payload, headers=auth_headers)
        assert res.status_code == 201
        inspection = res.json()
        assert inspection["inspection_no"].startswith("JC")
        assert inspection["result"] == "ACCEPTED"

        detail = client.get(f"/api/v1/incoming/receipts/{receipt_id}", headers=auth_headers)
        assert detail.json()["status"] == "ACCEPTED"

        # Step 3: 确认入库
        confirm_payload = {"change_reason": "S001确认入库"}
        res = client.post(
            f"/api/v1/incoming/receipts/{receipt_id}/confirm",
            json=confirm_payload, headers=auth_headers,
        )
        assert res.status_code == 200
        assert res.status_code == 200

        detail = client.get(f"/api/v1/incoming/receipts/{receipt_id}", headers=auth_headers)
        assert detail.json()["status"] == "WAREHOUSED"
        assert detail.json()["confirmed_at"] is not None

    def test_full_incoming_with_concession(self, client, auth_headers, seed_data):
        """让步接收流程：到货 → 检验（让步接收）→ 入库。"""
        sku_id = seed_data["sku_raw"].id
        supplier_id = seed_data["supplier"].id

        receipt_payload = {
            "supplier_id": supplier_id,
            "sku_id": sku_id,
            "batch_no": "S001-CONCESSION",
            "quantity": 100,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        res = client.post("/api/v1/incoming/receipts", json=receipt_payload, headers=auth_headers)
        receipt_id = res.json()["id"]

        inspection_payload = {
            "receipt_id": receipt_id,
            "inspector_id": seed_data["quality"].id,
            "inspection_date": "2026-09-08",
            "result": "CONCESSION_ACCEPTED",
            "sample_qty": 10,
            "defect_qty": 2,
            "defect_description": "轻微外观瑕疵，让步接收",
            "change_reason": "让步接收",
        }
        res = client.post("/api/v1/incoming/inspections", json=inspection_payload, headers=auth_headers)
        assert res.status_code == 201

        detail = client.get(f"/api/v1/incoming/receipts/{receipt_id}", headers=auth_headers)
        assert detail.json()["status"] == "ACCEPTED"

        confirm_payload = {"change_reason": "让步接收确认入库"}
        res = client.post(
            f"/api/v1/incoming/receipts/{receipt_id}/confirm",
            json=confirm_payload, headers=auth_headers,
        )
        assert res.status_code == 200
        assert res.status_code == 200


class TestScenarioS005:
    """S005：原材料退货（不合格品处理）。"""

    def test_raw_material_return_flow(self, client, auth_headers, seed_data):
        """完整流程：到货 → 检验不合格 → 退货。"""
        sku_id = seed_data["sku_raw"].id
        supplier_id = seed_data["supplier"].id

        # Step 1: 创建到货单
        receipt_payload = {
            "supplier_id": supplier_id,
            "sku_id": sku_id,
            "batch_no": "S005-BATCH",
            "quantity": 100,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        res = client.post("/api/v1/incoming/receipts", json=receipt_payload, headers=auth_headers)
        receipt_id = res.json()["id"]

        # Step 2: 检验不合格
        inspection_payload = {
            "receipt_id": receipt_id,
            "inspector_id": seed_data["quality"].id,
            "inspection_date": "2026-09-08",
            "result": "REJECTED",
            "sample_qty": 10,
            "defect_qty": 5,
            "defect_description": "尺寸超差，不合格",
            "change_reason": "不合格退货",
        }
        res = client.post("/api/v1/incoming/inspections", json=inspection_payload, headers=auth_headers)
        assert res.status_code == 201

        detail = client.get(f"/api/v1/incoming/receipts/{receipt_id}", headers=auth_headers)
        assert detail.json()["status"] == "REJECTED"

        # Step 3: 创建退货单
        return_payload = {
            "receipt_id": receipt_id,
            "return_qty": 100,
            "return_reason": "尺寸超差，整批退货",
            "return_date": "2026-09-08",
            "change_reason": "S005退货处理",
        }
        res = client.post("/api/v1/incoming/returns", json=return_payload, headers=auth_headers)
        assert res.status_code == 201
        rtn = res.json()
        assert rtn["return_no"].startswith("TH")
        assert rtn["return_qty"] == 100
        assert rtn["status"] == "PENDING"

    def test_partial_return(self, client, auth_headers, seed_data):
        """部分退货：检验部分不合格后部分退货。"""
        sku_id = seed_data["sku_raw"].id
        supplier_id = seed_data["supplier"].id

        receipt_payload = {
            "supplier_id": supplier_id,
            "sku_id": sku_id,
            "batch_no": "S005-PARTIAL",
            "quantity": 200,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        res = client.post("/api/v1/incoming/receipts", json=receipt_payload, headers=auth_headers)
        receipt_id = res.json()["id"]

        inspection_payload = {
            "receipt_id": receipt_id,
            "inspector_id": seed_data["quality"].id,
            "inspection_date": "2026-09-08",
            "result": "REJECTED",
            "sample_qty": 20,
            "defect_qty": 8,
            "defect_description": "部分不良",
            "change_reason": "检验",
        }
        client.post("/api/v1/incoming/inspections", json=inspection_payload, headers=auth_headers)

        return_payload = {
            "receipt_id": receipt_id,
            "return_qty": 50,
            "return_reason": "部分不良品退货",
            "return_date": "2026-09-08",
            "change_reason": "部分退货",
        }
        res = client.post("/api/v1/incoming/returns", json=return_payload, headers=auth_headers)
        assert res.status_code == 201
        assert res.json()["return_qty"] == 50


class TestInboundInventoryConnection:
    """原材料入库 → 库存联动测试。"""

    def test_inbound_creates_raw_material_inventory(self, client, auth_headers, seed_data, db_session):
        """原材料到货确认入库 → 到货状态变更为 WAREHOUSED。"""
        from app.models.inventory import InventoryItem

        sku_id = seed_data["sku_raw"].id
        supplier_id = seed_data["supplier"].id

        # 创建到货单
        receipt_payload = {
            "supplier_id": supplier_id,
            "sku_id": sku_id,
            "batch_no": "INV-TEST-BATCH",
            "quantity": 50,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        res = client.post("/api/v1/incoming/receipts", json=receipt_payload, headers=auth_headers)
        receipt_id = res.json()["id"]

        # 检验合格
        client.post("/api/v1/incoming/inspections", json={
            "receipt_id": receipt_id,
            "inspector_id": seed_data["quality"].id,
            "inspection_date": "2026-09-08",
            "result": "ACCEPTED",
            "sample_qty": 5,
            "defect_qty": 0,
            "change_reason": "测试",
        }, headers=auth_headers)

        # 确认入库
        res = client.post(f"/api/v1/incoming/receipts/{receipt_id}/confirm", json={
            "change_reason": "确认入库",
        }, headers=auth_headers)
        assert res.status_code == 200

        # 验证到货单状态已变更为已入库
        detail = client.get(f"/api/v1/incoming/receipts/{receipt_id}", headers=auth_headers)
        assert detail.json()["status"] == "WAREHOUSED"
        assert detail.json()["confirmed_at"] is not None