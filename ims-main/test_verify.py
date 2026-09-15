from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    errors = []
    page.on('pageerror', lambda err: errors.append(f"[PAGE ERROR] {err.message}"))

    # 1. Login
    page.goto('http://localhost:5173/login')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    page.fill('input[placeholder="用户名"]', 'admin')
    page.fill('input[placeholder="密码"]', 'admin123')
    page.click('button:has-text("登 录")')
    page.wait_for_timeout(3000)
    page.wait_for_load_state('networkidle')

    # 2. Navigate to RMA
    page.goto('http://localhost:5173/rma')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    print("=== 1. RMA PAGE CHECK ===")
    print(f"Title: {page.title()}")
    print(f"Table rows: {page.locator('.el-table__body tr').count()}")
    print(f"Page errors: {len(errors)}")

    headers = page.locator('.el-table__header th .cell').all()
    header_texts = [h.text_content().strip() for h in headers]
    print(f"Table columns ({len(header_texts)}): {header_texts}")

    # 3. Find a PENDING_DIAGNOSIS row and click diagnosis
    diag_btn = page.locator('button:has-text("诊断")').first
    if diag_btn.count() > 0:
        diag_btn.click()
        page.wait_for_timeout(1000)
        print("\n=== 2. DIAGNOSIS DIALOG ===")
        page.locator('.el-dialog').last.locator('input[placeholder="必填"]').fill('测试诊断变更原因')
        page.locator('.el-dialog').last.locator('textarea').first.fill('测试故障描述')
        page.locator('.el-dialog').last.locator('.el-date-editor input').first.fill('2026-09-04')
        print("Form filled")
        submit = page.locator('.el-dialog').last.locator('button:has-text("提交诊断")')
        print(f"Submit enabled: {not submit.is_disabled()}")
        if not submit.is_disabled():
            submit.click()
            page.wait_for_timeout(3000)
            print("Diagnosis done!")
            # Close dialog if still open
            close_btn = page.locator('.el-dialog button:has-text("关闭"), .el-dialog button:has-text("取消")').first
            if close_btn.count() > 0:
                try:
                    close_btn.click()
                    page.wait_for_timeout(1000)
                except:
                    page.keyboard.press('Escape')
                    page.wait_for_timeout(1000)

    # 4. Assign
    page.wait_for_timeout(1000)
    assign_btn = page.locator('button:has-text("分配")').first
    if assign_btn.count() > 0:
        assign_btn.click()
        page.wait_for_timeout(1000)
        print("\n=== 3. ASSIGN DIALOG ===")
        page.locator('.el-dialog').last.locator('input[placeholder="请填写分配原因（必填）"]').fill('测试分配原因')
        page.locator('.el-dialog').last.locator('input[placeholder="必填"]').fill('测试变更原因')
        submit = page.locator('.el-dialog').last.locator('button:has-text("确认分配")')
        print(f"Submit enabled: {not submit.is_disabled()}")
        if not submit.is_disabled():
            submit.click()
            page.wait_for_timeout(3000)
            print("Assign done!")
            close_btn = page.locator('.el-dialog button:has-text("关闭"), .el-dialog button:has-text("取消")').first
            if close_btn.count() > 0:
                try:
                    close_btn.click()
                    page.wait_for_timeout(1000)
                except:
                    page.keyboard.press('Escape')
                    page.wait_for_timeout(1000)

    # 5. Now check the REPAIR dialog
    page.wait_for_timeout(1000)
    repair_btn = page.locator('button:has-text("维修")').first
    if repair_btn.count() > 0:
        repair_btn.click()
        page.wait_for_timeout(1500)
        print("\n=== 4. REPAIR DIALOG (FIX VERIFICATION) ===")

        dt_pickers = page.locator('.el-dialog').last.locator('.el-date-editor').all()
        print(f"DateTime pickers: {len(dt_pickers)}")
        for i, dp in enumerate(dt_pickers):
            w = dp.evaluate('el => el.offsetWidth')
            ph = dp.get_attribute('placeholder') or 'N/A'
            print(f"  {i+1}. '{ph}' -> width={w}px")

        # check dialog width for comparison
        dialog_w = page.locator('.el-dialog').last.evaluate('el => el.offsetWidth')
        print(f"Dialog width: {dialog_w}px")

        # all form items in the dialog
        form_items = page.locator('.el-dialog').last.locator('.el-form-item').all()
        print(f"Form items: {len(form_items)}")

        page.screenshot(path='/tmp/repair_dialog_fixed.png', full_page=True)
        print("Screenshot: /tmp/repair_dialog_fixed.png")

        page.locator('.el-dialog').last.locator('button:has-text("取消")').click()
    else:
        print("\n=== No repair button found ===")
        # print all statuses in the table
        statuses = page.locator('.el-table__body .el-tag').all()
        print("Statuses in table:")
        for s in statuses:
            print(f"  {s.text_content()}")

    print(f"\nTotal page errors: {len(errors)}")
    if errors:
        for e in errors[:5]:
            print(f"  {e}")

    browser.close()