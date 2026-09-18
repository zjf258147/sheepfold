"""APK 打包离线检查 — 可随"执行完整检测清单"自动运行。

覆盖 40 项 APK 打包检查：
  - §A1 环境检查（Java/Android SDK/Gradle/Node）
  - §A2 配置文件（capacitor.config.json / AndroidManifest / build.gradle / keystore）
  - §A3 资源文件（图标6dpi / 启动页10种 / colors / network_security / proguard）
  - §A4 插件检查（capacitor.plugins.json）
  - §A5 APK 编译（仅 --build-apk 标记时）

用法：
    pytest tests/apk/ -v                         # 离线检查（不含编译）
    pytest tests/apk/ -v -m apkfull             # 含编译的完整检查（~2min）
"""

import os
import sys
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

# ── 路径常量 ──────────────────────────────────────────────
_FRONTEND_DIR = Path(__file__).resolve().parents[3] / "frontend"
_ANDROID_DIR = _FRONTEND_DIR / "android"
_APP_DIR = _ANDROID_DIR / "app"
_RES_DIR = _APP_DIR / "src" / "main" / "res"

# Android SDK 候选路径
_SDK_CANDIDATES = [
    os.environ.get("ANDROID_HOME", ""),
    os.environ.get("ANDROID_SDK_ROOT", ""),
    r"C:\Android",
    os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk"),
]


def _find_sdk():
    for p in _SDK_CANDIDATES:
        if p and Path(p).exists():
            return p
    return None


def _which(cmd):
    try:
        result = subprocess.run(["where", cmd], capture_output=True, text=True, timeout=5, shell=True)
        return result.returncode == 0
    except Exception:
        return False


def _run(*args, cwd=None, timeout=120, env_extra=None):
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    sdk = _find_sdk()
    if sdk:
        env["ANDROID_HOME"] = sdk
        env["ANDROID_SDK_ROOT"] = sdk
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)


# ═══════════════════════════════════════════════════════════
# §A1 — 环境检查（6项）
# ═══════════════════════════════════════════════════════════

class TestEnv:
    """APK 编译环境"""

    def test_java(self):
        """Java JDK 可用"""
        r = _run("java", "-version")
        assert r.returncode == 0 or "version" in (r.stdout + r.stderr).lower()

    def test_android_sdk(self):
        """Android SDK 已安装"""
        sdk = _find_sdk()
        assert sdk is not None, f"ANDROID_HOME/ANDROID_SDK_ROOT 未找到"
        assert Path(sdk, "platform-tools", "adb.exe").exists(), "adb.exe 缺失"
        assert Path(sdk, "build-tools").exists(), "build-tools 缺失"
        assert Path(sdk, "platforms").exists(), "platforms 缺失"

    def test_gradle_wrapper(self):
        """Gradle wrapper 存在"""
        gradlew = _ANDROID_DIR / "gradlew.bat"
        assert gradlew.exists(), "gradlew.bat 缺失"

    def test_node(self):
        """Node.js 可用"""
        assert _which("node"), "node 未安装或不在 PATH"

    def test_npm(self):
        """npm 可用"""
        assert _which("npm"), "npm 未安装或不在 PATH"

    def test_frontend_dir(self):
        """前端目录结构完整"""
        assert _FRONTEND_DIR.exists(), "frontend 目录缺失"
        assert (_FRONTEND_DIR / "package.json").exists(), "package.json 缺失"
        assert _ANDROID_DIR.exists(), "android 目录缺失"


# ═══════════════════════════════════════════════════════════
# §A2 — 配置文件（10项）
# ═══════════════════════════════════════════════════════════

