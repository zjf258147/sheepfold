---
name: "gui-generator"
description: "Generate and modify PySide6 GUI for transformer testing system. Invoke when user asks to create/modify GUI, add UI features, or fix UI issues in this project."
---

# GUI Generator — 变压器监测系统 GUI 生成器

## 项目 GUI 架构

本项目使用 **PySide6** 框架构建 GUI，主文件为 `src/app.py`。

### 架构概览

```
src/app.py
├── 全局变量/路径
│   ├── _APP_DIR          # 应用根目录（开发/打包兼容）
│   ├── _MAIN_SCRIPT       # 主测试脚本路径
│   ├── _SRC_DIR           # src 目录路径
│   └── find_excel_file()  # Excel 文件查找（支持 .xlsx/.xlsm）
├── 辅助类
│   ├── StdoutRedirector   # 标准输出重定向 → GUI 日志
│   ├── LoginWaitDialog    # 登录等待弹窗
│   ├── BatchSelectDialog  # 批次选择对话框（数据库导出）
│   └── TestWorker         # 测试工作线程（QThread）
└── MainWindow             # 主窗口（QMainWindow）
    ├── __init__           # 初始化窗口、信号连接
    ├── _setup_ui          # 构建 UI 布局
    ├── _load_defaults     # 加载默认配置
    ├── _on_browse_excel   # 浏览 Excel 文件
    ├── _on_open_excel     # 打开 Excel 文件
    ├── _on_start_test     # 开始测试
    ├── _on_pause_test     # 暂停/继续测试
    ├── _on_stop_test      # 停止测试
    ├── _on_export_report  # 导出报告（数据库→Excel）
    ├── _init_voice_manager # 初始化语音助手
    └── _append_log        # 追加日志到 GUI
```

## 修改 GUI 时的关键规则

### 1. 路径处理
```python
# 开发时 app.py 在 src/ 下，_APP_DIR 指向根目录
if getattr(sys, 'frozen', False):
    _APP_DIR = os.path.dirname(sys.executable)
else:
    _APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

### 2. 导入主模块
```python
# 主模块是中文文件名，必须用 importlib 动态导入
_SRC_DIR = os.path.join(_APP_DIR, 'src')
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import importlib.util
spec = importlib.util.spec_from_file_location("main_script", _MAIN_SCRIPT)
main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_module)
```

### 3. 线程安全
- 所有 GUI 更新通过 `Signal` 从子线程发送到主线程
- 测试线程不直接操作 GUI 控件
- 使用 `QThread` 的 `finished` 信号处理测试结束

### 4. 日志重定向
```python
class StdoutRedirector(QObject):
    text_written = Signal(str)
    def write(self, text):
        if text.strip():
            self.text_written.emit(text)
    def flush(self):
        pass
```
- 将 `sys.stdout` 重定向到 GUI 日志窗口
- 保留 `_orig_stdout` 用于恢复

### 5. 样式规范
- 主色调：蓝色系 `#2196F3`（按钮）、绿色 `#4CAF50`（导出）
- 字体：`Microsoft YaHei` 9pt 正文、12pt 标题
- 最小窗口：1100×750
- 使用 `QGroupBox` 分组配置区域

### 6. 配置加载
```python
def _load_defaults(self):
    from config import EXCEL_FILE, URL, _EXCEL_BASE
    default_excel = find_excel_file(_APP_DIR, _EXCEL_BASE)
    if default_excel:
        self.excel_path_edit.setText(default_excel)
```

## 对话框模式

### 登录等待对话框
```python
class LoginWaitDialog(QDialog):
    def __init__(self, parent=None):
        # 模态对话框，带倒计时
        # 显示 "请完成登录操作..." 提示
        # 30秒倒计时后自动关闭
```

### 批次选择对话框
```python
class BatchSelectDialog(QDialog):
    def __init__(self, batches, parent=None):
        # QTableWidget 显示批次列表
        # 列：批次ID、批次名称、开始时间、设备数
        # 导出按钮 + 取消按钮
```

## 测试工作线程

```python
class TestWorker(QThread):
    finished = Signal(bool, str)  # 成功/失败, 消息
    progress = Signal(int)        # 进度值
    log = Signal(str)             # 日志消息
    device_completed = Signal(str, dict)  # 设备完成
    
    def __init__(self, excel_path, device_number, mode, max_devices, url):
        # 参数：Excel路径、设备编号、测试模式、最大设备数、URL
        # _was_stopped 标志用于优雅停止
        # _login_event 用于等待登录
```

## 添加新 UI 组件的步骤

1. 在 `_setup_ui` 中添加控件布局
2. 如需配置，在 `_load_defaults` 中加载默认值
3. 添加对应的 `_on_xxx` 回调方法
4. 如需跨线程通信，使用 `Signal`
5. 添加中文注释说明功能
6. 运行 `py_compile` 验证语法

## 打包命令

```bash
pyinstaller --onefile --windowed --name="TransformerTester" src/app.py
```