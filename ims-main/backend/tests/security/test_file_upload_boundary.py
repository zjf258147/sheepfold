"""
文件上传边界安全测试。

覆盖：
  - 非 Excel 文件上传（.exe / .txt）
  - 空文件（0 字节）
  - 无扩展名文件
  - 格式正确但内容乱码的 .xlsx
"""

import io
import pytest


class TestFileUploadBoundary:
    """文件上传边界测试：使用 RMA 导入接口 POST /api/v1/rma/import"""

    def test_upload_exe_file_rejected(self, client, auth_headers):
        """上传 .exe 文件应被拒绝。"""
        fake_exe = io.BytesIO(b"MZ\x90\x00\x03\x00\x00\x00")
        resp = client.post(
            "/api/v1/rma/import",
            files={"file": ("malware.exe", fake_exe, "application/x-msdownload")},
            headers=auth_headers,
        )
        assert resp.status_code == 400, f"预期 400，实际 {resp.status_code}"
        data = resp.json()
        assert "xlsx" in data.get("detail", "").lower() or "xls" in data.get("detail", "").lower(), \
            f"应提示仅支持 Excel 文件，实际: {data.get('detail', '')}"

    def test_upload_txt_file_rejected(self, client, auth_headers):
        """上传 .txt 文件应被拒绝。"""
        fake_txt = io.BytesIO(b"this is a text file")
        resp = client.post(
            "/api/v1/rma/import",
            files={"file": ("test.txt", fake_txt, "text/plain")},
            headers=auth_headers,
        )
        assert resp.status_code == 400, f"预期 400，实际 {resp.status_code}"

    def test_upload_empty_file_rejected(self, client, auth_headers):
        """上传空文件（0 字节 .xlsx）应被拒绝。"""
        empty_file = io.BytesIO(b"")
        resp = client.post(
            "/api/v1/rma/import",
            files={"file": ("empty.xlsx", empty_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            headers=auth_headers,
        )
        assert resp.status_code in (400, 422, 500), \
            f"空文件应被拒绝，实际 {resp.status_code}"

    def test_upload_no_extension_rejected(self, client, auth_headers):
        """上传无扩展名文件应被拒绝。"""
        fake_content = io.BytesIO(b"test content")
        resp = client.post(
            "/api/v1/rma/import",
            files={"file": ("noextension", fake_content, "application/octet-stream")},
            headers=auth_headers,
        )
        assert resp.status_code == 400, f"预期 400，实际 {resp.status_code}"

    def test_upload_corrupted_xlsx_rejected(self, client, auth_headers):
        """上传格式正确但内容乱码（非有效 zip/xlsx）的 .xlsx 应被拒绝。"""
        corrupted = io.BytesIO(b"this is not a valid xlsx file content")
        resp = client.post(
            "/api/v1/rma/import",
            files={"file": ("corrupted.xlsx", corrupted, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            headers=auth_headers,
        )
        assert resp.status_code in (400, 422, 500), \
            f"乱码 xlsx 应被拒绝，实际 {resp.status_code}"

    def test_upload_valid_xlsx_accepted(self, client, auth_headers):
        """上传有效的 .xlsx 文件应被接受。"""
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.append(["SN", "SKU_ID", "客户名称", "退货原因", "退货日期", "备注"])
        ws.append(["SN-TEST-UPLOAD", "1", "测试客户", "测试原因", "2026-01-01", "测试"])
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)

        resp = client.post(
            "/api/v1/rma/import",
            files={"file": ("valid.xlsx", buf, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            headers=auth_headers,
        )
        assert resp.status_code in (200, 201), f"有效 xlsx 应被接受，实际 {resp.status_code}"