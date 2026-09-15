from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    page.goto('http://localhost:5173/login')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    page.fill('input[placeholder="用户名"]', 'admin')
    page.fill('input[placeholder="密码"]', 'admin123')
    page.click('button:has-text("登 录")')
    page.wait_for_timeout(3000)
    page.wait_for_load_state('networkidle')

    page.goto('http://localhost:5173/rma')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # click first 维修 button if available
    repair_btn = page.locator('button:has-text("维修")').first
    if repair_btn.count() > 0:
        repair_btn.click()
        page.wait_for_timeout(1500)

        # check the datetime pickers
        dt_pickers = page.locator('.el-dialog').last.locator('.el-date-editor').all()
        print(f"=== REPAIR DIALOG: {len(dt_pickers)} date pickers found ===")
        for i, dp in enumerate(dt_pickers):
            w = dp.evaluate('el => el.offsetWidth')
            placeholder = dp.get_attribute('placeholder')
            print(f"  Picker {i+1}: placeholder='{placeholder}', width={w}px")

        # screenshot just the dialog
        page.locator('.el-dialog').last.screenshot(path='/tmp/repair_dialog.png')
        print("  Screenshot saved to /tmp/repair_dialog.png")
    else:
        print("No repair button found - need to create a return first")

    browser.close()