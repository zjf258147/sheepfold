"""第12步 UAT全流程测试"""
from playwright.sync_api import sync_playwright
import requests
import json

BASE = 'http://localhost:5173'
API = 'http://localhost:8000/api/v1'
results = []

def check(name, condition):
    results.append((name, 'PASS' if condition else 'FAIL'))
    print(f"   {'PASS' if condition else 'FAIL'}: {name}")

# 预创建测试用户
def create_test_users():
    try:
        login_resp = requests.post(f'{API}/auth/login',
            json={'username': 'admin', 'password': 'admin123'}, timeout=5)
        if login_resp.status_code != 200:
            return
        token = login_resp.json().get('data', {}).get('access_token', '')
        if not token:
            return
        headers = {'Authorization': f'Bearer {token}'}
        for username, role in [('warehouse', 'WAREHOUSE'), ('quality', 'QUALITY'),
                                ('production', 'PRODUCTION'), ('tester', 'TEST_ENGINEER'),
                                ('staff', 'STAFF')]:
            requests.post(f'{API}/users', json={
                'username': username, 'password': '12345678',
                'nickname': username, 'role': role
            }, headers=headers, timeout=5)
    except Exception:
        pass

create_test_users()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on('pageerror', lambda err: print(f'  JS ERROR: {err}'))

    def login(u, p='12345678'):
        page.goto(f'{BASE}/')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        # 如果已登录，先登出
        if 'login' not in page.url.lower():
            # 点击右上角下拉菜单登出
            try:
                el = page.query_selector('.el-dropdown')
                if el:
                    el.click()
                    page.wait_for_timeout(500)
                    logout_btn = page.query_selector('text=退出登录')
                    if logout_btn:
                        logout_btn.click()
                        page.wait_for_timeout(1500)
            except:
                pass
            # 清除 localStorage
            page.evaluate('() => localStorage.clear()')
            page.goto(f'{BASE}/')
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)

        if 'login' in page.url.lower():
            page.fill('input[placeholder="用户名"]', u)
            page.fill('input[placeholder="密码"]', p)
            page.click('button span:has-text("登")')
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(3000)

    # ========== 1. 登录 + 权限验证 ==========
    print("\n=== 1. 多角色登录测试 ===")
    login('admin', 'admin123')
    check('admin 登录成功', 'dashboard' in page.url.lower() or '首页' in page.content())
    page.goto(f'{BASE}/bom')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    check('admin 可见创建BOM', '创建BOM' in page.content())

    login('warehouse')
    check('warehouse 登录成功', 'dashboard' in page.url.lower() or '首页' in page.content())
    page.goto(f'{BASE}/bom')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    check('warehouse 可见创建BOM', '创建BOM' in page.content())
    page.goto(f'{BASE}/settings')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    check('warehouse 不可见系统设置', 'dashboard' in page.url.lower())

    login('quality')
    check('quality 登录成功', 'dashboard' in page.url.lower() or '首页' in page.content())
    page.goto(f'{BASE}/bom')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    check('quality 不可见创建BOM', '创建BOM' not in page.content())

    login('production')
    check('production 登录成功', 'dashboard' in page.url.lower() or '首页' in page.content())
    page.goto(f'{BASE}/bom')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    check('production 可见创建BOM', '创建BOM' in page.content())

    login('tester')
    check('tester 登录成功', 'dashboard' in page.url.lower() or '首页' in page.content())
    menu_html = page.query_selector('.el-menu')
    menu_text = menu_html.inner_text() if menu_html else ''
    check('tester 不可见BOM菜单', 'BOM管理' not in menu_text and 'BOM' not in menu_text.split('\n'))

    login('staff')
    check('staff 登录成功', 'dashboard' in page.url.lower() or '首页' in page.content())
    # 检查侧边栏菜单（.el-menu），而非整个页面（dashboard 含"待审核入库单"）
    menu_html = page.query_selector('.el-menu')
    menu_text = menu_html.inner_text() if menu_html else ''
    check('staff 不可见BOM菜单', 'BOM管理' not in menu_text and 'BOM' not in menu_text.split('\n'))
    check('staff 不可见入库菜单', '入库' not in menu_text)

    # ========== 2. 页面导航测试 ==========
    print("\n=== 2. 页面导航测试 ===")
    login('admin', 'admin123')
    pages = [
        ('/dashboard', '首页'),
        ('/inventory', '实时库存'),
        ('/inventory/sku', 'SKU'),
        ('/inbound', '入库'),
        ('/incoming', '来料管理'),
        ('/rma', '返厂维修'),
        ('/shipment', '出货管理'),
        ('/bom', 'BOM管理'),
        ('/production-task', '生产任务'),
        ('/outbound', '出库'),
        ('/products', '商品SKU'),
        ('/partners', '往来单位'),
        ('/snapshot', '库存流水'),
        ('/settings', '系统设置'),
    ]
    for path, label in pages:
        page.goto(f'{BASE}{path}', timeout=15000)
        try:
            page.wait_for_load_state('networkidle', timeout=10000)
        except:
            pass
        page.wait_for_timeout(1000)
        check(f'页面 {path}', 'error' not in page.url.lower() and page.content() != '')

    # ========== 3. 主线A 来料管理测试 ==========
    print("\n=== 3. 主线A：来料管理 ===")
    page.goto(f'{BASE}/incoming')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    html = page.content()
    check('来料页面加载', '到货' in html or '来料' in html or 'incoming' in html.lower())

    # ========== 4. 主线B 返厂维修测试 ==========
    print("\n=== 4. 主线B：返厂维修 ===")
    page.goto(f'{BASE}/rma')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    html = page.content()
    check('返厂维修页面加载', 'SN' in html or '返厂' in html or 'rma' in html.lower())

    # ========== 5. 主线C 出货管理测试 ==========
    print("\n=== 5. 主线C：出货管理 ===")
    page.goto(f'{BASE}/shipment')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    html = page.content()
    check('出货管理页面加载', '出货' in html or 'shipment' in html.lower())

    # ========== 6. 主线D BOM管理测试 ==========
    print("\n=== 6. 主线D：BOM管理 ===")
    page.goto(f'{BASE}/bom')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)
    html = page.content()
    check('BOM搜索框', 'BOM编号' in html)
    check('BOM创建按钮', '创建BOM' in html)
    check('BOM导出按钮', '导出CSV' in html or '导出' in html)

    # Test BOM create dialog
    page.click('button:has-text("创建BOM")')
    page.wait_for_timeout(1000)
    html = page.content()
    check('BOM对话框打开', 'BOM名称' in html)
    check('BOM明细表', 'BOM明细' in html)
    check('添加物料按钮', '添加物料' in html)
    page.click('button:has-text("取消")')
    page.wait_for_timeout(500)

    # ========== 7. API健康检查 ==========
    print("\n=== 7. API健康检查 ===")
    import requests
    try:
        r = requests.get('http://localhost:8000/health', timeout=5)
        check('后端健康检查', r.status_code == 200)
    except Exception as e:
        check(f'后端健康检查 {e}', False)

    try:
        r = requests.get('http://localhost:8000/docs', timeout=5)
        check('Swagger文档可访问', r.status_code == 200)
    except Exception as e:
        check(f'Swagger文档 {e}', False)

    # ========== 汇总 ==========
    print("\n" + "=" * 50)
    passed = sum(1 for _, r in results if r == 'PASS')
    failed = sum(1 for _, r in results if r == 'FAIL')
    print(f"  UAT 测试结果: {passed}/{passed+failed} 通过, {failed} 失败")
    for name, result in results:
        if result == 'FAIL':
            print(f"    FAIL: {name}")
    print("=" * 50)

    browser.close()