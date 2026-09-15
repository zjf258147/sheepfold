from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import re

BASE = "https://localhost:5176"

ALL_STATIC_PAGES = [
    {"path": "/dashboard", "name": "Dashboard (首页)"},
    {"path": "/inventory", "name": "实时库存"},
    {"path": "/inventory/sku", "name": "按SKU统计库存"},
    {"path": "/inventory/partner", "name": "按关联单位出库统计"},
    {"path": "/inbound", "name": "入库列表"},
    {"path": "/incoming", "name": "来料管理"},
    {"path": "/rma", "name": "返厂维修"},
    {"path": "/shipment", "name": "出货管理"},
    {"path": "/bom", "name": "BOM管理"},
    {"path": "/production-task", "name": "生产任务"},
    {"path": "/outbound", "name": "出库列表"},
    {"path": "/snapshot", "name": "库存流水"},
    {"path": "/snapshot/statistics", "name": "库存快照汇总"},
    {"path": "/snapshot/details", "name": "快照明细"},
    {"path": "/products", "name": "商品SKU"},
    {"path": "/partners", "name": "往来单位"},
    {"path": "/station", "name": "场站管理"},
    {"path": "/device-ledger", "name": "设备台账"},
    {"path": "/stocktake", "name": "盘点管理"},
    {"path": "/adjustment", "name": "库存调整"},
    {"path": "/customers", "name": "客户管理"},
    {"path": "/workflow", "name": "业务流程"},
    {"path": "/settings", "name": "系统设置"},
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(ignore_https_errors=True)
    page = ctx.new_page()

    current_page = ""
    page_errors = []
    results = {}

    def capture_response(response):
        if response.status >= 400:
            page_errors.append({
                "page": current_page,
                "url": response.url,
                "status": response.status,
            })

    def capture_console(msg):
        if msg.type == "error":
            page_errors.append({
                "page": current_page,
                "url": "console",
                "status": 0,
                "console_error": msg.text,
            })

    page.on("response", capture_response)
    page.on("console", capture_console)

    print("=" * 70)
    print("登录中...")
    page.goto(f"{BASE}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[placeholder="用户名"]', "admin")
    page.fill('input[placeholder="密码"]', "admin123")
    page.click('button:has-text("登 录")')
    page.wait_for_url("**/dashboard**", timeout=10000)
    print("[OK] 登录成功\n")

    all_test_pages = list(ALL_STATIC_PAGES)

    for p_info in all_test_pages:
        current_page = p_info["name"]
        path = p_info["path"]
        page_errors.clear()

        print(f"测试: {current_page} ({path})", end=" ... ")

        page.goto(f"{BASE}{path}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2500)

        status_500 = [e for e in page_errors if e["status"] == 500]
        status_4xx = [e for e in page_errors if 400 <= e["status"] < 500 and e["status"] != 500]
        console_errs = [e for e in page_errors if e["status"] == 0]

        if status_500:
            urls = list(set(e["url"] for e in status_500))
            print(f"❌ 500错误! ({len(status_500)} 个请求)")
            for u in urls:
                print(f"      500: {u}")
        elif status_4xx:
            codes = list(set(f"{e['status']}" for e in status_4xx))
            print(f"⚠️ {','.join(codes)} 错误 ({len(status_4xx)} 个)")
            for e in status_4xx[:3]:
                print(f"      {e['status']}: {e['url']}")
        elif console_errs:
            print(f"⚠️ 控制台错误 ({len(console_errs)} 个)")
        else:
            print("✅")

        results[current_page] = {
            "path": path,
            "status_500": status_500,
            "status_4xx": status_4xx,
            "console_errors": console_errs,
        }

    print("\n" + "=" * 70)
    print("尝试获取动态详情页ID...")
    print("=" * 70)

    for list_path, detail_name, detail_path_prefix in [
        ("/inbound", "入库详情", "/inbound/"),
        ("/outbound", "出库详情", "/outbound/"),
    ]:
        current_page = detail_name
        page_errors.clear()
        detail_id = None

        print(f"\n先访问列表页 {list_path} 获取ID...")
        page.goto(f"{BASE}{list_path}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2500)

        try:
            first_link = page.locator("a[href*='" + detail_path_prefix + "']").first
            href = first_link.get_attribute("href")
            if href:
                detail_id = href.replace(detail_path_prefix, "")
                print(f"  找到ID: {detail_id}")

                current_page = detail_name
                page_errors.clear()
                print(f"测试: {detail_name} ({detail_path_prefix}{detail_id})", end=" ... ")

                page.goto(f"{BASE}{detail_path_prefix}{detail_id}")
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2500)

                status_500 = [e for e in page_errors if e["status"] == 500]
                status_4xx = [e for e in page_errors if 400 <= e["status"] < 500 and e["status"] != 500]

                if status_500:
                    urls = list(set(e["url"] for e in status_500))
                    print(f"❌ 500错误! ({len(status_500)} 个请求)")
                    for u in urls:
                        print(f"      500: {u}")
                elif status_4xx:
                    print(f"⚠️ {len(status_4xx)} 个4xx错误")
                else:
                    print("✅")

                results[detail_name] = {
                    "path": f"{detail_path_prefix}{detail_id}",
                    "status_500": status_500,
                    "status_4xx": status_4xx,
                    "console_errors": [],
                }
            else:
                print("  ⚠️ 未找到详情链接")
        except Exception as e:
            print(f"  ⚠️ 无法获取详情ID: {e}")

    print("\n" + "=" * 70)
    print("汇总报告")
    print("=" * 70)

    broken_pages = []
    warning_pages = []

    for name, data in results.items():
        if data["status_500"]:
            broken_pages.append((name, data))
        elif data["status_4xx"]:
            warning_pages.append((name, data))

    if broken_pages:
        print(f"\n{'='*50}")
        print(f"❌ 500错误页面 ({len(broken_pages)} 个):")
        print(f"{'='*50}")
        for name, data in broken_pages:
            print(f"\n  📄 {name} ({data['path']})")
            url_set = {}
            for e in data["status_500"]:
                u = e["url"]
                if u not in url_set:
                    url_set[u] = 0
                url_set[u] += 1
            for u, count in url_set.items():
                print(f"      500 x{count}: {u}")
    else:
        print("\n✅ 无500错误页面！")

    if warning_pages:
        print(f"\n{'='*50}")
        print(f"⚠️ 非500错误页面 ({len(warning_pages)} 个):")
        print(f"{'='*50}")
        for name, data in warning_pages:
            print(f"\n  📄 {name} ({data['path']})")
            for e in data["status_4xx"][:5]:
                print(f"      {e['status']}: {e['url']}")

    print("\n" + "=" * 70)
    print(f"总计: {len(results)} 页面 | ❌500: {len(broken_pages)} | ⚠️其他: {len(warning_pages)} | ✅正常: {len(results) - len(broken_pages) - len(warning_pages)}")
    print("=" * 70)

    browser.close()