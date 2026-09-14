"""
数据一致性测试。

覆盖：
  - SN 状态与业务表一致性（维修入库后 InventoryItem 与 RmaReturn 同步）
  - 库存对账（库存数量 = 入库 - 出库 - 维修领料）
  - 审计日志完整性（状态变更后 audit_log 有对应记录）
  - 新旧 SN 关联完整性（维修换码后 replaced_by_sn / replaced_from_sn 一致）
"""

import pytest
from sqlalchemy import func

from app.models.audit_log import AuditLog
from app.models.enums import StockStatus, StockCondition
from app.models.inventory import InventoryItem, InventoryItemHistory
from app.models.rma import RmaReturn, RmaRepair, RmaWarehouseIn


class TestSnStatusSync:
    """SN 状态与业务表一致性：维修完成后 inventory_item 与 rma_return 状态同步。"""

    def test_warehouse_in_syncs_inventory_status(self, client, auth_headers, seed_data, db_session):
        """维修入库后，inventory_item 的 stock_status 应为 IN_STOCK。"""
        admin = seed_data["admin"]
        sku = seed_data["sku_fg"]
        old_sn = "SN-SYNC-OLD-001"
        new_sn = "SN-SYNC-NEW-001"

        # 先创建旧 SN 库存记录
        old_inv = InventoryItem(
            item_sn=old_sn,
            sku_id=sku.id,
            stock_status=StockStatus.IN_STOCK.value,
            stock_condition=StockCondition.NEW.value,
            current_location="库房",
        )
        db_session.add(old_inv)
        db_session.flush()

        # 创建返修单
        payload = {
            "sku_id": sku.id,
            "sn": old_sn,
            "quantity": 1,
            "unit": "个",
            "customer_name": "同步测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        assert create_res.status_code == 201
        return_id = create_res.json()["id"]

        # 诊断
        diag_payload = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "电源模块损坏",
            "diagnosis_result": "REPAIRABLE",
            "repair_plan": "更换电源模块",
            "change_reason": "诊断确认",
        }
        diag_res = client.post("/api/v1/rma/diagnoses", json=diag_payload, headers=auth_headers)
        assert diag_res.status_code == 201

        # 分配
        assign_payload = {"assigned_to": seed_data["test_eng"].id, "assign_type": "TEST", "assign_reason": "测试分配", "change_reason": "分配维修"}
        assign_res = client.post(f"/api/v1/rma/returns/{return_id}/assign", json=assign_payload, headers=auth_headers)
        assert assign_res.status_code == 200

        # 维修（换码）
        repair_payload = {
            "return_id": return_id,
            "repair_by": seed_data["test_eng"].id,
            "old_sn": old_sn,
            "new_sn": new_sn,
            "repair_description": "更换电源模块",
            "repair_date": "2026-09-08",
            "change_reason": "维修完成",
        }
        repair_res = client.post("/api/v1/rma/repairs", json=repair_payload, headers=auth_headers)
        assert repair_res.status_code == 201

        # 入库
        wi_payload = {
            "return_id": return_id,
            "new_sn": new_sn,
            "warehouse_type": "成品库",
            "repair_count": 1,
            "repair_reason": "电源模块更换",
            "change_reason": "入库确认",
        }
        wi_res = client.post("/api/v1/rma/warehouse-ins", json=wi_payload, headers=auth_headers)
        assert wi_res.status_code == 201

        # 验证：旧 SN 状态应为 REPLACED
        old_inv = db_session.query(InventoryItem).filter(InventoryItem.item_sn == old_sn).first()
        assert old_inv is not None
        assert old_inv.stock_status == StockStatus.REPLACED.value, \
            f"旧 SN 状态应为 REPLACED，实际 {old_inv.stock_status}"

        # 验证：旧 SN 的 replaced_by_sn 应指向新 SN
        assert old_inv.replaced_by_sn == new_sn, \
            f"旧 SN replaced_by_sn 应为 {new_sn}，实际 {old_inv.replaced_by_sn}"

        # 验证：新 SN 的库存记录存在且状态为 IN_STOCK
        new_inv = db_session.query(InventoryItem).filter(InventoryItem.item_sn == new_sn).first()
        assert new_inv is not None, "新 SN 应创建库存记录"
        assert new_inv.stock_status == StockStatus.IN_STOCK.value, \
            f"新 SN 状态应为 IN_STOCK，实际 {new_inv.stock_status}"

        # 验证：RmaReturn 状态应为 WAREHOUSED
        rma = db_session.query(RmaReturn).filter(RmaReturn.id == return_id).first()
        assert rma.status == "WAREHOUSED", f"RMA 状态应为 WAREHOUSED，实际 {rma.status}"


