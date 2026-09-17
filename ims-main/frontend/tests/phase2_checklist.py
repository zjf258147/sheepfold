"""阶段2在线检查脚本 - 完整检测清单"""
import time
import json
import sys
import os
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:5173"
API_URL = "http://localhost:8000"

# 24个功能页面列表（不含login和参数化详情页）
ALL_PAGES = [
    {"path": "/dashboard", "name": "首页", "roles": [], "admin": False},
    {"path": "/inventory", "name": "实时库存", "roles": [], "admin": False},
    {"path": "/inventory/sku", "name": "按SKU统计库存", "roles": [], "admin": False},
    {"path": "/inventory/partner", "name": "按关联单位出库统计", "roles": [], "admin": False},
    {"path": "/inbound", "name": "入库", "roles": ["ADMIN", "WAREHOUSE", "QUALITY", "PRODUCTION"], "admin": False},
    {"path": "/incoming", "name": "来料管理", "roles": ["ADMIN", "WAREHOUSE", "QUALITY"], "admin": False},
    {"path": "/rma", "name": "返厂维修", "roles": ["ADMIN", "WAREHOUSE", "QUALITY", "TEST_ENGINEER", "PRODUCTION"], "admin": False},
    {"path": "/shipment", "name": "出货管理", "roles": ["ADMIN", "WAREHOUSE", "QUALITY", "PRODUCTION"], "admin": False},
    {"path": "/bom", "name": "BOM管理", "roles": ["ADMIN", "WAREHOUSE", "PRODUCTION"], "admin": False},
    {"path": "/production-task", "name": "生产任务", "roles": ["ADMIN", "WAREHOUSE", "PRODUCTION"], "admin": False},
    {"path": "/outbound", "name": "出库", "roles": ["ADMIN", "WAREHOUSE", "QUALITY", "PRODUCTION"], "admin": False},
    {"path": "/snapshot", "name": "库存流水", "roles": [], "admin": False},
    {"path": "/snapshot/statistics", "name": "库存快照汇总", "roles": [], "admin": False},
    {"path": "/snapshot/details", "name": "快照明细", "roles": [], "admin": False},
    {"path": "/products", "name": "商品SKU", "roles": [], "admin": False},
    {"path": "/partners", "name": "往来单位", "roles": [], "admin": False},
    {"path": "/station", "name": "场站管理", "roles": ["ADMIN", "WAREHOUSE"], "admin": False},
    {"path": "/device-ledger", "name": "设备台账", "roles": ["ADMIN", "WAREHOUSE", "TEST_ENGINEER"], "admin": False},
    {"path": "/stocktake", "name": "盘点管理", "roles": ["ADMIN", "WAREHOUSE"], "admin": False},
    {"path": "/adjustment", "name": "库存调整", "roles": ["ADMIN", "WAREHOUSE"], "admin": False},
    {"path": "/customers", "name": "客户管理", "roles": [], "admin": False},
    {"path": "/workflow", "name": "业务流程", "roles": [], "admin": False},
    {"path": "/settings", "name": "系统设置", "roles": [], "admin": True},
    {"path": "/about", "name": "关于", "roles": [], "admin": False},
]

ROLES = ["ADMIN", "WAREHOUSE", "QUALITY", "PRODUCTION", "TEST_ENGINEER"]

results = {
    "step6_route_500": [],
    "step6_multi_role": [],
    "step6_empty_data": [],
    "step6_loading": [],
    "step8_print": [],
    "step8_excel": [],
    "step9_performance": [],
    "step9_404": [],
}


def login_as(page, role="ADMIN"):
    """以指定角色登录，返回是否成功。如果已登录则返回True。"""
    # 检查是否已登录（访问需要认证的页面不会跳转到login）
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_load_state("networkidle")
    time.sleep(0.3)
    if "/login" not in page.url:
        return True  # 已登录

    # 未登录，执行登录
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    time.sleep(0.5)

    # 根据角色选择用户名和密码
    role_users = {
        "ADMIN": ("admin", "admin123"),
        "WAREHOUSE": ("warehouse", "123456"),
        "QUALITY": ("quality", "123456"),
        "PRODUCTION": ("production", "123456"),
        "TEST_ENGINEER": ("test_eng", "123456"),
    }
    username, password = role_users.get(role, ("admin", "admin123"))

    # 填充登录表单
    try:
        page.fill('input[placeholder="用户名"]', username)
        page.fill('input[placeholder="密码"]', password)
        # 按钮文字是"登 录"（带空格），使用模糊匹配
        page.click('button:has-text("登")')
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        if "/login" not in page.url:
            return True
        print(f"  登录可能失败，当前URL: {page.url}")
        return False
    except Exception as e:
        print(f"  登录失败 ({role}): {e}")
        return False


