from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on('pageerror', lambda err: print(f'  ERROR: {err}'))

    print("1. Login...")
    page.goto('http://localhost:5173/')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)
    if 'login' in page.url.lower():
        page.fill('input[placeholder="用户名"]', 'admin')
        page.fill('input[placeholder="密码"]', 'admin123')
        page.click('button span:has-text("登")')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(3000)

    print("2. Check sidebar...")
    html = page.content()
    for m in ['BOM', '出货管理', '来料管理', '返厂维修']:
        print(f"   {'PASS' if m in html else 'FAIL'}: {m}")

    print("3. BOM page...")
    page.goto('http://localhost:5173/bom')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    html = page.content()
    for c in ['BOM编号', 'BOM名称', '创建BOM', '导出CSV', '齐套', '任务']:
        print(f"   {'PASS' if c in html else 'FAIL'}: {c}")

    print("4. BOM dialog...")
    try:
        page.click('button:has-text("创建BOM")')
        page.wait_for_timeout(1000)
        html = page.content()
        for c in ['BOM名称', '成品物料', 'BOM明细', '添加物料', '单台用量', '损耗率']:
            print(f"   {'PASS' if c in html else 'FAIL'}: {c}")
        # close dialog
        cancel_btn = page.locator('.el-dialog button:has-text("取消")')
        if cancel_btn.count() > 0:
            cancel_btn.first.click()
        else:
            page.keyboard.press('Escape')
    except Exception as e:
        print(f"   FAIL: BOM dialog - {e}")

    print("5. ProductionTask page...")
    page.goto('http://localhost:5173/production-task')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    html = page.content()
    for c in ['任务编号', 'BOM编号', '齐套状态', '待生产', '生产中', '已完成']:
        print(f"   {'PASS' if c in html else 'FAIL'}: {c}")

    print("\n=== 主线D 收尾验证完成 ===")
    browser.close()