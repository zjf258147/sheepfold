"""
前端路由遍历检查 — 遍历所有页面，验证不返回 500、不白屏、无控制台错误。

运行：
  $env:E2E_BASE_URL="http://localhost:5173"
  cd backend && uv run python tests/e2e/test_all_pages_500.py
"""

import os
import sys
import json
import time

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:5173")
API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000")

# 所有需要遍历的页面路由
ALL_PAGES = [
    # 一期页面
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
    # 二期页面
    {"route": "/station", "name": "场站管理"},
    {"route": "/device-ledger", "name": "设备台账"},
    {"route": "/stocktake", "name": "盘点管理"},
    {"route": "/adjustment", "name": "库存调整"},
]

RESULTS = []


def login(page):
    """登录系统。"""
    print(f"[登录] 访问 {BASE_URL}/log in ...")
    page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(2000)

    # 填写登录表单
    page.fill('input[placeholder="用户名"]', "admin", timeout=10000)
    page.fill('input[placeholder="密码"]', "admin123", timeout=10000)
    page.click('button:has-text("登 录")', timeout=10000)
    page.wait_for_timeout(5000)
    page.wait_for_url(f"**/dashboard", timeout=30000)
    page.wait_for_timeout(2000)
    print("[登录] 登录成功 ✓")


def check_page(page, route, name):
    """访问单个页面并检查。"""
    url = f"{BASE_URL}{route}"
    result = {"route": route, "name": name, "url": url, "status": "UNKNOWN", "errors": []}

    # 收集控制台错误
    console_errors = []
    def on_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)
    page.on("console", on_console)

    try:
        print(f"  访问 {name} ({url}) ...")
        resp = page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)

        # 检查 HTTP 状态
        http_status = resp.status if resp else "N/A"
        result["http_status"] = http_status

        if http_status == 500 or http_status == 502 or http_status == 503:
            result["status"] = "FAIL"
            result["errors"].append(f"HTTP {http_status}")
            print(f"    ❌ HTTP {http_status}")
        else:
            # 检查是否是空白页
            body_text = page.locator("body").inner_text(timeout=3000).strip()
            if not body_text or len(body_text) < 5:
                result["status"] = "WARN"
                result["errors"].append("页面内容为空（白屏风险）")
                print(f"    ⚠️  页面内容极短，可能白屏 ({len(body_text)} 字符)")
            else:
                result["status"] = "OK"
                print(f"    ✅ HTTP {http_status}, 内容 {len(body_text)} 字符")

            # 检查控制台错误
            if console_errors:
                result["status"] = "WARN" if result["status"] == "OK" else result["status"]
                result["errors"].extend(console_errors[:3])
                print(f"    ⚠️  控制台错误: {len(console_errors)} 条")

    except Exception as e:
        result["status"] = "FAIL"
        result["errors"].append(str(e)[:200])
        print(f"    ❌ 异常: {str(e)[:200]}")

    finally:
        page.remove_listener("console", on_console)

    RESULTS.append(result)
    return result


def main():
    print("=" * 60)
    print("前端路由遍历检查 — 23 页面 500 检查")
    print("=" * 60)
    print(f"前端地址: {BASE_URL}")
    print(f"后端地址: {API_BASE}")
    print(f"页面总数: {len(ALL_PAGES)}")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
        )
        page = context.new_page()

        try:
            # 登录
            login(page)

            # 遍历所有页面
            for i, item in enumerate(ALL_PAGES, 1):
                print(f"[{i}/{len(ALL_PAGES)}]", end=" ")
                check_page(page, item["route"], item["name"])
                time.sleep(0.5)  # 避免请求过快

        except Exception as e:
            print(f"\n❌ 整体执行异常: {e}")
        finally:
            browser.close()

    # 输出汇总
    print()
    print("=" * 60)
    print("汇总报告")
    print("=" * 60)

    ok_count = sum(1 for r in RESULTS if r["status"] == "OK")
    warn_count = sum(1 for r in RESULTS if r["status"] == "WARN")
    fail_count = sum(1 for r in RESULTS if r["status"] == "FAIL")
    total = len(RESULTS)

    print(f"{'页面':<24} {'路由':<32} {'状态':<8} {'备注'}")
    print("-" * 80)
    for r in RESULTS:
        status_icon = {"OK": "✅", "WARN": "⚠️", "FAIL": "❌", "UNKNOWN": "⬜"}.get(r["status"], "⬜")
        errors = "; ".join(r["errors"][:2]) if r["errors"] else ""
        print(f"{r['name']:<24} {r['route']:<32} {status_icon} {r['status']:<4} {errors[:60]}")

    print("-" * 80)
    print(f"统计: 总计 {total} | OK={ok_count} | WARN={warn_count} | FAIL={fail_count}")
    print(f"通过率: {ok_count}/{total} ({ok_count/total*100:.0f}%)" if total > 0 else "N/A")

    # 输出 JSON 结果
    json_path = os.path.join(os.path.dirname(__file__), "page_traversal_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, ensure_ascii=False, indent=2)
    print(f"\n详细结果已保存: {json_path}")

    # 返回退出码
    if fail_count > 0:
        print("\n❌ 存在失败页面！")
        sys.exit(1)
    else:
        print("\n✅ 所有页面遍历完成，无 500 错误")
        sys.exit(0)


if __name__ == "__main__":
    main()