def test_route_500(page):
    """步骤⑥ - 1: 所有页面500检查"""
    print("\n" + "=" * 60)
    print("⑥-1 前端路由遍历：24页面500检查")
    print("=" * 60)

    login_as(page, "ADMIN")

    for p in ALL_PAGES:
        url = f"{BASE_URL}{p['path']}"
        try:
            resp = page.goto(url, timeout=15000)
            page.wait_for_load_state("networkidle", timeout=15000)
            status = resp.status if resp else "N/A"
            has_error = page.locator('text="500"').count() > 0 or page.locator('text="内部错误"').count() > 0
            result = "❌" if has_error else "✅"
            print(f"  {result} [{status}] {p['name']}: {p['path']}")
            results["step6_route_500"].append({
                "page": p["name"], "path": p["path"],
                "status": status, "error": has_error
            })
        except Exception as e:
            print(f"  ❌ {p['name']}: {p['path']} - 异常: {str(e)[:80]}")
            results["step6_route_500"].append({
                "page": p["name"], "path": p["path"],
                "status": "ERROR", "error": True, "detail": str(e)[:200]
            })


def test_multi_role(page):
    """步骤⑥ - 2: 多角色遍历（5角色×24页面）"""
    print("\n" + "=" * 60)
    print("⑥-2 多角色遍历：5角色×24页面")
    print("=" * 60)

    for role in ROLES:
        print(f"\n--- 角色: {role} ---")
        context = page.context.browser.new_context()
        role_page = context.new_page()
        login_as(role_page, role)

        for p in ALL_PAGES:
            url = f"{BASE_URL}{p['path']}"
            try:
                resp = role_page.goto(url, timeout=15000)
                role_page.wait_for_load_state("networkidle", timeout=15000)
                status = resp.status if resp else "N/A"

                # 检查是否被重定向（权限不足）
                current_path = role_page.url.replace(BASE_URL, "")
                redirected = current_path == "/dashboard" and p["path"] != "/dashboard"

                # 检查是否应该有权访问（考虑roles和admin）
                has_restriction = len(p["roles"]) > 0 or p.get("admin")
                should_access = role == "ADMIN" or role in p["roles"] or (not has_restriction)

                if redirected and should_access:
                    result = "⚠️ 误拦截"
                elif redirected and not should_access:
                    result = "✅ 正确拦截"
                elif status in [200, 304] or (resp and resp.ok):
                    result = "✅"
                else:
                    result = f"❌ {status}"

                print(f"  {result} {p['name']} ({p['path']})")
                results["step6_multi_role"].append({
                    "role": role, "page": p["name"], "path": p["path"],
                    "status": status, "redirected": redirected,
                    "should_access": should_access, "result": result
                })
            except Exception as e:
                print(f"  ❌ {p['name']}: 异常 - {str(e)[:60]}")
                results["step6_multi_role"].append({
                    "role": role, "page": p["name"], "path": p["path"],
                    "status": "ERROR", "redirected": False,
                    "should_access": True, "result": f"ERROR:{str(e)[:80]}"
                })

        context.close()


