"""诊断脚本：详细检查登录API调用"""
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:5176"

p = sync_playwright().start()
browser = p.chromium.launch(headless=True)
context = browser.new_context(ignore_https_errors=True)
page = context.new_page()

# 拦截所有请求
requests = []
def on_request(request):
    requests.append(f">>> {request.method} {request.url}")
def on_response(response):
    requests.append(f"<<< {response.status} {response.url}")

page.on("request", on_request)
page.on("response", on_response)

# 加载登录页
print("加载登录页...")
page.goto(f"{BASE_URL}/login", timeout=30000)
page.wait_for_load_state("networkidle")

# 填写并点击
page.fill('input[placeholder="用户名"]', "admin")
page.fill('input[placeholder="密码"]', "admin123")

# 监听 console
page.on("console", lambda msg: print(f"  CONSOLE [{msg.type}]: {msg.text}"))

print("点击登录...")
page.click('button:has-text("登 录")')

# 等待足够时间
page.wait_for_timeout(8000)

print(f"\n当前 URL: {page.url}")
print(f"页面标题: {page.title()}")

# 查看页面是否有错误消息
try:
    el_msg = page.query_selector(".el-message")
    if el_msg:
        print(f"消息提示: {el_msg.inner_text()}")
except:
    pass

# 检查 alert/dialog
try:
    dialog_text = page.evaluate("""() => {
        const msgs = document.querySelectorAll('.el-message__content');
        return Array.from(msgs).map(m => m.textContent).join(' | ');
    }""")
    if dialog_text:
        print(f"Element消息: {dialog_text}")
except:
    pass

# 显示相关请求
print("\n--- API 请求 ---")
for r in requests:
    if "/api/" in r or "/login" in r:
        print(r)

context.close()
browser.close()
p.stop()