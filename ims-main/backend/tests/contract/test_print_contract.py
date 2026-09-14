"""print API 契约测试。"""

import pytest
from datetime import date


class TestPrintContract:
    """打印 API 契约测试。"""

    def test_get_incoming_receipt_print_data(self, client, db_session, auth_headers, seed_data):
        """GET /print/incoming_receipt/{id} 返回收货单打印数据。"""
        from app.models.incoming import IncomingReceipt

        receipt = IncomingReceipt(
            receipt_no="RC-TEST-001",
            supplier_id=seed_data["supplier"].id,
            sku_id=seed_data["sku_raw"].id,
            batch_no="BATCH-TEST",
            quantity=100,
            unit="个",
            status="ACCEPTED",
            delivery_date=date.today(),
        )
        db_session.add(receipt)
        db_session.commit()
        db_session.refresh(receipt)
        rid = receipt.id

        res = client.get(f"/api/v1/print/incoming_receipt/{rid}", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["doc_type"] == "incoming_receipt"
        assert data["data"]["doc_title"] == "采购收货单"
        assert data["data"]["company"]["full_name"] == "西安敦临计量检测有限公司"
        assert data["data"]["company"]["short_name"] == "敦临计量"
        assert "data" in data["data"]
        assert data["data"]["data"]["receipt_no"] == "RC-TEST-001"

    def test_get_incoming_receipt_print_not_found(self, client, auth_headers):
        """GET /print/incoming_receipt/{id} 不存在的单据返回失败。"""
        res = client.get("/api/v1/print/incoming_receipt/99999", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] != 0

    def test_get_shipment_print_data(self, client, db_session, auth_headers, seed_data):
        """GET /print/shipment/{id} 返回出货单打印数据。"""
        from app.models.shipment import Shipment

        shipment = Shipment(
            shipment_no="SH-TEST-001",
            sku_id=seed_data["sku_fg"].id,
            sku_code=seed_data["sku_fg"].sku_code,
            sku_name=seed_data["sku_fg"].name,
            spec=seed_data["sku_fg"].spec,
            unit="个",
            sn_list="",
            quantity=10,
            ship_date=date.today(),
            address="测试地址",
            logistics_provider="顺丰速运",
            tracking_no="SF1234567890",
            created_by="admin",
        )
        db_session.add(shipment)
        db_session.commit()
        db_session.refresh(shipment)
        sid = shipment.id

        res = client.get(f"/api/v1/print/shipment/{sid}", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] == 0
        assert data["data"]["doc_type"] == "shipment"
        assert data["data"]["doc_title"] == "出货单"
        assert data["data"]["company"]["full_name"] == "西安敦临计量检测有限公司"
        assert "data" in data["data"]
        assert data["data"]["data"]["shipment_no"] == "SH-TEST-001"
        assert "items" in data["data"]

    def test_get_shipment_print_not_found(self, client, auth_headers):
        """GET /print/shipment/{id} 不存在的单据返回失败。"""
        res = client.get("/api/v1/print/shipment/99999", headers=auth_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["code"] != 0

    def test_print_requires_auth(self, client):
        """打印接口需要鉴权。"""
        res = client.get("/api/v1/print/incoming_receipt/1")
        assert res.status_code == 401