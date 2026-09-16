# Bug 记录

> 记录格式：编号、日期、严重程度、模块、现象、根因、修复方案、涉及文件、教训

---

## BUG-001

| 字段 | 内容 |
|------|------|
| 编号 | BUG-001 |
| 日期 | 2026-09-08 |
| 严重程度 | 中 |
| 模块 | 场景测试 - 主线A/B/C/D |
| 现象 | 场景测试多处报 `KeyError: 'data'` 或 `KeyError: 'id'`，测试无法通过 |
| 根因 | API 响应格式不统一：部分端点返回原始数据（Incoming、RMA POST），部分端点返回 `R` 包装数据（Shipment、BOM、RMA GET）。测试代码对响应格式的假设与实际不一致。 |
| 修复方案 | 逐一分析每个 API 端点的实际响应格式，修正测试中的断言：<br/>- Incoming POST/GET → 原始数据，移除 `["data"]`<br/>- RMA POST → 原始数据，移除 `["data"]`<br/>- RMA GET → R 包装，保留 `["data"]`<br/>- Shipment → R 包装，保留 `["data"]`<br/>- BOM POST → R 包装，添加 `["data"]` |
| 涉及文件 | `tests/scenario/test_scenario_mainline_a.py`<br/>`tests/scenario/test_scenario_mainline_b.py`<br/>`tests/scenario/test_scenario_mainline_c.py`<br/>`tests/scenario/test_scenario_mainline_d.py` |
| 教训 | 新模块开发时 API 响应格式应统一。建议在 `app/schemas/common.py` 的 `R` 类文档中注明各模块的响应格式约定。 |

---

## BUG-002

| 字段 | 内容 |
|------|------|
| 编号 | BUG-002 |
| 日期 | 2026-09-08 |
| 严重程度 | 中 |
| 模块 | 返厂维修 - 报废审批流程 |
| 现象 | S006 场景测试报错 `ValueError: 该返厂单已报废`，报废单创建被拦截 |
| 根因 | `rma_service.py` 中诊断结果设为 "SCRAP" 时，立即将返厂单状态设为 "SCRAPPED"。后续创建报废单时，状态校验发现已报废，拒绝创建。 |
| 修复方案 | 移除诊断时对 SCRAP 结果的自动状态设置。改为在报废审批通过时（`approve_scrap`）才将返厂单状态设为 "SCRAPPED"。 |
| 涉及文件 | `app/service/rma_service.py`（诊断逻辑） |
| 教训 | 业务流程的中间状态不应由上游操作自动设置，应由下游操作在完成时设置。避免状态机出现"跳步"问题。 |

---

## BUG-003

| 字段 | 内容 |
|------|------|
| 编号 | BUG-003 |
| 日期 | 2026-09-08 |
| 严重程度 | 低 |
| 模块 | 场景测试 - 主线C |
| 现象 | `assert res.status_code != 200` 断言失败，删除出货单后查询返回 200 |
| 根因 | 删除成功后查询已删除的出货单，API 使用 `R.fail()` 返回 HTTP 200 但 `code=-1`，不是 404。 |
| 修复方案 | 将断言改为 `assert res.json()["code"] != 0`，检查业务错误码而非 HTTP 状态码。 |
| 涉及文件 | `tests/scenario/test_scenario_mainline_c.py` |
| 教训 | 项目使用 `R` 统一包装，业务错误返回 HTTP 200 + code≠0。测试断言应检查 `code` 字段，而非 HTTP 状态码。 |

---

## BUG-004

| 字段 | 内容 |
|------|------|
| 编号 | BUG-004 |
| 日期 | 2026-09-08 |
| 严重程度 | 低 |
| 模块 | 场景测试 - 主线D |
| 现象 | 齐套分析断言 `assert availability["items"][0]["required_qty"] == 210.0` 失败，实际值为 200.0 |
| 根因 | BOM 创建时物料数量为 200，齐套分析中 required_qty 应为 200.0 而非 210.0。测试预期值写错。 |
| 修复方案 | 将预期值从 210.0 修正为 200.0。 |
| 涉及文件 | `tests/scenario/test_scenario_mainline_d.py` |
| 教训 | 测试预期值应与测试数据保持一致，避免复制粘贴导致的数值错误。 |

---

## BUG-005

| 字段 | 内容 |
|------|------|
| 编号 | BUG-005 |
| 日期 | 2026-09-16 |
| 严重程度 | 高 |
| 模块 | 移动端 - 扫码录入 |
| 现象 | 安装 APK 后打开扫码功能，不弹摄像头权限申请对话框，直接提示"原生扫码未识别请手动输入" |
| 根因 | ① `@capacitor/barcode-scanner` v3.1.2 不声明 `CAMERA` 权限也不内部请求权限；② 前端用 `BarcodeScanner.checkPermissions()` 但该 API 在 v3.1.2 不存在，抛异常后被 catch 吞掉；③ 改用 `Camera.checkPermissions()` 仍无效，因为 WebView 层 JS 调用 `Camera.requestPermissions()` 可能因 Capacitor 桥未就绪而失败 |
| 修复方案 | 在 `MainActivity.java` 的 `onCreate()` 中用原生 `ActivityCompat.requestPermissions()` 直接请求 `CAMERA` 权限，不依赖 JS 层权限调用。`BarcodeScanner.startScan()` 恢复为直接调用。 |
| 涉及文件 | `BarcodeScanner.vue`、`MainActivity.java`、`AndroidManifest.xml` |
| 教训 | Capacitor 插件的权限 API 版本差异大，建议在 Android 原生层用 `ActivityCompat.requestPermissions()` 统一处理敏感权限，不依赖 JS 层。 |

---

## BUG-006

