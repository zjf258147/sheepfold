"""
文档下载 API 契约测试
验证 /api/v1/docs 和 /api/v1/docs/download/{doc_id} 接口的请求/响应格式。
"""

import pytest

pytestmark = pytest.mark.contract


class TestDocsListContract:
    """文档列表 API 契约测试。"""

    def test_list_docs_returns_structure(self, client, auth_headers):
        """GET /docs 返回 items 数组。"""
        res = client.get("/api/v1/docs", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_list_docs_each_item_has_required_fields(self, client, auth_headers):
        """每个文档项包含必要的字段。"""
        res = client.get("/api/v1/docs", headers=auth_headers)
        assert res.status_code == 200
        for item in res.json()["items"]:
            for field in ("id", "name", "description", "icon", "category", "downloadUrl", "exists"):
                assert field in item, f"Missing field: {field}"

    def test_list_docs_contains_all_four(self, client, auth_headers):
        """文档列表应包含 4 份文档。"""
        res = client.get("/api/v1/docs", headers=auth_headers)
        assert res.status_code == 200
        ids = [item["id"] for item in res.json()["items"]]
        assert len(ids) == 4, f"Expected 4 docs, got {len(ids)}"
        expected = {"spec", "manual", "dev", "style"}
        assert set(ids) == expected, f"Expected {expected}, got {set(ids)}"

    def test_list_docs_no_auth_also_works(self, client):
        """GET /docs 无需鉴权（公开文档）。"""
        res = client.get("/api/v1/docs")
        assert res.status_code == 200
        data = res.json()
        assert "items" in data


class TestDocsDownloadContract:
    """文档下载 API 契约测试。"""

    def test_download_existing_doc_returns_file(self, client, auth_headers):
        """GET /docs/download/spec 返回 .docx 文件。"""
        res = client.get("/api/v1/docs/download/spec", headers=auth_headers)
        assert res.status_code == 200
        assert res.headers.get("content-type", "").startswith(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ), f"Unexpected content-type: {res.headers.get('content-type')}"
        content = res.content
        assert len(content) > 1000, f"File too small: {len(content)} bytes"

    def test_download_manual_returns_file(self, client, auth_headers):
        """GET /docs/download/manual 返回 .docx 文件。"""
        res = client.get("/api/v1/docs/download/manual", headers=auth_headers)
        assert res.status_code == 200
        assert len(res.content) > 1000

    def test_download_dev_not_allowed(self, client, auth_headers):
        """GET /docs/download/dev 不提供下载（内部开发文档）。"""
        res = client.get("/api/v1/docs/download/dev", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data.get("detail") == "此文档不提供下载"

    def test_download_style_not_allowed(self, client, auth_headers):
        """GET /docs/download/style 不提供下载（内部开发文档）。"""
        res = client.get("/api/v1/docs/download/style", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data.get("detail") == "此文档不提供下载"

    def test_download_invalid_doc_returns_error(self, client, auth_headers):
        """GET /docs/download/nonexistent 返回错误。"""
        res = client.get("/api/v1/docs/download/nonexistent", headers=auth_headers)
        assert res.status_code == 200  # FastAPI 仍返回 200，detail 在 JSON body
        data = res.json()
        assert "detail" in data

    def test_download_no_auth_works(self, client):
        """下载无需鉴权（仅可下载文档返回文件，内部文档返回提示）。"""
        for doc_id in ("spec", "manual"):
            res = client.get(f"/api/v1/docs/download/{doc_id}")
            assert res.status_code == 200, f"Failed for doc_id={doc_id}"
            assert len(res.content) > 1000
        for doc_id in ("dev", "style"):
            res = client.get(f"/api/v1/docs/download/{doc_id}")
            assert res.status_code == 200, f"Failed for doc_id={doc_id}"
            assert res.json().get("detail") == "此文档不提供下载"

    def test_download_filename_header(self, client, auth_headers):
        """下载响应包含正确的文件名头。"""
        res = client.get("/api/v1/docs/download/spec", headers=auth_headers)
        assert res.status_code == 200
        cd = res.headers.get("content-disposition", "")
        assert "系统说明书" in cd or "attachment" in cd.lower()