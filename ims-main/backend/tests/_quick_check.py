import urllib.request, json, sys

def api(path, method='GET', data=None, token=None):
    url = f'http://127.0.0.1:8000/api/v1{path}'
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return 0, str(e).encode()

status, body = api('/auth/login', 'POST', {'username':'admin','password':'admin123'})
token = json.loads(body).get('access_token','')
print(f'Login: {status} token={token[:20]}...')

print('=== Print ===')
for name, path in [('Incoming','/incoming-receipts/1/print'),('Shipment','/shipments/1/print'),('Inspection','/incoming-receipts/1/inspection-print'),('RMA','/rma-returns/1/print'),('Repair','/rma-returns/1/repair-print'),('BOM','/bom/1/print')]:
    s, _ = api(path, token=token)
    print(f'  {"OK" if s==200 else s} {name}')

print('=== Excel ===')
for name, path in [('Inventory','/inventory/export'),('Incoming','/incoming-receipts/export'),('RMA','/rma-returns/export'),('BOM','/bom/export'),('Outbound','/outbound/export'),('Inbound','/inbound/export'),('Products','/products/export'),('Partners','/partners/export')]:
    s, _ = api(path, token=token)
    print(f'  {"OK" if s==200 else s} {name}')