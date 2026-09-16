"""
E2E 端到端测试 — 13 个核心用例覆盖 4 条业务主线
===========================================
运行前提：
  1. 后端已启动: cd backend && uv run uvicorn main:app --port 8000
  2. 前端已启动: cd frontend && npm run dev
  3. 数据库已有种子用户: admin/admin123, warehouse/123456 等

运行方式：
  python -m pytest tests/e2e/ -v --tb=short
"""

import os
from playwright.sync_api import sync_playwright, Page

BASE_URL = os.environ.get("E2E_BASE_URL", "http://127.0.0.1:5173")
API_URL = os.environ.get("E2E_API_URL", "http://127.0.0.1:8000")

TEST_USER = {"username": "admin", "password": "admin123"}
WAIT_TIMEOUT = 30000


def _create_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    return p, browser, context


def login(page: Page, username=TEST_USER["username"], password=TEST_USER["password"]):
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)
    if "/dashboard" in page.url:
        return
    page.fill('input[placeholder="用户名"]', username)
    page.fill('input[placeholder="密码"]', password)
    page.wait_for_timeout(200)
    page.click('.el-button--primary')
    page.wait_for_timeout(2000)
    current = page.url
    if "/dashboard" not in current:
        page.fill('input[placeholder="密码"]', password)
        page.press('input[placeholder="密码"]', 'Enter')
        page.wait_for_timeout(2000)
    assert "/dashboard" in page.url or "/login" not in page.url, f"登录失败: {page.url}"


class TestE2EAuth:
    def test_login_success(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.wait_for_load_state("networkidle")
            assert "/dashboard" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_login_bad_password_shows_error(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            page.goto(f"{BASE_URL}/login")
            page.wait_for_load_state("networkidle")
            page.fill('input[placeholder="用户名"]', "admin")
            page.fill('input[placeholder="密码"]', "wrongpassword")
            page.click('.el-button--primary')
            page.wait_for_timeout(2000)
            assert "/login" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_logout_redirects_to_login(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.wait_for_load_state("networkidle")
            page.evaluate("() => localStorage.removeItem('token')")
            page.goto(f"{BASE_URL}/dashboard")
            page.wait_for_load_state("networkidle")
            assert "/login" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()


class TestE2EDashboard:
    def test_dashboard_loads_with_stats(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            body = page.inner_text("body")
            assert "仪表盘" in body or "首页" in body or "库存" in body
        finally:
            context.close()
            browser.close()
            p.stop()


class TestE2EMainlineAPurchase:
    def test_incoming_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/incoming")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/incoming" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_inbound_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/inbound")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/inbound" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()


class TestE2EMainlineBRMA:
    def test_rma_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/rma")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/rma" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()


class TestE2EMainlineCShipment:
    def test_shipment_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/shipment")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/shipment" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_outbound_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/outbound")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/outbound" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()


class TestE2EMainlineDBOM:
    def test_bom_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/bom")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/bom" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_production_task_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/production-task")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/production-task" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()


class TestE2EInventory:
    def test_inventory_list_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/inventory")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/inventory" in page.url
            has_table = page.locator('.el-table').count() > 0
            has_empty = page.locator('.el-empty').count() > 0
            assert has_table or has_empty, "库存页无表格也无空数据状态"
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_inventory_sku_summary_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/inventory/sku")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/inventory/sku" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_snapshot_ledger_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/snapshot")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/snapshot" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()


class TestE2EDataPages:
    def test_products_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/products")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/products" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_partners_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/partners")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/partners" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_station_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/station")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/station" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_workflow_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/workflow")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
            assert "/workflow" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_about_page_loads(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.goto(f"{BASE_URL}/about")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/about" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()


class TestE2EPermissions:
    def test_warehouse_blocked_from_settings(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page, "warehouse", "123456")
            page.goto(f"{BASE_URL}/settings")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/dashboard" in page.url or "/settings" not in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_quality_can_access_incoming(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page, "quality", "123456")
            page.goto(f"{BASE_URL}/incoming")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/incoming" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_test_engineer_can_access_rma(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page, "test_eng", "123456")
            page.goto(f"{BASE_URL}/rma")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/rma" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()

    def test_production_can_access_bom(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page, "production", "123456")
            page.goto(f"{BASE_URL}/bom")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            assert "/bom" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()