"""
阶段2 在线检查: 打印分页、Excel导出、并发测试、404路由
============================================================
"""
import os, json, time, asyncio
from datetime import datetime
import httpx

API_URL = "http://localhost:8000"
TEST_USER = {"username": "admin", "password": "admin123"}

def api_login():
    with httpx.Client(timeout=60, trust_env=False) as c:
        r = c.post(f"{API_URL}/api/v1/auth/login", json=TEST_USER)
        if r.status_code == 200:
            return r.json().get("data", {}).get("access_token", "")
        raise Exception(f"登录失败: {r.status_code}")

def api_get(token, path, params=None):
    with httpx.Client(timeout=60, trust_env=False) as c:
        r = c.get(f"{API_URL}{path}", headers={"Authorization": f"Bearer {token}"}, params=params or {})
        return r

def get_first_id(token, list_path, params=None, resp_key="items"):
    r = api_get(token, list_path, params)
    if r.status_code != 200:
        return None, 0, f"HTTP {r.status_code}"
    data = r.json()
    # 处理多种响应格式: {data: {items: [...]}} 或 [item, ...] 或 {items: [...]}
    if isinstance(data, list):
        # 直接返回列表
        if data:
            return data[0].get("id"), len(data), None
        return None, 0, None
    if isinstance(data, dict):
        d = data.get("data", data)
        if isinstance(d, list):
            if d:
                return d[0].get("id"), len(d), None
            return None, 0, None
        if isinstance(d, dict):
            items = d.get(resp_key, [])
            if items:
                return items[0].get("id"), len(items), None
            # 可能没有resp_key，尝试直接找id
            if "id" in d:
                return d.get("id"), 1, None
            return None, d.get("total", 0), None
    return None, 0, None

