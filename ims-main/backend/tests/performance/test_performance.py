"""
性能基准测试。

覆盖：
  - 核心 API 响应时间基准（P95 目标）
  - Excel 大文件导出性能
"""

import io
import time

import pytest
from openpyxl import Workbook


class TestApiResponseTime:
    """核心 API 响应时间基准测试。"""

    @pytest.mark.parametrize("endpoint,method,expected_max_ms", [
        ("/api/v1/auth/login", "POST", 500),
        ("/api/v1/rma/returns", "GET", 500),
        ("/api/v1/rma/returns", "POST", 500),
        ("/health", "GET", 200),
    ])
    def test_api_response_time(self, client, auth_headers, seed_data, endpoint, method, expected_max_ms):
        """核心 API 响应时间应在预期范围内。"""
        if method == "GET":
            if "health" in endpoint:
                start = time.perf_counter()
                resp = client.get(endpoint)
                elapsed = (time.perf_counter() - start) * 1000
            else:
                start = time.perf_counter()
                resp = client.get(endpoint, headers=auth_headers)
                elapsed = (time.perf_counter() - start) * 1000
        elif method == "POST":
            if "login" in endpoint:
                payload = {"username": "admin", "password": "admin123"}
                start = time.perf_counter()
                resp = client.post(endpoint, json=payload)
                elapsed = (time.perf_counter() - start) * 1000
            else:
                payload = {
                    "sku_id": seed_data["sku_fg"].id,
                    "sn": f"SN-PERF-{int(time.time() * 1000)}",
                    "quantity": 1,
                    "unit": "个",
                    "customer_name": "性能测试",
                    "return_reason": "设备故障",
                    "return_date": "2026-09-08",
                }
                start = time.perf_counter()
                resp = client.post(endpoint, json=payload, headers=auth_headers)
                elapsed = (time.perf_counter() - start) * 1000
        else:
            pytest.skip(f"不支持的 HTTP 方法: {method}")

        assert resp.status_code in (200, 201), f"{method} {endpoint} 返回 {resp.status_code}"
        assert elapsed < expected_max_ms, \
            f"{method} {endpoint} 响应时间 {elapsed:.0f}ms 超过上限 {expected_max_ms}ms"

    def test_rma_list_with_filter_response_time(self, client, auth_headers):
        """带筛选条件的列表查询响应时间。"""
        start = time.perf_counter()
        resp = client.get("/api/v1/rma/returns?page=1&page_size=20", headers=auth_headers)
        elapsed = (time.perf_counter() - start) * 1000
        assert resp.status_code == 200
        assert elapsed < 1000, f"列表查询响应时间 {elapsed:.0f}ms 超过 1000ms"


class TestExcelExportPerformance:
    """Excel 大文件导出性能测试。"""

    def test_rma_export_response_time(self, client, auth_headers):
        """RMA 导出响应时间应在合理范围内。"""
        start = time.perf_counter()
        resp = client.get("/api/v1/rma/export", headers=auth_headers)
        elapsed = (time.perf_counter() - start) * 1000
        assert resp.status_code == 200
        assert elapsed < 3000, f"RMA 导出响应时间 {elapsed:.0f}ms 超过 3000ms"

    def test_large_xlsx_export_does_not_crash(self, client, auth_headers, seed_data):
        """批量创建数据后导出不应崩溃。"""
        for i in range(10):
            payload = {
                "sku_id": seed_data["sku_fg"].id,
                "sn": f"SN-EXPORT-{i:04d}",
                "quantity": 1,
                "unit": "个",
                "customer_name": f"导出测试客户{i}",
                "return_reason": "设备故障",
                "return_date": "2026-09-08",
            }
            client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)

        start = time.perf_counter()
        resp = client.get("/api/v1/rma/export", headers=auth_headers)
        elapsed = (time.perf_counter() - start) * 1000

        assert resp.status_code == 200
        assert "spreadsheet" in resp.headers.get("content-type", "")
        assert elapsed < 5000, f"批量导出响应时间 {elapsed:.0f}ms 超过 5000ms"

    def test_export_content_is_valid_xlsx(self, client, auth_headers):
        """导出内容应是有效的 .xlsx 文件。"""
        resp = client.get("/api/v1/rma/export", headers=auth_headers)
        assert resp.status_code == 200

        from openpyxl import load_workbook
        wb = load_workbook(io.BytesIO(resp.content))
        assert wb.active is not None
        wb.close()