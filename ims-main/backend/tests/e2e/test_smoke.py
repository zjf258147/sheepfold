"""
前端页面冒烟测试 — 验证关键页面可正常渲染（无需后端/数据库）
============================================================
运行前提：
  1. 前端已启动: cd frontend && npm run dev (端口 5173)
  2. Playwright 浏览器已安装: python -m playwright install chromium

运行方式：
  python tests/e2e/test_smoke.py
"""

import os
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:5173")


def check_page_loads(url: str, expected_element: str, description: str) -> bool:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        try:
            page.goto(url, timeout=15000)
            page.wait_for_load_state("networkidle", timeout=30000)
            element = page.locator(expected_element)
            if element.count() > 0:
                print(f"  ✅ {description}")
                return True
            else:
                print(f"  ❌ {description} — 未找到元素: {expected_element}")
                page.screenshot(path=f"/tmp/e2e_smoke_fail_{description}.png", full_page=True)
                return False
        except Exception as e:
            print(f"  ❌ {description} — 异常: {e}")
            return False
        finally:
            context.close()
            browser.close()


def check_console_no_error(url: str, description: str) -> bool:
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        try:
            page.goto(url, timeout=15000)
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(1000)
            if errors:
                print(f"  ⚠️ {description} — 控制台错误: {errors[:3]}")
                return False
            else:
                print(f"  ✅ {description} — 无控制台错误")
                return True
        except Exception as e:
            print(f"  ❌ {description} — 异常: {e}")
            return False
        finally:
            context.close()
            browser.close()


def check_route_guard(url: str, description: str) -> bool:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        try:
            page.goto(url, timeout=15000)
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(1000)
            current_url = page.url
            if "/login" in current_url:
                print(f"  ✅ {description} — 正确跳转到登录页")
                return True
            else:
                print(f"  ❌ {description} — 未跳转登录页，当前: {current_url}")
                return False
        except Exception as e:
            print(f"  ❌ {description} — 异常: {e}")
            return False
        finally:
            context.close()
            browser.close()


def main():
    print("=" * 60)
    print("IMS 前端页面冒烟测试")
    print(f"BASE_URL = {BASE_URL}")
    print("=" * 60)

    pages = [
        (f"{BASE_URL}/login", "input[placeholder='用户名']", "登录页-用户名输入框"),
        (f"{BASE_URL}/login", "input[placeholder='密码']", "登录页-密码输入框"),
        (f"{BASE_URL}/login", "button:has-text('登')", "登录按钮存在"),
        (f"{BASE_URL}/login", "text=IMS", "页面标题IMS"),
    ]

    passed = 0
    failed = 0
    for url, selector, desc in pages:
        if check_page_loads(url, selector, desc):
            passed += 1
        else:
            failed += 1

    print("\n--- 控制台错误检查 ---")
    console_pages = [
        (f"{BASE_URL}/login", "登录页"),
        (f"{BASE_URL}/", "首页(路由守卫)"),
    ]
    for url, desc in console_pages:
        if check_console_no_error(url, desc):
            passed += 1
        else:
            failed += 1

    print("\n--- 路由守卫测试 ---")
    guard_pages = [
        (f"{BASE_URL}/dashboard", "Dashboard"),
        (f"{BASE_URL}/inbound", "入库管理"),
        (f"{BASE_URL}/outbound", "出库管理"),
        (f"{BASE_URL}/inventory", "库存管理"),
        (f"{BASE_URL}/rma/returns", "RMA返修"),
        (f"{BASE_URL}/bom", "BOM管理"),
        (f"{BASE_URL}/settings", "系统设置"),
    ]
    for url, desc in guard_pages:
        if check_route_guard(url, desc):
            passed += 1
        else:
            failed += 1

    print("=" * 60)
    print(f"结果: {passed} 通过, {failed} 失败, 共 {passed + failed} 项")
    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)