# APK 下载与远程加载方案

> 版本：v2.0 | 日期：2026-09-16 | 状态：已确认，待实现（修正🔴问题后）

## 一、背景

IMS 系统已具备 Android APK 打包能力（Capacitor），当前 APK 内嵌前端 `dist/` 目录，为"编译时快照"模式。每次前端功能变更后，用户必须重新下载安装新 APK 才能看到更新。

本方案解决两个问题：
1. **网页端下载 APK** — 用户从网页直接下载最新 APK
2. **APK 自动获取最新功能** — 不重新打包也能用到最新的前端代码

---

## 二、方案总览

```
┌────────────────────────────────────────────────────────────┐
│                     网页端（浏览器）                          │
│                                                              │
│  Login.vue ─── "下载移动端 App" ──→ http://IP:8000/download/ │
│  About.vue ─── "下载 Android App" ──→    ims-latest.apk      │
│                                                              │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│                     手机端（APK）                             │
│                                                              │
│  APK 启动 → 加载本地 dist/（安全兜底）                         │
│      ↓                                                       │
│  【首次配置引导】无服务器地址 → 醒目提示 + 配置按钮            │
│      ↓                                                       │
│  检查 Preferences.use_online                                 │
│      ├── 无 → 本地登录页 + "使用在线版本"按钮                  │
│      │         ↓ 用户点击（loading 过渡）                      │
│      │    连通性测试 /health → OK → 保存 Token → 记住选择      │
│      │                      → 跳转远程（URL 参数带 Token）     │
│      │              → 失败 → 停留在本地，提示不可达            │
│      └── 有 → 连通性测试                                     │
│               ├── OK → 传递 Token → 跳转远程                   │
│               └── 失败 → 停留在本地，静默（不报错）            │
│                                                              │
│  远程 http://IP:8080 — 启动时从 URL 参数恢复 Token             │
│      │                                                       │
│      └── About 页 "切回本地版本" → 清除 Preferences           │
│                                                              │
│  本地 dist/ — APK 打包时的快照，作为安全兜底                  │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

---

## 三、APK 下载功能（✅ 已实现）

### 3.1 后端

| 组件 | 说明 |
|------|------|
| 路径 | `backend/static/download/ims-latest.apk` |
| 挂载 | `main.py` → `app.mount("/download", StaticFiles(...))` |
| URL | `http://IP:8000/download/ims-latest.apk` |
| 鉴权 | 无（登录页也能下载） |

### 3.2 构建脚本

| 步骤 | 说明 |
|------|------|
| APK 构建 | `scripts/build_apk.ps1` → `dist-apk/DL-IMS-v{ver}-{date}.apk` |
| 固定副本 | 自动复制到 `backend/static/download/ims-latest.apk` |
| 文件名 | 始终为 `ims-latest.apk`，下载链接永不变化 |

### 3.3 前端入口

| 入口 | 位置 | 场景 |
|------|------|------|
| 登录页 | Login.vue 底部 → "下载移动端 App" | 未登录用户 |
| 关于页 | About.vue → "下载 Android App" 按钮 | 已登录用户 |

### 3.4 关键设计决策

| 决策 | 原因 |
|------|------|
| URL 用后端 8000 端口 | 前端 8080 路由会拦截 `/download` 路径，导致 404 |
| 文件名固定 `ims-latest.apk` | 下载链接不随版本变化，用户始终拿到最新版 |
| IP 动态获取 | 从 `apiConfig.js` 读取，换服务器无需改代码 |

---

## 四、APK 远程加载功能（⏳ 待实现）

### 4.1 设计原则

| 原则 | 说明 |
|------|------|
| **本地优先** | APK 永远先加载内嵌 `dist/`，安全兜底 |
| **连通测试** | 跳转前先发 `/health` 请求，确认服务器可达 |
| **手动切换** | 首次需用户主动点击"使用在线版本"，明确意图 |
| **记住选择** | 用 Capacitor Preferences 持久化，下次自动检测跳转 |

### 4.2 适用场景

| 场景 | 行为 |
|------|------|
| 首次安装 + 未配置服务器 | 本地登录页 → 设置服务器 → 点"使用在线版本" |
| 首次安装 + 已配置服务器 | 本地登录页 → 看到"使用在线版本"按钮 → 点击 |
| 已选择过在线 + 服务器可达 | 启动自动跳转远程，秒开最新版 |
| 已选择过在线 + 服务器不可达 | 停留在本地（旧版），静默不报错 |
| 在线版本中切换回本地 | 清除 Preferences 标记，重启 App 即回本地 |

