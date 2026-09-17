"""
种子数据脚本: 为打印测试创建来料检验单和返厂维修单数据
"""
import httpx
from datetime import date, datetime

API_URL = "http://localhost:8000"
USER = {"username": "admin", "password": "admin123"}


def login():
    with httpx.Client(timeout=30, trust_env=False) as c:
        r = c.post(f"{API_URL}/api/v1/auth/login", json=USER)
        if r.status_code != 200:
            raise Exception(f"登录失败: {r.status_code} {r.text[:200]}")
        return r.json()["data"]["access_token"]


def api_post(token, path, data):
    with httpx.Client(timeout=30, trust_env=False) as c:
        r = c.post(
            f"{API_URL}{path}",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        return r


def api_get(token, path, params=None):
    with httpx.Client(timeout=30, trust_env=False) as c:
        r = c.get(
            f"{API_URL}{path}",
            headers={"Authorization": f"Bearer {token}"},
            params=params or {},
        )
        return r


def get_first(token, path, key="items"):
    r = api_get(token, path, {"page": 1, "page_size": 1})
    if r.status_code == 200:
        data = r.json().get("data", r.json())
        items = data.get(key, []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        if items:
            return items[0]
    return None


def main():
    token = login()
    print("🔑 登录成功")

    # ============================================================
    # 1. 来料检验单 (需要 receipt_id + inspector_id)
    # ============================================================
    print("\n📋 创建来料检验单...")
    receipt = get_first(token, "/api/v1/incoming/receipts")
    if not receipt:
        print("  ❌ 无到货单，跳过")
        inspection_id = None
    else:
        rid = receipt["id"]
        print(f"  到货单 ID={rid}, 状态={receipt.get('status')}")

        r = api_post(token, "/api/v1/incoming/inspections", {
            "receipt_id": rid,
            "inspector_id": 1,
            "inspection_date": str(date.today()),
            "result": "ACCEPTED",
            "sample_qty": 10,
            "defect_qty": 0,
            "defect_description": None,
            "change_reason": "自动化测试-打印验证",
            "remark": "种子数据",
        })
        if r.status_code in (200, 201):
            resp = r.json()
            d = resp.get("data", resp)
            inspection_id = d.get("id")
            print(f"  ✅ 检验单创建成功 ID={inspection_id} 单号={d.get('inspection_no', d.get('data', {}).get('inspection_no', '?'))}")
        else:
            print(f"  ❌ 创建失败 HTTP {r.status_code}: {r.text[:200]}")
            inspection_id = None

    # ============================================================
    # 2. 返厂维修单 (需要: RMA退货->分配->诊断->维修)
    # ============================================================
    print("\n📋 创建返厂维修单...")

    # 2a. 获取SKU
    skus = get_first(token, "/api/v1/products/skus")
    if not skus:
        print("  ❌ 无SKU数据")
        return
    sku_id = skus["id"]
    sku_code = skus.get("sku_code", "?")
    print(f"  SKU: id={sku_id} code={sku_code}")

    # 2b. 查找现有RMA退货单
    existing_rma = get_first(token, "/api/v1/rma/returns", "returns")
    rma_return = None
    if existing_rma:
        # 直接用现有的
        rma_return = existing_rma
        print(f"  复用现有RMA退货单 ID={rma_return['id']} 状态={rma_return.get('status')}")
    else:
        # 创建新的RMA退货单
        print("  创建新RMA退货单...")
        r = api_post(token, "/api/v1/rma/returns", {
            "sku_id": sku_id,
            "sn": f"TEST-SN-{datetime.now().strftime('%H%M%S')}",
            "quantity": 1,
            "unit": "个",
            "customer_name": "测试客户",
            "return_reason": "自动化测试-打印验证",
            "return_date": str(date.today()),
            "remark": "种子数据",
        })
        if r.status_code in (200, 201):
            resp = r.json()
            rma_return = resp.get("data", resp)
            print(f"  ✅ RMA退货单创建成功 ID={rma_return.get('id')} 单号={rma_return.get('return_no', '?')}")
        else:
            print(f"  ❌ 创建RMA退货单失败 HTTP {r.status_code}: {r.text[:200]}")
            return

    return_id = rma_return["id"]
    status = rma_return.get("status", "")

    # 2c. 先诊断（PENDING_DIAGNOSIS → DIAGNOSED）
    if status in ("PENDING_DIAGNOSIS",):
        print("  先创建诊断...")
        r = api_post(token, "/api/v1/rma/diagnoses", {
            "return_id": return_id,
            "diagnosed_by": 1,
            "diagnosis_date": str(date.today()),
            "fault_description": "测试故障：电源模块异常",
            "diagnosis_result": "REPAIRABLE",
            "change_reason": "自动化测试-打印验证",
            "remark": "种子数据",
        })
        if r.status_code in (200, 201):
            resp = r.json()
            d = resp.get("data", resp)
            print(f"  ✅ 诊断创建成功 ID={d.get('id')}")
        else:
            print(f"  ⚠️ 诊断创建失败 (可能已存在): HTTP {r.status_code}")

    # 2d. 再分配（DIAGNOSED → ASSIGNED）
    print("  再分配...")
    r = api_post(token, f"/api/v1/rma/returns/{return_id}/assign", {
        "assigned_to": 1,
        "assign_type": "PRODUCTION",
        "assign_reason": "自动化测试",
        "change_reason": "自动化测试-打印验证",
    })
    if r.status_code in (200, 201):
        print(f"  ✅ 分配成功")
    else:
        print(f"  ⚠️ 分配失败 HTTP {r.status_code}: {r.text[:200]}")

    # 2e. 创建维修单（ASSIGNED → REPAIRING）
    print("  创建维修单...")
    r = api_post(token, "/api/v1/rma/repairs", {
        "return_id": return_id,
        "repair_by": 1,
        "old_sn": rma_return.get("sn", "TEST-SN"),
        "repair_description": "测试维修：更换电源模块",
        "materials_used": "电源模块 x1",
        "fault_code": "PWR001",
        "start_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "end_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "repair_date": str(date.today()),
        "change_reason": "自动化测试-打印验证",
        "remark": "种子数据",
    })
    if r.status_code in (200, 201):
        resp = r.json()
        d = resp.get("data", resp)
        print(f"  ✅ 维修单创建成功 ID={d.get('id')} 单号={d.get('repair_no', '?')}")
    else:
        print(f"  ❌ 维修单创建失败 HTTP {r.status_code}: {r.text[:200]}")

    # ============================================================
    # 3. 验证打印
    # ============================================================
    print("\n🔍 验证打印端点...")
    if inspection_id:
        r = api_get(token, f"/api/v1/print/incoming_inspection/{inspection_id}")
        if r.status_code == 200:
            print(f"  ✅ 来料检验单打印 OK (ID={inspection_id})")
        else:
            print(f"  ❌ 来料检验单打印失败: {r.status_code}")

    repairs = get_first(token, f"/api/v1/rma/returns/{return_id}/repairs", "repairs")
    if repairs:
        repair_id = repairs["id"]
        r = api_get(token, f"/api/v1/print/rma_repair/{repair_id}")
        if r.status_code == 200:
            print(f"  ✅ 返厂维修单打印 OK (ID={repair_id})")
        else:
            print(f"  ❌ 返厂维修单打印失败: {r.status_code}")
    else:
        print("  ⚠️ 找不到维修单ID")

    print("\n✅ 种子数据创建完成！")


if __name__ == "__main__":
    main()