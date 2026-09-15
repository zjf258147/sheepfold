from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on('pageerror', lambda err: print(f'  ERROR: {err}'))

    print("1. Login as admin...")
    page.goto('http://localhost:5173/')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)
    if 'login' in page.url.lower():
        page.fill('input[placeholder="用户名"]', 'admin')
        page.fill('input[placeholder="密码"]', 'admin123')
        page.click('button span:has-text("登")')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(3000)

    print("2. Check admin sidebar (all menus)...")
    html = page.content()
    for m in ['首页', '库存', '入库', '来料管理', '返厂维修', '出货管理', 'BOM', '出库', '商品SKU', '往来单位', '业务流程', '系统设置']:
        print(f"   {'PASS' if m in html else 'FAIL'}: {m}")

    print("3. Check BOM page role-based actions...")
    page.goto('http://localhost:5173/bom')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    html = page.content()
    for c in ['创建BOM', '导出CSV', '编辑', '齐套', '任务', '删除']:
        print(f"   {'PASS' if c in html else 'FAIL'}: {c}")

    print("4. Check ProductionTask page...")
    page.goto('http://localhost:5173/production-task')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    html = page.content()
    for c in ['任务编号', 'BOM编号', '齐套状态', '编辑', '删除']:
        print(f"   {'PASS' if c in html else 'FAIL'}: {c}")

    print("5. Check route guard for restricted page...")
    page.goto('http://localhost:5173/inbound')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    html = page.content()
    print(f"   {'PASS' if '入库' in html else 'FAIL'}: inbound page accessible")

    print("\n=== 第11步 权限验证 === 完成")
    browser.close()