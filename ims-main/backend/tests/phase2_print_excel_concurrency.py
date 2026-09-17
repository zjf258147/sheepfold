"""
阶段2 在线检查: 打印分页、Excel导出、并发测试、404路由
============================================================
运行前提: 后端+前端均已启动
"""

import os, sys, json, time, asyncio
from datetime import datetime
from io import BytesIO

# Playwright 浏览器测试
from playwright.sync_api import sync_playwright

# HTTP 异步并发
import httpx

BASE_URL = "http://localhost:5173"
API_URL = "http://localhost:8000"

TEST_USER = {"username": "admin", "password": "admin123"}

# ============================================================
# 工具函数
# ============================================================
def login(page):
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[placeholder="用户名"]', TEST_USER["username"])
    page.fill('input[placeholder="密码"]', TEST_USER["password"])
    page.click('button:has-text("登")')
    try:
        page.wait_for_url(f"{BASE_URL}/dashboard", timeout=5000)
        print("  ✅ 登录成功")
        return True
    except:
        print("  ❌ 登录失败")
        return False


def check_page_loaded(page, url, name):
    """检查页面是否正常加载，返回 (ok, content_len)"""
    try:
        page.goto(url, timeout=15000)
        page.wait_for_load_state("networkidle", timeout=10000)
        page.wait_for_timeout(1000)
        content = page.content()
        return True, len(content)
    except Exception as e:
        return False, str(e)[:80]


def login_httpx() -> str:
    """通过API登录获取token"""
    with httpx.Client(timeout=30) as c:
        try:
            r = c.post(f"{API_URL}/api/v1/auth/login", json=TEST_USER)
            if r.status_code == 200:
                data = r.json()
                token = data.get("data", {}).get("access_token", "")
                print(f"  ✅ API登录成功, token...{token[-10:] if token else 'N/A'}")
                return token
            else:
                print(f"  ❌ API登录失败: {r.status_code} {r.text[:100]}")
                return ""
        except Exception as e:
            print(f"  ❌ API连接失败: {str(e)[:80]}")
            return ""


# ============================================================
# 第一部分: 打印功能测试
# ============================================================
def test_print_pages(page):
    print("\n" + "=" * 60)
    print("📄 测试打印功能 (6种单据)")
    print("=" * 60)

    # 各打印API和对应数据ID范围
    print_apis = [
        ("到货单", "/api/v1/print/incoming_receipt/"),
        ("出货单", "/api/v1/print/shipment/"),
        ("来料检验单", "/api/v1/print/incoming_inspection/"),
        ("来料退货单", "/api/v1/print/incoming_return/"),
        ("返厂维修单", "/api/v1/print/rma_repair/"),
        ("BOM单", "/api/v1/print/bom/"),
    ]

    results = []
    token = login_httpx()

    for name, api_path in print_apis:
        # 先获取该类型的列表，取第一个ID
        try:
            # 用fetch API通过浏览器调用
            print(f"\n  📋 {name}...")
            # 直接用httpx查后端API
            list_ep = api_path.replace("/print/", "/").rstrip("/")  # 尝试对应列表端点
            # 直接用Playwright调API
            payload = page.evaluate(f"""async () => {{
                try {{
                    const r = await fetch('{API_URL}{list_ep}?page=1&page_size=1', {{
                        headers: {{ 'Authorization': 'Bearer {token}' }}
                    }});
                    const data = await r.json();
                    return {{ ok: true, count: data.total || 0, id: (data.items && data.items[0]) ? data.items[0].id : null }};
                }} catch(e) {{
                    return {{ ok: false, error: e.message }};
                }}
            }}""")
        except Exception as e:
            print(f"    ⚠️ 获取列表失败: {str(e)[:80]}")
            results.append((name, "⚠️ 列表获取失败", str(e)[:60]))
            continue

        if not payload.get("ok") or not payload.get("id"):
            print(f"    ⚠️ 无数据，跳过 ({payload})")
            results.append((name, "⚠️ 无数据", str(payload)[:60]))
            continue

        test_id = payload["id"]
        print(f"    数据ID={test_id}")

        # 请求打印数据
        try:
            print_url = f"{API_URL}{api_path}{test_id}"
            print_data = page.evaluate(f"""async () => {{
                try {{
                    const r = await fetch('{print_url}', {{
                        headers: {{ 'Authorization': 'Bearer {token}' }}
                    }});
                    if (!r.ok) return {{ ok: false, status: r.status, error: r.statusText }};
                    const data = await r.json();
                    return {{ ok: true, hasData: !!data, keys: Object.keys(data || {{}}).length }};
                }} catch(e) {{
                    return {{ ok: false, error: e.message }};
                }}
            }}""")

            if print_data.get("ok"):
                print(f"    ✅ API返回正常, 字段数={print_data.get('keys', '?')}")
                results.append((name, "✅", f"字段数={print_data.get('keys', '?')}"))
            else:
                print(f"    ❌ API返回异常: {print_data}")
                results.append((name, "❌", str(print_data)[:60]))
        except Exception as e:
            print(f"    ❌ 请求打印API失败: {str(e)[:80]}")
            results.append((name, "❌", str(e)[:60]))

    return results


