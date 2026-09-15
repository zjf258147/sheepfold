from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    page.screenshot(path='/tmp/rma_login.png', full_page=True)

    # discover all buttons
    buttons = page.locator('button').all()
    print("=== Buttons ===")
    for b in buttons:
        txt = b.text_content() or ''
        print(f"  Text: '{txt.strip()}' | Visible: {b.is_visible()}")

    # discover all inputs
    inputs = page.locator('input').all()
    print("\n=== Inputs ===")
    for i in inputs:
        ph = i.get_attribute('placeholder') or ''
        nm = i.get_attribute('name') or ''
        tp = i.get_attribute('type') or ''
        print(f"  Placeholder: '{ph}' | Name: '{nm}' | Type: '{tp}' | Visible: {i.is_visible()}")

    # discover text
    print("\n=== Page text (first 500 chars) ===")
    body = page.locator('body').first.text_content() or ''
    print(body[:500])

    print("\n=== Current URL ===")
    print(page.url)

    browser.close()