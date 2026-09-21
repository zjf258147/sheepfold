"""
改善点 #3 — 故障统计分析看板 契约测试
验证按型号/类型/场站/趋势统计和异常检测。
部分测试可基于现有RMA接口运行，统计端点待实现。
"""

import pytest
from datetime import date, timedelta


class TestFaultStatisticsContract:
    """故障统计分析 API 契约测试。"""

    # =========================================================================
    # 现有RMA数据就绪验证
    # =========================================================================

    def test_rma_list_filterable_by_date(self, client, auth_headers, seed_data):
        """RMA退货单可按日期筛选（统计数据基础）。"""
        res = client.get("/api/v1/rma/returns?return_date_from=2026-01-01&return_date_to=2026-12-31",
                         headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert "items" in data["data"]

    def test_rma_returns_contain_sku_info(self, client, auth_headers, seed_data):
        """RMA退货单含SKU关联（按型号统计的数据基础）。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-STAT-MODEL",
            "quantity": 1,
            "unit": "个",
            "customer_name": "统计测试客户",
            "return_reason": "质量问题",
            "return_date": str(date.today()),
        }
        res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["sku_id"] == seed_data["sku_fg"].id

    # =========================================================================
    # 统计端点（规格占位 — 待后端实现）
    # =========================================================================

    @pytest.mark.skip(reason="故障按型号统计端点尚未实现")
    def test_fault_by_model(self, client, auth_headers):
        """GET /rma/statistics/fault-by-model?top=10 按型号统计。"""
        res = client.get("/api/v1/rma/statistics/fault-by-model?top=10", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        for item in data["data"]:
            assert "sku_code" in item
            assert "fault_count" in item

    @pytest.mark.skip(reason="故障按类型统计端点尚未实现")
    def test_fault_by_type(self, client, auth_headers):
        """GET /rma/statistics/fault-by-type 按故障类型分布。"""
        res = client.get("/api/v1/rma/statistics/fault-by-type", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        for item in data["data"]:
            assert "fault_code" in item
            assert "count" in item

    @pytest.mark.skip(reason="故障按场站统计端点尚未实现")
    def test_fault_by_station(self, client, auth_headers):
        """GET /rma/statistics/fault-by-station 按场站统计。"""
        res = client.get("/api/v1/rma/statistics/fault-by-station", headers=auth_headers)
        assert res.status_code == 200

    @pytest.mark.skip(reason="故障趋势统计端点尚未实现")
    def test_fault_trend(self, client, auth_headers):
        """GET /rma/statistics/fault-trend?granularity=month 趋势统计。"""
        res = client.get("/api/v1/rma/statistics/fault-trend?granularity=month", headers=auth_headers)
        assert res.status_code == 200

    @pytest.mark.skip(reason="异常检测端点尚未实现")
    def test_anomaly_check(self, client, auth_headers):
        """GET /rma/statistics/anomaly-check 异常波动检测。"""
        res = client.get("/api/v1/rma/statistics/anomaly-check", headers=auth_headers)
        assert res.status_code == 200

    @pytest.mark.skip(reason="故障统计端点尚未实现")
    def test_empty_data_no_error(self, client, auth_headers):
        """无数据时返回空而非报错。"""
        res = client.get("/api/v1/rma/statistics/fault-by-model", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"] == [] or res.json()["data"] is None