from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto("http://localhost:5173/login")
    page.wait_for_load_state("networkidle")
    
    # Find all inputs and buttons
    inputs = page.locator("input").all()
    buttons = page.locator("button").all()
    
    print("=== INPUTS ===")
    for i, inp in enumerate(inputs):
        print(f"  [{i}] placeholder={inp.get_attribute('placeholder')} type={inp.get_attribute('type')} id={inp.get_attribute('id')}")
    
    print("\n=== BUTTONS ===")
    for i, btn in enumerate(buttons):
        print(f"  [{i}] text='{btn.text_content()}' class={btn.get_attribute('class')}")
    
    page.screenshot(path="tests/screenshots/login_inspect.png")
    print("\n  Screenshot saved.")
    browser.close()