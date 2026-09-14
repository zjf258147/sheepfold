"""
场景测试 S004：BOM导入 → 库存对比 → 生成采购建议（主线D完整流程）
"""

import pytest


class TestScenarioS004:
    """S004：BOM 导入 → 库存对比 → 生成采购建议（主线D完整流程）。"""

    def test_bom_availability_analysis(self, client, auth_headers, seed_data):
        """BOM创建 → 齐套分析 → 库存对比。"""
        sku_raw = seed_data["sku_raw"].id
        sku_fg = seed_data["sku_fg"].id

        # Step 1: 创建 BOM（单物料）
        bom_payload = {
            "bom_name": "S004-测试BOM",
            "version": "V1.0",
            "product_sku_id": sku_fg,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 100,
            "status": "PUBLISHED",
            "remark": "S004场景测试",
            "change_reason": "S004创建BOM",
            "details": [
                {
                    "material_sku_id": sku_raw,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 2.0,
                    "wastage_rate": 0.05,
                    "level": 2,
                    "process_note": "焊接工序",
                    "remark": "关键物料",
                }
            ],
        }
        res = client.post("/api/v1/bom/", json=bom_payload, headers=auth_headers)
        assert res.status_code == 201
        bom = res.json()["data"]
        assert bom["bom_no"] is not None
        assert bom["bom_name"] == "S004-测试BOM"
        assert bom["status"] == "PUBLISHED"
        assert len(bom["details"]) == 1
        bom_id = bom["id"]

        # Step 2: 齐套分析
        res = client.get(f"/api/v1/bom/{bom_id}/availability", headers=auth_headers)
        assert res.status_code == 200
        availability = res.json()["data"]
        assert availability["bom_id"] == bom_id
        assert "items" in availability
        assert len(availability["items"]) == 1
        assert availability["items"][0]["material_sku_code"] == "202-018"
        assert availability["items"][0]["required_qty"] == 200.0

        # Step 3: 创建生产任务
        task_payload = {
            "bom_id": bom_id,
            "plan_quantity": 50,
            "start_date": "2026-09-08",
            "end_date": "2026-10-08",
            "change_reason": "S004生产任务",
        }
        res = client.post("/api/v1/production-task/", json=task_payload, headers=auth_headers)
        assert res.status_code == 201
        task = res.json()["data"]
        assert task["task_no"] is not None
        assert task["bom_id"] == bom_id
        assert task["plan_quantity"] == 50

    def test_bom_with_multiple_materials(self, client, auth_headers, seed_data):
        """BOM 多物料齐套分析。"""
        sku_fg = seed_data["sku_fg"].id
        sku_raw = seed_data["sku_raw"].id

        bom_payload = {
            "bom_name": "S004-多物料BOM",
            "version": "V1.0",
            "product_sku_id": sku_fg,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 50,
            "status": "PUBLISHED",
            "change_reason": "S004多物料",
            "details": [
                {
                    "material_sku_id": sku_raw,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 2.0,
                    "wastage_rate": 0.03,
                    "level": 2,
                    "process_note": "焊接工序",
                },
                {
                    "material_sku_id": sku_raw,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 1.0,
                    "wastage_rate": 0.0,
                    "level": 2,
                    "process_note": "组装工序",
                },
            ],
        }
        res = client.post("/api/v1/bom/", json=bom_payload, headers=auth_headers)
        assert res.status_code == 201
        bom_id = res.json()["data"]["id"]

        res = client.get(f"/api/v1/bom/{bom_id}/availability", headers=auth_headers)
        assert res.status_code == 200
        availability = res.json()["data"]
        assert len(availability["items"]) == 2
        assert availability["overall_sufficient"] is False

    def test_bom_lifecycle(self, client, auth_headers, seed_data):
        """BOM 生命周期：创建 → 发布 → 更新 → 删除。"""
        sku_fg = seed_data["sku_fg"].id
        sku_raw = seed_data["sku_raw"].id

        # 创建草稿
        bom_payload = {
            "bom_name": "S004-生命周期BOM",
            "version": "V1.0",
            "product_sku_id": sku_fg,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 10,
            "status": "DRAFT",
            "change_reason": "创建草稿",
            "details": [
                {
                    "material_sku_id": sku_raw,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 1.0,
                    "level": 2,
                }
            ],
        }
        res = client.post("/api/v1/bom/", json=bom_payload, headers=auth_headers)
        assert res.status_code == 201
        bom_id = res.json()["data"]["id"]

        detail = client.get(f"/api/v1/bom/{bom_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "DRAFT"

        # 发布
        res = client.put(
            f"/api/v1/bom/{bom_id}",
            json={"change_reason": "发布", "status": "PUBLISHED"},
            headers=auth_headers,
        )
        assert res.status_code == 200

        detail = client.get(f"/api/v1/bom/{bom_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "PUBLISHED"

        # 删除
        res = client.delete(f"/api/v1/bom/{bom_id}", headers=auth_headers)
        assert res.status_code == 200

        res = client.get(f"/api/v1/bom/{bom_id}", headers=auth_headers)
        assert res.json()["code"] != 0

    def test_complete_task_creates_inventory(self, client, auth_headers, seed_data, db_session):
        """生产任务完成 → 自动创建成品库存。"""
        sku_fg = seed_data["sku_fg"].id
        sku_raw = seed_data["sku_raw"].id

        # 创建 BOM
        bom_payload = {
            "bom_name": "S004-成品入库测试",
            "version": "V1.0",
            "product_sku_id": sku_fg,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 3,
            "status": "PUBLISHED",
            "change_reason": "完成入库测试",
            "details": [
                {
                    "material_sku_id": sku_raw,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 1.0,
                    "level": 2,
                }
            ],
        }
        res = client.post("/api/v1/bom/", json=bom_payload, headers=auth_headers)
        assert res.status_code == 201
        bom_id = res.json()["data"]["id"]

        # 创建生产任务（成品类型）
        task_payload = {
            "bom_id": bom_id,
            "plan_quantity": 3,
            "product_type": "FINISHED_PRODUCT",
            "change_reason": "完成入库测试",
        }
        res = client.post("/api/v1/production-task/", json=task_payload, headers=auth_headers)
        assert res.status_code == 201
        task_id = res.json()["data"]["id"]
        assert res.json()["data"]["product_type"] == "FINISHED_PRODUCT"

        # 将任务状态改为已完成
        res = client.put(
            f"/api/v1/production-task/{task_id}",
            json={"status": "COMPLETED", "change_reason": "任务完成"},
            headers=auth_headers,
        )
        assert res.status_code == 200
        assert res.json()["data"]["status"] == "COMPLETED"

        # 验证库存中创建了 3 个成品单品
        from app.models.inventory import InventoryItem
        items = db_session.query(InventoryItem).filter(
            InventoryItem.sku_id == sku_fg,
            InventoryItem.warehouse_type == "FINISHED",
        ).all()
        assert len(items) == 3, f"预期3个成品库存，实际{len(items)}"
        for item in items:
            assert item.stock_status == "IN_STOCK"
            assert item.warehouse_type == "FINISHED"

    def test_complete_task_semi_finished(self, client, auth_headers, seed_data, db_session):
        """生产任务完成 → 半成品入库。"""
        sku_fg = seed_data["sku_fg"].id
        sku_raw = seed_data["sku_raw"].id

        bom_payload = {
            "bom_name": "S004-半成品入库测试",
            "version": "V1.0",
            "product_sku_id": sku_fg,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 2,
            "status": "PUBLISHED",
            "change_reason": "半成品测试",
            "details": [
                {
                    "material_sku_id": sku_raw,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 1.0,
                    "level": 2,
                }
            ],
        }
        res = client.post("/api/v1/bom/", json=bom_payload, headers=auth_headers)
        assert res.status_code == 201
        bom_id = res.json()["data"]["id"]

        task_payload = {
            "bom_id": bom_id,
            "plan_quantity": 2,
            "product_type": "SEMI_FINISHED",
            "change_reason": "半成品测试",
        }
        res = client.post("/api/v1/production-task/", json=task_payload, headers=auth_headers)
        assert res.status_code == 201
        task_id = res.json()["data"]["id"]
        assert res.json()["data"]["product_type"] == "SEMI_FINISHED"

        res = client.put(
            f"/api/v1/production-task/{task_id}",
            json={"status": "COMPLETED", "change_reason": "完成"},
            headers=auth_headers,
        )
        assert res.status_code == 200

        from app.models.inventory import InventoryItem
        items = db_session.query(InventoryItem).filter(
            InventoryItem.sku_id == sku_fg,
            InventoryItem.warehouse_type == "SEMI_FINISHED",
        ).all()
        assert len(items) == 2, f"预期2个半成品库存，实际{len(items)}"
        for item in items:
            assert item.warehouse_type == "SEMI_FINISHED"