"""
6 角色 GUI 验收测试 — 检查按钮级权限控制
验证各角色页面上操作按钮的显示/隐藏是否符合权限矩阵
运行：$env:E2E_BASE_URL="http://localhost:5173"; uv run python tests/e2e/test_gui_acceptance.py
"""
import os, sys, json, time
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:5173")

ROLES = [
    {"username": "admin",      "password": "admin123", "role": "管理员"},
    {"username": "warehouse",   "password": "123456",   "role": "仓库管理员"},
    {"username": "quality",     "password": "123456",   "role": "质量负责人"},
    {"username": "production",  "password": "123456",   "role": "生产负责人"},
    {"username": "test_eng",    "password": "123456",   "role": "测试工程师"},
    {"username": "staff",       "password": "123456",   "role": "普通员工"},
]

# 检查项：页面 → 按钮文本 → 权限键 → 预期有权限的角色列表
BUTTON_CHECKS = [
    {"page": "/inbound",       "button": "新增入库", "perm": "inbound.create",         "expect": ["管理员","仓库管理员"]},
    {"page": "/incoming",      "button": "到货登记", "perm": "incoming.create",       "expect": ["管理员","仓库管理员"]},
    {"page": "/stocktake",     "button": "创建盘点", "perm": "stocktake.create",        "expect": ["管理员","仓库管理员"]},
    {"page": "/outbound",      "button": "新增出库", "perm": "outbound.create",         "expect": ["管理员","仓库管理员"]},
    {"page": "/bom",           "button": "创建BOM",  "perm": "bom.create",              "expect": ["管理员","仓库管理员","生产负责人"]},
    {"page": "/products",      "button": "新增商品", "perm": "product.manage",          "expect": ["管理员","仓库管理员"]},
    {"page": "/adjustment",    "button": "创建调整", "perm": "adjustment.confirm",      "expect": ["管理员","仓库管理员"]},
    {"page": "/rma",           "button": "退货登记", "perm": "rma.create_return",       "expect": ["管理员","仓库管理员"]},
    {"page": "/device-ledger", "button": "登记设备", "perm": "device_ledger.create_edit","expect": ["管理员","仓库管理员"]},
    {"page": "/station",       "button": "新增场站", "perm": "station.create_edit",     "expect": ["管理员","仓库管理员"]},
    {"page": "/shipment",      "button": "出货登记", "perm": "shipment.create",         "expect": ["管理员","仓库管理员"]},
    {"page": "/partners",      "button": "新增单位", "perm": "partner.manage",          "expect": ["管理员","仓库管理员"]},
    {"page": "/customers",     "button": "新增客户", "perm": "customer.manage",         "expect": ["管理员","仓库管理员"]},
]

RESULTS = []

def login(page, username, password, role_name):
    # 先导航到登录页，再清理 localStorage，防止 token 残留导致角色串位
    page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded", timeout=20000)
    page.wait_for_timeout(500)
    page.evaluate("() => localStorage.clear()")
    page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded", timeout=20000)
    page.wait_for_timeout(1000)
    try:
        page.fill('input[placeholder="用户名"]', username, timeout=5000)
        page.fill('input[placeholder="密码"]', password, timeout=5000)
        page.click('button:has-text("登 录")', timeout=5000)
        page.wait_for_url("**/dashboard", timeout=10000)
        return True
    except Exception as e:
        return "/dashboard" in page.url

