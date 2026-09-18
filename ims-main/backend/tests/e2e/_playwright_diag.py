"""Quick Playwright connectivity diagnostic."""
from playwright.sync_api import sync_playwright

base = "http://localhost:5173"
p = sync_playwright().start()
try:
    b = p.chromium.launch(headless=True, args=['--no-sandbox','--disable-setuid-sandbox','--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True)
    page = ctx.new_page()

    msgs = []
    page.on("console", lambda m: msgs.append(f"[{m.type}] {m.text}"))

    failed = []
    page.on("requestfailed", lambda r: failed.append(f"FAIL: {r.url} - {r.failure}"))

    resp = page.goto(f"{base}/login", timeout=15000)
    print(f"Goto → HTTP {resp.status}")
    page.fill('input[placeholder="用户名"]', "admin", timeout=5000)
    page.fill('input[placeholder="密码"]', "admin123", timeout=5000)
    page.click('button:has-text("登 录")', timeout=5000)
    page.wait_for_timeout(8000)
    print(f"URL after: {page.url}")
    for m in msgs[-15:]:
        print(f"  {m[:200]}")
    for f in failed[-8:]:
        print(f"  {f[:200]}")

    # Also check page content
    body = page.locator("body").inner_text(timeout=3000)[:500]
    print(f"\nPAGE BODY (first 500 chars):\n{body}")

    b.close()
finally:
    p.stop()