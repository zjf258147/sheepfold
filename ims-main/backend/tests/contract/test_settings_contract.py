"""
品牌配置 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
需要管理员权限。
"""

import io

import pytest


class TestBrandingContract:
    """品牌配置 API 契约测试。"""

    def test_get_branding_public(self, client):
        """GET /settings/branding 无需鉴权也可访问。"""
        res = client.get("/api/v1/settings/branding")
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "app_name" in data["data"]

    def test_get_branding_with_auth(self, client, auth_headers):
        """GET /settings/branding 带鉴权也正常。"""
        res = client.get("/api/v1/settings/branding", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "app_name" in data["data"]
        assert "app_subtitle" in data["data"]

    def test_update_branding(self, client, auth_headers):
        """PUT /settings/branding 更新品牌文案。"""
        res = client.put("/api/v1/settings/branding", json={
            "app_name": "IMS测试系统",
            "app_subtitle": "契约测试副标题",
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["app_name"] == "IMS测试系统"

    def test_update_branding_validates_fields(self, client, auth_headers):
        """PUT /settings/branding 缺少字段返回 422。"""
        res = client.put("/api/v1/settings/branding", json={}, headers=auth_headers)
        assert res.status_code == 422


class TestLogoContract:
    """Logo 上传 / 删除 API 契约测试。"""

    @staticmethod
    def _make_png_bytes(width=1, height=1):
        """生成最小合法 PNG 字节。"""
        import struct
        import zlib

        def chunk(chunk_type, data):
            c = chunk_type + data
            crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
            return struct.pack(">I", len(data)) + c + crc

        signature = b'\x89PNG\r\n\x1a\n'
        ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
        ihdr = chunk(b'IHDR', ihdr_data)
        raw = b''
        for y in range(height):
            raw += b'\x00' + b'\xff\x00\x00' * width
        compressed = zlib.compress(raw)
        idat = chunk(b'IDAT', compressed)
        iend = chunk(b'IEND', b'')
        return signature + ihdr + idat + iend

    def test_upload_logo_png(self, client, auth_headers):
        """POST /settings/branding/logo 上传 PNG Logo。"""
        png_bytes = self._make_png_bytes(4, 4)
        files = {"file": ("logo.png", io.BytesIO(png_bytes), "image/png")}
        res = client.post("/api/v1/settings/branding/logo", files=files, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["logo_url"] is not None
        assert "branding" in data["data"]["logo_url"]

    def test_upload_logo_jpg(self, client, auth_headers):
        """POST /settings/branding/logo 上传 JPG Logo。"""
        jpg_bytes = (
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
            b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t'
            b'\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a'
            b'\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444'
            b'\x1f\'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01'
            b'\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01'
            b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06'
            b'\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02'
            b'\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11'
            b'\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1'
            b'\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789'
            b':CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88'
            b'\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5'
            b'\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2'
            b'\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8'
            b'\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3'
            b'\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x0c\x03\x01\x00\x02'
            b'\x11\x03\x11\x00?\x00\xfb\xa1\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xd9'
        )
        files = {"file": ("logo.jpg", io.BytesIO(jpg_bytes), "image/jpeg")}
        res = client.post("/api/v1/settings/branding/logo", files=files, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0

    def test_upload_logo_invalid_format(self, client, auth_headers):
        """POST /settings/branding/logo 不支持的文件格式返回 400。"""
        files = {"file": ("logo.txt", io.BytesIO(b"not an image"), "text/plain")}
        res = client.post("/api/v1/settings/branding/logo", files=files, headers=auth_headers)
        assert res.status_code == 400

    def test_upload_logo_empty_file(self, client, auth_headers):
        """POST /settings/branding/logo 空文件返回 400。"""
        files = {"file": ("empty.png", io.BytesIO(b""), "image/png")}
        res = client.post("/api/v1/settings/branding/logo", files=files, headers=auth_headers)
        assert res.status_code == 400

    def test_upload_logo_requires_admin(self, client):
        """POST /settings/branding/logo 无鉴权返回 401。"""
        png_bytes = self._make_png_bytes(1, 1)
        files = {"file": ("logo.png", io.BytesIO(png_bytes), "image/png")}
        res = client.post("/api/v1/settings/branding/logo", files=files)
        assert res.status_code == 401

    def test_delete_logo(self, client, auth_headers):
        """DELETE /settings/branding/logo 清除 Logo。先上传再删除。"""
        png_bytes = self._make_png_bytes(1, 1)
        files = {"file": ("logo.png", io.BytesIO(png_bytes), "image/png")}
        client.post("/api/v1/settings/branding/logo", files=files, headers=auth_headers)

        res = client.delete("/api/v1/settings/branding/logo", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["logo_url"] is None

    def test_delete_logo_requires_admin(self, client):
        """DELETE /settings/branding/logo 无鉴权返回 401。"""
        res = client.delete("/api/v1/settings/branding/logo")
        assert res.status_code == 401


class TestConnectionContract:
    """服务器连通性测试 API 契约测试。"""

    def test_connection_validates_url(self, client, auth_headers):
        """POST /settings/test-connection 缺少 url 返回 422。"""
        res = client.post("/api/v1/settings/test-connection", json={}, headers=auth_headers)
        assert res.status_code == 422

    def test_connection_unreachable(self, client, auth_headers):
        """POST /settings/test-connection 不可达地址返回 ok=False。"""
        res = client.post("/api/v1/settings/test-connection", json={
            "url": "http://127.0.0.1:19999"
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["ok"] is False

    def test_connection_invalid_url(self, client, auth_headers):
        """POST /settings/test-connection 无效 URL 返回 ok=False（不抛异常）。"""
        res = client.post("/api/v1/settings/test-connection", json={
            "url": "not-a-valid-url-::://"
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["ok"] is False