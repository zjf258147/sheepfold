"""
主线B - 返厂维修 契约测试
验证 API 请求参数格式、响应数据结构、状态码。
"""

import pytest


class TestRmaReturnContract:
    """退货登记 API 契约测试。"""

    def test_create_return_success(self, client, auth_headers, seed_data):
        """POST /rma/returns 创建返厂退货单成功返回 201。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-TEST-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
            "remark": "契约测试",
        }
        res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["return_no"] is not None
        assert data["return_no"].startswith("FC")
        assert data["status"] == "PENDING_DIAGNOSIS"
        assert data["sn"] == "SN-TEST-001"

    def test_list_returns_returns_page_result(self, client, auth_headers, seed_data):
        """GET /rma/returns 返回分页结构。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-TEST-002",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)

        res = client.get("/api/v1/rma/returns", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert "items" in data["data"]
        assert "total" in data["data"]

    def test_get_return_detail(self, client, auth_headers, seed_data):
        """GET /rma/returns/{id} 返回详情。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-TEST-003",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        res = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"]["id"] == return_id

    def test_export_returns_xlsx(self, client, auth_headers):
        """GET /rma/export 返回 Excel。"""
        res = client.get("/api/v1/rma/export", headers=auth_headers)
        assert res.status_code == 200
        assert "spreadsheet" in res.headers.get("content-type", "")


class TestRmaDiagnosisContract:
    """诊断报告 API 契约测试。"""

    def test_create_diagnosis_success(self, client, auth_headers, seed_data):
        """POST /rma/diagnoses 创建诊断报告。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-DIAG-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        diag_payload = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "电源模块损坏",
            "diagnosis_result": "REPAIRABLE",
            "repair_plan": "更换电源模块",
            "change_reason": "诊断",
        }
        res = client.post("/api/v1/rma/diagnoses", json=diag_payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["diagnosis_no"].startswith("DG")

        detail = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "DIAGNOSED"

    def test_diagnosis_requires_pending_status(self, client, auth_headers, seed_data):
        """只有待诊断的返厂单才能创建诊断报告。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-DIAG-002",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        diag = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "故障",
            "diagnosis_result": "REPAIRABLE",
            "change_reason": "诊断",
        }
        client.post("/api/v1/rma/diagnoses", json=diag, headers=auth_headers)

        res = client.post("/api/v1/rma/diagnoses", json=diag, headers=auth_headers)
        assert res.status_code == 400

    def test_get_diagnoses_list(self, client, auth_headers, seed_data):
        """GET /rma/returns/{id}/diagnoses 返回诊断列表。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-DIAG-003",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        res = client.get(f"/api/v1/rma/returns/{return_id}/diagnoses", headers=auth_headers)
        assert res.status_code == 200
        assert isinstance(res.json()["data"], list)


class TestRmaAssignContract:
    """分配 API 契约测试。"""

    def test_assign_return_success(self, client, auth_headers, seed_data):
        """POST /rma/returns/{id}/assign 分配返厂单。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-ASGN-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        diag = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "故障",
            "diagnosis_result": "REPAIRABLE",
            "change_reason": "诊断",
        }
        client.post("/api/v1/rma/diagnoses", json=diag, headers=auth_headers)

        assign_payload = {
            "assigned_to": seed_data["production"].id,
            "assign_type": "PRODUCTION",
            "assign_reason": "分配给生产部门维修",
            "change_reason": "分配",
        }
        res = client.post(
            f"/api/v1/rma/returns/{return_id}/assign",
            json=assign_payload, headers=auth_headers,
        )
        assert res.status_code == 200
        detail = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "ASSIGNED"


class TestRmaRepairContract:
    """维修工单 API 契约测试。"""

    def test_create_repair_success(self, client, auth_headers, seed_data):
        """POST /rma/repairs 创建维修工单。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-REP-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        diag = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "故障",
            "diagnosis_result": "REPAIRABLE",
            "change_reason": "诊断",
        }
        client.post("/api/v1/rma/diagnoses", json=diag, headers=auth_headers)

        assign = {
            "assigned_to": seed_data["production"].id,
            "assign_type": "PRODUCTION",
            "assign_reason": "分配维修",
            "change_reason": "分配",
        }
        client.post(f"/api/v1/rma/returns/{return_id}/assign", json=assign, headers=auth_headers)

        repair_payload = {
            "return_id": return_id,
            "repair_by": seed_data["production"].id,
            "old_sn": "SN-REP-001",
            "new_sn": "SN-REP-001-NEW",
            "repair_description": "更换电源模块",
            "materials_used": "电源模块x1",
            "fault_code": "E001",
            "start_time": "2026-09-08T09:00:00",
            "end_time": "2026-09-08T11:00:00",
            "repair_date": "2026-09-08",
            "change_reason": "维修",
        }
        res = client.post("/api/v1/rma/repairs", json=repair_payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["repair_no"].startswith("WX")


class TestRmaScrapContract:
    """报废审批 API 契约测试。"""

    def test_create_scrap_success(self, client, auth_headers, seed_data):
        """POST /rma/scraps 创建报废申请。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-SCRP-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        # 先诊断
        diag = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "故障",
            "diagnosis_result": "SCRAP",
            "change_reason": "诊断",
        }
        client.post("/api/v1/rma/diagnoses", json=diag, headers=auth_headers)

        scrap_payload = {
            "return_id": return_id,
            "scrap_reason": "无法修复，建议报废",
            "change_reason": "报废申请",
        }
        res = client.post("/api/v1/rma/scraps", json=scrap_payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["scrap_no"].startswith("BF")
        assert data["status"] == "PENDING"

    def test_approve_scrap(self, client, auth_headers, seed_data):
        """POST /rma/scraps/{id}/approve 审批报废单。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-SCRP-002",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        # 先诊断
        diag = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "故障",
            "diagnosis_result": "SCRAP",
            "change_reason": "诊断",
        }
        client.post("/api/v1/rma/diagnoses", json=diag, headers=auth_headers)

        scrap_res = client.post("/api/v1/rma/scraps", json={
            "return_id": return_id,
            "scrap_reason": "建议报废",
            "change_reason": "报废申请",
        }, headers=auth_headers)
        scrap_id = scrap_res.json()["id"]

        approve_res = client.post(
            f"/api/v1/rma/scraps/{scrap_id}/approve",
            json={"change_reason": "同意报废"},
            headers=auth_headers,
        )
        assert approve_res.status_code == 200


