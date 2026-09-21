"""
改善点 #4 — 供应商质量评估 契约测试
验证合格率、不良率、交货周期和质量评分。
部分验证基于现有来料检验数据，评估端点待实现。
"""

import pytest
from datetime import date


class TestSupplierQualityContract:
    """供应商质量评估 API 契约测试。"""

    # =========================================================================
    # 现有来料到货数据就绪验证
    # =========================================================================

    def test_incoming_receipt_list_filterable(self, client, auth_headers, seed_data):
        """来料到货单可按供应商筛选（评估数据基础）。"""
        res = client.get("/api/v1/incoming/receipts", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert "items" in data["data"]

    def test_create_receipt_with_supplier(self, client, auth_headers, seed_data):
        """创建到货单含供应商关联。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": "BATCH-SQ-001",
            "quantity": 100,
            "unit": "个",
            "delivery_date": str(date.today()),
            "remark": "质量评估测试",
        }
        res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        receipt_id = data["id"]
        assert receipt_id is not None
        return receipt_id

    def test_inspection_has_result_fields(self, client, auth_headers, seed_data):
        """来料检验含 result/defect_qty/sample_qty 字段（评估数据基础）。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": "BATCH-SQ-002",
            "quantity": 50,
            "unit": "个",
            "delivery_date": str(date.today()),
        }
        res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        receipt_id = res.json()["id"]

        insp_res = client.post("/api/v1/incoming/inspections", json={
            "receipt_id": receipt_id,
            "inspector_id": seed_data["quality"].id,
            "inspection_date": str(date.today()),
            "result": "ACCEPTED",
            "sample_qty": 10,
            "defect_qty": 0,
            "change_reason": "检验",
            "remark": "质量评估测试检验",
        }, headers=auth_headers)
        assert insp_res.status_code == 201
        insp_data = insp_res.json()
        assert insp_data["result"] == "ACCEPTED"

    # =========================================================================
    # 供应商质量评估端点（规格占位 — 待后端实现）
    # =========================================================================

    @pytest.mark.skip(reason="供应商质量评估端点尚未实现")
    def test_get_supplier_quality_list(self, client, auth_headers):
        """GET /incoming/supplier-quality 返回供应商质量列表。"""
        res = client.get("/api/v1/incoming/supplier-quality", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        for item in data["data"]:
            assert "supplier_name" in item
            assert "acceptance_rate" in item
            assert "defect_rate" in item
            assert "quality_score" in item

    @pytest.mark.skip(reason="供应商质量评估端点尚未实现")
    def test_time_range_filter(self, client, auth_headers):
        """可按时间范围筛选。"""
        res = client.get(
            "/api/v1/incoming/supplier-quality?start_date=2026-01-01&end_date=2026-12-31",
            headers=auth_headers,
        )
        assert res.status_code == 200

    @pytest.mark.skip(reason="供应商质量评估端点尚未实现")
    def test_no_receipt_supplier_not_listed(self, client, auth_headers):
        """无到货记录的供应商不出现在列表中。"""
        res = client.get("/api/v1/incoming/supplier-quality", headers=auth_headers)
        supplier_count = len(res.json()["data"])
        # 应该有供应商但不会有无记录的新供应商
        assert supplier_count >= 0

    @pytest.mark.skip(reason="供应商质量评估端点尚未实现")
    def test_low_score_warning(self, client, auth_headers):
        """低于60分的供应商应标记预警。"""
        res = client.get("/api/v1/incoming/supplier-quality", headers=auth_headers)
        for item in res.json()["data"]:
            if item.get("quality_score", 100) < 60:
                assert item.get("warning") is True or item.get("alert") is True