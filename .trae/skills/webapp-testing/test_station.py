from playwright.sync_api import sync_playwright

BASE = "https://localhost:5173"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(ignore_https_errors=True)
    page = ctx.new_page()

    page.goto(f"{BASE}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[placeholder="用户名"]', "admin")
    page.fill('input[placeholder="密码"]', "admin123")
    page.click('button:has-text("登 录")')
    page.wait_for_url("**/dashboard**", timeout=10000)
    print("[OK] Login succeeded, at dashboard")

    page.goto(f"{BASE}/station")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)

    title = page.locator(".page-title").text_content()
    print(f"[OK] Page title: {title}")
    assert "场站" in title, f"Expected page title, got: {title}"

    add_btn = page.locator('button:has-text("新增场站")')
    assert add_btn.is_visible(), "Add button not visible"
    print("[OK] Add button visible")

    search_btn = page.locator('button:has-text("搜索")')
    assert search_btn.is_visible(), "Search button not visible"
    print("[OK] Search button visible")

    table = page.locator("table")
    assert table.count() > 0, "Table not found"
    print("[OK] Table loaded")

    page.screenshot(path="station_test.png", full_page=True)
    print("[OK] Screenshot saved: station_test.png")

    browser.close()
    print("\n=== Station page verification PASSED ===")