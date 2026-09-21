"""
改善点 #2 — 维修知识库 契约测试
验证知识库 CRUD、搜索推荐、工单沉淀。
当前状态：知识库表/API 尚未实现，测试为规格占位。
"""

import pytest


class TestRmaKnowledgeBaseContract:
    """维修知识库 API 契约测试。"""

    # =========================================================================
    # 现有RMA数据验证（知识库将依赖这些数据源）
    # =========================================================================

    def test_existing_rma_returns_have_fault_data(self, client, auth_headers, seed_data):
        """RMA退货单已存在，可含故障描述。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-KB-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "知识库测试客户",
            "return_reason": "电源模块故障",
            "return_date": "2026-09-20",
        }
        res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        assert res.status_code == 201
        data = res.json()
        assert data["return_no"] is not None
        assert data["status"] == "PENDING_DIAGNOSIS"
        return data["id"]

    def test_existing_diagnosis_has_fault_description(self, client, auth_headers, seed_data):
        """诊断记录含故障描述，可作为知识库数据源。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-KB-002",
            "quantity": 1,
            "unit": "个",
            "customer_name": "诊断测试客户",
            "return_reason": "设备无法开机",
            "return_date": "2026-09-20",
        }
        res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        assert res.status_code == 201
        return_id = res.json()["id"]

        diag_res = client.post("/api/v1/rma/diagnoses", json={
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-20",
            "fault_description": "电源模块损坏，无法正常启动",
            "diagnosis_result": "REPAIRABLE",
            "repair_plan": "更换电源模块",
            "change_reason": "诊断",
        }, headers=auth_headers)
        assert diag_res.status_code == 201
        assert diag_res.json()["fault_description"] == "电源模块损坏，无法正常启动"

        detail = client.get(f"/api/v1/rma/returns/{return_id}", headers=auth_headers)
        assert detail.json()["data"]["status"] == "DIAGNOSED"

    # =========================================================================
    # 知识库端点（规格占位 — 待后端实现）
    # =========================================================================

    def test_create_knowledge_base_entry(self, client, auth_headers):
        """POST /rma/knowledge-base 创建知识库条目。"""
        res = client.post("/api/v1/rma/knowledge-base", json={
            "title": "电源模块故障",
            "fault_code": "E001",
            "fault_symptom": "设备无法开机",
            "solution": "更换电源模块",
            "tags": ["电源", "开机"],
        }, headers=auth_headers)
        assert res.status_code == 201

    def test_search_knowledge_base(self, client, auth_headers):
        """GET /rma/knowledge-base/search 关键词搜索。"""
        res = client.get("/api/v1/rma/knowledge-base/search?keyword=无法开机", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data["data"], list)

    def test_search_no_results(self, client, auth_headers):
        """搜索无匹配结果时返回空数组。"""
        res = client.get("/api/v1/rma/knowledge-base/search?keyword=xyz123notfound", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["data"] == []

    def test_create_from_repair(self, client, auth_headers, seed_data):
        """POST /rma/knowledge-base/from-repair/{repair_id} 从维修工单沉淀。"""
        res = client.post("/api/v1/rma/knowledge-base/from-repair/1", headers=auth_headers)
        assert res.status_code == 201

    def test_unauthorized_access(self, client):
        """未登录访问返回 401。"""
        res = client.get("/api/v1/rma/knowledge-base/search?keyword=test")
        assert res.status_code == 401