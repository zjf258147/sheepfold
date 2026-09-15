from playwright.sync_api import sync_playwright

BASE = "https://localhost:5173"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(ignore_https_errors=True)
    page = ctx.new_page()

    page.goto(f"{BASE}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[placeholder="用户名"]', "admin")
    page.fill('input[placeholder="密码"]', "admin123")
    page.click('button:has-text("登 录")')
    page.wait_for_url("**/dashboard**", timeout=10000)
    print("[OK] Login succeeded, at dashboard")

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    title = page.locator(".page-title").text_content()
    print(f"[OK] Page title: {title}")

    pending_cards = page.locator(".audit-card")
    count = pending_cards.count()
    print(f"[OK] Pending audit cards: {count}")

    phase2_cards = page.locator(".phase2-card")
    count_p2 = phase2_cards.count()
    print(f"[OK] Phase 2 stat cards: {count_p2}")
    assert count_p2 == 6, f"Expected 6 phase2 cards, got {count_p2}"

    labels = ["活跃场站", "运行中设备", "故障设备", "进行中盘点", "库存调整", "质保将到期"]
    for i in range(count_p2):
        card_label = phase2_cards.nth(i).locator(".p2-label").text_content()
        print(f"  Card {i + 1}: {card_label}")
        assert card_label in labels, f"Unexpected card label: {card_label}"

    phase2_cards.nth(0).click()
    page.wait_for_timeout(1500)
    assert "station" in page.url.lower(), f"Expected station page, got {page.url}"
    print("[OK] Navigated to station page via card click")

    page.goto(f"{BASE}/dashboard")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)

    has_stock = page.locator('text=实时库存统计').is_visible()
    print(f"[OK] Stock summary visible: {has_stock}")

    has_partner = page.locator('text=出库商品统计').is_visible()
    print(f"[OK] Partner summary visible: {has_partner}")

    print("\n[PASS] All dashboard phase2 checks passed!")

    browser.close()