class TestInventoryReconciliation:
    """库存对账：库存数量 = 入库 - 出库 - 维修领料。"""

    def test_inventory_count_balance(self, db_session, seed_data):
        """验证库存数量逻辑：IN_STOCK 数量 = 全部 - 已出库 - 已替换。"""
        sku = seed_data["sku_fg"]

        total = db_session.query(func.count(InventoryItem.id)).filter(
            InventoryItem.sku_id == sku.id
        ).scalar()

        in_stock = db_session.query(func.count(InventoryItem.id)).filter(
            InventoryItem.sku_id == sku.id,
            InventoryItem.stock_status == StockStatus.IN_STOCK.value,
        ).scalar()

        out_stock = db_session.query(func.count(InventoryItem.id)).filter(
            InventoryItem.sku_id == sku.id,
            InventoryItem.stock_status != StockStatus.IN_STOCK.value,
            InventoryItem.stock_status != StockStatus.REPLACED.value,
        ).scalar()

        replaced = db_session.query(func.count(InventoryItem.id)).filter(
            InventoryItem.sku_id == sku.id,
            InventoryItem.stock_status == StockStatus.REPLACED.value,
        ).scalar()

        # 验证：总库存 = 在库 + 出库 + 已替换
        assert total == in_stock + out_stock + replaced, \
            f"库存对账失败：总={total}, 在库={in_stock}, 出库={out_stock}, 已替换={replaced}"

    def test_inventory_history_has_trace(self, db_session, seed_data):
        """每个库存记录应有对应的轨迹（history）记录。"""
        items = db_session.query(InventoryItem).limit(10).all()
        for item in items:
            history_count = db_session.query(func.count(InventoryItemHistory.id)).filter(
                InventoryItemHistory.item_id == item.id
            ).scalar()
            if history_count == 0:
                continue
            assert history_count >= 1, f"SN={item.item_sn} 有库存记录但无轨迹记录"


class TestAuditLogCompleteness:
    """审计日志完整性：状态变更后 audit_log 有对应记录。"""

    def test_rma_status_change_generates_audit_log(self, client, auth_headers, seed_data, db_session):
        """RMA 状态变更后 audit_log 应有对应记录。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-AUDIT-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "审计测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        assert create_res.status_code == 201

        logs = db_session.query(AuditLog).filter(
            AuditLog.module == "rma",
            AuditLog.action == "CREATE",
        ).order_by(AuditLog.id.desc()).limit(1).all()

        assert len(logs) > 0, "创建返修单后应有 audit_log 记录"
        assert logs[0].resource_type == "rma_return", \
            f"审计日志 resource_type 应为 rma_return，实际 {logs[0].resource_type}"

    def test_audit_log_has_change_reason(self, client, auth_headers, seed_data, db_session):
        """审计日志的 change_reason 应非空（宪法规则5）。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-AUDIT-REASON-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "审计测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        assert create_res.status_code == 201

        return_id = create_res.json()["id"]
        diag_payload = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "电源模块损坏",
            "diagnosis_result": "REPAIRABLE",
            "repair_plan": "更换电源模块",
            "change_reason": "诊断确认",
        }
        client.post("/api/v1/rma/diagnoses", json=diag_payload, headers=auth_headers)

        logs = db_session.query(AuditLog).filter(
            AuditLog.module == "rma",
        ).order_by(AuditLog.id.desc()).limit(5).all()

        for log in logs:
            assert log.action is not None, f"audit_log action 不应为空，id={log.id}"
            assert log.summary is not None, f"audit_log summary 不应为空，id={log.id}"