### 4.3 前端地址推导（🔴 已修正）

**问题**：旧方案用 `baseUrl.replace(':8000', ':8080')` 字符串替换推导前端地址，脆弱且易出错。

**修正**：用 `URL` 对象构造 + 环境变量，不依赖字符串替换。

```javascript
// apiConfig.js 新增
export function getFrontendUrl() {
  const backendUrl = getApiBaseUrl()
  const frontendPort = import.meta.env.VITE_FRONTEND_PORT || '8080'
  const url = new URL(backendUrl)
  url.port = frontendPort
  return url.origin  // 例: "http://192.168.1.100:8080"
}
```

| 环境 | 后端端口 | 前端端口 | VITE_FRONTEND_PORT |
|------|:---:|:---:|:---:|
| 开发 (Vite) | 8000 | 5173 | `5173` |
| 生产 (Docker/Nginx) | 8000 | 8080 | `8080`（默认值） |

需要在 `.env` / `.env.production` 中新增 `VITE_FRONTEND_PORT`。

### 4.4 Token 跨域传递（🔴 已修正）

**问题**：跳转后 `localStorage` 跨端口不共享（`localhost:5173` vs `192.168.1.100:8080`），Token 丢失导致需重新登录。

**修正**：跳转前将 Token 存入 Capacitor Preferences + URL 参数双通道。

```javascript
// 跳转前：双重保存
const token = localStorage.getItem('token') || ''
await Preferences.set({ key: 'jump_token', value: token })
const frontendUrl = getFrontendUrl()
window.location.href = `${frontendUrl}/login?token=${encodeURIComponent(token)}`
```

```javascript
// main.js 远程版恢复
const urlParams = new URLSearchParams(window.location.search)
const tokenFromUrl = urlParams.get('token')
if (tokenFromUrl) {
  localStorage.setItem('token', tokenFromUrl)
  // 清除 URL 参数，防止分享链接泄露 Token
  window.history.replaceState({}, '', window.location.pathname)
}
```

验证：`/health` 端点已存在于 `main.py:135`，无需新增。

### 4.5 从远程切回本地

远程版的 About.vue 新增"切回本地版本"按钮：

```javascript
const switchToLocal = async () => {
  await ElMessageBox.confirm(
    '切回本地版本后，下次打开 App 将使用旧版本功能。确定吗？',
    '切回本地',
    { type: 'warning' }
  )
  await Preferences.set({ key: 'use_online', value: 'false' })
  await Preferences.remove({ key: 'jump_token' })
  ElMessage.success('已切回本地版本，请重启 App')
}
```

### 4.6 首次配置引导

新员工安装后 API 调用会失败（无服务器地址）。登录页需醒目提示：

```vue
<div v-if="isApp && !hasServerConfig" class="server-guide">
  <el-alert title="首次使用" type="info" :closable="false">
    <p>请先配置服务器地址，或联系管理员获取地址</p>
    <el-button type="primary" @click="serverRef.open()">配置服务器地址</el-button>
  </el-alert>
</div>
```

### 4.7 跳转 Loading 过渡

```vue
<!-- 跳转中 -->
<div v-if="switchingToOnline" class="switch-overlay">
  <el-icon class="is-loading"><Loading /></el-icon>
  <p>正在连接服务器...</p>
</div>
```

### 4.8 双版本号显示

About 页应显示两个版本号，让用户知道当前用的是哪个版本。

| 版本 | 来源 | 含义 |
|------|------|------|
| 本地版本 | APK 打包时 `package.json` 的 `version` | APK 兜底版本 |
| 在线版本 | API `/api/v1/app/version` 返回的 `server_version` | 服务器最新版本 |

```vue
<el-descriptions-item label="本地版本">v{{ localVersion }}</el-descriptions-item>
<el-descriptions-item label="在线版本" v-if="isRemote">
  v{{ remoteVersion }}
  <el-tag v-if="remoteVersion !== localVersion" type="warning" size="small">可更新</el-tag>
</el-descriptions-item>
```

### 4.9 实现清单

