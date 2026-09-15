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
    print("[OK] Login")

    page.goto(f"{BASE}/device-ledger")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)

    title = page.locator(".page-title").text_content()
    print(f"[OK] Title: {title}")
    assert "设备台账" in title

    add_btn = page.locator('button:has-text("登记设备")')
    assert add_btn.is_visible()
    print("[OK] Register button visible")

    warranty_btn = page.locator('button:has-text("质保查询")')
    assert warranty_btn.is_visible()
    print("[OK] Warranty button visible")

    table = page.locator("table")
    assert table.count() > 0
    print("[OK] Table loaded")

    page.screenshot(path="device_ledger_test.png", full_page=True)
    print("[OK] Screenshot saved")

    browser.close()
    print("\n=== DeviceLedger page verification PASSED ===")