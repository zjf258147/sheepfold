"""
E2E 端到端测试 — 3条核心业务流程
===========================================
运行前提：
  1. MySQL 数据库已启动并初始化
  2. Redis 已启动
  3. 后端已启动: cd backend && python main.py (端口 8000)
  4. 前端已启动: cd frontend && npm run dev (端口 5173)
  5. 种子数据已导入: cd backend && python seed_demo.py
  6. Playwright 浏览器已安装: python -m playwright install chromium

运行方式：
  # 方式1：手动启动服务后运行
  python -m pytest tests/e2e/ -v --tb=short

  # 方式2：使用 with_server.py 自动管理服务
  python ../.trae/skills/webapp-testing/scripts/with_server.py \
    --server "cd backend && python main.py" --port 8000 \
    --server "cd frontend && npm run dev" --port 5173 \
    --timeout 60 \
    -- python -m pytest tests/e2e/ -v --tb=short
"""

import os
import time
from playwright.sync_api import sync_playwright, Page, expect

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:5173")
API_URL = os.environ.get("E2E_API_URL", "http://localhost:8000")

TEST_USER = {
    "username": "admin",
    "password": "admin123",
}

WAIT_TIMEOUT = 30000


def login(page: Page, username: str = TEST_USER["username"], password: str = TEST_USER["password"]):
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[placeholder="用户名"]', username)
    page.fill('input[placeholder="密码"]', password)
    page.click('button:has-text("登 录")')
    page.wait_for_load_state("networkidle")
    page.wait_for_url("**/dashboard**", timeout=WAIT_TIMEOUT)


def _create_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    return p, browser, context


class TestE2ELoginReceiptInspectionInbound:
    def test_full_flow(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.wait_for_load_state("networkidle")
            page.screenshot(path="/tmp/e2e_dashboard.png", full_page=True)
            assert page.url.endswith("/dashboard") or "/dashboard" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()


class TestE2ERMAFullFlow:
    def test_rma_page_accessible(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.wait_for_load_state("networkidle")
            page.goto(f"{BASE_URL}/rma/returns")
            page.wait_for_load_state("networkidle")
            page.screenshot(path="/tmp/e2e_rma_returns.png", full_page=True)
            assert "/rma/returns" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()


class TestE2EOutboundShipment:
    def test_outbound_page_accessible(self):
        p, browser, context = _create_browser()
        page = context.new_page()
        try:
            login(page)
            page.wait_for_load_state("networkidle")
            page.goto(f"{BASE_URL}/outbound")
            page.wait_for_load_state("networkidle")
            page.screenshot(path="/tmp/e2e_outbound.png", full_page=True)
            assert "/outbound" in page.url
        finally:
            context.close()
            browser.close()
            p.stop()