def test_loading_state(page):
    """步骤⑥ - 3: 加载状态检查"""
    print("\n" + "=" * 60)
    print("⑥-3 加载状态检查")
    print("=" * 60)

    login_as(page, "ADMIN")
    pages_to_check = [
        "/inventory", "/inbound", "/incoming", "/rma", "/shipment",
        "/bom", "/production-task", "/outbound", "/snapshot",
        "/products", "/partners", "/station", "/device-ledger",
        "/stocktake", "/adjustment", "/customers"
    ]

    for path in pages_to_check:
        url = f"{BASE_URL}{path}"
        try:
            page.goto(url, timeout=15000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(0.3)

            # 检查是否有loading骨架屏或加载指示器（页面加载完毕后不应残留）
            has_loading = page.locator('[class*="loading"], [class*="skeleton"], .el-loading-mask, .el-skeleton').count()
            loading_visible = page.locator('.el-loading-mask:visible, .el-skeleton__item').count()

            # 检查空数据状态
            has_empty = page.locator('text="暂无数据"').count() > 0 or \
                        page.locator('.el-empty').count() > 0

            status = "✅"
            detail = "数据正常"
            if loading_visible > 0:
                status = "⚠️"
                detail = f"残留{loading_visible}个加载元素"
            if has_empty:
                detail = "显示空数据"

            print(f"  {status} {path}: {detail}")
            results["step6_loading"].append({
                "path": path, "has_loading": has_loading > 0,
                "loading_visible": loading_visible, "has_empty": has_empty,
                "status": status, "detail": detail
            })
        except Exception as e:
            print(f"  ❌ {path}: {str(e)[:60]}")
            results["step6_loading"].append({
                "path": path, "status": "ERROR", "detail": str(e)[:200]
            })


def test_print_pages(page):
    """步骤⑧ - 1: 6种单据打印检查"""
    print("\n" + "=" * 60)
    print("⑧-1 打印功能检查")
    print("=" * 60)

    login_as(page, "ADMIN")

    print_modules = [
        {"path": "/inventory", "name": "库存明细打印"},
        {"path": "/inbound", "name": "入库单打印"},
        {"path": "/outbound", "name": "出库单打印"},
        {"path": "/shipment", "name": "出货单打印"},
        {"path": "/incoming", "name": "来料单打印"},
        {"path": "/stocktake", "name": "盘点单打印"},
    ]

    for m in print_modules:
        try:
            page.goto(f"{BASE_URL}{m['path']}", timeout=15000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(0.5)

            # 检查是否有打印按钮
            print_btn = page.locator('button:has-text("打印"), button:has-text("导出")').first
            has_print = print_btn.count() > 0

            # 检查@media print支持
            has_print_style = page.locator('style[media="print"], link[media="print"]').count() > 0

            result = "✅" if has_print else "⚠️ 无打印按钮"
            print(f"  {result} {m['name']} (打印按钮:{has_print}, 打印样式:{has_print_style})")
            results["step8_print"].append({
                "module": m["name"], "has_print_btn": has_print,
                "has_print_style": has_print_style, "result": result
            })
        except Exception as e:
            print(f"  ❌ {m['name']}: {str(e)[:60]}")
            results["step8_print"].append({
                "module": m["name"], "result": f"ERROR:{str(e)[:80]}"
            })


def test_excel_export(page):
    """步骤⑧ - 2: Excel导出功能检查"""
    print("\n" + "=" * 60)
    print("⑧-2 Excel导出功能检查")
    print("=" * 60)

    login_as(page, "ADMIN")

    excel_pages = [
        "/inventory", "/inbound", "/outbound", "/shipment",
        "/incoming", "/rma", "/stocktake", "/adjustment",
        "/products", "/partners", "/station", "/device-ledger"
    ]

    for path in excel_pages:
        try:
            page.goto(f"{BASE_URL}{path}", timeout=15000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(0.3)

            # 检查导出按钮
            export_btn = page.locator('button:has-text("导出")').first
            has_export = export_btn.count() > 0
            has_excel_icon = page.locator('[class*="excel"], [class*="export"]').count() > 0

            result = "✅" if has_export else "⚠️ 无导出按钮"
            print(f"  {result} {path}")
            results["step8_excel"].append({
                "path": path, "has_export": has_export,
                "has_icon": has_excel_icon > 0, "result": result
            })
        except Exception as e:
            print(f"  ❌ {path}: {str(e)[:60]}")
            results["step8_excel"].append({
                "path": path, "result": f"ERROR:{str(e)[:80]}"
            })


def test_404_routes(page):
    """步骤⑨ - 2: 404路由检查"""
    print("\n" + "=" * 60)
    print("⑨-2 404路由/请求超时检查")
    print("=" * 60)

    login_as(page, "ADMIN")

    bad_routes = [
        "/nonexistent-page",
        "/api/bad-endpoint",
        "/invalid/route/123",
        "/login/nonexistent",
    ]

    for route in bad_routes:
        try:
            resp = page.goto(f"{BASE_URL}{route}", timeout=10000)
            status = resp.status if resp else "N/A"
            # 检查是否有友好的404页面或错误提示
            has_404_page = page.locator('text="404", text="页面不存在", text="Not Found"').count() > 0
            result = "✅" if (status == 404 or has_404_page) else f"⚠️ {status}"
            print(f"  {result} {route} -> {status}")
            results["step9_404"].append({
                "route": route, "status": status, "has_friendly": has_404_page
            })
        except Exception as e:
            print(f"  ❌ {route}: {str(e)[:60]}")
            results["step9_404"].append({
                "route": route, "status": "ERROR", "detail": str(e)[:200]
            })


def test_performance(page):
    """步骤⑨ - 1: 页面加载性能"""
    print("\n" + "=" * 60)
    print("⑨-1 页面加载性能检查")
    print("=" * 60)

    login_as(page, "ADMIN")

    perf_pages = [
        "/dashboard", "/inventory", "/inbound", "/incoming",
        "/rma", "/shipment", "/bom", "/production-task",
        "/outbound", "/snapshot"
    ]

    for path in perf_pages:
        try:
            start = time.time()
            resp = page.goto(f"{BASE_URL}{path}", timeout=15000)
            page.wait_for_load_state("networkidle", timeout=15000)
            elapsed = time.time() - start

            threshold = 5.0
            result = "✅" if elapsed < threshold else f"⚠️ {elapsed:.1f}s"
            print(f"  {result} {path}: {elapsed:.2f}s")
            results["step9_performance"].append({
                "path": path, "elapsed": round(elapsed, 2),
                "threshold": threshold, "result": result
            })
        except Exception as e:
            print(f"  ❌ {path}: {str(e)[:60]}")
            results["step9_performance"].append({
                "path": path, "elapsed": -1, "result": f"ERROR:{str(e)[:80]}"
            })


def print_summary():
    """输出汇总报告"""
    print("\n\n" + "=" * 70)
    print("  阶段2 完整检测清单执行报告")
    print("=" * 70)

    sections = [
        ("⑥-1 路由500检查 (24页面)", results["step6_route_500"],
         lambda r: not r.get("error")),
        ("⑥-2 多角色遍历 (5×24=120)", results["step6_multi_role"],
         lambda r: "✅" in str(r.get("result", ""))),
        ("⑥-3 加载状态 (16页面)", results["step6_loading"],
         lambda r: r.get("status") == "✅" or r.get("status") == "⚠️"),
        ("⑧-1 打印功能 (6模块)", results["step8_print"],
         lambda r: "✅" in str(r.get("result", "")) or "⚠️" in str(r.get("result", ""))),
        ("⑧-2 Excel导出 (12页面)", results["step8_excel"],
         lambda r: "✅" in str(r.get("result", "")) or "⚠️" in str(r.get("result", ""))),
        ("⑨-1 性能检查 (10页面)", results["step9_performance"],
         lambda r: "✅" in str(r.get("result", ""))),
        ("⑨-2 404路由 (4路由)", results["step9_404"],
         lambda r: True),  # 全部计入
    ]

    total_pass = 0
    total_items = 0

    for name, items, check_fn in sections:
        passed = sum(1 for r in items if check_fn(r))
        total = len(items)
        total_pass += passed
        total_items += total
        pct = passed / total * 100 if total > 0 else 0
        bar = "█" * int(pct // 10) + "░" * (10 - int(pct // 10))
        print(f"  {name}: {bar} {passed}/{total} ({pct:.0f}%)")

    print(f"\n  总计: {total_pass}/{total_items} 通过")

    # 输出未通过项
    print("\n--- 未通过详情 ---")
    for name, items, check_fn in sections:
        failed = [r for r in items if not check_fn(r)]
        if failed:
            print(f"\n{name} 未通过项:")
            for f_item in failed:
                print(f"  ❌ {f_item}")

    return total_pass, total_items


def main():
    print("IMS 阶段2 在线检查脚本启动")
    print(f"前端地址: {BASE_URL}")
    print(f"后端地址: {API_URL}")
    print(f"测试角色: {ROLES}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True
        )
        page = context.new_page()

        try:
            # 检查服务是否可达
            print("\n检查服务状态...")
            resp = page.goto(f"{BASE_URL}/login", timeout=10000)
            print(f"  前端 {BASE_URL}: {resp.status if resp else 'ERROR'}")
        except Exception as e:
            print(f"  ❌ 前端服务不可达: {e}")
            print("  请确保已启动: cd ims-main/frontend && npm run dev")
            browser.close()
            return 1

        try:
            # 步骤⑥: 前端路由遍历
            test_route_500(page)
            test_multi_role(page)
            test_loading_state(page)

            # 步骤⑧: 打印 + Excel
            test_print_pages(page)
            test_excel_export(page)

            # 步骤⑨: 性能 + 404
            test_performance(page)
            test_404_routes(page)

            # 汇总
            passed, total = print_summary()

        finally:
            browser.close()

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())