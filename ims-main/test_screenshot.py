from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    # login
    page.goto('http://localhost:5173/login')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    page.fill('input[placeholder="用户名"]', 'admin')
    page.fill('input[placeholder="密码"]', 'admin123')
    page.click('button:has-text("登 录")')
    page.wait_for_timeout(3000)
    page.wait_for_load_state('networkidle')

    # navigate to RMA
    page.goto('http://localhost:5173/rma')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    # full page screenshot
    page.screenshot(path='/tmp/rma_full.png', full_page=True)

    # get table HTML to inspect
    table_html = page.locator('.el-table').inner_html()
    print("=== TABLE HTML (first 2000 chars) ===")
    print(table_html[:2000])

    print("\n=== END ===")
    browser.close()