| # | 文件 | 改动 | 状态 |
|---|------|------|:---:|
| 1 | `apiConfig.js` | 新增 `getFrontendUrl()` | ⏳ |
| 2 | `.env` / `.env.production` | 新增 `VITE_FRONTEND_PORT` | ⏳ |
| 3 | `Login.vue` | 首次配置引导 + "使用在线版本"按钮 + 连通性测试 + Token传递 + Loading过渡 | ⏳ |
| 4 | `main.js` | 启动时检测 Preferences/URL参数 → 恢复Token → 自动跳转远程 | ⏳ |
| 5 | `About.vue` | 新增"切回本地版本" + 双版本号显示 | ⏳ |
| 6 | `capacitor.config.json` | **不改**（不加 `server.url`，保持本地模式） | — |

### 4.10 Login.vue 改动细节（v2.0 修正版）

```javascript
// ── 新增变量 ──
const isApp = ref(false)
const switchingToOnline = ref(false)
const checking = ref(false)
const hasServerConfig = ref(false)
const onlineAvailable = ref(false)

// ── onMounted 中检测 App 环境 ──
onMounted(async () => {
  isApp.value = !!(window.Capacitor?.isNativePlatform?.())
  if (isApp.value) {
    await checkOnlineAvailability()
  }
})

// ── 检查在线版本可用性 ──
const checkOnlineAvailability = async () => {
  if (!isApp.value) return
  const url = getCachedBaseUrl() || (await getApiBaseUrl())
  if (!url) return
  hasServerConfig.value = true
  try {
    const controller = new AbortController()
    setTimeout(() => controller.abort(), 3000)
    const res = await fetch(`${url}/health`, { signal: controller.signal })
    onlineAvailable.value = res.ok
  } catch {
    onlineAvailable.value = false
  }
}

// ── 切换到在线版本 ──
const switchToOnline = async () => {
  const baseUrl = getCachedBaseUrl() || (await getApiBaseUrl())
  if (!baseUrl) {
    ElMessage.warning('请先配置服务器地址')
    serverRef.value?.open()
    return
  }
  switchingToOnline.value = true
  try {
    const controller = new AbortController()
    setTimeout(() => controller.abort(), 3000)
    const res = await fetch(`${baseUrl}/health`, { signal: controller.signal })
    if (res.ok) {
      // ① 保存 Token（双通道）
      const token = localStorage.getItem('token') || ''
      const { Preferences } = await import('@capacitor/preferences')
      await Promise.all([
        Preferences.set({ key: 'use_online', value: 'true' }),
        Preferences.set({ key: 'jump_token', value: token }),
      ])
      // ② 跳转（URL 参数带 Token）
      const frontendUrl = getFrontendUrl(baseUrl)
      window.location.href = `${frontendUrl}/login?token=${encodeURIComponent(token)}`
    } else {
      ElMessage.error('服务器不可达，请检查网络或服务器地址')
    }
  } catch {
    ElMessage.error('服务器不可达，请检查网络或服务器地址')
  } finally {
    switchingToOnline.value = false
  }
}
```

**模板新增**：

```vue
<!-- 首次使用引导 -->
<div v-if="isApp && !hasServerConfig" class="server-guide">
  <el-alert title="首次使用" type="info" :closable="false">
    请先配置服务器地址，或联系管理员获取地址
  </el-alert>
  <el-button type="primary" @click="serverRef.open()">配置服务器地址</el-button>
</div>

<!-- 使用在线版本 -->
<el-button v-if="isApp && hasServerConfig && onlineAvailable"
  type="primary" :loading="switchingToOnline" @click="switchToOnline">
  使用在线版本（最新功能）
</el-button>

<!-- 跳转 Loading -->
<div v-if="switchingToOnline" class="switch-overlay">
  <el-icon class="is-loading"><Loading /></el-icon>
  <p>正在连接服务器...</p>
</div>
```

### 4.11 apiConfig.js 新增 getFrontendUrl

```javascript
/**
 * 获取前端地址（用于 APK 远程加载跳转）
 * 用 URL 对象构造，不依赖字符串替换
 */
export function getFrontendUrl(backendUrl) {
  const base = backendUrl || getApiBaseUrl()
  const frontendPort = import.meta.env.VITE_FRONTEND_PORT || '8080'
  try {
    const url = new URL(base)
    url.port = frontendPort
    return url.origin  // 例: "http://192.168.1.100:8080"
  } catch {
    // 兜底：字符串替换
    return base.replace(/:8000$/, `:${frontendPort}`)
  }
}
```

### 4.12 .env 新增环境变量

