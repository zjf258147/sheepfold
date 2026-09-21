"""
改善点 #13 — 数据归档清理 契约测试
验证数据摸底、归档策略、清理脚本的幂等性和可恢复性。
"""

import pytest


class TestDataArchiveContract:
    """数据归档清理 API 契约测试。"""

    # =========================================================================
    # 现有数据量验证（归档摸底依据）
    # =========================================================================

    def test_inbound_orders_queryable(self, client, auth_headers):
        """入库单数据可查询。"""
        res = client.get("/api/v1/inbound/orders", headers=auth_headers)
        assert res.status_code == 200

    def test_outbound_orders_queryable(self, client, auth_headers):
        """出库单数据可查询。"""
        res = client.get("/api/v1/outbound/orders", headers=auth_headers)
        assert res.status_code == 200

    def test_rma_returns_queryable(self, client, auth_headers):
        """RMA退货单数据可查询。"""
        res = client.get("/api/v1/rma/returns", headers=auth_headers)
        assert res.status_code == 200

    def test_shipment_list_queryable(self, client, auth_headers, seed_data):
        """出货单数据可查询。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id, "sku_code": "202-046",
            "sku_name": "测试成品", "spec": "规格B", "unit": "个",
            "sn_list": ["SN-ARCHIVE-001"], "quantity": 1,
            "ship_date": "2024-01-01",
            "address": "归档测试地址",
            "logistics_provider": "顺丰",
            "tracking_no": "SF-ARCHIVE-001",
            "remark": "归档测试",
        }
        res = client.post("/api/v1/shipment/", json=payload, headers=auth_headers)
        assert res.status_code == 201

    def test_incoming_receipts_queryable(self, client, auth_headers):
        """来料到货单数据可查询。"""
        res = client.get("/api/v1/incoming/receipts", headers=auth_headers)
        assert res.status_code == 200

    def test_device_ledger_queryable(self, client, auth_headers):
        """设备台账数据可查询。"""
        res = client.get("/api/v1/device-ledger", headers=auth_headers)
        assert res.status_code == 200

    # =========================================================================
    # 数据归档端点（规格占位 — 待实现）
    # =========================================================================

    @pytest.mark.skip(reason="数据审计脚本尚未实现")
    def test_data_audit_script_exists(self):
        """scripts/data_audit.py 脚本存在且可执行。"""
        from pathlib import Path
        script = Path(__file__).resolve().parents[2] / "scripts" / "data_audit.py"
        assert script.exists()

    @pytest.mark.skip(reason="数据归档脚本尚未实现")
    def test_data_archive_script_exists(self):
        """scripts/data_archive.py 脚本存在且可执行。"""
        from pathlib import Path
        script = Path(__file__).resolve().parents[2] / "scripts" / "data_archive.py"
        assert script.exists()

    @pytest.mark.skip(reason="数据归档端点尚未实现")
    def test_archive_api_accessible(self, client, auth_headers):
        """POST /system/data/archive 归档端点可访问。"""
        res = client.post("/api/v1/system/data/archive", json={
            "table": "inbound_order",
            "before_date": "2024-12-31",
            "dry_run": True,
        }, headers=auth_headers)
        assert res.status_code == 200

    @pytest.mark.skip(reason="数据归档端点尚未实现")
    def test_archive_idempotent(self, client, auth_headers):
        """归档脚本幂等（重复运行不报错）。"""
        res1 = client.post("/api/v1/system/data/archive", json={
            "table": "inbound_order", "before_date": "2024-12-31",
        }, headers=auth_headers)
        res2 = client.post("/api/v1/system/data/archive", json={
            "table": "inbound_order", "before_date": "2024-12-31",
        }, headers=auth_headers)
        assert res1.status_code == 200
        assert res2.status_code == 200

    @pytest.mark.skip(reason="数据归档端点尚未实现")
    def test_archive_data_still_queryable(self, client, auth_headers):
        """归档后数据仍可查询。"""
        res = client.get("/api/v1/inbound/orders/archive", headers=auth_headers)
        assert res.status_code == 200
        assert "items" in res.json()["data"]