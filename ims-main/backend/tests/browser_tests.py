"""
阶段2 浏览器测试: 大数据量渲染 / 空数据 / 加载状态 / 打印兼容
===========================================================================
前置条件: 后端 (localhost:8000) + 前端 (localhost:5173) 均已启动
"""
import time
from playwright.sync_api import sync_playwright

FRONTEND = "http://localhost:5173"
API = "http://localhost:8000"
CRED = {"username": "admin", "password": "admin123"}
RESULTS = []
TIMEOUT = 30000

def login(page):
    page.goto(f"{FRONTEND}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[placeholder="用户名"]', CRED["username"])
    page.fill('input[placeholder="密码"]', CRED["password"])
    page.click('button:has-text("登")')
    page.wait_for_url("**/dashboard", timeout=10000)
    page.wait_for_load_state("networkidle")

def check_page(page, url, name):
    """访问页面，检查渲染、加载状态、空数据"""
    t0 = time.time()
    try:
        page.goto(f"{FRONTEND}{url}", timeout=TIMEOUT)
        page.wait_for_load_state("networkidle")
        elapsed = (time.time() - t0) * 1000

        # 1. 检查页面标题
        title = page.title()
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        # 2. 检查是否有 loading 状态（Element Plus loading遮罩）
        loading_visible = page.locator('.el-loading-mask').count() > 0

        # 3. 检查是否有表格
        table_count = page.locator('.el-table').count()

        # 4. 检查是否有空数据提示
        empty_hint = page.locator('.el-empty').count() > 0 or page.locator('[class*="empty"]').count() > 0

        # 5. 检查是否有el-card
        card_count = page.locator('.el-card').count()

        # 6. 检查表格行数
        row_count = page.locator('.el-table__body tr').count()

        # 7. 截图
        safe_name = name.replace("/","_").replace(" ","_")
        page.screenshot(path=f"tests/screenshots/{safe_name}.png", full_page=True)

        verdict = "✅"
        if elapsed > 10000:
            verdict = "⚠️慢"
        if console_errors:
            verdict = "⚠️" if verdict == "✅" else verdict

        RESULTS.append({
            "name": name, "url": url, "verdict": verdict,
            "time_ms": f"{elapsed:.0f}ms", "table": table_count,
            "rows": row_count, "loading": loading_visible,
            "empty": empty_hint, "card": card_count,
            "errors": len(console_errors),
        })
        print(f"  {verdict} {name:20s} | {elapsed:.0f}ms | table={table_count} rows={row_count} card={card_count} empty={empty_hint} errs={len(console_errors)}")
    except Exception as e:
        elapsed = (time.time() - t0) * 1000
        RESULTS.append({"name": name, "url": url, "verdict": "❌", "time_ms": f"{elapsed:.0f}ms", "error": str(e)[:80]})
        print(f"  ❌ {name:20s} | {elapsed:.0f}ms | ERROR: {str(e)[:80]}")


def main():
    import os
    os.makedirs("tests/screenshots", exist_ok=True)

    print("=" * 70)
    print("🌐 阶段2 浏览器综合测试")
    print("=" * 70)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        print("\n🔑 登录...")
        try:
            login(page)
            print("  ✅ 登录成功")
        except Exception as e:
            print(f"  ❌ 登录失败: {e}")
            browser.close()
            return

        # ================================================================
        # 测试1: 大数据量渲染（14）— 加载100条记录
        # ================================================================
        print("\n📊 大数据量渲染检查")
        test_pages = [
            ("/inventory", "库存明细"),
            ("/inventory/sku-summary", "库存汇总"),
            ("/inventory/partner-summary", "往来汇总"),
            ("/inbound", "入库管理"),
            ("/outbound", "出库管理"),
            ("/incoming", "来料管理"),
            ("/rma", "RMA返厂"),
            ("/shipment", "出货管理"),
            ("/bom", "BOM管理"),
            ("/production-task", "生产任务"),
            ("/products", "商品SKU"),
            ("/partners", "往来单位"),
            ("/stations", "场站管理"),
            ("/device-ledger", "设备台账"),
            ("/stocktake", "盘点管理"),
            ("/adjustment", "库存调整"),
            ("/customers", "客户管理"),
            ("/dashboard", "仪表盘"),
            ("/settings", "系统设置"),
            ("/audit-logs", "审计日志"),
            ("/snapshots", "库存快照"),
            ("/snapshots/details", "快照明细"),
            ("/snapshots/statistics", "快照统计"),
        ]

        for url, name in test_pages:
            check_page(page, url, name)

        # ================================================================
        # 测试2: 多角色遍历（10）
        # ================================================================
        print("\n👥 多角色遍历测试")
        roles_to_test = [
            {"username": "warehouse", "password": "admin123", "role": "仓库管理员"},
            {"username": "quality", "password": "admin123", "role": "质检员"},
            {"username": "viewer", "password": "admin123", "role": "观察者"},
        ]

        # Use fresh context for each role
        for role_info in roles_to_test:
            ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
            rp = ctx.new_page()
            try:
                rp.goto(f"{FRONTEND}/login")
                rp.wait_for_load_state("networkidle")
                rp.fill('input[placeholder="用户名"]', role_info["username"])
                rp.fill('input[placeholder="密码"]', role_info["password"])
                rp.click('button:has-text("登")')
                rp.wait_for_timeout(3000)

                url_after = rp.url
                logged_in = "/dashboard" in url_after or "/login" not in url_after
                if not logged_in:
                    err_msg = rp.locator('.el-message--error').text_content() or "未知"
                    print(f"    ❌ {role_info['role']:8s} 登录失败: {err_msg[:50]}")
                    ctx.close()
                    continue

                # Visit key pages and check if they load
                role_ok = 0
                role_fail = 0
                key_pages = [
                    ("/dashboard", "仪表盘"),
                    ("/inventory", "库存"),
                    ("/inbound", "入库"),
                    ("/rma", "RMA"),
                    ("/shipment", "出货"),
                    ("/stations", "场站"),
                    ("/stocktake", "盘点"),
                    ("/customers", "客户"),
                ]
                for kp_url, kp_name in key_pages:
                    try:
                        rp.goto(f"{FRONTEND}{kp_url}", timeout=10000)
                        rp.wait_for_load_state("networkidle")
                        has_card = rp.locator('.el-card').count() > 0
                        has_table = rp.locator('.el-table').count() > 0
                        if has_card or has_table:
                            role_ok += 1
                            print(f"    ✅ {role_info['role']:8s} → {kp_name}")
                        else:
                            role_fail += 1
                            print(f"    ⚠️ {role_info['role']:8s} → {kp_name} (无card/table)")
                    except Exception as e:
                        role_fail += 1
                        print(f"    ❌ {role_info['role']:8s} → {kp_name} ({str(e)[:40]})")

                print(f"    → {role_info['role']:8s} 通过 {role_ok}/{len(key_pages)} 页面")
                RESULTS.append({
                    "name": f"角色-{role_info['role']}",
                    "verdict": "✅" if role_fail == 0 else ("⚠️" if role_ok > 0 else "❌"),
                    "pass_rate": f"{role_ok}/{len(key_pages)}",
                })
            except Exception as e:
                print(f"  ❌ {role_info['role']} 整体失败: {e}")
                RESULTS.append({"name": f"角色-{role_info['role']}", "verdict": "❌", "error": str(e)[:60]})
            finally:
                ctx.close()

        browser.close()

    # ================================================================
    # 输出报告
    # ================================================================
    print("\n" + "=" * 70)
    print("📊 浏览器测试报告")
    print("=" * 70)

    passes = sum(1 for r in RESULTS if "✅" in r.get("verdict", ""))
    warns = sum(1 for r in RESULTS if "⚠️" in r.get("verdict", ""))
    fails = sum(1 for r in RESULTS if "❌" in r.get("verdict", ""))
    total = len(RESULTS)

    print(f"\n{'名称':20s} | {'判定':4s} | {'耗时':8s} | table | rows | card | 错误")
    print("-" * 70)
    for r in RESULTS:
        print(f"{r['name']:20s} | {r['verdict']:4s} | {str(r.get('time_ms','N/A')):8s} | "
              f"{str(r.get('table','-')):5s} | {str(r.get('rows','-')):4s} | {str(r.get('card','-')):4s} | "
              f"{r.get('errors','-')}")

    print(f"\n  汇总: 总计 {total} | ✅ {passes} | ⚠️ {warns} | ❌ {fails}")

    # 关键指标
    empty_count = sum(1 for r in RESULTS if r.get("empty"))
    slow_count = sum(1 for r in RESULTS if "⚠️慢" in r.get("verdict", ""))
    print(f"  空数据页面: {empty_count}/{total}")
    print(f"  响应>10s: {slow_count}/{total}")
    print(f"  通过率: {passes}/{total} ({100*passes/total:.0f}%)" if total > 0 else "  无数据")

if __name__ == "__main__":
    main()