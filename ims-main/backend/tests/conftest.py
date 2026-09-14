"""
共享测试 fixture：使用 SQLite 内存数据库隔离测试。
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import BigInteger, create_engine, event, Integer
from sqlalchemy.orm import sessionmaker, Session

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.base import Base
from app.db.database import get_db
from app.core.security import create_access_token

# 确保所有模型在 create_all 之前注册到 Base.metadata
import app.models  # noqa: F401
import app.models.incoming  # noqa: F401
import app.models.raw_material  # noqa: F401


SQLITE_URL = "sqlite:///file::memory:?cache=shared&uri=true"


@pytest.fixture(scope="session")
def engine():
    """创建 SQLite 内存引擎，session 级别复用。"""
    eng = create_engine(SQLITE_URL, connect_args={"check_same_thread": False}, echo=False)

    @event.listens_for(eng, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return eng


@pytest.fixture(scope="session")
def tables(engine):
    """创建所有表。SQLite 不支持 BigInteger autoincrement，建表前转换主键类型。"""
    for table in Base.metadata.tables.values():
        for col in table.columns:
            if isinstance(col.type, BigInteger) and col.primary_key:
                col.type = Integer()

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(engine, tables):
    """每个测试函数独立的数据库会话，测试结束后回滚。"""
    connection = engine.connect()
    transaction = connection.begin()
    TestSession = sessionmaker(bind=connection, autocommit=False, autoflush=False)
    session = TestSession()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        if trans.nested and not trans._parent.nested:
            sess.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Session):
    """FastAPI TestClient，注入测试数据库会话。"""

    from main import create_app

    app = create_app()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, raise_server_exceptions=False) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def seed_data(db_session: Session):
    """插入基础种子数据：用户、分类、SKU、供应商、分组。"""
    from tests.seed_data import create_all_seed_data

    return create_all_seed_data(db_session)


@pytest.fixture
def admin_token(seed_data):
    """生成管理员 JWT Token。"""
    return create_access_token({"user_id": seed_data["admin"].id, "username": "admin"})


@pytest.fixture
def warehouse_token(seed_data):
    """生成仓库管理员 JWT Token。"""
    return create_access_token({"user_id": seed_data["warehouse"].id, "username": "warehouse"})


@pytest.fixture
def auth_headers(admin_token):
    """带管理员 Token 的请求头。"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def auth_headers_warehouse(warehouse_token):
    """带仓库管理员 Token 的请求头。"""
    return {"Authorization": f"Bearer {warehouse_token}"}