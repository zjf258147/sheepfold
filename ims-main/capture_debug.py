from playwright.sync_api import sync_playwright

OUTPUT = r"c:\Users\25075\Desktop\IMS生产线物料与产品追溯管理系统\ims-main\IMS系统业务流程关系图.png"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(ignore_https_errors=True)
    page = ctx.new_page(viewport={"width": 1920, "height": 1080})

    try:
        resp = page.goto("https://localhost:5173/", wait_until="networkidle", timeout=30000)
        print(f"Status: {resp.status}")
    except Exception as e:
        print(f"HTTPS failed: {e}")
        try:
            resp = page.goto("http://localhost:5173/", wait_until="networkidle", timeout=30000)
            print(f"HTTP Status: {resp.status}")
        except Exception as e2:
            print(f"HTTP also failed: {e2}")

    print(f"URL: {page.url}")
    print(f"Title: {page.title()}")

    page.wait_for_timeout(2000)
    page.screenshot(path=r"c:\Users\25075\Desktop\IMS生产线物料与产品追溯管理系统\ims-main\debug_root.png", full_page=True)
    print("Debug screenshot saved")

    browser.close()