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

    page.goto(f"{BASE}/adjustment")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)

    title = page.locator(".page-title").text_content()
    print(f"[OK] Title: {title}")
    assert "库存调整" in title

    add_btn = page.locator('button:has-text("创建调整")')
    assert add_btn.is_visible()
    print("[OK] Create button visible")

    add_btn.click()
    page.wait_for_timeout(800)
    dialog = page.locator('.el-dialog')
    assert dialog.is_visible()
    print("[OK] Create dialog opened")

    steps = page.locator('.el-step')
    count = steps.count()
    print(f"[OK] Steps count: {count}")

    page.click('.el-dialog button:has-text("取消")')
    page.wait_for_timeout(500)

    table = page.locator("table")
    assert table.count() > 0
    print("[OK] Table loaded")

    page.screenshot(path="adjustment_test.png", full_page=True)
    print("[OK] Screenshot saved")

    browser.close()
    print("\n=== InventoryAdjustment page verification PASSED ===")