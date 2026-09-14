"""跨浏览器兼容性测试（P2）

使用 Playwright 在 Chrome / Edge / Firefox 中验证：
  1. 登录页渲染
  2. 表单元素可用性
  3. 无控制台 JS 错误
  4. 响应式布局（移动端视口）

运行前提：
  1. 前端已启动: cd frontend && npm run dev
  2. Playwright 浏览器已安装:
     python -m playwright install chromium firefox
     (Edge 使用 Windows 内置 channel)

运行方式：
  cd backend && python -m pytest tests/e2e/test_cross_browser.py -v --tb=short
"""

import os
import pytest
from playwright.sync_api import sync_playwright, Browser, Page

BASE_URL = os.environ.get("E2E_BASE_URL", "https://localhost:5173")

try:
    from playwright.sync_api import sync_playwright as _sp
    _sp().start().stop()
    FIREFOX_AVAILABLE = True
except Exception:
    FIREFOX_AVAILABLE = False


def _launch_browser(p, browser_name: str, channel: str | None) -> Browser:
    if channel:
        return p.chromium.launch(channel=channel, headless=True)
    return getattr(p, browser_name).launch(headless=True)


def _check_page(browser_name: str, browser_label: str, channel: str | None, url: str, check_fn) -> bool:
    with sync_playwright() as p:
        browser = _launch_browser(p, browser_name, channel)
        context = browser.new_context(
            ignore_https_errors=True,
            viewport={"width": 1440, "height": 900},
        )
        page = context.new_page()
        try:
            page.goto(url, timeout=15000)
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(1000)
            return check_fn(page, browser_label)
        except Exception as e:
            print(f"  ❌ {browser_label}: {e}")
            return False
        finally:
            context.close()
            browser.close()


class TestCrossBrowserLogin:

    def test_login_page_renders_chromium(self):
        result = _check_page("chromium", "Chrome", None, f"{BASE_URL}/login", _check)
        assert result, "Chrome 登录页渲染失败"

    def test_login_page_renders_edge(self):
        result = _check_page("chromium", "Edge", "msedge", f"{BASE_URL}/login", _check)
        assert result, "Edge 登录页渲染失败"

    @pytest.mark.skipif(not FIREFOX_AVAILABLE, reason="Firefox 未安装")
    def test_login_page_renders_firefox(self):
        result = _check_page("firefox", "Firefox", None, f"{BASE_URL}/login", _check)
        assert result, "Firefox 登录页渲染失败"


class TestCrossBrowserConsole:

    def test_no_console_errors_chromium(self):
        def check(page: Page, label: str):
            errors = _collect_errors(page)
            if errors:
                print(f"  ! {label} 控制台错误: {errors[:3]}")
                return False
            return True
        result = _check_page("chromium", "Chrome", None, f"{BASE_URL}/login", check)
        assert result, "Chrome 控制台错误"

    def test_no_console_errors_edge(self):
        def check(page: Page, label: str):
            errors = _collect_errors(page)
            if errors:
                print(f"  ! {label} 控制台错误: {errors[:3]}")
                return False
            return True
        result = _check_page("chromium", "Edge", "msedge", f"{BASE_URL}/login", check)
        assert result, "Edge 控制台错误"

    @pytest.mark.skipif(not FIREFOX_AVAILABLE, reason="Firefox 未安装")
    def test_no_console_errors_firefox(self):
        def check(page: Page, label: str):
            errors = _collect_errors(page)
            if errors:
                print(f"  ! {label} 控制台错误: {errors[:3]}")
                return False
            return True
        result = _check_page("firefox", "Firefox", None, f"{BASE_URL}/login", check)
        assert result, "Firefox 控制台错误"


class TestCrossBrowserRouteGuard:

    def test_route_guard_chromium(self):
        def check(page: Page, label: str):
            page.goto(f"{BASE_URL}/dashboard")
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(1000)
            if "/login" in page.url:
                return True
            print(f"  ! {label} 路由守卫未跳转: {page.url}")
            return False
        result = _check_page("chromium", "Chrome", None, f"{BASE_URL}/dashboard", check)
        assert result, "Chrome 路由守卫失败"

    def test_route_guard_edge(self):
        def check(page: Page, label: str):
            page.goto(f"{BASE_URL}/dashboard")
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(1000)
            if "/login" in page.url:
                return True
            print(f"  ! {label} 路由守卫未跳转: {page.url}")
            return False
        result = _check_page("chromium", "Edge", "msedge", f"{BASE_URL}/dashboard", check)
        assert result, "Edge 路由守卫失败"


class TestCrossBrowserResponsive:

    def test_mobile_viewport_chromium(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                ignore_https_errors=True,
                viewport={"width": 375, "height": 812},
            )
            page = context.new_page()
            try:
                page.goto(f"{BASE_URL}/login", timeout=15000)
                page.wait_for_load_state("networkidle", timeout=30000)
                page.wait_for_timeout(1000)
                title = page.title()
                assert "IMS" in title, f"移动端标题不包含IMS: {title}"
                assert page.locator("button:has-text('登')").count() > 0
            finally:
                context.close()
                browser.close()

    def test_mobile_viewport_edge(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=True)
            context = browser.new_context(
                ignore_https_errors=True,
                viewport={"width": 375, "height": 812},
            )
            page = context.new_page()
            try:
                page.goto(f"{BASE_URL}/login", timeout=15000)
                page.wait_for_load_state("networkidle", timeout=30000)
                page.wait_for_timeout(1000)
                title = page.title()
                assert "IMS" in title, f"移动端标题不包含IMS: {title}"
                assert page.locator("button:has-text('登')").count() > 0
            finally:
                context.close()
                browser.close()


def _check(page: Page, label: str) -> bool:
    username = page.locator('input[placeholder="用户名"]')
    password = page.locator('input[placeholder="密码"]')
    login_btn = page.locator("button:has-text('登')")

    if username.count() == 0:
        print(f"  ! {label}: 用户名输入框不存在")
        return False
    if password.count() == 0:
        print(f"  ! {label}: 密码输入框不存在")
        return False
    if login_btn.count() == 0:
        print(f"  ! {label}: 登录按钮不存在")
        return False

    title = page.title()
    if "IMS" not in title:
        print(f"  ! {label}: 标题不包含IMS: {title}")
        return False

    return True


def _collect_errors(page: Page) -> list[str]:
    errors = []
    def _on_console(msg):
        if msg.type == "error":
            errors.append(msg.text)
    page.on("console", _on_console)
    page.wait_for_timeout(1000)
    return errors