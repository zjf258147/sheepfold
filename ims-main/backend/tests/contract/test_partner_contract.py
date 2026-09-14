"""
往来单位 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestPartnerGroupContract:
    """分组 API 契约测试。"""

    def test_list_groups(self, client, auth_headers, seed_data):
        """GET /partners/groups 返回分组列表。"""
        res = client.get("/api/v1/partners/groups", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    def test_create_group_success(self, client, auth_headers):
        """POST /partners/groups 创建分组成功。"""
        payload = {"name": "契约测试分组"}
        res = client.post("/api/v1/partners/groups", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["name"] == "契约测试分组"

    def test_create_group_duplicate(self, client, auth_headers, seed_data):
        """POST /partners/groups 重复名称返回 409。"""
        payload = {"name": seed_data["partner_group"].name}
        res = client.post("/api/v1/partners/groups", json=payload, headers=auth_headers)
        assert res.status_code == 409

    def test_update_group(self, client, auth_headers, seed_data):
        """PUT /partners/groups/{id} 更新分组。"""
        res = client.put(
            f"/api/v1/partners/groups/{seed_data['partner_group'].id}",
            json={"name": "已更新分组"},
            headers=auth_headers,
        )
        assert res.status_code == 200

    def test_delete_group(self, client, auth_headers):
        """DELETE /partners/groups/{id} 删除分组。"""
        create_res = client.post(
            "/api/v1/partners/groups",
            json={"name": "待删除分组"},
            headers=auth_headers,
        )
        group_id = create_res.json()["data"]["id"]

        delete_res = client.delete(f"/api/v1/partners/groups/{group_id}", headers=auth_headers)
        assert delete_res.status_code == 200


class TestPartnerContract:
    """往来单位 API 契约测试。"""

    def test_list_partners(self, client, auth_headers):
        """GET /partners 返回分页结构。"""
        res = client.get("/api/v1/partners", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_create_partner_success(self, client, auth_headers, seed_data):
        """POST /partners 创建往来单位成功。"""
        payload = {
            "name": "契约测试单位",
            "group_id": seed_data["partner_group"].id,
            "partner_type": 2,
        }
        res = client.post("/api/v1/partners", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["name"] == "契约测试单位"

    def test_get_partner_detail(self, client, auth_headers, seed_data):
        """GET /partners/{id} 返回单位详情。"""
        res = client.get(f"/api/v1/partners/{seed_data['supplier'].id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"]["id"] == seed_data["supplier"].id

    def test_update_partner(self, client, auth_headers, seed_data):
        """PUT /partners/{id} 更新单位。"""
        res = client.put(
            f"/api/v1/partners/{seed_data['supplier'].id}",
            json={"name": "已更新单位"},
            headers=auth_headers,
        )
        assert res.status_code == 200

    def test_delete_partner(self, client, auth_headers, seed_data):
        """DELETE /partners/{id} 删除单位。"""
        create_res = client.post("/api/v1/partners", json={
            "name": "待删除单位",
            "group_id": seed_data["partner_group"].id,
            "partner_type": 2,
        }, headers=auth_headers)
        partner_id = create_res.json()["data"]["id"]

        delete_res = client.delete(f"/api/v1/partners/{partner_id}", headers=auth_headers)
        assert delete_res.status_code == 200

    def test_export_partners_xlsx(self, client, auth_headers):
        """GET /partners/partners/export 返回 Excel。"""
        res = client.get("/api/v1/partners/partners/export", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_template_download(self, client, auth_headers):
        """GET /partners/partners/template 返回模板。"""
        res = client.get("/api/v1/partners/partners/template", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_get_partner_not_found(self, client, auth_headers):
        """GET /partners/{id} 单位不存在返回 404。"""
        res = client.get("/api/v1/partners/99999", headers=auth_headers)
        assert res.status_code == 404