# ============================================================
# 打印测试
# ============================================================
def test_print(token):
    print("\n" + "=" * 60)
    print("📄 打印功能测试 (6种单据)")
    print("=" * 60)

    # 先获取到货单ID，用于检验单/退货单
    rid, _, _ = get_first_id(token, "/api/v1/incoming/receipts")
    # 先获取RMA退货单ID，用于维修单
    rma_id, _, _ = get_first_id(token, "/api/v1/rma/returns")

    configs = [
        ("到货单",     "/api/v1/print/incoming_receipt",     rid),
        ("出货单",     "/api/v1/print/shipment",             None),
        ("来料检验单", "/api/v1/print/incoming_inspection",  None),
        ("来料退货单", "/api/v1/print/incoming_return",      None),
        ("返厂维修单", "/api/v1/print/rma_repair",           None),
        ("BOM单",      "/api/v1/print/bom",                  None),
    ]

    # 先通过列表API找到可用ID
    print("  正在查找各打印单据的可用ID...\n")
    id_map = {}

    # 出货单 -> /api/v1/shipment/list
    sid, _, err = get_first_id(token, "/api/v1/shipment/list", {"page": 1, "page_size": 1})
    if sid: id_map["shipment"] = sid
    else: print(f"  ⚠️ 出货单列表无数据: {err}")

    # 来料检验单: 通过 receipt -> inspections
    if rid:
        iid, _, err = get_first_id(token, f"/api/v1/incoming/receipts/{rid}/inspections", None, "inspections")
        if iid: id_map["inspection"] = iid
        else: print(f"  ⚠️ 来料检验单无数据: {err}")
    else:
        print("  ⚠️ 无到货单，无法获取检验单")

    # 来料退货单: incoming_returns 没有独立列表API, 尝试直接查询
    rret_id, _, err = get_first_id(token, "/api/v1/incoming/receipts")
    # 直接用 receipt 的 ID 去查 print/incoming_return (IncomingReturn表)
    # 先试ID=1,如果不成功则为None
    test_r = api_get(token, "/api/v1/print/incoming_return/1")
    if test_r.status_code == 200:
        id_map["incoming_return"] = 1
        print(f"  来料退货单打印端点可用 (ID=1)")
    else:
        id_map["incoming_return"] = None
        print(f"  ⚠️ 来料退货单无数据")

    # 返厂维修单: 通过 rma_return -> repairs
    if rma_id:
        jid, _, err = get_first_id(token, f"/api/v1/rma/returns/{rma_id}/repairs", None, "repairs")
        if jid: id_map["rma_repair"] = jid
        else: print(f"  ⚠️ 返厂维修单无数据: {err}")
    else:
        print("  ⚠️ 无RMA退货单，无法获取维修单")

    # BOM单 -> /api/v1/bom/list
    bid, _, err = get_first_id(token, "/api/v1/bom/list", {"page": 1, "page_size": 1})
    if bid: id_map["bom"] = bid
    else: print(f"  ⚠️ BOM列表无数据: {err}")

    # 开始测试打印
    tests = [
        ("到货单",     "/api/v1/print/incoming_receipt",     rid),
        ("出货单",     "/api/v1/print/shipment",             id_map.get("shipment")),
        ("来料检验单", "/api/v1/print/incoming_inspection",  id_map.get("inspection")),
        ("来料退货单", "/api/v1/print/incoming_return",      id_map.get("incoming_return")),
        ("返厂维修单", "/api/v1/print/rma_repair",           id_map.get("rma_repair")),
        ("BOM单",      "/api/v1/print/bom",                  id_map.get("bom")),
    ]

    results = []
    for name, base, tid in tests:
        print(f"  📋 {name} (ID={tid})...", end=" ")
        if tid is None:
            print("⚠️ 无可用ID")
            results.append((f"打印-{name}", "⚠️", "无可用数据ID"))
            continue

        r = api_get(token, f"{base}/{tid}")
        if r.status_code == 200:
            data = r.json()
            inner = data.get("data", data)
            keys = len(inner.keys()) if isinstance(inner, dict) else 0
            print(f"✅ 字段数={keys}")
            results.append((f"打印-{name}", "✅", f"{keys}字段"))
        elif r.status_code == 404:
            print(f"⚠️ 404")
            results.append((f"打印-{name}", "⚠️", "404无此数据"))
        else:
            print(f"❌ HTTP {r.status_code}")
            results.append((f"打印-{name}", "❌", str(r.status_code)))

    return results

