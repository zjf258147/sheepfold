# DL-IMS APK 打包检查方案

> 版本：v1.0 | 日期：2026-09-15 | 状态：方案阶段

---

## 一、背景与目标

### 1.1 背景

最近一次 APK 打包踩坑：**代码改了但没提交，打包时缺代码**。涉及 6 个未提交文件：

| 文件 | 改动类型 |
|------|:---:|
| `src/utils/apiConfig.js` | 新增 |
| `src/components/ServerSettingsDialog.vue` | 新增 |
| `src/utils/request.js` | 修改 |
| `src/views/Login.vue` | 修改 |
| `backend/app/api/settings.py` | 修改 |
| `android/app/src/main/AndroidManifest.xml` | 修改 |

### 1.2 目标

1. **防止再次出现"代码没提交就打包"** → 打包脚本强制检查
2. **快速确认 APK 版本** → App 内"关于"页面显示版本信息

---

## 二、任务清单

| 优先级 | 任务 | 文件 | 工作量 |
|:---:|------|------|:---:|
| P0 | 打包脚本 `build_apk.ps1` | `scripts/build_apk.ps1`（新建） | 0.5天 |
| P0 | 版本号注入 | `vite.config.js`（修改） | 0.5天 |
| P0 | 关于页面 | `src/views/About.vue`（新建） | 0.5天 |
| P0 | 路由 + 菜单入口 | `router/index.js` + `MainLayout.vue`（修改） | 0.5天 |

---

## 三、任务1：打包脚本 `scripts/build_apk.ps1`

### 3.1 脚本流程（9 步）

```
┌──────────────────────────────────────┐
│ ① git status --porcelain             │
│    → 不为空则报错退出                │
├──────────────────────────────────────┤
│ ② 检查 6 个关键文件是否在 Git 中     │
│    → 缺失则警告继续                  │
├──────────────────────────────────────┤
│ ③ 清理 dist/ 目录                    │
│    → 避免新旧文件混杂                │
├──────────────────────────────────────┤
│ ④ 跑后端测试                         │
│    uv run pytest tests/ -v            │
│    → 不通过则退出                    │
├──────────────────────────────────────┤
│ ⑤ 跑前端测试                         │
│    npm run test                       │
│    → 不通过则退出                    │
├──────────────────────────────────────┤
│ ⑥ npm run build                      │
│    → 不通过则退出                    │
├──────────────────────────────────────┤
│ ⑦ npx cap sync android               │
│    → 同步 Web 资源到 Android 项目     │
├──────────────────────────────────────┤
│ ⑧ cd android && ./gradlew assembleDebug │
│    → 构建 APK                        │
├──────────────────────────────────────┤
│ ⑨ 复制 APK 到 dist-apk/              │
│    输出：版本号 + 构建时间 + commit   │
└──────────────────────────────────────┘
```

### 3.2 关键文件清单（6 个）

| # | 文件路径 | 说明 |
|---|----------|------|
| 1 | `frontend/src/utils/apiConfig.js` | 动态 API URL 配置 |
| 2 | `frontend/src/components/ServerSettingsDialog.vue` | 服务器设置弹窗 |
| 3 | `frontend/src/utils/request.js` | Axios 动态 baseURL |
| 4 | `frontend/src/views/Login.vue` | 登录页服务器入口 |
| 5 | `backend/app/api/settings.py` | 测试连接代理端点 |
| 6 | `frontend/android/.../AndroidManifest.xml` | HTTP 明文配置 |

### 3.3 不通过则报错退出的检查

| # | 检查项 | 命令 |
|---|--------|------|
| 1 | 工作区干净 | `git status --porcelain` |
| 2 | Node 可用 | `node --version` |
| 3 | 后端测试通过 | `uv run pytest tests/ -v` |
| 4 | 前端测试通过 | `npm run test` |
| 5 | 前端构建成功 | `npm run build` |
| 6 | dist 非空 | 检查 `dist/index.html` |

### 3.4 输出示例

