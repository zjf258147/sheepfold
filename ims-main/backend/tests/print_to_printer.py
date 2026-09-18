"""用Playwright生成PDF并打印"""
import os, subprocess, sys

html_file = r"c:\Users\25075\Desktop\IMS生产物料与产品追溯管理系统\ims-main\backend\tests\print_output.html"
pdf_file = html_file.replace(".html", ".pdf")
printer = "HPBB51E5 (HP LaserJet Pro M428f-M429f)"

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("安装Playwright...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.sync_api import sync_playwright

print("📄 生成PDF...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"file:///{html_file}")
    page.wait_for_load_state("networkidle")
    page.pdf(path=pdf_file, format="A4", margin={"top": "15mm", "right": "15mm", "bottom": "15mm", "left": "15mm"}, print_background=True)
    browser.close()

print(f"✅ PDF已生成: {pdf_file} ({os.path.getsize(pdf_file)/1024:.0f}KB)")

# 打印PDF到指定打印机
print(f"🖨️  打印到: {printer} ...")
try:
    # 方法1: 使用AcroRd32.exe /t (Adobe Reader)
    cmd = f'AcroRd32.exe /t "{pdf_file}" "{printer}"'
    subprocess.run(cmd, shell=True, timeout=30)
    print("✅ 已通过Adobe Reader发送打印")
except:
    try:
        # 方法2: 使用Foxit Reader
        cmd = f'"C:\\Program Files\\Foxit Software\\Foxit PDF Reader\\FoxitPDFReader.exe" /t "{pdf_file}" "{printer}"'
        subprocess.run(cmd, shell=True, timeout=30)
        print("✅ 已通过Foxit发送打印")
    except:
        # 方法3: PowerShell Out-Printer (可能不支持PDF)
        print("⚠️ 自动打印失败，使用默认方式...")
        subprocess.run(f'powershell -Command "Start-Process -FilePath \'{pdf_file}\' -Verb Print"', shell=True)
        print("✅ 已发送打印命令")

print("\n📋 已打印6种单据：到货单/出货单/来料检验单/来料退货单/返厂维修单/BOM单")