# ============================================================
# Excel导出测试
# ============================================================
def test_excel(token):
    print("\n" + "=" * 60)
    print("📊 Excel导出测试 (10个端点)")
    print("=" * 60)

    # snapshot日期参数需要实际存在的日期
    # 先获取存在的快照日期
    dates_r = api_get(token, "/api/v1/snapshots/dates")
    snapshot_date = None
    if dates_r.status_code == 200:
        dates = dates_r.json().get("data", [])
        if dates:
            snapshot_date = dates[0]
            print(f"  快照可用日期: {snapshot_date}")

    date_from = snapshot_date or "2026-09-01"
    date_to = snapshot_date or "2026-09-16"

    endpoints = [
        ("库存流水日报", "/api/v1/snapshots/daily-ledger/export",
         {"date_from": date_from, "date_to": date_to}),
        ("库存流水汇总", "/api/v1/snapshots/ledger-summary/export",
         {"date_from": date_from, "date_to": date_to}),
        ("库存单品导出", "/api/v1/snapshots/items/export",
         {"snapshot_date": snapshot_date} if snapshot_date else
         {"snapshot_date": date_from}),
        ("RMA导出",      "/api/v1/rma/export", {}),
        ("出库单导出",   "/api/v1/outbound/orders/export", {}),
        ("库存明细导出", "/api/v1/inventory/items/export", {}),
        ("来料到货导出", "/api/v1/incoming/receipts/export", {}),
        ("入库单导出",   "/api/v1/inbound/orders/export", {}),
        ("BOM导出",      "/api/v1/bom/export", {}),
        ("生产任务导出", "/api/v1/production-task/export", {}),
    ]

    results = []
    for name, ep, params in endpoints:
        print(f"  📊 {name}...", end=" ")
        try:
            with httpx.Client(timeout=60, follow_redirects=True, trust_env=False) as c:
                r = c.get(f"{API_URL}{ep}",
                          headers={"Authorization": f"Bearer {token}"},
                          params=params if params else None)

            ct = r.headers.get("content-type", "")
            cd = r.headers.get("content-disposition", "")
            cl = len(r.content)
            kb = cl / 1024
            is_excel = any(x in ct.lower() for x in ["spreadsheet", "excel", "officedocument"]) \
                       or any(x in (cd or "").lower() for x in [".xlsx", ".xls"])

            if r.status_code == 200 and cl > 0 and is_excel:
                print(f"✅ {kb:.1f}KB Excel")
                results.append((f"导出-{name}", "✅", f"{kb:.1f}KB Excel"))
            elif r.status_code == 200 and cl > 0:
                print(f"✅ {kb:.1f}KB (非Excel: {ct[:30]})")
                results.append((f"导出-{name}", "✅", f"{kb:.1f}KB {ct[:25]}"))
            elif r.status_code == 200 and cl == 0:
                print(f"⚠️ 空文件")
                results.append((f"导出-{name}", "⚠️", "空文件0字节"))
            elif r.status_code == 404:
                print(f"⚠️ 404")
                results.append((f"导出-{name}", "⚠️", "404"))
            elif r.status_code == 422:
                print(f"⚠️ 422参数错误: {r.text[:60]}")
                results.append((f"导出-{name}", "⚠️", f"422 {r.text[:40]}"))
            elif r.status_code == 500:
                print(f"❌ 500: {r.text[:60]}")
                results.append((f"导出-{name}", "❌", f"500 {r.text[:40]}"))
            else:
                print(f"⚠️ HTTP {r.status_code}")
                results.append((f"导出-{name}", "⚠️", str(r.status_code)))
        except Exception as e:
            print(f"❌ {str(e)[:60]}")
            results.append((f"导出-{name}", "❌", str(e)[:40]))
    return results

# ============================================================
# 并发测试
# ============================================================
async def test_concurrency(token):
    print("\n" + "=" * 60)
    print("⚡ 并发测试 (50用户)")
    print("=" * 60)

    targets = [
        ("仪表盘-库存摘要", "/api/v1/dashboard/stock-summary"),
        ("仪表盘-待审核",   "/api/v1/dashboard/pending-audit"),
        ("库存列表",        "/api/v1/inventory/items?page=1&page_size=5"),
        ("商品SKU",         "/api/v1/products/skus?page=1&page_size=5"),
        ("往来单位",        "/api/v1/partners?page=1&page_size=5"),
    ]

    results = []

    async def one_req(client, path):
        t0 = time.time()
        try:
            r = await client.get(f"{API_URL}{path}", headers={"Authorization": f"Bearer {token}"}, timeout=30)
            return {"ok": r.status_code == 200, "status": r.status_code, "time": time.time() - t0}
        except Exception as e:
            return {"ok": False, "error": str(e)[:60], "time": time.time() - t0}

    N = 50
    async with httpx.AsyncClient(trust_env=False) as client:
        for name, path in targets:
            print(f"  ⚡ {name} ({N}并发)...")
            tasks = [one_req(client, path) for _ in range(N)]
            t_start = time.time()
            res = await asyncio.gather(*tasks)
            t_total = time.time() - t_start

            ok_count = sum(1 for r in res if r.get("ok"))
            fail_count = N - ok_count
            times = [r["time"] * 1000 for r in res]
            avg_ms = sum(times) / len(times) if times else 0
            max_ms = max(times) if times else 0
            errors = [r.get("error") for r in res if not r.get("ok") and r.get("error")]

            icon = "✅" if fail_count == 0 else ("⚠️" if fail_count <= 2 else "❌")
            err_info = f", 错误: {errors[:2]}" if errors else ""
            print(f"    {icon} {ok_count}/{N} 平均{avg_ms:.0f}ms 最大{max_ms:.0f}ms 总{t_total:.1f}s{err_info}")
            results.append((f"并发-{name}", icon,
                            f"{ok_count}/{N} 平均{avg_ms:.0f}ms 最大{max_ms:.0f}ms"))
    return results