# ============================================================
# 第二部分: Excel 导出测试
# ============================================================
def test_excel_exports(page):
    print("\n" + "=" * 60)
    print("📊 测试Excel导出功能 (10个端点)")
    print("=" * 60)

    token = login_httpx()

    export_endpoints = [
        ("库存流水日报导出", "/api/v1/snapshots/daily-ledger/export", "GET"),
        ("库存流水汇总导出", "/api/v1/snapshots/ledger-summary/export", "GET"),
        ("库存单品导出", "/api/v1/snapshots/items/export", "GET"),
        ("RMA导出", "/api/v1/rma/export", "GET"),
        ("出库单导出", "/api/v1/outbound/orders/export", "GET"),
        ("库存明细导出", "/api/v1/inventory/items/export", "GET"),
        ("来料到货导出", "/api/v1/incoming/receipts/export", "GET"),
        ("入库单导出", "/api/v1/inbound/orders/export", "GET"),
        ("BOM导出", "/api/v1/bom/export", "GET"),
        ("生产任务导出", "/api/v1/production-tasks/export", "GET"),
    ]

    results = []

    for name, endpoint, method in export_endpoints:
        print(f"\n  📊 {name} ({endpoint})...")
        url = f"{API_URL}{endpoint}"

        try:
            payload = page.evaluate(f"""async () => {{
                try {{
                    const r = await fetch('{url}?start_date=2024-01-01&end_date=2026-12-31', {{
                        headers: {{ 'Authorization': 'Bearer {token}' }}
                    }});
                    const ct = r.headers.get('content-type') || '';
                    const cd = r.headers.get('content-disposition') || '';
                    const len = r.headers.get('content-length') || '0';
                    return {{
                        ok: r.ok,
                        status: r.status,
                        contentType: ct,
                        contentDisposition: cd,
                        contentLength: parseInt(len) || 0
                    }};
                }} catch(e) {{
                    return {{ ok: false, error: e.message, status: 0 }};
                }}
            }}""")

            if payload.get("ok", False):
                ct = payload.get("contentType", "")
                cl = payload.get("contentLength", 0)
                cd = payload.get("contentDisposition", "")
                # 检查是否是Excel格式
                is_excel = "spreadsheet" in ct.lower() or "excel" in ct.lower() or "xlsx" in cd.lower() or "xls" in cd.lower()
                if cl > 0:
                    kb = cl / 1024
                    print(f"    ✅ 导出成功, {kb:.1f}KB, Content-Type: {ct[:50]}, isExcel: {is_excel} 文件名: {cd[:60]}")
                    results.append((name, "✅", f"{kb:.1f}KB {'Excel' if is_excel else '下载'}"))
                else:
                    print(f"    ⚠️ 文件为空或0字节, status={payload.get('status')}")
                    results.append((name, "⚠️", f"0字节, status={payload.get('status')}"))
            elif payload.get("status", 0) == 404:
                print(f"    ⚠️ 404 端点不存在")
                results.append((name, "⚠️", "404 端点不存在"))
            elif payload.get("status", 0) == 500:
                print(f"    ❌ 500 服务器错误")
                results.append((name, "❌", "500 服务器错误"))
            else:
                print(f"    ⚠️ 其他错误: {payload}")
                results.append((name, "⚠️", str(payload.get('error', payload))[:60]))
        except Exception as e:
            print(f"    ❌ 异常: {str(e)[:80]}")
            results.append((name, "❌", str(e)[:60]))

    return results


