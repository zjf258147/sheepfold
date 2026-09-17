"""
空数据渲染 & 加载状态检查 — 24页面的空状态、加载态、内容态
运行：$env:E2E_BASE_URL="http://localhost:5174"; uv run python tests/e2e/test_empty_loading.py
"""
import os, sys, json, time
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:5173")

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

def login(page):
    page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded", timeout=20000)
    page.wait_for_timeout(1000)
    if "/dashboard" in page.url:
        return True
    page.fill('input[placeholder="用户名"]', "admin", timeout=5000)
    page.fill('input[placeholder="密码"]', "admin123", timeout=5000)
    page.click('button:has-text("登 录")', timeout=5000)
    page.wait_for_timeout(3000)
    return True

def analyze_page(page, route, name):
    url = f"{BASE_URL}{route}"
    result = {
        "page": name, "route": route,
        "has_loading": False, "has_empty": False, "has_content": False,
        "content_size": 0, "issues": []
    }
    
    try:
        # 先访问页面，捕捉加载态
        resp = page.goto(url, wait_until="domcontentloaded", timeout=15000)
        
        # 等500ms捕捉loading
        page.wait_for_timeout(500)
        
        # 检查加载指示器
        loading_selectors = [
            ".el-loading-mask", ".el-loading-spinner", 
            "[v-loading]", ".loading-overlay", ".skeleton",
            ".el-skeleton", ".loading-text"
        ]
        for sel in loading_selectors:
            try:
                el = page.locator(sel)
                if el.count() > 0 and el.first.is_visible():
                    result["has_loading"] = True
                    break
            except: pass
        
        # 等待数据加载完成（等待loading消失或timeout）
        try:
            page.wait_for_selector(".el-loading-mask", state="detached", timeout=5000)
        except: pass
        page.wait_for_timeout(1000)
        
        # 检查空状态
        empty_selectors = [
            ".el-empty", ".el-empty__description",
            "[class*='empty']", "[class*='no-data']",
        ]
        for sel in empty_selectors:
            try:
                el = page.locator(sel)
                if el.count() > 0 and el.first.is_visible():
                    result["has_empty"] = True
                    break
            except: pass
        
        # 检查空状态文字
        body = page.locator("body").inner_text(timeout=3000).strip()
        empty_keywords = ["暂无数据", "暂无记录", "暂无内容", "无数据", "没有数据", "空空如也"]
        for kw in empty_keywords:
            if kw in body:
                result["has_empty"] = True
                break
        
        # 检查有内容
        content_selectors = [
            ".el-table__body tr", ".el-table__row",
            "tbody tr", ".card", ".el-card",
            ".stat-item", ".chart", ".data-row",
            "table tbody tr:not(.el-table__empty-row)"
        ]
        for sel in content_selectors:
            try:
                el = page.locator(sel)
                cnt = el.count()
                if cnt > 0:
                    result["has_content"] = True
                    result["content_rows"] = cnt
                    break
            except: pass
        
        if not result["has_content"]:
            # 检查是否有表单/输入框（即页面有交互元素但无数据行）
            try:
                inputs = page.locator("input, select, textarea, button").count()
                if inputs > 1:
                    result["has_content"] = True
                    result["content_type"] = "form"
            except: pass
        
        result["content_size"] = len(body)
        result["http_status"] = resp.status if resp else 0
        
        # 判断状态
        if result["has_content"]:
            result["status"] = "✅ 有数据"
        elif result["has_empty"]:
            result["status"] = "📭 空状态"
        else:
            result["status"] = "⚠️ 需确认" if result["content_size"] > 50 else "❌ 空白"
        
    except Exception as e:
        result["status"] = "❌ 异常"
        result["issues"].append(str(e)[:80])
    
    RESULTS.append(result)
    return result

def main():
    print("=" * 60)
    print("空数据渲染 & 加载状态 — 24页面检查")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        
        login(page)
        
        for i, pg in enumerate(ALL_PAGES, 1):
            r = analyze_page(page, pg["route"], pg["name"])
            load_icon = "🔄" if r["has_loading"] else "  "
            print(f"[{i:>2}/24] {load_icon} {r['status']:<10} | {r['page']:<20} | HTTP{r['http_status']} | {r['content_size']}chars")
            if r["issues"]: print(f"      ⚠️ {r['issues'][0]}")
            time.sleep(0.3)
        
        context.close()
    
    # 汇总
    print("\n" + "=" * 60)
    print("汇总报告")
    print("=" * 60)
    
    has_data = sum(1 for r in RESULTS if "有数据" in r["status"] or "form" in str(r.get("content_type","")))
    has_empty = sum(1 for r in RESULTS if "空状态" in r["status"])
    has_loading = sum(1 for r in RESULTS if r["has_loading"])
    warn = sum(1 for r in RESULTS if "需确认" in r["status"] or "空白" in r["status"] or "异常" in r["status"])
    
    print(f"{'页面':<22} {'状态':<12} {'加载态':<8} {'内容':<8} {'备注'}")
    print("-" * 80)
    for r in RESULTS:
        load = "✅" if r["has_loading"] else "—"
        rows = f"{r.get('content_rows','')}行" if r.get("content_rows") else ""
        print(f"{r['page']:<22} {r['status']:<12} {load:<8} {r['content_size']}chars {rows}")
    print("-" * 80)
    print(f"总计: {len(RESULTS)} | 有数据:{has_data} | 空状态:{has_empty} | 加载态:{has_loading} | 需关注:{warn}")
    
    json_path = os.path.join(os.path.dirname(__file__), "empty_loading_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"summary": {"total": len(RESULTS), "has_data": has_data, "has_empty": has_empty, "has_loading": has_loading, "warn": warn}, "details": RESULTS}, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存: {json_path}")
    return 0 if warn == 0 else 1

if __name__ == "__main__":
    sys.exit(main())