"""
大数据量渲染测试 — 1000+行页面渲染性能
运行：$env:E2E_BASE_URL="http://localhost:5174"; uv run python tests/e2e/test_large_data_render.py
"""
import os, sys, time
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:5173")

# 测试页面：有列表数据的关键页面
TEST_PAGES = [
    {"route": "/inventory?page_size=500", "name": "实时库存(500条)"},
    {"route": "/incoming?page_size=500", "name": "来料管理(500条)"},
    {"route": "/rma?page_size=500", "name": "返厂维修(500条)"},
]

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

def test_page(page, route, name):
    results = {"page": name, "route": route}
    url = f"{BASE_URL}{route}"
    
    try:
        # 测量首次渲染时间
        start = time.time()
        resp = page.goto(url, wait_until="domcontentloaded", timeout=30000)
        first_paint = round((time.time() - start) * 1000)
        results["first_paint_ms"] = first_paint
        
        # 等待数据加载
        try:
            page.wait_for_selector(".el-table__body", timeout=15000)
            page.wait_for_timeout(2000)
        except:
            results["table_found"] = False
        else:
            results["table_found"] = True
            # 计算渲染行数
            try:
                rows = page.locator(".el-table__body tr").count()
                results["row_count"] = rows
            except:
                results["row_count"] = 0
            
            # 内存使用（JS估算）
            try:
                mem = page.evaluate("() => performance.memory ? performance.memory.usedJSHeapSize : 0")
                results["js_heap_mb"] = round(mem / 1024 / 1024, 1)
            except:
                results["js_heap_mb"] = -1
        
        load_done = round((time.time() - start) * 1000)
        results["total_load_ms"] = load_done
        
        # 滚动测试
        try:
            table = page.locator(".el-table__body-wrapper")
            if table.count() > 0:
                scroll_start = time.time()
                # 模拟滚动到底部
                table.first.evaluate("el => el.scrollTop = el.scrollHeight")
                page.wait_for_timeout(1000)
                scroll_time = round((time.time() - scroll_start) * 1000)
                results["scroll_to_bottom_ms"] = scroll_time
                
                # 滚动回顶部
                table.first.evaluate("el => el.scrollTop = 0")
                page.wait_for_timeout(500)
        except:
            results["scroll_test"] = "failed"
        
        # 分页切换测试
        try:
            page_btns = page.locator(".el-pagination button.btn-next")
            if page_btns.count() > 0 and page_btns.first.is_enabled():
                page_start = time.time()
                page_btns.first.click()
                page.wait_for_timeout(2000)
                page_time = round((time.time() - page_start) * 1000)
                results["page_switch_ms"] = page_time
                # 翻回
                page.locator(".el-pagination button.btn-prev").first.click()
                page.wait_for_timeout(1000)
        except:
            pass
        
    except Exception as e:
        results["error"] = str(e)[:80]
    
    return results

def main():
    print("=" * 60)
    print("大数据量渲染测试 — 1000+行页面性能")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        
        login(page)
        
        all_results = []
        for pg in TEST_PAGES:
            print(f"\n测试: {pg['name']} → {pg['route']}")
            r = test_page(page, pg["route"], pg["name"])
            all_results.append(r)
            
            print(f"  首屏渲染: {r.get('first_paint_ms','?')}ms")
            print(f"  总加载: {r.get('total_load_ms','?')}ms")
            print(f"  数据行数: {r.get('row_count','?')}")
            print(f"  表格渲染: {'✅' if r.get('table_found') else '❌'}")
            if r.get("scroll_to_bottom_ms"):
                print(f"  滚到底部: {r['scroll_to_bottom_ms']}ms")
            if r.get("page_switch_ms"):
                print(f"  翻页切换: {r['page_switch_ms']}ms")
            if r.get("error"):
                print(f"  ❌ {r['error']}")
            time.sleep(0.5)
        
        context.close()
    
    # 汇总
    print("\n" + "=" * 60)
    print("汇总报告")
    print("-" * 60)
    for r in all_results:
        fps = r.get("first_paint_ms", 0)
        tlr = r.get("total_load_ms", 0)
        rows = r.get("row_count", 0)
        icon = "✅" if r.get("table_found") and fps < 5000 else ("⚠️" if fps < 10000 else "❌")
        print(f"  {icon} {r['page']:<20} | 首屏{fps}ms | 共{tlr}ms | {rows}行")
    
    ok = sum(1 for r in all_results if r.get("table_found"))
    print("-" * 60)
    print(f"全部: {ok}/{len(all_results)} 正常渲染")
    
    if ok == len(all_results):
        print("✅ 大数据量页面渲染正常")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())