# ============================================================
# 第三部分: 并发测试 (50并发)
# ============================================================
async def test_concurrency():
    print("\n" + "=" * 60)
    print("⚡ 并发测试 (50用户同时请求)")
    print("=" * 60)

    token = login_httpx()
    if not token:
        return [("并发测试", "❌", "登录失败")]

    endpoints = [
        ("GET", "/api/v1/dashboard/stats"),
        ("GET", "/api/v1/inventory/items?page=1&page_size=5"),
        ("GET", "/api/v1/products?page=1&page_size=5"),
        ("GET", "/api/v1/partners?page=1&page_size=5"),
    ]

    results = []

    async def make_request(client, ep):
        method, path = ep
        headers = {"Authorization": f"Bearer {token}"}
        t0 = time.time()
        try:
            if method == "GET":
                r = await client.get(f"{API_URL}{path}", headers=headers, timeout=30)
            t1 = time.time()
            return {"ok": r.status_code == 200, "status": r.status_code, "time": t1 - t0}
        except Exception as e:
            t1 = time.time()
            return {"ok": False, "error": str(e)[:60], "time": t1 - t0}

    async with httpx.AsyncClient() as client:
        for name, method, path in [
            ("仪表盘统计", "GET", "/api/v1/dashboard/stats"),
            ("库存列表", "GET", "/api/v1/inventory/items?page=1&page_size=5"),
            ("商品SKU", "GET", "/api/v1/products?page=1&page_size=5"),
            ("往来单位", "GET", "/api/v1/partners?page=1&page_size=5"),
        ]:
            print(f"\n  ⚡ {name} ({path})...")
            # 50个并发请求
            CONCURRENT = 50
            tasks = [make_request(client, (method, path)) for _ in range(CONCURRENT)]
            t_start = time.time()
            res = await asyncio.gather(*tasks)
            t_total = time.time() - t_start

            ok_count = sum(1 for r in res if r.get("ok"))
            fail_count = CONCURRENT - ok_count
            avg_time = sum(r["time"] for r in res) / CONCURRENT if res else 0
            errors = [r.get("error") for r in res if not r.get("ok")]

            status_line = "✅" if fail_count == 0 else ("⚠️" if fail_count <= 2 else "❌")
            print(f"    {status_line} {ok_count}/{CONCURRENT} 成功, "
                  f"平均 {avg_time*1000:.0f}ms, 总耗时 {t_total:.1f}s"
                  + (f", 错误: {errors[:3]}" if errors else ""))

            results.append((f"并发-{name}", status_line,
                            f"{ok_count}/{CONCURRENT}成功, {avg_time*1000:.0f}ms/req, {t_total:.1f}s总"))

    return results


