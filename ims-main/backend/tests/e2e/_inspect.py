"""临时脚本：截图查看登录页DOM"""
import os
from playwright.sync_api import sync_playwright

BASE_URL = "https://localhost:5174"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    page.screenshot(path="/tmp/login_page.png", full_page=True)
    print("截图已保存: /tmp/login_page.png")
    
    inputs = page.locator("input").all()
    for i, inp in enumerate(inputs):
        print(f"  input[{i}]: type={inp.get_attribute('type')}, placeholder={inp.get_attribute('placeholder')}, class={inp.get_attribute('class')}")
    
    buttons = page.locator("button").all()
    for i, btn in enumerate(buttons):
        print(f"  button[{i}]: text='{btn.text_content()}'")
    
    print("\n页面标题:", page.title())
    
    context.close()
    browser.close()