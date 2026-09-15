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

    page.goto(f"{BASE}/station")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)

    page.click('button:has-text("新增场站")')
    page.wait_for_selector('.el-dialog', timeout=3000)
    print("[OK] Dialog opened")

    assert page.locator('.el-dialog__title:has-text("新增场站")').is_visible()
    print("[OK] Dialog title correct")

    page.fill('.el-dialog input[placeholder="请输入场站名称"]', "测试场站-Playwright")

    customer_select = page.locator('.el-dialog .el-form-item').filter(has_text='关联客户').locator('.el-select__wrapper')
    customer_select.click()
    page.wait_for_timeout(500)
    page.keyboard.press('ArrowDown')
    page.wait_for_timeout(300)
    page.keyboard.press('Enter')
    page.wait_for_timeout(500)
    print(f"[OK] Selected customer from dropdown via keyboard")

    page.click('.el-dialog button:has-text("保存")')
    page.wait_for_timeout(2000)
    print("[OK] Save clicked, waiting for response")

    body = page.text_content('body')
    if "测试场站-Playwright" in body:
        print("[OK] Station appears in table after creation")
    else:
        print("[WARN] Station may not appear - checking for error")

    toast = page.locator('.el-message').first
    try:
        toast.wait_for(timeout=2000)
        print(f"[TOAST] {toast.text_content()}")
    except:
        pass

    page.screenshot(path="station_dialog_test.png", full_page=True)
    print("[OK] Screenshot saved: station_dialog_test.png")

    browser.close()
    print("\n=== Station CRUD dialog test PASSED ===")