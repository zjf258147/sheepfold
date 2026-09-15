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

    # check table scroll behavior
    info = page.evaluate('''() => {
        const bodyWrapper = document.querySelector('.el-table__body-wrapper');
        const headerWrapper = document.querySelector('.el-table__header-wrapper');
        const main = document.querySelector('.el-main');
        const table = document.querySelector('.el-table');
        return {
            bodyWrapper: bodyWrapper ? {scrollW: bodyWrapper.scrollWidth, clientW: bodyWrapper.clientWidth, scrollH: bodyWrapper.scrollHeight, clientH: bodyWrapper.clientHeight} : null,
            headerWrapper: headerWrapper ? {scrollW: headerWrapper.scrollWidth, clientW: headerWrapper.clientWidth} : null,
            main: main ? {scrollW: main.scrollWidth, clientW: main.clientWidth} : null,
            table: table ? {scrollW: table.scrollWidth, clientW: table.clientWidth} : null,
            viewport: {w: window.innerWidth, h: window.innerHeight}
        };
    }''')
    print("=== DIMENSIONS ===")
    for k, v in info.items():
        print(f"  {k}: {v}")

    # get all table cell text for first 3 rows
    rows = page.locator('.el-table__body tr').all()
    print(f"\n=== FIRST 3 ROWS DATA ===")
    for i, row in enumerate(rows[:3]):
        cells = row.locator('td').all()
        cell_data = []
        for j, cell in enumerate(cells):
            txt = cell.text_content().strip()
            # check if cell has any special styling
            inner = cell.locator('.cell').first
            has_overflow = inner.evaluate('el => el.scrollWidth > el.clientWidth') if inner.count() > 0 else False
            cell_data.append(f'"{txt}"{"[OVF]" if has_overflow else ""}')
        print(f"  Row {i+1}: {cell_data}")

    # check search bar layout
    print("\n=== SEARCH BAR ===")
    search_html = page.locator('.search-bar').first.inner_html() if page.locator('.search-bar').count() > 0 else 'N/A'
    print(search_html[:500])

    # check for any CSS that might hide content
    hidden_els = page.evaluate('''() => {
        const tds = document.querySelectorAll('.el-table__body td');
        let issues = [];
        tds.forEach((td, i) => {
            const cell = td.querySelector('.cell');
            if (cell) {
                const style = window.getComputedStyle(cell);
                if (style.overflow === 'hidden' && cell.scrollWidth > cell.clientWidth) {
                    issues.push({idx: i, text: cell.textContent.substring(0,30), overflow: 'hidden', scrollW: cell.scrollWidth, clientW: cell.clientWidth});
                }
            }
        });
        return issues.slice(0, 20);
    }''')
    print(f"\n=== CELL OVERFLOW ISSUES ===")
    if hidden_els:
        for issue in hidden_els:
            print(f"  {issue}")
    else:
        print("  None")

    browser.close()