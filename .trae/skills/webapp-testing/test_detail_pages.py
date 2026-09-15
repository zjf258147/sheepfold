import requests

BASE = "http://localhost:8000"
r = requests.post(f"{BASE}/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
token = r.json()["data"]["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Get inbound list to find an ID
# Test inbound detail
r = requests.get(f"{BASE}/api/v1/inbound/orders?page=1&page_size=1", headers=headers)
data = r.json()
print(f"Inbound list status: {r.status_code}")
if data.get("code") == 0 and data.get("data", {}).get("items"):
    first = data["data"]["items"][0]
    item_id = first["id"]
    print(f"First inbound id: {item_id}, order_no: {first.get('order_no')}")
    r2 = requests.get(f"{BASE}/api/v1/inbound/orders/{item_id}", headers=headers)
    print(f"Inbound detail (id) status: {r2.status_code}")
    if r2.status_code != 200:
        r3 = requests.get(f"{BASE}/api/v1/inbound/orders/{first.get('order_no')}", headers=headers)
        print(f"Inbound detail (order_no) status: {r3.status_code}")
else:
    print(f"Inbound list empty or error: {data}")

# Test outbound detail
r = requests.get(f"{BASE}/api/v1/outbound/orders?page=1&page_size=1", headers=headers)
data = r.json()
print(f"\nOutbound list status: {r.status_code}")
if data.get("code") == 0 and data.get("data", {}).get("items"):
    first = data["data"]["items"][0]
    item_id = first["id"]
    print(f"First outbound id: {item_id}, order_no: {first.get('order_no')}")
    r2 = requests.get(f"{BASE}/api/v1/outbound/orders/{item_id}", headers=headers)
    print(f"Outbound detail (id) status: {r2.status_code}")
    if r2.status_code != 200:
        r3 = requests.get(f"{BASE}/api/v1/outbound/orders/{first.get('order_no')}", headers=headers)
        print(f"Outbound detail (order_no) status: {r3.status_code}")
else:
    print(f"Outbound list empty or error: {data}")

# Test other dynamic detail pages (using correct API paths)
# Check API paths from router.py for each module
other_tests = [
    ("/api/v1/inventory/items?page=1&page_size=1", "/api/v1/inventory/items/{}", "inventory-detail"),
]

for list_url, detail_template, name in other_tests:
    r = requests.get(f"{BASE}{list_url}", headers=headers)
    data = r.json()
    print(f"\n{name} list status: {r.status_code}")
    if data.get("code") == 0 and data.get("data", {}).get("items"):
        first = data["data"]["items"][0]
        item_id = str(first.get("id"))
        r2 = requests.get(f"{BASE}{detail_template.format(item_id)}", headers=headers)
        print(f"{name} detail status: {r2.status_code}")
        if r2.status_code == 500:
            print(f"  ⚠️ 500 ERROR: {r2.text[:200]}")
    else:
        print(f"{name} list empty or error: {data}")