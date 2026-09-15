"""第12步：数据迁移 + UAT 测试数据初始化

按真实人员名单创建用户账号。
角色固定，人员可变 —— 人员流动时只增删用户，不改角色。
"""
from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()
try:
    # ── 真实人员列表 ─────────────────────────────────────────────
    # (登录名, 昵称, 角色, 密码)
    users = [
        # ── 管理员（最大权限） ──
        ("admin", "管理员", "ADMIN"),
        ("zwf",   "左文峰", "ADMIN"),
        # ── 生产 ──
        ("yd",    "颜冬",   "PRODUCTION"),
        ("qs",    "乔森",   "PRODUCTION"),
        # ── 质检 ──
        ("lfq",  "吕芳强", "QUALITY"),
        # ── 测试工程师 × 4 ──
        ("lxj",  "刘晓娟", "TEST_ENGINEER"),
        ("hb",   "何奔",   "TEST_ENGINEER"),
        ("zjf",  "赵建飞", "TEST_ENGINEER"),
        ("zlq", "左留启", "TEST_ENGINEER"),
        # ── 仓库管理员 ──
        ("zd",   "赵丹",   "WAREHOUSE"),
        # ── 普通员工（公共账号） ──
        ("qz",   "群众",   "STAFF"),
    ]

    for uname, nick, role in users:
        exists = db.query(User).filter(User.username == uname).first()
        if not exists:
            db.add(User(
                username=uname,
                password=hash_password("12345678"),
                nickname=nick,
                role=role,
                status=1,
            ))
            print(f"  ✅ Created: {uname:6s} ({nick}) -> {role}")
        else:
            print(f"  ⏭️  Exists:  {uname:6s} ({nick}) -> {role}")
    db.commit()
    print(f"\n✅ 用户种子数据完成，共 {len(users)} 个用户")
    print("   💡 初始密码统一为 12345678，首次登录后请修改")
finally:
    db.close()