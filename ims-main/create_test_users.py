"""创建测试用户"""
import requests
BASE = 'http://localhost:8000/api/v1'

# First login as admin to get token
login_resp = requests.post(f'{BASE}/auth/login',
    json={'username': 'admin', 'password': 'admin123'})
print('Admin login:', login_resp.status_code)
data = login_resp.json()
token = data.get('data', {}).get('access_token', '')
print('Token:', token[:20] + '...' if token else 'NONE')

headers = {'Authorization': f'Bearer {token}'}

# Create missing users
users_to_create = [
    ('warehouse', '仓库管理员', 'WAREHOUSE'),
    ('quality', '质检员', 'QUALITY'),
    ('production', '生产管理员', 'PRODUCTION'),
    ('tester', '测试员', 'TEST_ENGINEER'),
    ('staff', '普通员工', 'STAFF'),
]

for username, nickname, role in users_to_create:
    r = requests.post(f'{BASE}/users', json={
        'username': username,
        'password': '12345678',
        'nickname': nickname,
        'role': role
    }, headers=headers)
    msg = r.json().get('msg', r.json().get('message', str(r.status_code)))
    print(f'Create {username}: {r.status_code} - {msg}')