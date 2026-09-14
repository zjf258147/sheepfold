"""
场景测试 S002：成品返厂 → 诊断 → 维修 → 换SN → 再出货（主线B完整流程）
场景测试 S006：报废审批（发起 → 审批 → 通过/驳回）
"""

import pytest


class TestScenarioS002:
    """S002：成品返厂 → 诊断 → 维修 → 换SN → 再出货（主线B完整流程）。"""

    def test_full_rma_repair_flow(self, client, auth_headers, seed_data, db_session):
        """完整返厂维修流程：退货登记 → 诊断 → 分配 → 维修 → 质检 → 入库 → 再出货。"""
        sku_id = seed_data["sku_fg"].id

        # Step 1: 退货登记
        return_payload = {
            "sku_id": sku_id,
            "sn": "SN-S002-FULL",
            "quantity": 1,
            "unit": "个",
            "customer_name": "S002场景客户",
            "return_reason": "设备运行异常",
            "return_date": "2026-09-01",
            "remark": "S002场景测试",
        }
        res = client.post("/api/v1/rma/returns", json=return_payload, headers=auth_headers)
        assert res.status_code == 201
        rma = res.json()
        assert rma["status"] == "PENDING_DIAGNOSIS"
        assert rma["return_no"].startswith("FC")
        return_id = rma["id"]

        # Step 2: 诊断报告
        diagnosis_payload = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-02",
            "fault_description": "电源模块输出电压异常，主板部分电容老化",
            "diagnosis_result": "REPAIRABLE",
            "repair_plan": "更换电源模块，更换主板电容",
            "inspection_report_no": "JY-2026-001",
            "change_reason": "S002诊断",
        }
        res = client.post("/api/v1/rma/diagnoses", json=diagnosis_payload, headers=auth_headers)
        assert res.status_code == 201
        assert res.json()["diagnosis_no"].startswith("DG")

        detail = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "DIAGNOSED"

        # Step 3: 分配
        assign_payload = {
            "assigned_to": seed_data["production"].id,
            "assign_type": "PRODUCTION",
            "assign_reason": "分配给生产部门维修",
            "change_reason": "S002分配",
        }
        res = client.post(
            f"/api/v1/rma/returns/{return_id}/assign",
            json=assign_payload, headers=auth_headers,
        )
        assert res.status_code == 200

        detail = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "ASSIGNED"

        # Step 4: 维修工单（换SN）
        repair_payload = {
            "return_id": return_id,
            "repair_by": seed_data["production"].id,
            "old_sn": "SN-S002-FULL",
            "new_sn": "SN-S002-FULL-REPAIRED",
            "repair_description": "更换电源模块和主板电容",
            "materials_used": "电源模块x1, 电容x3",
            "fault_code": "E002",
            "start_time": "2026-09-03T09:00:00",
            "end_time": "2026-09-03T14:00:00",
            "repair_date": "2026-09-03",
            "change_reason": "S002维修",
        }
        res = client.post("/api/v1/rma/repairs", json=repair_payload, headers=auth_headers)
        assert res.status_code == 201
        repair = res.json()
        assert repair["repair_no"].startswith("WX")
        assert repair["new_sn"] == "SN-S002-FULL-REPAIRED"

        detail = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "REPAIRED"
        assert detail.json()["data"]["new_sn"] == "SN-S002-FULL-REPAIRED"

        # Step 5: 质量检验
        qc_payload = {
            "return_id": return_id,
            "checked_by": seed_data["quality"].id,
            "check_date": "2026-09-04",
            "check_result": "PASS",
            "check_description": "维修后各项指标合格",
            "change_reason": "S002质检",
        }
        res = client.post("/api/v1/rma/quality-checks", json=qc_payload, headers=auth_headers)
        assert res.status_code == 201

        detail = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "QUALITY_CHECK"

        # Step 6: 入库
        wh_payload = {
            "return_id": return_id,
            "new_sn": "SN-S002-FULL-REPAIRED",
            "repair_count": 1,
            "repair_reason": "更换电源模块",
            "change_reason": "S002入库",
        }
        res = client.post("/api/v1/rma/warehouse-ins", json=wh_payload, headers=auth_headers)
        assert res.status_code == 201

        detail = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "WAREHOUSED"

        # SN 关联逻辑验证：旧SN应指向新SN，新SN应指向旧SN
        from app.models.inventory import InventoryItem
        old_item = db_session.query(InventoryItem).filter(InventoryItem.item_sn == "SN-S002-FULL").first()
        new_item = db_session.query(InventoryItem).filter(InventoryItem.item_sn == "SN-S002-FULL-REPAIRED").first()
        if old_item:
            assert old_item.replaced_by_sn == "SN-S002-FULL-REPAIRED", \
                f"旧SN应指向新SN，实际: {old_item.replaced_by_sn}"
            assert old_item.stock_status == "REPLACED", \
                f"旧SN状态应为REPLACED，实际: {old_item.stock_status}"
        if new_item:
            assert new_item.replaced_from_sn == "SN-S002-FULL", \
                f"新SN应指向旧SN，实际: {new_item.replaced_from_sn}"

        # Step 7: 再出货
        reship_payload = {
            "return_id": return_id,
            "new_sn": "SN-S002-FULL-REPAIRED",
            "software_version": "V2.0.5",
            "ship_date": "2026-09-05",
            "recipient": "S002场景客户",
            "change_reason": "S002再出货",
        }
        res = client.post("/api/v1/rma/reships", json=reship_payload, headers=auth_headers)
        assert res.status_code == 201
        reship = res.json()
        assert reship["reship_no"].startswith("RH")
        assert reship["software_version"] == "V2.0.5"

        detail = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "RESHIPPED"

    def test_direct_reship_flow(self, client, auth_headers, seed_data):
        """诊断结论为可直接再出货的流程。"""
        sku_id = seed_data["sku_fg"].id

        return_payload = {
            "sku_id": sku_id,
            "sn": "SN-S002-DIRECT",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "误退回",
            "return_date": "2026-09-01",
        }
        res = client.post("/api/v1/rma/returns", json=return_payload, headers=auth_headers)
        return_id = res.json()["id"]

        diagnosis_payload = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-02",
            "fault_description": "设备无故障，客户误退回",
            "diagnosis_result": "DIRECT_RESHIP",
            "change_reason": "诊断",
        }
        res = client.post("/api/v1/rma/diagnoses", json=diagnosis_payload, headers=auth_headers)
        assert res.status_code == 201

        detail = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert detail.json()["data"]["diagnosis_result"] == "DIRECT_RESHIP"