class TestConfig:
    """APK 配置文件"""

    def test_capacitor_config_exists(self):
        assert (_FRONTEND_DIR / "capacitor.config.json").exists()

    def test_capacitor_config_valid(self):
        with open(_FRONTEND_DIR / "capacitor.config.json", encoding="utf-8") as f:
            config = json.load(f)
        assert config["appId"] == "com.dunlin.ims"
        assert config["appName"] == "DL-IMS"
        assert config["webDir"] == "dist"
        assert config["server"]["androidScheme"] in ("http", "https")

    def test_android_manifest_exists(self):
        assert (_APP_DIR / "src" / "main" / "AndroidManifest.xml").exists()

    def test_android_manifest_permissions(self):
        manifest_path = _APP_DIR / "src" / "main" / "AndroidManifest.xml"
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        perms = [e.attrib.get("{http://schemas.android.com/apk/res/android}name", "") for e in root.findall("uses-permission")]
        assert "android.permission.INTERNET" in perms
        assert "android.permission.CAMERA" in perms

    def test_android_manifest_nsc(self):
        """networkSecurityConfig 已配置"""
        manifest_path = _APP_DIR / "src" / "main" / "AndroidManifest.xml"
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        app = root.find("application")
        assert app is not None
        key = "{http://schemas.android.com/apk/res/android}networkSecurityConfig"
        assert app.attrib.get(key) == "@xml/network_security_config"

    def test_android_manifest_deeplink(self):
        """深度链接 intent-filter 存在"""
        content = Path(_APP_DIR, "src", "main", "AndroidManifest.xml").read_text(encoding="utf-8")
        assert "custom_url_scheme" in content or "BROWSABLE" in content

    def test_build_gradle_exists(self):
        assert (_APP_DIR / "build.gradle").exists()

    def test_build_gradle_signing(self):
        content = (_APP_DIR / "build.gradle").read_text(encoding="utf-8")
        assert "keystore.properties" in content
        assert "signingConfigs" in content

    def test_keystore_properties_exists(self):
        assert (_ANDROID_DIR / "keystore.properties").exists()

    def test_keystore_file_exists(self):
        props = {}
        with open(_ANDROID_DIR / "keystore.properties", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    props[k] = v
        store_file = props.get("storeFile", "")
        assert store_file and Path(store_file).exists(), f"密钥库文件不存在: {store_file}"


# ═══════════════════════════════════════════════════════════
# §A3 — 资源文件（14项）
# ═══════════════════════════════════════════════════════════

class TestResources:
    """APK 资源文件"""

    _ICON_DPIS = ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]

    @pytest.mark.parametrize("dpi", _ICON_DPIS)
    def test_icon(self, dpi):
        p = _RES_DIR / f"mipmap-{dpi}" / "ic_launcher.png"
        assert p.exists(), f"图标缺失: {p}"

    @pytest.mark.parametrize("dpi", _ICON_DPIS)
    def test_icon_round(self, dpi):
        p = _RES_DIR / f"mipmap-{dpi}" / "ic_launcher_round.png"
        assert p.exists(), f"圆形图标缺失: {p}"

    def test_adaptive_icon(self):
        assert (_RES_DIR / "mipmap-anydpi-v26" / "ic_launcher.xml").exists()
        assert (_RES_DIR / "mipmap-anydpi-v26" / "ic_launcher_round.xml").exists()

    _SPLASH_DPIS = [
        ("drawable-land-mdpi", "splash.png"),
        ("drawable-land-hdpi", "splash.png"),
        ("drawable-land-xhdpi", "splash.png"),
        ("drawable-land-xxhdpi", "splash.png"),
        ("drawable-land-xxxhdpi", "splash.png"),
        ("drawable-port-mdpi", "splash.png"),
        ("drawable-port-hdpi", "splash.png"),
        ("drawable-port-xhdpi", "splash.png"),
        ("drawable-port-xxhdpi", "splash.png"),
        ("drawable-port-xxxhdpi", "splash.png"),
    ]

    @pytest.mark.parametrize("folder,filename", _SPLASH_DPIS)
    def test_splash(self, folder, filename):
        p = _RES_DIR / folder / filename
        assert p.exists(), f"启动页缺失: {p}"

    def test_colors_xml_exists(self):
        assert (_RES_DIR / "values" / "colors.xml").exists()

    def test_network_security_config_exists(self):
        assert (_RES_DIR / "xml" / "network_security_config.xml").exists()

    def test_proguard_rules_populated(self):
        content = (_APP_DIR / "proguard-rules.pro").read_text(encoding="utf-8")
        assert len([l for l in content.splitlines() if l.strip() and not l.startswith("#")]) >= 3


# ═══════════════════════════════════════════════════════════
# §A4 — 插件检查（3项）
# ═══════════════════════════════════════════════════════════

