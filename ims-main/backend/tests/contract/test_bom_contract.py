"""
主线D - BOM管理 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestBomContract:
    """BOM 管理 API 契约测试。"""

    def test_create_bom_success(self, client, auth_headers, seed_data):
        """POST /bom/ 创建 BOM 成功。"""
        payload = {
            "bom_name": "测试BOM-001",
            "version": "V1.0",
            "product_sku_id": seed_data["sku_fg"].id,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 100,
            "status": "DRAFT",
            "remark": "契约测试",
            "change_reason": "创建BOM",
            "details": [
                {
                    "material_sku_id": seed_data["sku_raw"].id,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 2.0,
                    "wastage_rate": 0.05,
                    "level": 2,
                    "process_note": "焊接",
                    "remark": "零件",
                }
            ],
        }
        res = client.post("/api/v1/bom/", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["bom_no"] is not None
        assert data["data"]["bom_name"] == "测试BOM-001"
        assert data["data"]["version"] == "V1.0"
        assert data["data"]["status"] == "DRAFT"
        assert len(data["data"]["details"]) == 1

    def test_list_boms_returns_page_result(self, client, auth_headers, seed_data):
        """GET /bom/list 返回分页结构。"""
        payload = {
            "bom_name": "测试BOM-002",
            "version": "V1.0",
            "product_sku_id": seed_data["sku_fg"].id,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 50,
            "status": "DRAFT",
            "change_reason": "创建",
            "details": [
                {
                    "material_sku_id": seed_data["sku_raw"].id,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 1.0,
                    "level": 2,
                }
            ],
        }
        client.post("/api/v1/bom/", json=payload, headers=auth_headers)

        res = client.get("/api/v1/bom/list", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_get_bom_detail(self, client, auth_headers, seed_data):
        """GET /bom/{id} 返回 BOM 详情。"""
        payload = {
            "bom_name": "测试BOM-003",
            "version": "V1.0",
            "product_sku_id": seed_data["sku_fg"].id,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 30,
            "status": "DRAFT",
            "change_reason": "创建",
            "details": [
                {
                    "material_sku_id": seed_data["sku_raw"].id,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 3.0,
                    "level": 2,
                }
            ],
        }
        create_res = client.post("/api/v1/bom/", json=payload, headers=auth_headers)
        bom_id = create_res.json()["data"]["id"]

        res = client.get(f"/api/v1/bom/{bom_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"]["id"] == bom_id

    def test_update_bom(self, client, auth_headers, seed_data):
        """PUT /bom/{id} 更新 BOM。"""
        payload = {
            "bom_name": "测试BOM-004",
            "version": "V1.0",
            "product_sku_id": seed_data["sku_fg"].id,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 20,
            "status": "DRAFT",
            "change_reason": "创建",
            "details": [
                {
                    "material_sku_id": seed_data["sku_raw"].id,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 1.0,
                    "level": 2,
                }
            ],
        }
        create_res = client.post("/api/v1/bom/", json=payload, headers=auth_headers)
        bom_id = create_res.json()["data"]["id"]

        update_res = client.put(
            f"/api/v1/bom/{bom_id}",
            json={"bom_name": "测试BOM-004-已更新", "status": "PUBLISHED", "change_reason": "更新"},
            headers=auth_headers,
        )
        assert update_res.status_code == 200

    def test_delete_bom(self, client, auth_headers, seed_data):
        """DELETE /bom/{id} 删除 BOM。"""
        payload = {
            "bom_name": "测试BOM-005",
            "version": "V1.0",
            "product_sku_id": seed_data["sku_fg"].id,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 10,
            "status": "DRAFT",
            "change_reason": "创建",
            "details": [
                {
                    "material_sku_id": seed_data["sku_raw"].id,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 1.0,
                    "level": 2,
                }
            ],
        }
        create_res = client.post("/api/v1/bom/", json=payload, headers=auth_headers)
        bom_id = create_res.json()["data"]["id"]

        delete_res = client.delete(f"/api/v1/bom/{bom_id}", headers=auth_headers)
        assert delete_res.status_code == 200

    def test_check_availability(self, client, auth_headers, seed_data):
        """GET /bom/{id}/availability 齐套分析。"""
        payload = {
            "bom_name": "测试BOM-006",
            "version": "V1.0",
            "product_sku_id": seed_data["sku_fg"].id,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 10,
            "status": "DRAFT",
            "change_reason": "创建",
            "details": [
                {
                    "material_sku_id": seed_data["sku_raw"].id,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 2.0,
                    "level": 2,
                }
            ],
        }
        create_res = client.post("/api/v1/bom/", json=payload, headers=auth_headers)
        bom_id = create_res.json()["data"]["id"]

        res = client.get(f"/api/v1/bom/{bom_id}/availability", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "overall_sufficient" in data["data"]
        assert data["data"]["bom_id"] == bom_id

    def test_export_bom_xlsx(self, client, auth_headers):
        """GET /bom/export 返回 Excel。"""
        res = client.get("/api/v1/bom/export", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_template_download(self, client, auth_headers):
        """GET /bom/template 返回模板。"""
        res = client.get("/api/v1/bom/template", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")

    def test_create_bom_requires_details(self, client, auth_headers, seed_data):
        """创建 BOM 需要至少一个明细。"""
        payload = {
            "bom_name": "空BOM",
            "version": "V1.0",
            "product_sku_id": seed_data["sku_fg"].id,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 10,
            "status": "DRAFT",
            "details": [],
        }
        res = client.post("/api/v1/bom/", json=payload, headers=auth_headers)
        assert res.status_code == 422


class TestProductionTaskContract:
    """生产任务 API 契约测试。"""

    def test_create_task_success(self, client, auth_headers, seed_data):
        """POST /production-task/ 创建生产任务。"""
        bom_payload = {
            "bom_name": "BOM-TASK-001",
            "version": "V1.0",
            "product_sku_id": seed_data["sku_fg"].id,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 50,
            "status": "PUBLISHED",
            "change_reason": "创建",
            "details": [
                {
                    "material_sku_id": seed_data["sku_raw"].id,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 1.0,
                    "level": 2,
                }
            ],
        }
        bom_res = client.post("/api/v1/bom/", json=bom_payload, headers=auth_headers)
        bom_id = bom_res.json()["data"]["id"]

        task_payload = {
            "bom_id": bom_id,
            "plan_quantity": 100,
            "start_date": "2026-09-08",
            "end_date": "2026-10-08",
            "change_reason": "创建任务",
        }
        res = client.post("/api/v1/production-task/", json=task_payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["task_no"] is not None

    def test_list_tasks(self, client, auth_headers, seed_data):
        """GET /production-task/list 返回任务列表。"""
        bom_payload = {
            "bom_name": "BOM-TASK-002",
            "version": "V1.0",
            "product_sku_id": seed_data["sku_fg"].id,
            "product_sku_code": "202-046",
            "product_sku_name": "测试成品",
            "plan_quantity": 50,
            "status": "PUBLISHED",
            "change_reason": "创建",
            "details": [
                {
                    "material_sku_id": seed_data["sku_raw"].id,
                    "material_sku_code": "202-018",
                    "material_sku_name": "测试原材料",
                    "spec": "规格A",
                    "unit": "个",
                    "quantity_per_unit": 1.0,
                    "level": 2,
                }
            ],
        }
        bom_res = client.post("/api/v1/bom/", json=bom_payload, headers=auth_headers)
        bom_id = bom_res.json()["data"]["id"]

        client.post("/api/v1/production-task/", json={
            "bom_id": bom_id, "plan_quantity": 50, "change_reason": "创建",
        }, headers=auth_headers)

        res = client.get("/api/v1/production-task/list", headers=auth_headers)
        assert res.status_code == 200
        assert "items" in res.json()["data"]

    def test_export_tasks(self, client, auth_headers):
        """GET /production-task/export 返回 Excel。"""
        res = client.get("/api/v1/production-task/export", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")