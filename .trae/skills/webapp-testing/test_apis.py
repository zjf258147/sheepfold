import requests
import json
import urllib3
urllib3.disable_warnings()

BASE = "http://localhost:8000"

# Login
r = requests.post(f"{BASE}/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
token = r.json().get("data", {}).get("access_token", "")
headers = {"Authorization": f"Bearer {token}"}

# Test failing APIs
apis = [
    ("customers", "/api/v1/customers?page=1&page_size=15"),
    ("inventory/items", "/api/v1/inventory/items?page=1&page_size=15"),
    ("production-task/list", "/api/v1/production-task/list?page=1&page_size=15"),
    ("snapshots/items", "/api/v1/snapshots/items?snapshot_date=2026-09-07&page=1&page_size=15"),
    ("customers (large)", "/api/v1/customers?page_size=1000"),
]

for name, path in apis:
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {BASE}{path}")
    r = requests.get(f"{BASE}{path}", headers=headers)
    print(f"Status: {r.status_code}")
    try:
        detail = r.json()
        print(f"Response: {json.dumps(detail, indent=2, ensure_ascii=False)[:2000]}")
    except:
        print(f"Response: {r.text[:1000]}")