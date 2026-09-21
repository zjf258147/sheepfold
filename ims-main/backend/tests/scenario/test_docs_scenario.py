"""
文档下载 & APK 下载 场景测试
验证文档中心端到端下载流程和 APK 下载功能。
"""

import pytest

pytestmark = pytest.mark.scenario


class TestDocsDownloadScenario:
    """文档下载端到端流程。"""

    def test_browse_and_download_all_docs(self, client):
        """场景：进入文档中心 → 查看4份文档 → 可下载的下载，不可下载的返回提示。"""
        # 步骤1：获取文档列表
        res = client.get("/api/v1/docs")
        assert res.status_code == 200
        items = res.json()["items"]
        assert len(items) == 4

        # 步骤2：可下载文档返回文件，内部文档返回"不提供下载"
        downloaded = 0
        not_allowed = 0
        for item in items:
            doc_id = item["id"]
            dl_res = client.get(f"/api/v1/docs/download/{doc_id}")
            assert dl_res.status_code == 200, f"Download failed for {doc_id}"

            if item.get("downloadable"):
                content = dl_res.content
                assert len(content) > 500, f"{doc_id} file too small"
                downloaded += 1
            else:
                data = dl_res.json()
                assert data.get("detail") == "此文档不提供下载", f"Unexpected detail for {doc_id}"
                not_allowed += 1

        assert downloaded == 2, f"Expected 2 downloadable docs, got {downloaded}"
        assert not_allowed == 2, f"Expected 2 non-downloadable docs, got {not_allowed}"

    def test_invalid_doc_returns_proper_message(self, client):
        """场景：请求不存在的文档，返回明确错误信息。"""
        res = client.get("/api/v1/docs/download/fake-doc")
        assert res.status_code == 200
        data = res.json()
        assert data.get("detail") == "文档不存在"


class TestApkDownloadScenario:
    """APK 下载功能验证。"""

    def test_apk_file_exists_and_served(self, client):
        """APK 文件通过 /download/ims-latest.apk 可访问。"""
        res = client.get("/download/ims-latest.apk")
        # 文件可能存在也可能不存在（取决于是否构建过APK）
        if res.status_code == 200:
            assert len(res.content) > 100000, f"APK file suspiciously small: {len(res.content)} bytes"
            ct = res.headers.get("content-type", "")
            assert "octet-stream" in ct or "apk" in ct.lower() or "vnd.android" in ct.lower(), \
                f"Unexpected content-type for APK: {ct}"
        else:
            # APK 文件不存在时不应崩溃
            assert res.status_code in (200, 404), f"Unexpected status: {res.status_code}"

    def test_apk_download_from_about_page_flow(self, client, auth_headers):
        """场景：用户在关于页面点击下载APK → 获取文件。"""
        # 步骤1：访问关于页面的API（如果有）
        # 步骤2：下载APK
        res = client.get("/download/ims-latest.apk", headers=auth_headers)
        if res.status_code == 200:
            assert len(res.content) > 100000, "APK too small"
            # 验证是 ZIP 格式（APK 本质是 ZIP）
            assert res.content[:2] == b"PK", "APK should start with PK (ZIP header)"
        else:
            assert res.status_code == 404

    def test_docs_and_apk_coexist(self, client):
        """验证文档下载和APK下载互不影响。"""
        # 文档API
        docs_res = client.get("/api/v1/docs")
        assert docs_res.status_code == 200

        # APK下载
        apk_res = client.get("/download/ims-latest.apk")
        assert apk_res.status_code in (200, 404)