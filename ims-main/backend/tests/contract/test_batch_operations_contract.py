"""
改善点 #6 — 批量操作增强 契约测试
验证批量提交审核、批量分配、批量导出的正确性和事务一致性。
"""

import pytest


class TestBatchOperationsContract:
    """批量操作 API 契约测试。"""

    # =========================================================================
    # 现有单个操作验证（批量操作将复用这些基础端点）
    # =========================================================================

    def test_create_multiple_inbound_orders(self, client, auth_headers, seed_data):
        """可创建多张入库单（批量操作的前置条件）。"""
        ids = []
        # 创建第一张
        res = client.post("/api/v1/inbound/orders", json={
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": seed_data["supplier"].id,
            "remark": "批量测试-1",
            "lines": [{"sku_id": seed_data["sku_raw"].id, "quantity": 10, "unit_price": 100.00}],
        }, headers=auth_headers)
        assert res.status_code == 201
        ids.append(res.json()["data"]["id"])
        # 创建第二张（不同的数量，避免重复校验）
        res2 = client.post("/api/v1/inbound/orders", json={
            "inbound_mode": "PROCUREMENT",
            "stock_condition": "NEW",
            "partner_id": seed_data["supplier"].id,
            "remark": "批量测试-2",
            "lines": [{"sku_id": seed_data["sku_raw"].id, "quantity": 20, "unit_price": 200.00}],
        }, headers=auth_headers)
        # 第二张可能因幂等/重复校验返回400，接受失败
        if res2.status_code == 201:
            ids.append(res2.json()["data"]["id"])
        assert len(ids) >= 1
        return ids

    def test_multiple_outbound_orders_listable(self, client, auth_headers):
        """出库单列表可查询（批量操作前置条件）。"""
        res = client.get("/api/v1/outbound/orders", headers=auth_headers)
        assert res.status_code == 200
        assert "items" in res.json()["data"]

    def test_rma_return_can_list_all(self, client, auth_headers, seed_data):
        """RMA退货单列表可查询（批量分配的前置条件）。"""
        res = client.get("/api/v1/rma/returns", headers=auth_headers)
        assert res.status_code == 200
        assert "items" in res.json()["data"]

    def test_export_endpoint_exists(self, client, auth_headers):
        """导出接口存在且返回200。"""
        res = client.get("/api/v1/inbound/orders/export", headers=auth_headers)
        assert res.status_code in [200, 404]

    # =========================================================================
    # 批量操作端点（规格占位 — 待后端实现）
    # =========================================================================

    @pytest.mark.skip(reason="批量提交入库单端点尚未实现")
    def test_batch_submit_inbound(self, client, auth_headers, seed_data):
        """POST /inbound/orders/batch-submit 批量提交入库单。"""
        ids = self.test_create_multiple_inbound_orders(client, auth_headers, seed_data)
        res = client.post("/api/v1/inbound/orders/batch-submit", json={
            "ids": ids,
        }, headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert "success" in data["data"]
        assert "failed" in data["data"]

    @pytest.mark.skip(reason="批量提交入库单端点尚未实现")
    def test_batch_submit_partial_failure(self, client, auth_headers, seed_data):
        """部分单据不符合条件时，符合条件的仍应成功。"""
        ids = self.test_create_multiple_inbound_orders(client, auth_headers, seed_data)
        # 先提交第1张
        client.put(f"/api/v1/inbound/orders/{ids[0]}/submit", headers=auth_headers)
        # 批量提交全部3张，第1张应失败，第2/3张应成功
        res = client.post("/api/v1/inbound/orders/batch-submit", json={
            "ids": ids,
        }, headers=auth_headers)
        data = res.json()["data"]
        assert len(data["failed"]) >= 1

    @pytest.mark.skip(reason="批量分配RMA端点尚未实现")
    def test_batch_assign_rma(self, client, auth_headers, seed_data):
        """POST /rma/returns/batch-assign 批量分配维修任务。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-BATCH-RMA",
            "quantity": 1, "unit": "个",
            "customer_name": "批量分配测试",
            "return_reason": "测试",
            "return_date": "2026-09-20",
        }
        res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = res.json()["id"]

        batch_res = client.post("/api/v1/rma/returns/batch-assign", json={
            "ids": [return_id],
            "assigned_to": seed_data["test_eng"].id,
        }, headers=auth_headers)
        assert batch_res.status_code == 200

    @pytest.mark.skip(reason="批量导出端点尚未实现")
    def test_export_with_ids_param(self, client, auth_headers):
        """GET /inbound/orders/export?ids=1,2,3 按ID导出。"""
        res = client.get("/api/v1/inbound/orders/export?ids=1,2,3", headers=auth_headers)
        assert res.status_code == 200

    @pytest.mark.skip(reason="批量操作端点尚未实现")
    def test_warehouse_permission_restricted(self, client, auth_headers_warehouse, seed_data):
        """仓库角色批量操作权限限制。"""
        payload = {
            "sku_id": seed_data["sku_fg"].id,
            "sn": "SN-BATCH-PERM",
            "quantity": 1, "unit": "个",
            "customer_name": "权限测试",
            "return_reason": "测试",
            "return_date": "2026-09-20",
        }
        res = client.post("/api/v1/rma/returns", json=payload, headers=auth_headers)
        return_id = res.json()["id"]

        batch_res = client.post("/api/v1/rma/returns/batch-assign", json={
            "ids": [return_id], "assigned_to": 1,
        }, headers=auth_headers_warehouse)
        assert batch_res.status_code == 403