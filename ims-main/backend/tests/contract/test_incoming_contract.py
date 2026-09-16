"""
主线A - 来料管理 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestIncomingReceiptContract:
    """到货登记 API 契约测试。"""

    def test_list_receipts_returns_page_result(self, client, auth_headers, seed_data):
        """GET /incoming/receipts 返回分页结构。"""
        res = client.get("/api/v1/incoming/receipts", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert "page" in data["data"]
        assert "page_size" in data["data"]
        assert isinstance(data["data"]["items"], list)

    def test_create_receipt_validates_required_fields(self, client, auth_headers, seed_data):
        """POST /incoming/receipts 创建到货单需要必填字段。"""
        res = client.post("/api/v1/incoming/receipts", json={}, headers=auth_headers)
        assert res.status_code == 422

    def test_create_receipt_success_returns_201(self, client, auth_headers, seed_data):
        """POST /incoming/receipts 创建到货单成功返回 201。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": "BATCH-001",
            "quantity": 100,
            "unit": "个",
            "delivery_date": "2026-09-08",
            "remark": "契约测试",
        }
        res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["receipt_no"] is not None
        assert data["receipt_no"].startswith("RC")
        assert data["status"] == "PENDING_INSPECTION"

    def test_get_receipt_returns_detail(self, client, auth_headers, seed_data):
        """GET /incoming/receipts/{id} 返回到货单详情。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": "BATCH-002",
            "quantity": 50,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        receipt_id = create_res.json()["id"]

        res = client.get(f"/api/v1/incoming/receipts/{receipt_id}", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == receipt_id
        assert data["receipt_no"].startswith("RC")

    def test_update_receipt_modifies_fields(self, client, auth_headers, seed_data):
        """PUT /incoming/receipts/{id} 更新到货单。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": "BATCH-003",
            "quantity": 30,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        receipt_id = create_res.json()["id"]

        update_res = client.put(
            f"/api/v1/incoming/receipts/{receipt_id}",
            json={"quantity": 60, "remark": "已更新"},
            headers=auth_headers,
        )
        assert update_res.status_code == 200

    def test_export_receipts_returns_xlsx(self, client, auth_headers, seed_data):
        """GET /incoming/receipts/export 返回 Excel 文件。"""
        res = client.get("/api/v1/incoming/receipts/export", headers=auth_headers)
        assert res.status_code == 200
        ct = res.headers.get("content-type", "")
        assert "spreadsheet" in ct

    def test_template_download_returns_xlsx(self, client, auth_headers):
        """GET /incoming/receipts/template 返回模板文件。"""
        res = client.get("/api/v1/incoming/receipts/template", headers=auth_headers)
        assert res.status_code == 200
        ct = res.headers.get("content-type", "")
        assert "spreadsheet" in ct


class TestIncomingInspectionContract:
    """来料检验 API 契约测试。"""

    def test_create_inspection_validates_fields(self, client, auth_headers, seed_data):
        """POST /incoming/inspections 创建检验报告需要必填字段。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": "BATCH-INSP",
            "quantity": 100,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        receipt_id = create_res.json()["id"]

        insp_payload = {
            "receipt_id": receipt_id,
            "inspector_id": seed_data["quality"].id,
            "inspection_date": "2026-09-08",
            "result": "ACCEPTED",
            "sample_qty": 10,
            "defect_qty": 0,
            "change_reason": "检验测试",
        }
        res = client.post("/api/v1/incoming/inspections", json=insp_payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["inspection_no"] is not None
        assert data["inspection_no"].startswith("JC")

    def test_list_inspections_returns_array(self, client, auth_headers, seed_data):
        """GET /incoming/receipts/{id}/inspections 返回检验列表。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": "BATCH-INSP2",
            "quantity": 100,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        receipt_id = create_res.json()["id"]

        res = client.get(f"/api/v1/incoming/receipts/{receipt_id}/inspections", headers=auth_headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    @pytest.mark.parametrize("result,expected_status", [
        ("ACCEPTED", "ACCEPTED"),
        ("CONCESSION_ACCEPTED", "ACCEPTED"),
        ("REJECTED", "REJECTED"),
    ])
    def test_inspection_result_updates_receipt_status(
        self, client, auth_headers, seed_data, result, expected_status
    ):
        """检验结果同步更新到货单状态。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": f"BATCH-{result}",
            "quantity": 50,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        receipt_id = create_res.json()["id"]

        insp = {
            "receipt_id": receipt_id,
            "inspector_id": seed_data["quality"].id,
            "inspection_date": "2026-09-08",
            "result": result,
            "sample_qty": 5,
            "defect_qty": 0 if result != "REJECTED" else 3,
            "change_reason": "检验",
        }
        client.post("/api/v1/incoming/inspections", json=insp, headers=auth_headers)

        detail_res = client.get(f"/api/v1/incoming/receipts/{receipt_id}", headers=auth_headers)
        assert detail_res.json()["status"] == expected_status


class TestIncomingConfirmContract:
    """确认入库 API 契约测试。"""

    def test_confirm_requires_accepted_status(self, client, auth_headers, seed_data):
        """只有 ACCEPTED 状态的到货单才能确认入库。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": "BATCH-CFM",
            "quantity": 50,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        receipt_id = create_res.json()["id"]

        res = client.post(
            f"/api/v1/incoming/receipts/{receipt_id}/confirm",
            json={"change_reason": "确认入库"},
            headers=auth_headers,
        )
        assert res.status_code == 400

    def test_confirm_success(self, client, auth_headers, seed_data):
        """确认入库成功。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": "BATCH-CFM2",
            "quantity": 50,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        receipt_id = create_res.json()["id"]

        insp = {
            "receipt_id": receipt_id,
            "inspector_id": seed_data["quality"].id,
            "inspection_date": "2026-09-08",
            "result": "ACCEPTED",
            "sample_qty": 5,
            "defect_qty": 0,
            "change_reason": "检验",
        }
        client.post("/api/v1/incoming/inspections", json=insp, headers=auth_headers)

        res = client.post(
            f"/api/v1/incoming/receipts/{receipt_id}/confirm",
            json={"change_reason": "确认入库"},
            headers=auth_headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "WAREHOUSED"
        detail = client.get(f"/api/v1/incoming/receipts/{receipt_id}", headers=auth_headers)
        assert detail.json()["status"] == "WAREHOUSED"


class TestIncomingReturnContract:
    """原材料退货 API 契约测试。"""

    def test_create_return_validates_fields(self, client, auth_headers, seed_data):
        """POST /incoming/returns 创建退货单。"""
        payload = {
            "supplier_id": seed_data["supplier"].id,
            "sku_id": seed_data["sku_raw"].id,
            "batch_no": "BATCH-RET",
            "quantity": 100,
            "unit": "个",
            "delivery_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/incoming/receipts", json=payload, headers=auth_headers)
        receipt_id = create_res.json()["id"]

        return_payload = {
            "receipt_id": receipt_id,
            "return_qty": 20,
            "return_reason": "外观不良",
            "return_date": "2026-09-08",
            "change_reason": "退货",
        }
        res = client.post("/api/v1/incoming/returns", json=return_payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["return_no"] is not None
        assert data["return_no"].startswith("TH")

        detail = client.get(f"/api/v1/incoming/receipts/{receipt_id}", headers=auth_headers)
        assert detail.json()["status"] == "REJECTED"