```bash
# .env（开发）
VITE_FRONTEND_PORT=5173

# .env.production（生产）
VITE_FRONTEND_PORT=8080
```

### 4.13 main.js 改动细节（v2.0 修正版）

```javascript
// ── app.mount 之前插入 ──

const initRemoteDetection = async () => {
  const isApp = !!(window.Capacitor?.isNativePlatform?.())
  if (!isApp) return

  try {
    // ① 从 URL 参数恢复 Token（从本地跳转过来时携带）
    const urlParams = new URLSearchParams(window.location.search)
    const tokenFromUrl = urlParams.get('token')
    if (tokenFromUrl) {
      localStorage.setItem('token', tokenFromUrl)
      window.history.replaceState({}, '', window.location.pathname)
    }

    // ② 检查是否需要自动跳转远程
    const { Preferences } = await import('@capacitor/preferences')
    const { value } = await Preferences.get({ key: 'use_online' })
    if (value !== 'true') return

    // ③ 连通性测试
    const apiBase = localStorage.getItem('api_base_url')
    const baseUrl = apiBase || ''
    if (!baseUrl) return

    const controller = new AbortController()
    setTimeout(() => controller.abort(), 3000)
    const res = await fetch(`${baseUrl}/health`, { signal: controller.signal })

    if (res.ok) {
      // ④ 传递 Token → 跳转远程
      const token = localStorage.getItem('token') || ''
      await Preferences.set({ key: 'jump_token', value: token })
      // 动态 import getFrontendUrl
      const { getFrontendUrl } = await import('@/utils/apiConfig')
      const frontendUrl = getFrontendUrl(baseUrl)
      window.location.href = `${frontendUrl}/login?token=${encodeURIComponent(token)}`
    }
    // 不可达 → 静默留在本地
  } catch {
    // 留在本地，不报错
  }
}

// 在品牌信息加载完成后执行
brand.fetchBranding().finally(async () => {
  await initRemoteDetection()
  app.mount('#app')
})
```

### 4.14 About.vue 新增切回本地 + 双版本号

```javascript
// ── 切回本地版本 ──
const isApp = !!(window.Capacitor?.isNativePlatform?.())
const isRemote = computed(() => {
  // 远程版：URL 不含 capacitor:// 协议
  return isApp && !window.location.href.startsWith('capacitor://')
})

const switchToLocal = async () => {
  await ElMessageBox.confirm(
    '切回本地版本后，下次打开 App 将使用旧版功能。确定吗？',
    '切回本地', { type: 'warning' }
  )
  const { Preferences } = await import('@capacitor/preferences')
  await Preferences.set({ key: 'use_online', value: 'false' })
  await Preferences.remove({ key: 'jump_token' })
  ElMessage.success('已切回本地版本，请重启 App')
}

// ── 双版本号 ──
const localVersion = ref(import.meta.env.PACKAGE_VERSION || '—')
const remoteVersion = ref('—')

onMounted(async () => {
  if (isRemote.value) {
    try {
      const res = await getAppVersion()
      remoteVersion.value = res.server_version || '—'
    } catch { /* 忽略 */ }
  }
})
```

```vue
<!-- 模板 -->
<el-descriptions-item label="本地版本">v{{ localVersion }}</el-descriptions-item>
<el-descriptions-item v-if="isRemote" label="在线版本">
  v{{ remoteVersion }}
  <el-tag v-if="remoteVersion !== localVersion" type="warning" size="small">可更新</el-tag>
</el-descriptions-item>

<el-button v-if="isRemote" @click="switchToLocal" type="warning" plain>
  切回本地版本
</el-button>
```

---

## 五、为什么不动 capacitor.config.json

| 方案 | 做法 | 风险 |
|------|------|------|
| ❌ 加 `server.url` | WebView 直接加载远程 URL | IP 变了 → App 白屏 → 死锁 |
| ✅ 保持本地模式 | 永远先加载本地 `dist/` | 无风险，本地兜底始终可用 |

保持 `capacitor.config.json` 不改，让 APK 始终有一份可运行的本地副本。远程加载由 JavaScript 层在启动后按需触发，失败自动回退。

---

## 六、v1.0 → v2.0 修正记录