class TestScenarioS006:
    """S006：报废审批（发起 → 审批 → 通过/驳回）。"""

    def test_scrap_approve_flow(self, client, auth_headers, seed_data):
        """报废审批通过流程。"""
        sku_id = seed_data["sku_fg"].id

        # Step 1: 创建返厂退货单
        return_payload = {
            "sku_id": sku_id,
            "sn": "SN-S006-APPROVE",
            "quantity": 1,
            "unit": "个",
            "customer_name": "S006客户",
            "return_reason": "设备严重损坏",
            "return_date": "2026-09-01",
        }
        res = client.post("/api/v1/rma/returns", json=return_payload, headers=auth_headers)
        return_id = res.json()["id"]

        # Step 2: 诊断结果为 SCRAP
        diagnosis_payload = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-02",
            "fault_description": "主板烧毁，外壳破损，无法修复",
            "diagnosis_result": "SCRAP",
            "change_reason": "诊断",
        }
        res = client.post("/api/v1/rma/diagnoses", json=diagnosis_payload, headers=auth_headers)
        assert res.status_code == 201

        # Step 3: 发起报废申请
        scrap_payload = {
            "return_id": return_id,
            "scrap_reason": "主板烧毁，外壳破损，维修成本高于新设备",
            "change_reason": "S006报废申请",
        }
        res = client.post("/api/v1/rma/scraps", json=scrap_payload, headers=auth_headers)
        assert res.status_code == 201
        scrap = res.json()
        assert scrap["scrap_no"].startswith("BF")
        assert scrap["status"] == "PENDING"
        scrap_id = scrap["id"]

        # Step 4: 审批通过
        approve_payload = {"change_reason": "同意报废，已核实情况"}
        res = client.post(
            f"/api/v1/rma/scraps/{scrap_id}/approve",
            json=approve_payload, headers=auth_headers,
        )
        assert res.status_code == 200
        assert res.status_code == 200

    def test_scrap_reject_flow(self, client, auth_headers, seed_data):
        """报废审批驳回流程。"""
        sku_id = seed_data["sku_fg"].id

        return_payload = {
            "sku_id": sku_id,
            "sn": "SN-S006-REJECT",
            "quantity": 1,
            "unit": "个",
            "customer_name": "S006客户",
            "return_reason": "设备损坏",
            "return_date": "2026-09-01",
        }
        res = client.post("/api/v1/rma/returns", json=return_payload, headers=auth_headers)
        return_id = res.json()["id"]

        diagnosis_payload = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-02",
            "fault_description": "部分损坏",
            "diagnosis_result": "SCRAP",
            "change_reason": "诊断",
        }
        client.post("/api/v1/rma/diagnoses", json=diagnosis_payload, headers=auth_headers)

        scrap_payload = {
            "return_id": return_id,
            "scrap_reason": "建议报废",
            "change_reason": "报废申请",
        }
        res = client.post("/api/v1/rma/scraps", json=scrap_payload, headers=auth_headers)
        scrap_id = res.json()["id"]

        # 审批驳回
        approve_payload = {
            "change_reason": "驳回报废申请",
            "reject_reason": "设备仍有维修价值，请重新评估",
        }
        res = client.post(
            f"/api/v1/rma/scraps/{scrap_id}/approve",
            json=approve_payload, headers=auth_headers,
        )
        assert res.status_code == 200