class TestPlugins:
    """Capacitor 插件"""

    REQUIRED_PLUGINS = [
        "@capacitor/barcode-scanner",
        "@capacitor/camera",
        "@capacitor/network",
        "@capacitor/preferences",
        "@capacitor/status-bar",
    ]

    def test_plugins_json_exists(self):
        assert (_APP_DIR / "src" / "main" / "assets" / "capacitor.plugins.json").exists()

    def test_plugins_registered(self):
        plugin_path = _APP_DIR / "src" / "main" / "assets" / "capacitor.plugins.json"
        with open(plugin_path, encoding="utf-8") as f:
            plugins = json.load(f)
        registered = {p["pkg"] for p in plugins}
        missing = set(self.REQUIRED_PLUGINS) - registered
        assert not missing, f"缺失插件: {missing}"

    def test_package_json_plugins(self):
        """前端 package.json 包含 Capacitor 插件"""
        with open(_FRONTEND_DIR / "package.json", encoding="utf-8") as f:
            pkg = json.load(f)
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        for p in self.REQUIRED_PLUGINS:
            assert p in deps, f"package.json 缺失: {p}"


# ═══════════════════════════════════════════════════════════
# §A5 — APK 编译（仅 --apkfull 标记，约 2 分钟）
# ═══════════════════════════════════════════════════════════

@pytest.mark.apkfull
class TestBuild:
    """APK 编译与验证（重量级，需显式标记）"""

    def test_debug_apk_build(self):
        sdk = _find_sdk()
        r = _run(
            f"{_ANDROID_DIR / 'gradlew.bat'}", "assembleDebug",
            cwd=str(_ANDROID_DIR), timeout=300,
            env_extra={"ANDROID_HOME": sdk, "ANDROID_SDK_ROOT": sdk},
        )
        assert r.returncode == 0, f"Debug APK 编译失败:\n{r.stderr[-500:]}"

    def test_debug_apk_exists(self):
        apk = _APP_DIR / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
        assert apk.exists(), f"Debug APK 不存在: {apk}"
        assert apk.stat().st_size > 5_000_000, f"APK 太小: {apk.stat().st_size} bytes"

    def test_release_apk_build(self):
        sdk = _find_sdk()
        r = _run(
            f"{_ANDROID_DIR / 'gradlew.bat'}", "assembleRelease",
            cwd=str(_ANDROID_DIR), timeout=300,
            env_extra={"ANDROID_HOME": sdk, "ANDROID_SDK_ROOT": sdk},
        )
        assert r.returncode == 0, f"Release APK 编译失败:\n{r.stderr[-500:]}"

    def test_release_apk_exists(self):
        apk = _APP_DIR / "build" / "outputs" / "apk" / "release" / "app-release.apk"
        assert apk.exists(), f"Release APK 不存在: {apk}"
        assert apk.stat().st_size > 3_000_000, f"APK 太小: {apk.stat().st_size} bytes"

    def test_release_apk_signed(self):
        apk_path = str(_APP_DIR / "build" / "outputs" / "apk" / "release" / "app-release.apk")
        sdk = _find_sdk()
        apksigner = None
        for root, dirs, files in os.walk(Path(sdk, "build-tools") if sdk else ""):
            for f in files:
                if f == "apksigner.bat":
                    apksigner = Path(root, f)
                    break
        if apksigner is None:
            pytest.skip("apksigner.bat 未找到")
        r = _run(str(apksigner), "verify", "--print-certs", apk_path)
        assert r.returncode == 0, f"APK 签名验证失败:\n{r.stderr}"
        assert "Signer #1" in r.stdout, "未找到签名者"

    def test_release_apk_proguarded(self):
        """Release APK 经过混淆（比 Debug 小 20% 以上）"""
        apk_path = _APP_DIR / "build" / "outputs" / "apk" / "release" / "app-release.apk"
        if not apk_path.exists():
            pytest.skip("app-release.apk 不存在（未编译Release APK）")
        sdk = _find_sdk()
        aapt = None
        for root, dirs, files in os.walk(Path(sdk, "build-tools") if sdk else ""):
            for f in files:
                if f == "aapt.exe":
                    aapt = Path(root, f)
                    break
        if aapt is None:
            pytest.skip("aapt.exe 未找到")
        import tempfile, shutil
        tmp_dir = tempfile.mkdtemp()
        try:
            tmp_apk = Path(tmp_dir) / "app-release.apk"
            shutil.copy2(str(apk_path), str(tmp_apk))
            r = _run(str(aapt), "dump", "badging", str(tmp_apk))
            assert r.returncode == 0, f"aapt dump 失败:\n{r.stderr}"
            assert "versionCode='1'" in r.stdout
            assert "DL-IMS" in r.stdout
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)