| # | 问题 | v1.0 | v2.0 |
|---|------|------|------|
| 🔴1 | 端口推导 | `baseUrl.replace(':8000', ':8080')` | `new URL(base).port = frontendPort` + 环境变量 |
| 🔴2 | Token 跨域 | 未处理 | Capacitor Preferences + URL 参数双通道 |
| 🟡3 | /health 端点 | 未确认 | ✅ 已确认存在 (main.py:135) |
| 🟡4 | 切回本地 | 无 UI | About.vue "切回本地版本"按钮 |
| 🟡5 | 首次配置引导 | 无 | Login.vue 醒目提示 + 配置按钮 |
| 🟡6 | 跳转 Loading | 无 | 遮罩层 + 加载动画 |
| 🟢7 | 双版本号 | 无 | About.vue 显示本地+在线版本号 |
| 🟢8 | 自动化测试 | 无 | `tests/e2e/test_apk_download.py` 建议 |

---

## 七、完整用户流程

### 7.1 新员工首次使用

```
1. 浏览器打开 http://IP:8080
2. 登录页底部点击"下载移动端 App"
3. 下载 ims-latest.apk，安装
4. 打开 App → 看到本地登录页
5. 页面顶部醒目提示"首次使用，请配置服务器地址"
6. 点击"配置服务器地址" → 输入 http://192.168.1.100:8000
7. 看到"使用在线版本（最新功能）"按钮 → 点击
8. Loading 过渡 → 自动跳转到 http://192.168.1.100:8080/login
9. Token 自动传递，无需重新登录
10. 以后每次打开 App，自动检测并跳转在线版
```

### 7.2 前端功能更新后

```
1. 开发者改代码 → npm run build → 部署到服务器
2. 手机上打开 App
3. 自动检测连通 → 跳转远程 http://IP:8080
4. 看到的就是最新版
5. APK 无需重新打包
```

### 7.3 服务器维护/宕机

```
1. 手机打开 App
2. 连通性检测失败 → 停留在本地页面
3. 用户可以使用旧版功能（本地 dist/）
4. 服务器恢复后，重启 App 即回到在线版
```

### 7.4 切回本地版本

```
1. 远程版 → 打开 About 页面
2. 看到"在线版本 v2.7"和"本地版本 v2.5"
3. 点击"切回本地版本"
4. 确认 → 下次启动将使用本地版本
```

---

## 八、检测清单

### 8.1 手动验证（12项）

| # | 检查项 | 验证方式 | 状态 |
|---|--------|---------|:---:|
| 1 | `/download/ims-latest.apk` 可访问 | 浏览器访问后端 8000 端口 | ⬜ |
| 2 | About 页下载按钮 | 登录 → 关于 → 点击下载 | ⬜ |
| 3 | 登录页下载链接 | 未登录 → 底部下载链接 | ⬜ |
| 4 | 下载链接 IP 动态获取 | 改服务器地址后刷新页面验证 | ⬜ |
| 5 | 构建脚本输出固定文件名 | `build_apk.ps1` 后检查 `static/download/ims-latest.apk` | ⬜ |
| 6 | App 首次启动看到本地登录页 + 配置引导 | 清除 App 数据后启动 | ⬜ |
| 7 | "使用在线版本"按钮出现 | 配置服务器后登录页出现按钮 | ⬜ |
| 8 | 连通性测试 + Token传递 → 跳转不重登录 | 点按钮 → 跳转 → 直接进入首页 | ⬜ |
| 9 | 连通性测试失败提示 | 关闭服务器 → 点按钮 → 错误提示 | ⬜ |
| 10 | 记住选择后自动跳转 | 重启 App → 自动跳转远程 | ⬜ |
| 11 | 服务器不可达时静默停留 | 关服务器 → 重启 App → 本地页面正常 | ⬜ |
| 12 | "切回本地版本" → 重启回本地 | 远程版 About → 切回 → 重启 | ⬜ |

### 8.2 自动化测试（建议）

```python
# tests/e2e/test_apk_download.py
import requests

BASE_URL = "http://localhost:8000"

def test_apk_endpoint_accessible():
    """测试 APK 下载端点可访问"""
    res = requests.get(f"{BASE_URL}/download/ims-latest.apk", timeout=10)
    assert res.status_code in (200, 404)  # 404 = 无APK文件也正常
    if res.status_code == 200:
        assert res.headers["Content-Type"] in (
            "application/vnd.android.package-archive",
            "application/octet-stream"
        )

def test_health_endpoint():
    """测试健康检查端点（远程加载依赖）"""
    res = requests.get(f"{BASE_URL}/health", timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
```