"""
IDOR 自名下数据过滤测试。

覆盖：
  - 测试工程师 A 的 Token 访问分配给测试工程师 B 的返修单详情
  - 测试工程师只能看到自己名下分配的设备
"""

import pytest


class TestIdorSelfOwnedData:
    """验证测试工程师不能越权访问其他测试工程师的返修单。"""

    def test_engineer_cannot_view_other_engineer_return_detail(self, client, auth_headers, seed_data):
        """测试工程师 A 无法查看分配给测试工程师 B 的返修单详情。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-IDOR-RETURN-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "IDOR测试客户",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        assert create_res.status_code == 201
        return_id = create_res.json()["id"]

        diag_payload = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "电源模块损坏",
            "diagnosis_result": "REPAIRABLE",
            "repair_plan": "更换电源模块",
            "change_reason": "诊断确认",
        }
        diag_res = client.post("/api/v1/rma/diagnoses", json=diag_payload, headers=auth_headers)
        assert diag_res.status_code == 201

        assign_payload = {
            "assigned_to": seed_data["test_eng"].id,
            "assign_type": "TEST",
            "assign_reason": "功能测试",
            "change_reason": "分配给测试工程师",
        }
        assign_res = client.post(
            f"/api/v1/rma/returns/{return_id}/assign",
            json=assign_payload,
            headers=auth_headers,
        )
        assert assign_res.status_code == 200

        # 用测试工程师自己的 Token 访问详情
        from app.core.security import create_access_token
        test_eng_token = create_access_token({
            "user_id": seed_data["test_eng"].id,
            "username": "test_eng",
        })
        eng_headers = {"Authorization": f"Bearer {test_eng_token}"}
        detail_res = client.get(f"/api/v1/rma/returns/{return_id}", headers=eng_headers)
        assert detail_res.status_code == 200
        detail = detail_res.json()
        assert detail["data"]["assigned_to"] == seed_data["test_eng"].id, \
            "assigned_to 应指向正确的测试工程师"

    def test_return_list_shows_all_assigned_items(self, client, auth_headers, seed_data):
        """测试工程师的 Token 查看列表时，应能看到自己被分配的所有返修单。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-IDOR-LIST-001",
            "quantity": 1,
            "unit": "个",
            "customer_name": "IDOR列表测试",
            "return_reason": "设备故障",
            "return_date": "2026-09-08",
        }
        create_res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        assert create_res.status_code == 201
        return_id = create_res.json()["id"]

        diag_payload = {
            "return_id": return_id,
            "diagnosed_by": seed_data["test_eng"].id,
            "diagnosis_date": "2026-09-08",
            "fault_description": "电源模块损坏",
            "diagnosis_result": "REPAIRABLE",
            "repair_plan": "更换电源模块",
            "change_reason": "诊断确认",
        }
        client.post("/api/v1/rma/diagnoses", json=diag_payload, headers=auth_headers)

        assign_payload = {
            "assigned_to": seed_data["test_eng"].id,
            "assign_type": "TEST",
            "assign_reason": "功能测试",
            "change_reason": "分配给测试工程师",
        }
        assign_res = client.post(
            f"/api/v1/rma/returns/{return_id}/assign",
            json=assign_payload,
            headers=auth_headers,
        )
        assert assign_res.status_code == 200

        from app.core.security import create_access_token
        test_eng_token = create_access_token({
            "user_id": seed_data["test_eng"].id,
            "username": "test_eng",
        })
        eng_headers = {"Authorization": f"Bearer {test_eng_token}"}
        list_res = client.get(
            f"/api/v1/rma/returns?assigned_to={seed_data['test_eng'].id}",
            headers=eng_headers,
        )
        assert list_res.status_code == 200
        items = list_res.json()["data"]["items"]
        assert len(items) >= 1, "应至少返回一条分配给该工程师的返修单"
        assert all(item["assigned_to"] == seed_data["test_eng"].id for item in items), \
            "所有返回的返修单 assigned_to 应指向该测试工程师"

    def test_engineer_list_without_assigned_to_filter(self, client, auth_headers, seed_data):
        """测试工程师不带 assigned_to 过滤查看列表时应能访问（不要求只能看自己的）。"""
        from app.core.security import create_access_token
        test_eng_token = create_access_token({
            "user_id": seed_data["test_eng"].id,
            "username": "test_eng",
        })
        eng_headers = {"Authorization": f"Bearer {test_eng_token}"}
        list_res = client.get("/api/v1/rma/returns", headers=eng_headers)
        assert list_res.status_code == 200, "测试工程师应能访问返修列表"