class TestRmaReshipContract:
    """再出货 API 契约测试。"""

    def test_create_reship_success(self, client, auth_headers, seed_data):
        """POST /rma/reships 创建再出货单。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-RSHP-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        # 诊断
        diag = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "故障",
            "diagnosis_result": "REPAIRABLE",
            "change_reason": "诊断",
        }
        client.post("/api/v1/rma/diagnoses", json=diag, headers=auth_headers)

        # 分配
        assign = {
            "assigned_to": seed_data["production"].id,
            "assign_type": "PRODUCTION",
            "assign_reason": "分配维修",
            "change_reason": "分配",
        }
        client.post(f"/api/v1/rma/returns/{return_id}/assign", json=assign, headers=auth_headers)

        # 维修
        repair = {
            "return_id": return_id,
            "repair_by": seed_data["production"].id,
            "old_sn": "SN-RSHP-001",
            "new_sn": "SN-RSHP-001-NEW",
            "repair_description": "维修",
            "start_time": "2026-09-08T09:00:00",
            "end_time": "2026-09-08T11:00:00",
            "repair_date": "2026-09-08",
            "change_reason": "维修",
        }
        client.post("/api/v1/rma/repairs", json=repair, headers=auth_headers)

        # 质检
        qc = {
            "return_id": return_id,
            "checked_by": seed_data["quality"].id,
            "check_date": "2026-09-08",
            "check_result": "PASS",
            "check_description": "检验通过",
            "change_reason": "质检",
        }
        client.post("/api/v1/rma/quality-checks", json=qc, headers=auth_headers)

        # 入库
        wh = {
            "return_id": return_id,
            "confirmed_by": seed_data["warehouse"].id,
            "new_sn": "SN-RSHP-001-NEW",
            "warehouse_type": "ZERO_COST_FINISHED",
            "change_reason": "入库",
        }
        client.post("/api/v1/rma/warehouse-ins", json=wh, headers=auth_headers)

        reship_payload = {
            "return_id": return_id,
            "new_sn": "SN-RSHP-001-NEW-RSHP",
            "software_version": "V2.0.1",
            "ship_date": "2026-09-08",
            "recipient": "测试客户",
            "change_reason": "再出货",
        }
        res = client.post("/api/v1/rma/reships", json=reship_payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["reship_no"].startswith("RH")


class TestRmaQualityCheckContract:
    """质量检验 API 契约测试。"""

    def test_create_quality_check(self, client, auth_headers, seed_data):
        """POST /rma/quality-checks 创建质量检验。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-QC-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        diag = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "故障",
            "diagnosis_result": "REPAIRABLE",
            "change_reason": "诊断",
        }
        client.post("/api/v1/rma/diagnoses", json=diag, headers=auth_headers)

        assign = {
            "assigned_to": seed_data["production"].id,
            "assign_type": "PRODUCTION",
            "assign_reason": "分配维修",
            "change_reason": "分配",
        }
        client.post(f"/api/v1/rma/returns/{return_id}/assign", json=assign, headers=auth_headers)

        repair = {
            "return_id": return_id,
            "repair_by": seed_data["production"].id,
            "old_sn": "SN-QC-001",
            "new_sn": "SN-QC-001-NEW",
            "repair_description": "维修",
            "start_time": "2026-09-08T09:00:00",
            "end_time": "2026-09-08T11:00:00",
            "repair_date": "2026-09-08",
            "change_reason": "维修",
        }
        client.post("/api/v1/rma/repairs", json=repair, headers=auth_headers)

        qc_payload = {
            "return_id": return_id,
            "checked_by": seed_data["quality"].id,
            "check_date": "2026-09-08",
            "check_result": "PASS",
            "check_description": "维修后检验通过",
            "change_reason": "质检",
        }
        res = client.post("/api/v1/rma/quality-checks", json=qc_payload, headers=auth_headers)
        assert res.status_code == 201


