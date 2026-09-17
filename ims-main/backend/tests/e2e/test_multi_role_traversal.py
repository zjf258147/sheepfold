"""
多角色遍历检查 — 5角色 × 24页面
验证各角色权限隔离是否正确
运行：$env:E2E_BASE_URL="http://localhost:5174"; uv run python tests/e2e/test_multi_role_traversal.py
"""
import os, sys, json, time
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:5173")

ROLES = [
    {"username": "admin", "password": "admin123", "role": "管理员"},
    {"username": "warehouse", "password": "123456", "role": "仓库管理员"},
    {"username": "quality", "password": "123456", "role": "质量负责人"},
    {"username": "production", "password": "123456", "role": "生产负责人"},
    {"username": "test_eng", "password": "123456", "role": "测试工程师"},
]

ALL_PAGES = [
    {"route": "/dashboard", "name": "首页"},
    {"route": "/inventory", "name": "实时库存"},
    {"route": "/inventory/sku", "name": "按SKU统计库存"},
    {"route": "/inventory/partner", "name": "按关联单位出库统计"},
    {"route": "/inbound", "name": "入库"},
    {"route": "/incoming", "name": "来料管理"},
    {"route": "/rma", "name": "返厂维修"},
    {"route": "/shipment", "name": "出货管理"},
    {"route": "/bom", "name": "BOM管理"},
    {"route": "/production-task", "name": "生产任务"},
    {"route": "/outbound", "name": "出库"},
    {"route": "/snapshot", "name": "库存流水"},
    {"route": "/snapshot/statistics", "name": "库存快照汇总"},
    {"route": "/snapshot/details", "name": "快照明细"},
    {"route": "/products", "name": "商品SKU"},
    {"route": "/partners", "name": "往来单位"},
    {"route": "/customers", "name": "客户管理"},
    {"route": "/settings", "name": "系统设置"},
    {"route": "/about", "name": "关于"},
    {"route": "/workflow", "name": "业务流程"},
    {"route": "/station", "name": "场站管理"},
    {"route": "/device-ledger", "name": "设备台账"},
    {"route": "/stocktake", "name": "盘点管理"},
    {"route": "/adjustment", "name": "库存调整"},
]

RESULTS = []

def login(page, username, password, role_name):
    page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded", timeout=20000)
    page.wait_for_timeout(1000)
    if "/dashboard" in page.url:
        return True
    try:
        page.fill('input[placeholder="用户名"]', username, timeout=5000)
        page.fill('input[placeholder="密码"]', password, timeout=5000)
        page.click('button:has-text("登 录")', timeout=5000)
        page.wait_for_timeout(3000)
        if "/dashboard" in page.url:
            return True
        page.wait_for_url("**/dashboard", timeout=10000)
        return True
    except:
        return "/dashboard" in page.url

def check_page(page, route, name):
    url = f"{BASE_URL}{route}"
    console_errors = []
    def on_console(msg):
        if msg.type == "error": console_errors.append(msg.text)
    page.on("console", on_console)
    try:
        resp = page.goto(url, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(1500)
        status = resp.status if resp else 0
        body = page.locator("body").inner_text(timeout=3000).strip()
        has_content = len(body) > 10
        
        # 判断：有内容 + 非登录页 = 可访问
        if has_content and "/login" not in page.url and status in [200, 304]:
            result = "✅"
        elif status == 401 or status == 403 or "/login" in page.url:
            result = "🔒"  # 权限拒绝（符合预期）
        else:
            result = "⚠️" if status in [200, 304] else "❌"
        
        detail = f"HTTP{status} {len(body)}chars"
        if console_errors:
            detail += f" err{len(console_errors)}"
        return result, detail
    except Exception as e:
        return "❌", str(e)[:60]
    finally:
        page.remove_listener("console", on_console)

def main():
    print("=" * 60)
    print("多角色遍历检查 — 5角色 × 24页面")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for role_info in ROLES:
            role_name = role_info["role"]
            print(f"\n--- {role_name} ({role_info['username']}) ---")
            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()
            
            logged_in = login(page, role_info["username"], role_info["password"], role_name)
            if not logged_in:
                print(f"  ❌ 登录失败")
                context.close()
                for pg in ALL_PAGES:
                    RESULTS.append({"role": role_name, "page": pg["name"], "route": pg["route"], "result": "❌", "detail": "登录失败"})
                continue
            
            page_results = []
            for pg in ALL_PAGES:
                r, d = check_page(page, pg["route"], pg["name"])
                page_results.append((r, d))
                RESULTS.append({"role": role_name, "page": pg["name"], "route": pg["route"], "result": r, "detail": d})
            
            # 汇总该角色
            ok = sum(1 for r, _ in page_results if r == "✅")
            locked = sum(1 for r, _ in page_results if r == "🔒")
            warn = sum(1 for r, _ in page_results if r == "⚠️")
            fail = sum(1 for r, _ in page_results if r == "❌")
            
            # 列式输出
            cols = 4
            for i in range(0, len(ALL_PAGES), cols):
                line = ""
                for j in range(cols):
                    idx = i + j
                    if idx < len(ALL_PAGES):
                        line += f"{page_results[idx][0]} {ALL_PAGES[idx]['name']:<12}"
                print(f"  {line}")
            
            print(f"  → 可访问:{ok} 拒绝:{locked} 警告:{warn} 失败:{fail}")
            context.close()
    
    # 汇总表
    print("\n" + "=" * 60)
    print("多角色权限矩阵")
    print("=" * 60)
    
    # 表头
    roles = [r["role"] for r in ROLES]
    header = f"{'页面':<22}"
    for r in roles:
        short = r[:4] if len(r) > 4 else r
        header += f" {short:<6}"
    print(header)
    print("-" * (22 + 7 * len(roles)))
    
    for pg in ALL_PAGES:
        line = f"{pg['name']:<22}"
        for role in roles:
            item = next((r for r in RESULTS if r["role"] == role and r["page"] == pg["name"]), None)
            icon = item["result"] if item else "⬜"
            line += f" {icon:<5}"
        print(line)
    
    # 统计
    print("-" * (22 + 7 * len(roles)))
    total_checks = len(RESULTS)
    ok_count = sum(1 for r in RESULTS if r["result"] == "✅")
    locked_count = sum(1 for r in RESULTS if r["result"] == "🔒")
    warn_count = sum(1 for r in RESULTS if r["result"] == "⚠️")
    fail_count = sum(1 for r in RESULTS if r["result"] == "❌")
    print(f"总检查:{total_checks} | 可访问:{ok_count} 拒绝:{locked_count} 警告:{warn_count} 失败:{fail_count}")
    
    json_path = os.path.join(os.path.dirname(__file__), "multi_role_traversal_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"total": total_checks, "ok": ok_count, "locked": locked_count, "warn": warn_count, "fail": fail_count, "results": RESULTS}, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存: {json_path}")
    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())