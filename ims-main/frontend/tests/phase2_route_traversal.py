"""
阶段2 - 步骤⑥：前端路由遍历检查（使用系统Chrome）
- 23页面500检查
- 多角色遍历（admin + 4角色）
- 空数据渲染
- 加载状态
"""
from playwright.sync_api import sync_playwright
import json

BASE = "http://localhost:5174"

ADMIN_CRED = {"username": "admin", "password": "admin123"}

ALL_ROUTES = [
    "/dashboard",
    "/inventory",
    "/inventory/sku",
    "/inventory/partner",
    "/inbound",
    "/incoming",
    "/rma",
    "/shipment",
    "/bom",
    "/production-task",
    "/outbound",
    "/snapshot",
    "/snapshot/statistics",
    "/snapshot/details",
    "/products",
    "/partners",
    "/station",
    "/device-ledger",
    "/stocktake",
    "/adjustment",
    "/customers",
    "/workflow",
    "/settings",
    "/about",
]

ROLE_USERS = {
    "WAREHOUSE": {"username": "warehouse", "password": "123456"},
    "QUALITY": {"username": "quality", "password": "123456"},
    "PRODUCTION": {"username": "production", "password": "123456"},
    "TEST_ENGINEER": {"username": "test_eng", "password": "123456"},
}


def login(context, username, password):
    page = context.new_page()
    try:
        page.goto(f"{BASE}/login", timeout=10000)
        page.wait_for_load_state("networkidle", timeout=5000)
        page.wait_for_timeout(500)

        current = page.url
        if "/dashboard" in current:
            print(f"    已登录状态，跳过表单")
            page.close()
            return True

        page.fill('input[placeholder="用户名"]', username)
        page.fill('input[placeholder="密码"]', password)
        page.wait_for_timeout(300)
        page.click('.el-button--primary')
        page.wait_for_timeout(2000)

        current = page.url
        if "/dashboard" in current:
            page.wait_for_load_state("networkidle")
            page.close()
            return True

        err_el = page.locator('.el-message--error')
        if err_el.count() > 0:
            err_text = err_el.first.inner_text()
            print(f"    登录错误: {err_text}")
        else:
            page.screenshot(path=f"tests/login_debug_{username}.png")
            print(f"    未跳转，当前URL: {current}，截图已保存")

        page.close()
        return False
    except Exception as e:
        print(f"    登录异常: {str(e)[:100]}")
        try:
            page.screenshot(path=f"tests/login_error_{username}.png")
            page.close()
        except:
            pass
        return False


def check_page(page, route, role="ADMIN"):
    url = f"{BASE}{route}"
    result = {"route": route, "role": role, "url": url, "status": "OK", "issues": []}

    try:
        resp = page.goto(url, timeout=15000)
        page.wait_for_load_state("networkidle", timeout=10000)

        if resp and resp.status >= 500:
            result["status"] = "500_ERROR"
            result["issues"].append(f"HTTP {resp.status}")
            return result
        if resp and resp.status >= 400:
            result["issues"].append(f"HTTP {resp.status}")

        page.wait_for_timeout(1200)

        body_text = page.inner_text("body")[:500]
        if "500" in body_text and "Internal Server Error" in body_text:
            result["status"] = "500_ERROR"
            result["issues"].append("页面显示500错误")
            return result

        current_url = page.url
        if "/dashboard" in current_url and route != "/dashboard":
            result["status"] = "REDIRECTED"
            result["issues"].append("无权限，重定向到 /dashboard")
            return result

        has_empty = page.locator('.el-empty').count() > 0
        has_no_data = page.locator('text=暂无数据').count() > 0
        has_loading = page.locator('.el-loading-mask').count() > 0
        has_skeleton = page.locator('.el-skeleton').count() > 0

        if has_empty or has_no_data:
            result["empty_data"] = True
        if has_loading or has_skeleton:
            result["loading"] = True

        has_table = page.locator('.el-table').count() > 0
        has_form = page.locator('.el-form').count() > 0
        has_card = page.locator('.el-card').count() > 0
        has_content = has_table or has_form or has_card
        if not has_content:
            result["issues"].append("无主要内容元素")

        if result["issues"]:
            result["status"] = "WARN"

    except Exception as e:
        result["status"] = "ERROR"
        result["issues"].append(str(e)[:200])

    return result


def test_role(browser, role_name, creds, results):
    print(f"\n{'='*50}")
    print(f"[{role_name}] 角色遍历...")
    context = browser.new_context()
    if not login(context, **creds):
        print(f"  ⚠️ 登录失败，跳过")
        context.close()
        return

    page = context.new_page()
    for route in ALL_ROUTES:
        r = check_page(page, route, role_name)
        icon = {"OK": "✅", "WARN": "⚠️", "ERROR": "❌", "500_ERROR": "💀", "REDIRECTED": "🔒"}.get(r["status"], "❓")
        extra = ""
        if r.get("empty_data"):
            extra += " [空]"
        if r.get("loading"):
            extra += " [加载]"
        print(f"  {icon} {route} ({r['status']}){extra}")
        results.append(r)

    page.close()
    context.close()


def main():
    print("=" * 70)
    print("阶段2-步骤⑥：前端路由遍历检查 (Chrome)")
    print(f"前端: {BASE}")
    print("=" * 70)

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)

        test_role(browser, "ADMIN", ADMIN_CRED, results)

        for role_name, creds in ROLE_USERS.items():
            test_role(browser, role_name, creds, results)

        browser.close()

    print("\n" + "=" * 70)
    print("路由遍历汇总报告")
    print("=" * 70)

    ok_count = sum(1 for r in results if r["status"] == "OK")
    warn_count = sum(1 for r in results if r["status"] == "WARN")
    error_count = sum(1 for r in results if r["status"] == "ERROR")
    http500_count = sum(1 for r in results if r["status"] == "500_ERROR")
    redirect_count = sum(1 for r in results if r["status"] == "REDIRECTED")
    empty_count = sum(1 for r in results if r.get("empty_data"))

    total = len(results)
    print(f"总计: {total} 次页面访问")
    print(f"  ✅ OK: {ok_count}")
    print(f"  ⚠️ WARN: {warn_count}")
    print(f"  ❌ ERROR: {error_count}")
    print(f"  💀 500错误: {http500_count}")
    print(f"  🔒 无权限重定向: {redirect_count}")
    print(f"  📭 空数据页: {empty_count}")

    if error_count > 0 or http500_count > 0:
        print("\n❌ 问题页面:")
        for r in results:
            if r["status"] in ("ERROR", "500_ERROR"):
                print(f"  - {r['route']} [{r['role']}]: {r['issues']}")

    warn_pages = [r for r in results if r["status"] == "WARN"]
    if warn_pages:
        print(f"\n⚠️ 警告页面 ({len(warn_pages)}):")
        for r in warn_pages:
            print(f"  - {r['route']} [{r['role']}]: {r['issues']}")

    print(f"\n结论: {'✅ 全部通过（无500/ERROR）' if error_count == 0 and http500_count == 0 else '❌ 存在问题需修复'}")


if __name__ == "__main__":
    main()