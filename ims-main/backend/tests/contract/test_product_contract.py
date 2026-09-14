"""
产品管理 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestCategoryContract:
    """分类 API 契约测试。"""

    def test_list_categories(self, client, auth_headers, seed_data):
        """GET /products/categories 返回分类列表。"""
        res = client.get("/api/v1/products/categories", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    def test_create_category_success(self, client, auth_headers):
        """POST /products/categories 创建分类成功。"""
        payload = {"name": "契约测试分类"}
        res = client.post("/api/v1/products/categories", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["name"] == "契约测试分类"

    def test_create_category_duplicate(self, client, auth_headers, seed_data):
        """POST /products/categories 重复名称返回 409。"""
        payload = {"name": seed_data["category"].name}
        res = client.post("/api/v1/products/categories", json=payload, headers=auth_headers)
        assert res.status_code == 409

    def test_update_category(self, client, auth_headers, seed_data):
        """PUT /products/categories/{id} 更新分类。"""
        cat_id = seed_data["category"].id
        res = client.put(
            f"/api/v1/products/categories/{cat_id}",
            json={"name": "已更新分类"},
            headers=auth_headers,
        )
        assert res.status_code == 200

    def test_delete_category(self, client, auth_headers):
        """DELETE /products/categories/{id} 删除分类。"""
        create_res = client.post(
            "/api/v1/products/categories",
            json={"name": "待删除分类"},
            headers=auth_headers,
        )
        cat_id = create_res.json()["data"]["id"]

        delete_res = client.delete(f"/api/v1/products/categories/{cat_id}", headers=auth_headers)
        assert delete_res.status_code == 200

    def test_update_not_found(self, client, auth_headers):
        """PUT /products/categories/{id} 分类不存在返回 404。"""
        res = client.put("/api/v1/products/categories/99999", json={"name": "不存在"}, headers=auth_headers)
        assert res.status_code == 404


class TestSkuContract:
    """SKU API 契约测试。"""

    def test_list_skus_returns_page_result(self, client, auth_headers, seed_data):
        """GET /products/skus 返回分页结构。"""
        res = client.get("/api/v1/products/skus", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_create_sku_success(self, client, auth_headers, seed_data):
        """POST /products/skus 创建 SKU 成功。"""
        payload = {
            "name": "契约测试SKU",
            "category_id": seed_data["category"].id,
            "barcode": "CT-TEST-001",
            "sn_mode": "BOTH",
            "unit": "个",
            "sku_code": "CT-001",
            "spec": "测试规格",
            "sku_type": "RAW_MATERIAL",
        }
        res = client.post("/api/v1/products/skus", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["name"] == "契约测试SKU"

    def test_get_sku_detail(self, client, auth_headers, seed_data):
        """GET /products/skus/{id} 返回 SKU 详情。"""
        res = client.get(f"/api/v1/products/skus/{seed_data['sku_fg'].id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"]["id"] == seed_data["sku_fg"].id

    def test_update_sku(self, client, auth_headers, seed_data):
        """PUT /products/skus/{id} 更新 SKU。"""
        res = client.put(
            f"/api/v1/products/skus/{seed_data['sku_fg'].id}",
            json={"name": "已更新SKU"},
            headers=auth_headers,
        )
        assert res.status_code == 200

    def test_delete_sku(self, client, auth_headers, seed_data):
        """DELETE /products/skus/{id} 删除 SKU。"""
        create_res = client.post("/api/v1/products/skus", json={
            "name": "待删除SKU",
            "category_id": seed_data["category"].id,
            "barcode": "CT-DEL-001",
            "sn_mode": "BOTH",
            "unit": "个",
            "sku_code": "CT-DEL",
            "spec": "测试",
            "sku_type": "RAW_MATERIAL",
        }, headers=auth_headers)
        sku_id = create_res.json()["data"]["id"]

        delete_res = client.delete(f"/api/v1/products/skus/{sku_id}", headers=auth_headers)
        assert delete_res.status_code == 200

    def test_export_skus_xlsx(self, client, auth_headers):
        """GET /products/skus/export 返回 Excel。"""
        res = client.get("/api/v1/products/skus/export", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_template_download(self, client, auth_headers):
        """GET /products/skus/template 返回模板。"""
        res = client.get("/api/v1/products/skus/template", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_get_sku_not_found(self, client, auth_headers):
        """GET /products/skus/{id} SKU 不存在返回 404。"""
        res = client.get("/api/v1/products/skus/99999", headers=auth_headers)
        assert res.status_code == 404