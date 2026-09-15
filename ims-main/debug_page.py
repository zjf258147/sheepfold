"""调试页面加载"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    console = []
    page.on('console', lambda msg: console.append(f'[{msg.type}] {msg.text}'))
    page.on('pageerror', lambda err: console.append(f'[ERROR] {err}'))

    page.goto('http://localhost:5173/')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    print('URL:', page.url)
    if 'login' in page.url.lower():
        page.fill('input[placeholder="用户名"]', 'admin')
        page.fill('input[placeholder="密码"]', 'admin123')
        page.click('button span:has-text("登")')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(5000)

    print('After login URL:', page.url)

    html = page.content()
    print('Content length:', len(html))

    body_text = page.locator('body').inner_text()
    print('Body text (first 2000):', body_text[:2000])

    for c in console[:20]:
        print(c)
    browser.close()