# ============================================================
# 第四部分: 404 路由测试
# ============================================================
def test_404_routes(page):
    print("\n" + "=" * 60)
    print("🛡️ 404路由 + 超时测试")
    print("=" * 60)

    non_existent_routes = [
        "/nonexistent-page-xyz",
        "/api/nonexistent",
        "/123456/invalid",
        "/.env",
        "/wp-admin",
    ]

    results = []
    for route in non_existent_routes:
        url = f"{BASE_URL}{route}"
        print(f"\n  🔗 {url}...")
        ok, detail = check_page_loaded(page, url, route)
        if ok:
            # 前端应该正确处理不存在的路由（SPA路由）
            print(f"    ✅ 前端正常处理 ({detail}字符)")
            results.append((f"404-{route}", "✅", f"{detail}字符"))
        else:
            print(f"    ⚠️ {detail}")
            results.append((f"404-{route}", "⚠️", detail))

    # 后端API 404
    api_404s = [
        "/api/v1/nonexistent_endpoint",
        "/api/v1/auth/nonexistent",
    ]
    token = login_httpx()
    for ep in api_404s:
        url = f"{API_URL}{ep}"
        print(f"\n  🔗 API {url}...")
        try:
            with httpx.Client(timeout=10) as c:
                r = c.get(url, headers={"Authorization": f"Bearer {token}"})
                if r.status_code == 404:
                    print(f"    ✅ 正确返回404")
                    results.append((f"API404-{ep}", "✅", "404"))
                elif r.status_code == 200:
                    print(f"    ⚠️ 返回200但不应该")
                    results.append((f"API404-{ep}", "⚠️", "200"))
                else:
                    print(f"    ⚠️ 返回{r.status_code}")
                    results.append((f"API404-{ep}", "⚠️", str(r.status_code)))
        except Exception as e:
            print(f"    ❌ {str(e)[:60]}")
            results.append((f"API404-{ep}", "❌", str(e)[:60]))

    # 超时测试 (后端慢端点不应挂死)
    print(f"\n  ⏱️ 请求超时测试...")
    try:
        with httpx.Client(timeout=5) as c:
            r = c.get(f"{API_URL}/api/v1/inventory/items?page=1&page_size=10000",
                      headers={"Authorization": f"Bearer {token}"})
            t = r.elapsed.total_seconds()
            print(f"    大页面请求耗时: {t:.2f}s, status={r.status_code}")
            results.append(("超时-大数据量", "✅" if t < 5 else "⚠️", f"{t:.2f}s"))
    except httpx.TimeoutException:
        print(f"    ❌ 超时!")
        results.append(("超时-大数据量", "❌", "超时"))
    except Exception as e:
        print(f"    ⚠️ {str(e)[:60]}")
        results.append(("超时-大数据量", "⚠️", str(e)[:60]))

    return results


# ============================================================
# 主测试流程
# ============================================================
def main():
    print("=" * 60)
    print("🔍 阶段2 综合测试: 打印 + Excel导出 + 并发 + 404")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    all_results = {}

    # ===== 打印测试 =====
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        if not login(page):
            browser.close()
            return

        # 1. 打印测试
        print_results = test_print_pages(page)
        all_results["打印"] = print_results

        # 2. Excel 导出测试
        export_results = test_excel_exports(page)
        all_results["Excel导出"] = export_results

        # 3. 404 路由测试
        notfound_results = test_404_routes(page)
        all_results["404路由"] = notfound_results

        context.close()
        browser.close()

    # ===== 并发测试 (异步) =====
    conc_results = asyncio.run(test_concurrency())
    all_results["并发"] = conc_results

    # ===== 输出报告 =====
    print("\n" + "=" * 60)
    print("📊 阶段2 综合测试报告")
    print("=" * 60)

    total_ok = 0
    total_warn = 0
    total_fail = 0
    total = 0

    for category, results in all_results.items():
        print(f"\n--- {category} ---")
        for name, status, detail in results:
            icon = "✅" if "✅" in status else ("⚠️" if "⚠️" in status else "❌")
            print(f"  {icon} {name}: {detail}")
            if "✅" in status:
                total_ok += 1
            elif "⚠️" in status:
                total_warn += 1
            else:
                total_fail += 1
            total += 1

    print(f"\n{'='*60}")
    print(f"📊 汇总: 总计 {total} | ✅ {total_ok} | ⚠️ {total_warn} | ❌ {total_fail}")
    print(f"   通过率: {total_ok}/{total} ({total_ok*100//total}%)" if total else "N/A")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 保存结果
    result_file = os.path.join(os.path.dirname(__file__), "phase2_results.json")
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "results": {k: [list(r) for r in v] for k, v in all_results.items()}, "summary": {"total": total, "ok": total_ok, "warn": total_warn, "fail": total_fail}}, f, ensure_ascii=False, indent=2)
    print(f"\n详细结果已保存: {result_file}")


if __name__ == "__main__":
    main()