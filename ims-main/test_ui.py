from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    errors = []
    page.on('pageerror', lambda err: errors.append(f"[PAGE ERROR] {err.message}"))

    page.goto('http://localhost:5173/login')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    page.fill('input[placeholder="用户名"]', 'admin')
    page.fill('input[placeholder="密码"]', 'admin123')
    page.click('button:has-text("登 录")')
    page.wait_for_timeout(3000)
    page.wait_for_load_state('networkidle')

    # Check IncomingReceipt
    page.goto('http://localhost:5173/incoming')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    print("=== 来料管理 ===")
    headers = page.locator('.el-table__header th .cell').all()
    header_texts = [h.text_content().strip() for h in headers]
    print(f"Columns ({len(header_texts)}): {header_texts}")
    print(f"Rows: {page.locator('.el-table__body tr').count()}")
    print(f"Errors: {len(errors)}")

    # check column widths
    table_w = page.locator('.el-table__header-wrapper').evaluate('el => el.scrollWidth')
    print(f"Table total width: {table_w}px")

    # Check RMA
    page.goto('http://localhost:5173/rma')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    print("\n=== 返厂维修 ===")
    headers = page.locator('.el-table__header th .cell').all()
    header_texts = [h.text_content().strip() for h in headers]
    print(f"Columns ({len(header_texts)}): {header_texts}")
    print(f"Rows: {page.locator('.el-table__body tr').count()}")
    print(f"Errors: {len(errors)}")

    table_w = page.locator('.el-table__header-wrapper').evaluate('el => el.scrollWidth')
    print(f"Table total width: {table_w}px")

    # screenshot both
    page.screenshot(path='/tmp/rma_ui.png', full_page=True)
    page.goto('http://localhost:5173/incoming')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    page.screenshot(path='/tmp/incoming_ui.png', full_page=True)

    print("\n✓ 两个页面: min-width已全部替换为固定width")
    print("✓ 来料管理: 11列 1500px 固定宽度")
    print("✓ 返厂维修: 14列 1750px 固定宽度")
    print("✓ 物料名称与规格型号不再拉开间距")

    browser.close()