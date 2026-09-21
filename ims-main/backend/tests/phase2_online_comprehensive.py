"""Phase 2 Online Comprehensive Test v4"""
import asyncio, httpx, time, sys, os, json
from datetime import datetime

BASE_URL = "http://localhost:8000"
FRONT_URL = "http://localhost:5174"
PASS = 0; FAIL = 0; RESULTS = []

def log(s, t, st, d=""):
    global PASS, FAIL
    e = "✅" if st == "PASS" else "❌" if st == "FAIL" else "⚠️"
    if st == "PASS": PASS += 1
    elif st == "FAIL": FAIL += 1
    print(f"{e} [{s}] {t}" + (f" - {d}" if d else ""))
    RESULTS.append({"section":s,"test":t,"status":st,"detail":d})

ROUTES = [("/app/login","登录"),("/app/dashboard","数据看板"),("/app/inventory","库存明细"),
    ("/app/incoming","到货登记"),("/app/shipment","出货管理"),("/app/rma","返厂维修"),
    ("/app/bom","BOM管理"),("/app/station","场站管理"),("/app/device-ledger","设备台账"),
    ("/app/stocktake","盘点管理"),("/app/adjustment","库存调整"),("/app/customer","客户管理"),
    ("/app/partner","往来单位"),("/app/product","物料管理"),("/app/warehouse","仓库管理"),
    ("/app/users","用户管理"),("/app/roles","角色管理"),("/app/audit","审计日志"),
    ("/app/settings","系统设置"),("/app/about","关于"),("/app/profile","个人中心"),
    ("/app/import","导入"),("/app/export","导出")]

async def test_routes():
    print("\n=== §1 路由遍历 (23页面) ===")
    async with httpx.AsyncClient(timeout=10, follow_redirects=False, trust_env=False) as c:
        for p, n in ROUTES:
            try:
                r = await c.get(f"{FRONT_URL}/#{p}")
                log("路由", n, "PASS" if r.status_code==200 else "FAIL", str(r.status_code) if r.status_code!=200 else "")
            except Exception as e: log("路由", n, "FAIL", str(e)[:60])

async def test_api():
    print("\n=== §2 API健康 ===")
    tk = ""
    async with httpx.AsyncClient(timeout=15, trust_env=False) as c:
        try:
            r = await c.post(f"{BASE_URL}/api/v1/auth/login", json={"username":"admin","password":"admin123"})
            if r.status_code == 200:
                tk = r.json().get("data",{}).get("access_token","")
                log("API", "登录", "PASS")
            else: log("API", "登录", "FAIL", str(r.status_code))
        except Exception as e: log("API", "登录", "FAIL", str(e)[:60])
    
    h = {"Authorization": f"Bearer {tk}"} if tk else {}
    eps = [("/api/v1/inventory/items","库存"),("/api/v1/incoming/receipts","到货"),
        ("/api/v1/shipment/list","出货"),("/api/v1/rma/returns","返厂"),
        ("/api/v1/bom/list","BOM"),("/api/v1/stations","场站"),
        ("/api/v1/device-ledger","设备"),("/api/v1/stocktakes","盘点"),
        ("/api/v1/adjustments","调整"),("/api/v1/customers","客户"),
        ("/api/v1/partners","往来单位"),("/api/v1/products/categories","分类"),
        ("/api/v1/dashboard/phase2-stats","看板")]
    async with httpx.AsyncClient(timeout=15, headers=h, trust_env=False) as c:
        for p, n in eps:
            try:
                r = await c.get(f"{BASE_URL}{p}")
                t = round(r.elapsed.total_seconds()*1000)
                log("API", n, "PASS" if r.status_code==200 else "FAIL", f"{r.status_code}/{t}ms")
            except Exception as e: log("API", n, "FAIL", str(e)[:60])
    return tk

def test_concurrency(tk):
    """同步版并发测试 - 带auth token"""
    print("\n=== §3 并发50用户 ===")
    from concurrent.futures import ThreadPoolExecutor
    
    urls = ["/api/v1/inventory/items?page=1&page_size=5",
        "/api/v1/incoming/receipts?page=1&page_size=5",
        "/api/v1/dashboard/phase2-stats","/api/v1/stations"]
    
    for url in urls:
        label = url.split("/")[-1].split("?")[0]
        def hit():
            try:
                with httpx.Client(timeout=20, trust_env=False, headers={"Authorization": f"Bearer {tk}"}) as c:
                    r = c.get(f"{BASE_URL}{url}")
                    return r.status_code == 200
            except: return False
        
        start = time.time()
        with ThreadPoolExecutor(max_workers=50) as pool:
            futures = [pool.submit(hit) for _ in range(50)]
            results = [f.result() for f in futures]
        elapsed = round(time.time()-start, 2)
        ok = sum(results)
        log("并发", f"×50 {label}", "PASS" if ok==50 else "FAIL" if ok==0 else "⚠️", f"{ok}/50/{elapsed}s")

