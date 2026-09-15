import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='ims', password='ims_pass', database='ims')
cursor = conn.cursor()

tables = ['customer', 'inventory_item', 'inventory_item_snapshot', 'production_task']
for t in tables:
    cursor.execute(f"SHOW COLUMNS FROM {t}")
    cols = [row[0] for row in cursor.fetchall()]
    print(f"\n{t} ({len(cols)} cols):")
    for c in cols:
        print(f"  - {c}")

conn.close()