class TestRmaWarehouseInContract:
    """入库审核 API 契约测试。"""

    def test_create_warehouse_in(self, client, auth_headers, seed_data):
        """POST /rma/warehouse-ins 返厂入库。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-WH-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = create_res.json()["id"]

        diag = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "故障",
            "diagnosis_result": "REPAIRABLE",
            "change_reason": "诊断",
        }
        client.post("/api/v1/rma/diagnoses", json=diag, headers=auth_headers)

        assign = {
            "assigned_to": seed_data["production"].id,
            "assign_type": "PRODUCTION",
            "assign_reason": "分配维修",
            "change_reason": "分配",
        }
        client.post(f"/api/v1/rma/returns/{return_id}/assign", json=assign, headers=auth_headers)

        repair = {
            "return_id": return_id,
            "repair_by": seed_data["production"].id,
            "old_sn": "SN-WH-001",
            "repair_description": "维修",
            "start_time": "2026-09-08T09:00:00",
            "end_time": "2026-09-08T11:00:00",
            "repair_date": "2026-09-08",
            "change_reason": "维修",
        }
        client.post("/api/v1/rma/repairs", json=repair, headers=auth_headers)

        qc = {
            "return_id": return_id,
            "checked_by": seed_data["quality"].id,
            "check_date": "2026-09-08",
            "check_result": "PASS",
            "check_description": "通过",
            "change_reason": "质检",
        }
        client.post("/api/v1/rma/quality-checks", json=qc, headers=auth_headers)

        wh_payload = {
            "return_id": return_id,
            "new_sn": "SN-WH-001-NEW",
            "repair_count": 1,
            "repair_reason": "更换电源模块",
            "change_reason": "入库",
        }
        res = client.post("/api/v1/rma/warehouse-ins", json=wh_payload, headers=auth_headers)
        assert res.status_code == 201