# ============================================================
# 404 + 超时测试
# ============================================================
def test_404_and_timeout(token):
    print("\n" + "=" * 60)
    print("🛡️ 404路由 + 超时测试")
    print("=" * 60)
    results = []

    for name, ep in [("不存在端点", "/api/v1/nonexistent_endpoint_xyz"),
                      ("不存在认证", "/api/v1/auth/nonexistent_op")]:
        print(f"  🔗 {ep}...", end=" ")
        r = api_get(token, ep)
        if r.status_code == 404:
            print("✅ 正确404")
            results.append((f"API404-{name}", "✅", "404"))
        else:
            print(f"⚠️ {r.status_code}")
            results.append((f"API404-{name}", "⚠️", str(r.status_code)))

    print(f"  ⏱️ 大数据量请求...", end=" ")
    t0 = time.time()
    r = api_get(token, "/api/v1/inventory/items?page=1&page_size=100")
    t = time.time() - t0
    print(f"✅ {t:.2f}s {len(r.content)}B")
    results.append(("超时-大数据量", "✅" if t < 10 else "⚠️", f"{t:.2f}s"))

    print(f"  🌐 前端404路由...")
    with httpx.Client(timeout=30, trust_env=False) as c:
        for route in ["/nonexistent-page", "/.env", "/wp-admin"]:
            url = f"http://localhost:5173{route}"
            r = c.get(url)
            ok = r.status_code in (200, 404)
            print(f"    {route} → {r.status_code} {'✅' if ok else '⚠️'}")
            results.append((f"前端404-{route}", "✅" if ok else "⚠️", f"{r.status_code}"))
    return results

# ============================================================
def main():
    print("=" * 60)
    print("🔍 阶段2 综合测试: 打印 + Excel导出 + 并发 + 404")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        token = api_login()
        print(f"🔑 登录成功")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return

    all_results = {
        "📄 打印": test_print(token),
        "📊 Excel导出": test_excel(token),
        "⚡ 并发(50用户)": asyncio.run(test_concurrency(token)),
        "🛡️ 404+超时": test_404_and_timeout(token),
    }

    print("\n" + "=" * 60)
    print("📊 阶段2 综合测试报告")
    print("=" * 60)

    total_ok = total_warn = total_fail = total = 0
    for cat, results in all_results.items():
        ok_c = sum(1 for _, s, _ in results if "✅" in s)
        wc = sum(1 for _, s, _ in results if "⚠️" in s)
        fc = sum(1 for _, s, _ in results if "❌" in s)
        print(f"\n--- {cat} ---")
        for n, s, d in results:
            icon = "✅" if "✅" in s else ("⚠️" if "⚠️" in s else "❌")
            print(f"  {icon} {n}: {d}")
        print(f"  小计: ✅{ok_c} ⚠️{wc} ❌{fc}")
        total_ok += ok_c; total_warn += wc; total_fail += fc; total += ok_c + wc + fc

    print(f"\n{'='*60}")
    pct = total_ok * 100 // total if total else 0
    print(f"📊 汇总: 总计 {total} | ✅ {total_ok} | ⚠️ {total_warn} | ❌ {total_fail}  ({pct}%)")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    result_file = os.path.join(os.path.dirname(__file__), "phase2_results.json")
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump({"ts": datetime.now().isoformat(), "results": {k: [[n,s,d] for n,s,d in v] for k,v in all_results.items()},
                   "summary": {"total": total, "ok": total_ok, "warn": total_warn, "fail": total_fail}}, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存: {result_file}")

if __name__ == "__main__":
    main()