| 字段 | 内容 |
|------|------|
| 编号 | BUG-006 |
| 日期 | 2026-09-16 |
| 严重程度 | 中 |
| 模块 | 移动端 - 表格操作列 |
| 现象 | 手机端表格左右滑动时，操作列固定在右侧不跟随滚动，占据大量屏幕空间 |
| 根因 | 所有列表页的 `el-table-column` 操作列设置了 `fixed="right"` 属性，Element Plus 将其渲染为独立的固定层（`el-table__fixed-right`），脱离主表格滚动流。CSS 隐藏固定层方案不可靠（部分场景仍有显示问题）。 |
| 修复方案 | 批量移除 19 个 Vue 文件中所有操作列的 `fixed="right"` 属性，在 `style.css` 手机端媒体查询中设 `th:last-child, td:last-child { max-width:100px }` 限制宽度 |
| 涉及文件 | `style.css` + 19 个 views/*.vue（BOM、Customer、Dashboard、DeviceLedger、Inbound、IncomingReceipt、InventoryDetail、InventorySkuSummary、Outbound、Partners、ProductionTask、Products、RmaReturn、Settings、Shipment、SnapshotDetails、SnapshotLedger、Station、Stocktake） |
| 教训 | 移动端表格固定列体验差，应从源头去掉 `fixed` 属性而非仅用 CSS 覆盖。批量修改用 PowerShell `-replace` 高效可靠。 |

---

## BUG-007

| 字段 | 内容 |
|------|------|
| 编号 | BUG-007 |
| 日期 | 2026-09-16 |
| 严重程度 | 中 |
| 模块 | 移动端 - 侧边菜单 |
| 现象 | 手机端左侧菜单栏无法上下滚动，菜单项多时被截断无法看到底部菜单 |
| 根因 | `.aside--mobile` 设置了 `overflow-y:auto` 但内部 `el-menu` 组件没有弹性布局约束，`overflow` 实际未生效 |
| 修复方案 | `.aside--mobile` 改为 `display:flex; flex-direction:column; overflow:hidden`；`.aside--mobile .el-menu` 新增 `flex:1; overflow-y:auto; overflow-x:hidden` |
| 涉及文件 | `MainLayout.vue` |
| 教训 | Element Plus 的 `el-menu` 在 flex 容器中需显式设 `flex:1` + `overflow-y:auto` 才能滚动；父容器 `overflow-y:auto` 在子元素无明确高度时不会生效。 |

---

## BUG-008

| 字段 | 内容 |
|------|------|
| 编号 | BUG-008 |
| 日期 | 2026-09-15 |
| 严重程度 | 高 |
| 模块 | 全局异常处理 |
| 现象 | 冒烟测试 4 项失败：对不存在的资源（到货单/报废单）发起操作时，API 返回 500 而非 400/404。合约测试 2 项断言 `status_code == 500` 通过（实为 Bug 得到"正确的错误结果"）。 |
| 根因 | `main.py` 的全局 `Exception` 处理器将服务层抛出的 `ValueError`（如"到货单不存在"、"状态不允许操作"）统一返回 `500 服务器内部错误`。FastAPI 异常处理器的优先级规则是"子类先于父类"，但 `ValueError` 没有专用处理器，被最宽泛的 `Exception` 处理器捕获。 |
| 修复方案 | 在 `Exception` 处理器之前添加 `@app.exception_handler(ValueError)`，返回 `400 Bad Request` + `str(exc)` 作为 `msg`。同时将 2 个合约测试的断言从 `500` 修正为 `400`。 |
| 涉及文件 | `main.py`（新增 ValueError 处理器）<br/>`tests/contract/test_incoming_contract.py`（500→400）<br/>`tests/contract/test_rma_contract.py`（500→400） |
| 教训 | ① 全局异常处理器必须为业务异常（ValueError、KeyError 等）设置专用处理器，不能只依赖最宽泛的 `Exception`；② 测试不应将"错误的 HTTP 状态码"当作正确行为来断言。 |

---

## BUG-009

| 字段 | 内容 |
|------|------|
| 编号 | BUG-009 |
| 日期 | 2026-09-15 |
| 严重程度 | 高 |
| 模块 | E2E 测试 / API 配置 |
| 现象 | E2E 测试 3 项全部失败：Playwright 登录后页面停留在 `/login`，未跳转到 `/dashboard`，`wait_for_url("**/dashboard**")` 超时（15s→30s 均超时）。Control 测试 10 项通过但 3 项登录流程失败。 |
| 根因 | `frontend/src/utils/apiConfig.js` 的 `DEFAULT_BASE_URL` 硬编码为 `http://192.168.10.77:8000`。开发环境下前端页面通过 `localhost:5176` 访问，但 Axios 直接向 `192.168.10.77:8000` 发请求，绕过 Vite 的 `/api` 代理，触发浏览器 CORS 拦截。登录 API 失败后 `router.push('/dashboard')` 无法执行。 |
| 修复方案 | ① `DEFAULT_BASE_URL` 改为空字符串 `''`，使 Axios 使用相对路径，经 Vite 代理转发到后端；② 修复 `cachedBaseUrl` 的空值判断（`if cachedBaseUrl` → `if cachedBaseUrl !== null`），避免空字符串被误判为"未初始化"；③ E2E 测试超时从 15s 增至 30s，登录后增加 `wait_for_load_state("networkidle")`。 |
| 涉及文件 | `frontend/src/utils/apiConfig.js`<br/>`tests/e2e/test_e2e_flows.py` |
| 教训 | ① 前端 API 基础 URL 在开发环境下必须为空或 `/`，不能硬编码具体 IP，否则绕过 Vite 代理导致 CORS；② 布尔判断空字符串时要区分"未初始化"（null）和"空值"（''），用 `!== null` 而非 truthy 判断。 |