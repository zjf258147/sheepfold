import requests

BASE = "http://localhost:8000"
r = requests.post(f"{BASE}/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
token = r.json()["data"]["access_token"]
h = {"Authorization": f"Bearer {token}"}

checks = [
    ("Shipment", f"{BASE}/api/v1/shipment/list"),
    ("Dashboard", f"{BASE}/api/v1/dashboard"),
    ("BOM Detail", f"{BASE}/api/v1/bom/1"),
    ("Incoming", f"{BASE}/api/v1/incoming/receipts"),
    ("RMA", f"{BASE}/api/v1/rma/returns"),
    ("Inventory", f"{BASE}/api/v1/inventory/items"),
    ("Inbound", f"{BASE}/api/v1/inbound/orders"),
    ("Outbound", f"{BASE}/api/v1/outbound/orders"),
    ("Product SKU", f"{BASE}/api/v1/products/skus"),
]

for name, url in checks:
    r2 = requests.get(url, headers=h)
    if r2.status_code == 200:
        j = r2.json()
        d = j.get("data", j)
        if isinstance(d, dict):
            total = d.get("total", "?")
        elif isinstance(d, list):
            total = len(d)
        else:
            total = "?"
        print(f"  [OK] {name}: {r2.status_code} total={total}")
    else:
        print(f"  [{r2.status_code}] {name}")

print("All checks done!")