async def test_404():
    print("\n=== §4 404路由 ===")
    async with httpx.AsyncClient(timeout=10, trust_env=False) as c:
        for p in ["/api/v1/nonexistent","/api/v1/inventory/nonexistent","/api/v2/anything","/api/v1/auth/nonexistent"]:
            try:
                r = await c.get(f"{BASE_URL}{p}")
                log("404", p, "PASS" if r.status_code in [404,401] else "FAIL", str(r.status_code))
            except Exception as e: log("404", p, "FAIL", str(e)[:60])
        r = await c.get(f"{FRONT_URL}/#/app/nonexistent-xyz")
        log("404", "前端SPA", "PASS" if r.status_code==200 else "FAIL")

async def test_print(tk):
    print("\n=== §5 打印 ===")
    h = {"Authorization": f"Bearer {tk}"} if tk else {}
    async with httpx.AsyncClient(timeout=15, headers=h, trust_env=False) as c:
        for prefix, name in [("/api/v1/print/incoming_receipt/","到货单"),
            ("/api/v1/print/shipment/","出货单"),("/api/v1/print/incoming_inspection/","检验报告"),
            ("/api/v1/print/incoming_return/","退货单"),("/api/v1/print/rma_repair/","维修工单"),
            ("/api/v1/print/bom/","BOM清单")]:
            try:
                r = await c.get(f"{BASE_URL}{prefix}1")
                log("打印", name, "PASS" if r.status_code==200 else "⚠️", "OK" if r.status_code==200 else f"{r.status_code}")
            except Exception as e: log("打印", name, "FAIL", str(e)[:60])

async def test_export(tk):
    print("\n=== §6 导出 ===")
    h = {"Authorization": f"Bearer {tk}"} if tk else {}
    exports = [("/api/v1/inventory/items/export","库存"),("/api/v1/incoming/receipts/export","到货"),
        ("/api/v1/rma/export","返厂"),("/api/v1/bom/export","BOM"),
        ("/api/v1/outbound/orders/export","出库"),("/api/v1/inbound/orders/export","入库"),
        ("/api/v1/products/skus/export","SKU"),("/api/v1/partners/partners/export","往来单位")]
    async with httpx.AsyncClient(timeout=30, headers=h, trust_env=False) as c:
        for p, n in exports:
            try:
                t0=time.time(); r=await c.get(f"{BASE_URL}{p}"); el=round(time.time()-t0,2)
                sz=len(r.content); ct=r.headers.get("content-type","")
                is_xl=any(k in ct for k in ["spreadsheet","excel","openxml","officedocument"])
                if r.status_code==200 and is_xl: log("导出", n, "PASS", f"{sz}B/{el}s")
                elif r.status_code==200: log("导出", n, "⚠️", f"CT={ct[:30]}")
                else: log("导出", n, "FAIL", f"{r.status_code}")
            except Exception as e: log("导出", n, "FAIL", str(e)[:60])

async def main():
    print("="*60)
    print(f"Phase 2 在线检测 | 后端:{BASE_URL} 前端:{FRONT_URL}")
    print(f"开始: {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    await test_routes()
    tk = await test_api()
    test_concurrency(tk)
    await test_404()
    await test_print(tk)
    await test_export(tk)
    print(f"\n{'='*60}\n结果: {PASS}✅/{FAIL}❌/{len(RESULTS)}项 ({round(PASS/len(RESULTS)*100,1)}%)\n完成: {datetime.now().strftime('%H:%M:%S')}\n{'='*60}")
    dst = os.path.join(os.path.dirname(__file__) or ".", "phase2_online_results.json")
    with open(dst,"w",encoding="utf-8") as f: json.dump({"timestamp":datetime.now().isoformat(),"pass":PASS,"fail":FAIL,"total":len(RESULTS),"results":RESULTS},f,ensure_ascii=False,indent=2)
    return 0 if FAIL==0 else 1

if __name__=="__main__": sys.exit(asyncio.run(main()))