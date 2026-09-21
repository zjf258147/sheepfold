"""快速添加 staff 用户到开发数据库。"""
from app.db.database import SessionLocal
from app.models.user import User
from app.models.enums import UserRole
from app.core.security import hash_password

db = SessionLocal()
try:
    existing = db.query(User).filter(User.username == "staff").first()
    if existing:
        print(f"[跳过] staff 用户已存在 (id={existing.id}, role={existing.role})")
    else:
        u = User(
            username="staff",
            password=hash_password("123456"),
            nickname="普通员工",
            role=UserRole.STAFF.value,
            status=1,
        )
        db.add(u)
        db.commit()
        print(f"[OK] staff 用户创建成功 (id={u.id})")
finally:
    db.close()