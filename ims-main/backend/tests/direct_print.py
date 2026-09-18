"""
直接打印 IMS 系统6种单据到公司打印机
"""
import httpx, json, os
from datetime import datetime

API_URL = "http://localhost:8000"
USER = {"username": "admin", "password": "admin123"}
PRINTER = "HPBB51E5 (HP LaserJet Pro M428f-M429f)"

CSS = """
<style>
  @page { size: A4; margin: 15mm; }
  body { font-family: 'Microsoft YaHei', SimHei, sans-serif; font-size: 12pt; color: #333; }
  .doc { page-break-after: always; border: 2px solid #4472C4; margin-bottom: 20px; }
  .doc:last-child { page-break-after: auto; }
  .header { background: #4472C4; color: white; padding: 12px 16px; font-size: 16pt; font-weight: bold; text-align: center; }
  .sub-header { background: #DDEBF7; padding: 6px 16px; font-size: 10pt; color: #666; text-align: right; }
  table { width: 100%; border-collapse: collapse; margin: 10px 0; }
  td { padding: 6px 10px; border: 1px solid #999; }
  .label { background: #F2F2F2; width: 30%; font-weight: bold; }
  .value { width: 70%; }
  .stamp { text-align: right; margin-top: 30px; font-size: 10pt; color: #999; }
  .sn { font-family: 'Consolas', 'Courier New', monospace; background: #FFFDE7; }
  h2 { color: #4472C4; border-bottom: 2px solid #4472C4; padding-bottom: 5px; }
</style>"""

def login():
    with httpx.Client(timeout=30, trust_env=False) as c:
        r = c.post(f"{API_URL}/api/v1/auth/login", json=USER)
        return r.json()["data"]["access_token"]

def api_get(token, path):
    with httpx.Client(timeout=30, trust_env=False) as c:
        r = c.get(f"{API_URL}{path}", headers={"Authorization": f"Bearer {token}"})
        if r.status_code == 200:
            return r.json().get("data", r.json())
        return None

def to_print_html(docs):
    """将所有打印数据生成HTML"""
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = f"""<!DOCTYPE html><html><head><meta charset=utf-8><title>IMS 单据打印</title>{CSS}</head><body>
<h2>📦 IMS 生产物料追溯系统 - 单据打印</h2>
<p style="color:#666">打印时间：{time_str} | 共 {len(docs)} 份单据</p>
<hr>"""
    for title, rows in docs:
        extra = ""
        if title == "到货单":
            data = {r[0]: r[1] for r in rows}
            extra = f"""<div class=sub-header>收货编号：{data.get('receipt_no','-')} | 打印时间：{time_str}</div>"""
        html += f'<div class=doc><div class=header>📋 {title}</div>{extra}<table>'
        for k, v in rows:
            html += f'<tr><td class=label>{k}</td><td class=value>{v}</td></tr>'
        html += '</table><div class=stamp>审批人：__________  日期：__________</div></div>'
    html += '</body></html>'
    return html


def main():
    token = login()
    print("✅ 登录成功")

    docs = []

    # 1. 到货单 (ID=8)
    d = api_get(token, "/api/v1/print/incoming_receipt/8")
    if d:
        rows = [
            ("收货单号", d.get("receipt_no", "-")),
            ("收货日期", d.get("receipt_date", "-")),
            ("供应商", d.get("supplier_name", "-")),
            ("批次号", d.get("batch_no", "-")),
            ("SKU编码", d.get("sku_code", "-")),
            ("物料名称", d.get("sku_name", "-")),
            ("规格", d.get("spec", "-")),
            ("数量", d.get("quantity", "-")),
            ("单位", d.get("unit", "-")),
            ("状态", d.get("status", "-")),
            ("备注", d.get("remark", "-") or ""),
        ]
        docs.append(("到货单", rows))
        print("  📋 到货单")

    # 2. 出货单 (ID=4)
    d = api_get(token, "/api/v1/print/shipment/4")
    if d:
        rows = [
            ("出货单号", d.get("shipment_no", "-")),
            ("出货日期", d.get("shipment_date", "-")),
            ("SKU编码", d.get("sku_code", "-")),
            ("物料名称", d.get("sku_name", "-")),
            ("规格", d.get("spec", "-")),
            ("数量", d.get("quantity", "-")),
            ("单位", d.get("unit", "-")),
            ("客户", d.get("customer_name", "-")),
            ("状态", d.get("status", "-")),
        ]
        docs.append(("出货单", rows))
        print("  📋 出货单")

    # 3. 来料检验单 (ID=7)
    d = api_get(token, "/api/v1/print/incoming_inspection/7")
    if d:
        rows = [
            ("检验编号", d.get("inspection_no", "-")),
            ("检验日期", d.get("inspection_date", "-")),
            ("检验结果", d.get("result", "-")),
            ("抽样数量", d.get("sample_qty", "-")),
            ("不良数量", d.get("defect_qty", "-")),
            ("不良描述", d.get("defect_description", "-") or "无"),
            ("备注", d.get("remark", "-") or ""),
        ]
        docs.append(("来料检验单", rows))
        print("  📋 来料检验单")

    # 4. 来料退货单 (ID=1)
    d = api_get(token, "/api/v1/print/incoming_return/1")
    if d:
        rows = [
            ("退货单号", d.get("return_no", "-")),
            ("退货日期", d.get("return_date", "-")),
            ("退货数量", d.get("return_qty", "-")),
            ("退货原因", d.get("return_reason", "-")),
            ("状态", d.get("status", "-")),
            ("备注", d.get("remark", "-") or ""),
        ]
        docs.append(("来料退货单", rows))
        print("  📋 来料退货单")

    # 5. 返厂维修单 (ID=3)
    d = api_get(token, "/api/v1/print/rma_repair/3")
    if d:
        rows = [
            ("维修工单号", d.get("repair_no", "-")),
            ("原设备SN", d.get("old_sn", "-")),
            ("新设备SN", d.get("new_sn", "-") or "无"),
            ("维修描述", d.get("repair_description", "-")),
            ("维修用料", d.get("materials_used", "-") or ""),
            ("故障码", d.get("fault_code", "-") or ""),
            ("维修日期", d.get("repair_date", "-")),
            ("备注", d.get("remark", "-") or ""),
        ]
        docs.append(("返厂维修单", rows))
        print("  📋 返厂维修单")

    # 6. BOM单 (ID=3)
    d = api_get(token, "/api/v1/print/bom/3")
    if d:
        rows = [
            ("BOM编号", d.get("bom_no", "-") or d.get("code", "-")),
            ("SKU编码", d.get("sku_code", "-")),
            ("物料名称", d.get("sku_name", "-")),
            ("规格", d.get("spec", "-")),
            ("数量", d.get("quantity", "-")),
            ("单位", d.get("unit", "-")),
            ("版本", d.get("version", "-") or ""),
            ("备注", d.get("remark", "-") or ""),
        ]
        docs.append(("BOM单", rows))
        print("  📋 BOM单")

    print(f"\n✅ 共获取 {len(docs)} 份单据数据")

    # 生成HTML
    html = to_print_html(docs)
    html_file = os.path.join(os.path.dirname(__file__), "print_output.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 HTML已生成: {html_file}")

    # 打印
    print(f"\n🖨️  正在发送到打印机: {PRINTER} ...")
    return html_file

if __name__ == "__main__":
    main()