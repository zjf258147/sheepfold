import urllib.request, json

def api(method, path, data=None, token=None):
    url = f'http://localhost:8000{path}'
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

# Login
status, body = api('POST', '/api/v1/auth/login', {'username': 'admin', 'password': 'admin123'})
print('Login:', status, json.dumps(body, indent=2, ensure_ascii=False)[:500])
token = body.get('data', {}).get('access_token')
print('Token:', token[:20] if token else 'NOT FOUND')

# RMA list
status, body = api('GET', '/api/v1/rma/returns', token=token)
print('RMA Status:', status)
if status == 200:
    print('Total:', body['data']['total'])
    for item in body['data']['items']:
        print(' ', item['return_no'], item['sn'])
else:
    print('Error:', body[:500])