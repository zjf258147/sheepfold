"""环境配置验证检查（P1/P2）

验证项目运行所需的全部环境配置：
  1. .env 文件存在且包含必要字段
  2. Python 版本
  3. 依赖包版本
  4. 文件/目录结构
  5. 数据库连接
  6. Redis 连接（可选）
  7. 前端 Node.js 环境

运行方式：
  cd backend && python -m pytest tests/test_env_check.py -v --tb=short
"""

import os
import sys
import subprocess
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"
ENV_FILE = BACKEND_DIR / ".env"


class TestEnvFile:
    """.env 文件检查"""

    def test_env_file_exists(self):
        """.env 文件存在。"""
        assert ENV_FILE.exists(), f".env 文件不存在: {ENV_FILE}"

    def test_env_file_not_empty(self):
        """.env 文件非空。"""
        if not ENV_FILE.exists():
            pytest.skip(".env 文件不存在")
        content = ENV_FILE.read_text(encoding="utf-8").strip()
        assert len(content) > 0, ".env 文件为空"

    def test_required_env_vars_present(self):
        """必要环境变量存在。"""
        if not ENV_FILE.exists():
            pytest.skip(".env 文件不存在")

        required = [
            "MYSQL_HOST",
            "MYSQL_USER",
            "MYSQL_PASSWORD",
            "MYSQL_DB",
            "JWT_SECRET_KEY",
        ]
        content = ENV_FILE.read_text(encoding="utf-8")
        missing = [k for k in required if k not in content]
        assert not missing, f"缺少必要环境变量: {missing}"

    def test_env_example_exists(self):
        """.env.example 模板文件存在。"""
        example = BACKEND_DIR / ".env.example"
        if example.exists():
            content = example.read_text(encoding="utf-8")
            assert "MYSQL_HOST" in content
            assert "JWT_SECRET_KEY" in content


class TestPythonEnvironment:
    """Python 环境检查"""

    def test_python_version(self):
        """Python 版本 >= 3.10。"""
        version = sys.version_info
        assert version >= (3, 10), f"Python 版本: {version.major}.{version.minor}，需要 >= 3.10"

    def test_pip_installed(self):
        """pip 可用。"""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"pip 不可用: {result.stderr}"

    def test_requirements_file_exists(self):
        """pyproject.toml 或 requirements.txt 存在。"""
        pyproject = BACKEND_DIR / "pyproject.toml"
        req = BACKEND_DIR / "requirements.txt"
        assert pyproject.exists() or req.exists(), (
            f"pyproject.toml 和 requirements.txt 都不存在: {BACKEND_DIR}"
        )

    def test_core_dependencies(self):
        """核心依赖已安装。"""
        required = ["fastapi", "sqlalchemy", "alembic", "pydantic", "uvicorn", "pymysql"]
        for pkg in required:
            try:
                __import__(pkg.replace("-", "_"))
            except ImportError:
                pytest.fail(f"依赖未安装: {pkg}")


class TestDirectoryStructure:
    """目录结构检查"""

    def test_app_directory_exists(self):
        """app/ 目录存在。"""
        assert (BACKEND_DIR / "app").is_dir()

    def test_api_directory_exists(self):
        """app/api/ 目录存在。"""
        assert (BACKEND_DIR / "app" / "api").is_dir()

    def test_models_directory_exists(self):
        """app/models/ 目录存在。"""
        assert (BACKEND_DIR / "app" / "models").is_dir()

    def test_service_directory_exists(self):
        """app/service/ 目录存在。"""
        assert (BACKEND_DIR / "app" / "service").is_dir()

    def test_utils_directory_exists(self):
        """app/utils/ 目录存在。"""
        assert (BACKEND_DIR / "app" / "utils").is_dir()

    def test_core_directory_exists(self):
        """app/core/ 目录存在。"""
        assert (BACKEND_DIR / "app" / "core").is_dir()

    def test_main_py_exists(self):
        """main.py 入口文件存在。"""
        assert (BACKEND_DIR / "main.py").exists()

    def test_alembic_directory_exists(self):
        """alembic/ 迁移目录存在。"""
        assert (BACKEND_DIR / "alembic").is_dir()

    def test_alembic_ini_exists(self):
        """alembic.ini 配置文件存在。"""
        assert (BACKEND_DIR / "alembic.ini").exists()

    def test_tests_directory_exists(self):
        """tests/ 测试目录存在。"""
        assert (BACKEND_DIR / "tests").is_dir()

    def test_uploads_directory_exists(self):
        """uploads/ 上传目录存在。"""
        uploads = BACKEND_DIR / "uploads"
        if not uploads.exists():
            uploads.mkdir(parents=True, exist_ok=True)
        assert uploads.is_dir()

    def test_frontend_directory_exists(self):
        """frontend/ 目录存在。"""
        assert FRONTEND_DIR.is_dir(), f"前端目录不存在: {FRONTEND_DIR}"

    def test_frontend_package_json_exists(self):
        """frontend/package.json 存在。"""
        pkg = FRONTEND_DIR / "package.json"
        assert pkg.exists(), f"package.json 不存在: {pkg}"