```
========================================
DL-IMS APK Build Script
========================================
[1/9] 检查工作区状态... ✅ 干净
[2/9] 检查关键文件... ✅ 6/6
[3/9] 清理 dist/... ✅
[4/9] 后端测试... ✅ 通过
[5/9] 前端测试... ✅ 通过
[6/9] 前端构建... ✅ dist/ 生成
[7/9] Capacitor 同步... ✅
[8/9] Gradle 打包... ✅
[9/9] 复制 APK... ✅

========================================
打包完成！
  版  本：2.0.0
  构建时间：2026-09-15 14:30:00
  最新提交：abc1234 [app] 新增打包脚本和关于页面
  APK 路径：dist-apk/DL-IMS-2.0.0-20260915-143000.apk
========================================
```

---

## 四、任务2：关于页面

### 4.1 版本号注入机制

**文件**：`vite.config.js`

```javascript
import { readFileSync } from 'node:fs'
const pkg = JSON.parse(readFileSync('./package.json', 'utf-8'))

export default defineConfig({
  define: {
    __APP_VERSION__: JSON.stringify(pkg.version),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
  },
})
```

### 4.2 关于页面内容

| 显示项 | 来源 |
|--------|------|
| App 名称 / 副标题 | Brand Store（品牌配置） |
| App 版本号 | `__APP_VERSION__`（构建时注入） |
| 构建时间 | `__BUILD_TIME__`（构建时注入） |
| 服务器地址 | `getApiBaseUrl()`（动态获取） |

### 4.3 页面布局

```
┌──────────────────────────────────────┐
│                                      │
│         [Logo / 图标]                │
│         DL-IMS                       │
│         生产物料与产品追溯管理系统     │
│                                      │
│  ┌────────────────────────────────┐  │
│  │ App 版本    │ 2.0.0            │  │
│  │ 构建时间    │ 2026-09-15 14:30 │  │
│  │ 服务器地址  │ `http://192...`   │  │
│  └────────────────────────────────┘  │
│                                      │
│  [切换服务器]      [复制版本信息]    │
│                                      │
│  © 2026 西安敦临计量检测有限公司     │
└──────────────────────────────────────┘
```

### 4.4 入口位置

| 位置 | 是否添加 | 说明 |
|------|:---:|------|
| 侧边栏菜单 | ❌ | 不占用侧边栏 |
| 用户下拉菜单 | ✅ | 与"修改密码""服务器设置""退出"并列 |

### 4.5 "复制版本信息"功能

点击后将以下文本复制到剪贴板：

```
DL-IMS v2.0.0
构建时间：2026-09-15T14:30:00
服务器：http://192.168.1.100:8000
提交：abc1234
```

---

## 五、涉及文件总览

| 文件 | 操作 | 说明 |
|------|:---:|------|
| `frontend/vite.config.js` | 修改 | 注入 `__APP_VERSION__` + `__BUILD_TIME__` |
| `frontend/src/views/About.vue` | **新建** | 关于页面 |
| `frontend/src/router/index.js` | 修改 | 新增 `/about` 路由（`public: true`） |
| `frontend/src/layout/MainLayout.vue` | 修改 | 用户下拉菜单新增"关于"入口 |
| `scripts/build_apk.ps1` | **新建** | APK 打包脚本 |

---

## 六、执行顺序

```
① 修改 vite.config.js（注入版本号）
② 新建 About.vue
③ 修改 router/index.js（加路由）
④ 修改 MainLayout.vue（加下拉入口）
⑤ 新建 scripts/build_apk.ps1
⑥ 验证：启动前后端，浏览关于页面
⑦ git commit
```

---

## 七、后续扩展（P1/P2）

| 优先级 | 任务 | 说明 |
|:---:|------|------|
| P1 | `@capacitor/barcode-scanner` 替换 `html5-qrcode` | 原生扫码 |
| P1 | `@capacitor/network` 断网提示 | 场站网络监控 |
| P2 | `@capacitor/filesystem` + `share` | 导出分享 |
| P3 | 自建 OTA 热更新 | 二期完成后评估 |