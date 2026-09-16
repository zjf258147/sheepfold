"""诊断脚本：检查登录流程哪个环节卡住"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:5176"

p = sync_playwright().start()
browser = p.chromium.launch(headless=True)
context = browser.new_context(ignore_https_errors=True)
page = context.new_page()

# Step 1: 加载登录页
print("1. 加载登录页...")
page.goto(f"{BASE_URL}/login", timeout=30000)
page.wait_for_load_state("networkidle")
page.screenshot(path="e2e_debug_01_login_page.png")
print(f"   页面 URL: {page.url}")
print(f"   页面标题: {page.title()}")

# Step 2: 填写表单
print("2. 填写用户名...")
try:
    page.fill('input[placeholder="用户名"]', "admin")
    print("   OK")
except Exception as e:
    print(f"   失败: {e}")

print("3. 填写密码...")
try:
    page.fill('input[placeholder="密码"]', "admin123")
    print("   OK")
except Exception as e:
    print(f"   失败: {e}")

# Step 3: 截图填写后的状态
page.screenshot(path="e2e_debug_02_filled.png")

# Step 4: 点击登录
print("4. 点击登录按钮...")
try:
    page.click('button:has-text("登 录")')
    print("   OK")
except Exception as e:
    print(f"   失败: {e}")

# Step 5: 等待
page.wait_for_timeout(5000)
page.screenshot(path="e2e_debug_03_after_click.png")
print(f"   当前 URL: {page.url}")
print(f"   页面标题: {page.title()}")

# Step 6: 输出页面文本
try:
    body_text = page.inner_text("body")
    print(f"   页面内容前200字: {body_text[:200]}")
except Exception as e:
    print(f"   获取内容失败: {e}")

# Step 7: 检查 console 错误
print("\n5. Console 消息:")
for msg in page.context.console if hasattr(page.context, 'console') else []:
    print(f"   [{msg.type}] {msg.text}")

context.close()
browser.close()
p.stop()
print("\n诊断完成，截图已保存")