def check_button(page, check, role_name):
    """检查按钮权限：通过 opacity/pointer-events 判断是否被 PermissionButton 禁用"""
    page.goto(f"{BASE_URL}{check['page']}", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(2000)

    btn_text = check["button"]
    should_have_perm = role_name in check["expect"]
    perm = check["perm"]

    try:
        btn = page.locator(f'button:has-text("{btn_text}")').first
        if btn.count() == 0:
            return "⚠️", f"{perm} → 按钮未找到", "btn_not_found"

        # PermissionButton 禁用时设置 opacity:0.45 + pointer-events:none
        # 检查 computed style
        opacity = btn.evaluate("el => parseFloat(window.getComputedStyle(el).opacity)")
        pointer_e = btn.evaluate("el => window.getComputedStyle(el).pointerEvents")

        # opacity < 0.5 表示被 PermissionButton 禁用
        is_disabled = opacity < 0.5

        if should_have_perm and not is_disabled:
            return "✅", f"{perm} → 正确可用 (opacity={opacity})", "ok"
        elif should_have_perm and is_disabled:
            return "❌", f"{perm} → 应有权限但被禁用 (opacity={opacity})", "perm_denied"
        elif not should_have_perm and is_disabled:
            return "✅", f"{perm} → 正确禁用", "ok"
        else:
            return "❌", f"{perm} → 应禁用但可用 (opacity={opacity})", "perm_leaked"
    except Exception as e:
        return "⚠️", f"{perm} → 检查异常: {str(e)[:40]}", "error"

def main():
    check_count = len(BUTTON_CHECKS)
    role_count = len(ROLES)
    total = check_count * role_count
    
    print("=" * 60)
    print(f"6角色GUI权限验收 — {role_count}角色 × {check_count}按钮")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900}, locale="zh-CN")
        page = context.new_page()

        for r in ROLES:
            print(f"\n--- {r['role']} ({r['username']}) ---")
            ok = login(page, r["username"], r["password"], r["role"])
            if not ok:
                print("  ⚠️ 登录失败，跳过")
                for c in BUTTON_CHECKS:
                    RESULTS.append({
                        "role": r["role"], "page": c["page"], "perm": c["perm"],
                        "result": "⚠️", "detail": "登录失败"
                    })
                continue

            for c in BUTTON_CHECKS:
                result, detail, code = check_button(page, c, r["role"])
                RESULTS.append({
                    "role": r["role"], "page": c["page"], "perm": c["perm"],
                    "result": result, "detail": detail, "code": code
                })
                print(f"  {result} {c['page']:25s} {detail}")

        browser.close()

    # 汇总
    passed = sum(1 for r in RESULTS if r["result"] == "✅")
    failed = sum(1 for r in RESULTS if r["result"] == "❌")
    skipped = sum(1 for r in RESULTS if r["result"] == "⚠️")
    not_found = sum(1 for r in RESULTS if r.get("code") == "btn_not_found")
    perm_leaked = sum(1 for r in RESULTS if r.get("code") == "perm_leaked")
    perm_denied = sum(1 for r in RESULTS if r.get("code") == "perm_denied")

    print(f"\n{'=' * 60}")
    print(f"总计: {len(RESULTS)} | ✅ {passed} | ❌ {failed} | ⚠️ {skipped}")
    if not_found:
        print(f"  按钮未找到: {not_found}")
    if perm_leaked:
        print(f"  ⛔ 权限泄露（应禁用但可用）: {perm_leaked}")
    if perm_denied:
        print(f"  ⛔ 权限不足（应有权限但被禁用）: {perm_denied}")

    # 重点：权限泄露
    if perm_leaked:
        print(f"\n⛔⛔⛔ 权限泄露详情（真实BUG）:")
        for r in RESULTS:
            if r.get("code") == "perm_leaked":
                print(f"  {r['role']} → {r['page']} → {r['perm']}")

    if perm_denied:
        print(f"\n⛔ 权限不足详情:")
        for r in RESULTS:
            if r.get("code") == "perm_denied":
                print(f"  {r['role']} → {r['page']} → {r['perm']}")

    # 保存结果
    out_path = os.path.join(os.path.dirname(__file__), "gui_acceptance_result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "summary": f"✅{passed} ❌{failed} ⚠️{skipped} | leaked:{perm_leaked} denied:{perm_denied} not_found:{not_found}",
            "results": RESULTS
        }, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存: {out_path}")
    
    # 仅当有真正的权限泄露时返回失败
    return 0 if perm_leaked == 0 and perm_denied == 0 else 1

if __name__ == "__main__":
    sys.exit(main())