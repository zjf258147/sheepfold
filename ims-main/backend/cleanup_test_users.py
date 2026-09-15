import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='ims', password='ims_pass', database='ims')
cur = conn.cursor()

test_users = ('warehouse','quality','production','test_eng','tester','staff')

# 1. 先删审计日志
cur.execute(
    "DELETE FROM sys_audit_log WHERE operator_id IN (SELECT id FROM sys_user WHERE username IN %s)",
    (test_users,)
)
print(f"Audit logs deleted: {cur.rowcount}")

# 2. 再删用户
cur.execute(
    "DELETE FROM sys_user WHERE username IN %s",
    (test_users,)
)
print(f"Users deleted: {cur.rowcount}")

conn.commit()
conn.close()
print("Done")