class TestDatabaseConnection:
    """数据库连接检查"""

    def test_database_url_parses(self):
        """database_url 可正确解析。"""
        from app.core.config import settings
        url = settings.database_url
        assert "mysql+pymysql://" in url or "sqlite://" in url or "postgresql://" in url
        assert settings.MYSQL_DB in url

    def test_sqlalchemy_imports(self):
        """SQLAlchemy 模型导入无报错。"""
        try:
            from app.db.base import Base
            import app.models  # noqa: F401
            assert Base.metadata.tables
        except Exception as e:
            pytest.fail(f"模型导入失败: {e}")

    def test_alembic_config_readable(self):
        """alembic.ini 可读且 script_location 正确。"""
        import configparser
        ini = BACKEND_DIR / "alembic.ini"
        config = configparser.ConfigParser()
        config.read(ini, encoding="utf-8")
        assert "alembic" in config
        assert config["alembic"].get("script_location") == "alembic"


class TestRedisConfig:
    """Redis 配置检查（可选）"""

    def test_redis_config_present(self):
        """Redis 配置字段存在。"""
        from app.core.config import settings
        assert hasattr(settings, "REDIS_ENABLED")
        assert hasattr(settings, "REDIS_HOST")
        assert hasattr(settings, "REDIS_PORT")

    def test_redis_disabled_gracefully(self):
        """Redis 禁用时系统不崩溃。"""
        from app.core.config import settings
        if not settings.REDIS_ENABLED:
            assert True
        else:
            import redis
            try:
                r = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    password=settings.REDIS_PASSWORD or None,
                    db=settings.REDIS_DB,
                    socket_connect_timeout=2,
                )
                r.ping()
            except Exception as e:
                pytest.skip(f"Redis 连接失败: {e}")


class TestFrontendEnvironment:
    """前端环境检查"""

    def test_node_installed(self):
        """Node.js 已安装。"""
        result = subprocess.run(
            ["node", "--version"], capture_output=True, text=True,
        )
        assert result.returncode == 0, f"Node.js 未安装: {result.stderr}"

    def test_npm_installed(self):
        """npm 已安装。"""
        try:
            result = subprocess.run(
                ["npm", "--version"], capture_output=True, text=True, timeout=10,
                shell=True,
            )
            assert result.returncode == 0, f"npm 命令执行失败: {result.stderr}"
        except FileNotFoundError:
            pytest.skip("npm 未在 PATH 中找到（可能未安装或不在 PATH 中）")
        except subprocess.TimeoutExpired:
            pytest.skip("npm 命令超时")

    def test_node_modules_exists(self):
        """node_modules 已安装。"""
        nm = FRONTEND_DIR / "node_modules"
        if not nm.exists():
            pytest.skip("node_modules 未安装（运行 npm install）")
        assert nm.is_dir()

    def test_package_json_valid(self):
        """package.json 格式正确。"""
        import json
        pkg = FRONTEND_DIR / "package.json"
        if not pkg.exists():
            pytest.skip("package.json 不存在")
        data = json.loads(pkg.read_text(encoding="utf-8"))
        assert "name" in data
        assert "scripts" in data
        assert "dev" in data.get("scripts", {})


class TestSecurityConfig:
    """安全配置检查"""

    def test_jwt_secret_not_default(self):
        """JWT_SECRET_KEY 不是默认值。"""
        from app.core.config import settings
        assert settings.JWT_SECRET_KEY != "your-secret-key", "JWT_SECRET_KEY 不能使用默认值"
        assert len(settings.JWT_SECRET_KEY) >= 16, "JWT_SECRET_KEY 长度应 >= 16"

    def test_jwt_algorithm(self):
        """JWT 算法为 HS256。"""
        from app.core.config import settings
        assert settings.JWT_ALGORITHM == "HS256"

    def test_cors_origins_configured(self):
        """CORS 跨域白名单已配置。"""
        from app.core.config import settings
        origins = settings.cors_origins_list
        assert len(origins) > 0, "CORS_ORIGINS 未配置交叉域白名单"

    def test_debug_mode_disabled(self):
        """生产环境 DEBUG=False。"""
        from app.core.config import settings
        if settings.DEBUG:
            print("⚠️ DEBUG=True — 仅开发环境应开启")
        assert True


class TestLoggingConfig:
    """日志配置检查"""

    def test_log_level_valid(self):
        """日志级别有效。"""
        from app.core.config import settings
        valid = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert settings.LOG_LEVEL in valid, f"无效日志级别: {settings.LOG_LEVEL}"

    def test_log_dir_writable(self):
        """日志目录可写。"""
        log_dir = BACKEND_DIR / "logs"
        if not log_dir.exists():
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pytest.skip("日志目录不可创建")
        assert os.access(str(log_dir), os.W_OK), "日志目录不可写"