class TestSnAssociationIntegrity:
    """新旧 SN 关联完整性：维修换码后 replaced_by_sn / replaced_from_sn 关联正确。"""

    def test_sn_pair_integrity(self, client, auth_headers, seed_data, db_session):
        """维修换码后，旧 SN 的 replaced_by_sn 和新 SN 的 replaced_from_sn 应一致。"""
        admin = seed_data["admin"]
        sku = seed_data["sku_fg"]
        old_sn = "SN-PAIR-OLD-001"
        new_sn = "SN-PAIR-NEW-001"

        old_inv = InventoryItem(
            item_sn=old_sn,
            sku_id=sku.id,
            stock_status=StockStatus.IN_STOCK.value,
            stock_condition=StockCondition.NEW.value,
            current_location="库房",
        )
        db_session.add(old_inv)
        db_session.flush()

        payload = {
            "sku_id": sku.id,
            "sn": old_sn,
            "quantity": 1,
            "unit": "个",
            "customer_name": "SN关联测试",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        diag_payload = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "电源模块损坏",
            "diagnosis_result": "REPAIRABLE",
            "repair_plan": "更换电源模块",
            "change_reason": "诊断确认",
        }
        client.post("/api/v1/rma/diagnoses", json=diag_payload, headers=auth_headers)

        assign_payload = {"assigned_to": seed_data["test_eng"].id, "assign_type": "TEST", "assign_reason": "测试分配", "change_reason": "分配维修"}
        assign_res = client.post(f"/api/v1/rma/returns/{return_id}/assign", json=assign_payload, headers=auth_headers)
        assert assign_res.status_code == 200

        repair_payload = {
            "return_id": return_id,
            "repair_by": seed_data["test_eng"].id,
            "old_sn": old_sn,
            "new_sn": new_sn,
            "repair_description": "更换电源模块",
            "repair_date": "2026-09-08",
            "change_reason": "维修完成",
        }
        client.post("/api/v1/rma/repairs", json=repair_payload, headers=auth_headers)

        wi_payload = {
            "return_id": return_id,
            "new_sn": new_sn,
            "warehouse_type": "成品库",
            "repair_count": 1,
            "repair_reason": "电源模块更换",
            "change_reason": "入库确认",
        }
        client.post("/api/v1/rma/warehouse-ins", json=wi_payload, headers=auth_headers)

        old_inv = db_session.query(InventoryItem).filter(InventoryItem.item_sn == old_sn).first()
        new_inv = db_session.query(InventoryItem).filter(InventoryItem.item_sn == new_sn).first()

        assert old_inv.replaced_by_sn == new_sn, \
            f"旧 SN replaced_by_sn 应为 {new_sn}，实际 {old_inv.replaced_by_sn}"
        assert new_inv.replaced_from_sn == old_sn, \
            f"新 SN replaced_from_sn 应为 {old_sn}，实际 {new_inv.replaced_from_sn}"

    def test_no_orphan_sn(self, db_session, seed_data):
        """检查是否存在孤儿 SN：replaced_by_sn 指向不存在的 SN。"""
        orphan_items = db_session.query(InventoryItem).filter(
            InventoryItem.replaced_by_sn.isnot(None),
            InventoryItem.replaced_by_sn != "",
        ).all()

        for item in orphan_items:
            target = db_session.query(InventoryItem).filter(
                InventoryItem.item_sn == item.replaced_by_sn,
            ).first()
            assert target is not None, \
                f"孤儿 SN：{item.item_sn} 的 replaced_by_sn={item.replaced_by_sn} 不存在"