class TestRMAInventoryConnection:
    """RMA 入库 → 库存联动测试。"""

    def test_warehouse_in_creates_inventory(self, client, auth_headers, seed_data, db_session):
        """RMA 入库 → 自动创建零成本仓库存。"""
        from app.models.inventory import InventoryItem

        sku_id = seed_data["sku_fg"].id

        # 创建返厂单
        return_payload = {
            "sku_id": sku_id,
            "sn": "SN-RMA-INV-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "库存联动测试",
            "return_reason": "测试库存联动",
            "return_date": "2026-09-01",
        }
        res = client.post("/api/v1/rma/returns", json=return_payload, headers=auth_headers)
        return_id = res.json()["id"]

        # 诊断
        client.post("/api/v1/rma/diagnoses", json={
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-02",
            "fault_description": "测试",
            "diagnosis_result": "REPAIRABLE",
            "change_reason": "测试",
        }, headers=auth_headers)

        # 分配
        client.post(f"/api/v1/rma/returns/{return_id}/assign", json={
            "assigned_to": seed_data["production"].id,
            "assign_type": "PRODUCTION",
            "assign_reason": "测试",
            "change_reason": "测试",
        }, headers=auth_headers)

        # 维修
        client.post("/api/v1/rma/repairs", json={
            "return_id": return_id,
            "repair_by": seed_data["production"].id,
            "old_sn": "SN-RMA-INV-001",
            "new_sn": "SN-RMA-INV-001-NEW",
            "repair_description": "测试维修",
            "start_time": "2026-09-03T09:00:00",
            "end_time": "2026-09-03T12:00:00",
            "repair_date": "2026-09-03",
            "change_reason": "测试",
        }, headers=auth_headers)

        # 质检
        client.post("/api/v1/rma/quality-checks", json={
            "return_id": return_id,
            "checked_by": seed_data["quality"].id,
            "check_date": "2026-09-04",
            "check_result": "PASS",
            "check_description": "测试通过",
            "change_reason": "测试",
        }, headers=auth_headers)

        # 入库 - 零成本仓-成品
        res = client.post("/api/v1/rma/warehouse-ins", json={
            "return_id": return_id,
            "new_sn": "SN-RMA-INV-001-NEW",
            "repair_count": 1,
            "repair_reason": "测试维修",
            "warehouse_type": "ZERO_COST_FINISHED",
            "change_reason": "测试入库",
        }, headers=auth_headers)
        assert res.status_code == 201

        # 验证库存中创建了零成本仓成品
        item = db_session.query(InventoryItem).filter(
            InventoryItem.item_sn == "SN-RMA-INV-001-NEW",
        ).first()
        assert item is not None
        assert item.stock_status == "IN_STOCK"
        assert item.stock_condition == "RETURNED_FROM_REPAIR"
        assert item.warehouse_type == "ZERO_COST_FINISHED"
        assert item.replaced_from_sn == "SN-RMA-INV-001"

        # 验证旧 SN 被标记为 REPLACED
        old_item = db_session.query(InventoryItem).filter(
            InventoryItem.item_sn == "SN-RMA-INV-001",
        ).first()
        if old_item:
            assert old_item.stock_status == "REPLACED"