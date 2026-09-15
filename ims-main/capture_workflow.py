import pathlib
from playwright.sync_api import sync_playwright

HTML = pathlib.Path(r"c:\Users\25075\Desktop\IMS生产物料与产品追溯管理系统\ims-main\render_workflow.html").as_uri()
OUTPUT = r"c:\Users\25075\Desktop\IMS生产线物料与产品追溯管理系统\ims-main\IMS系统业务流程关系图.png"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()

    page.goto(HTML, wait_until="networkidle", timeout=60000)
    page.wait_for_selector("svg", timeout=30000)
    page.wait_for_timeout(3000)

    page.screenshot(path=OUTPUT, full_page=True)
    print(f"OK: {OUTPUT}")
    browser.close()