# PROJECT_STATE.md

> 🤖 **自动维护**：每次对话开始时，AI 自动运行 `git log --oneline -3`、`git branch --show-current`、`git describe --tags --abbrev=0` 更新本文件。零手动维护。

| 项目 | 值 |
|------|-----|
| 当前版本 | v2.7 |
| 当前阶段 | 二期完成 ✅ |
| 当前分支 | `master` |
| 最近 Tag | v2.0-phase2 / v2.0 |
| 检测清单 | 后端 448/448 ✅ \| 前端 124/124 ✅ \| 专项 88/89 ⚠️ |

---

## 一、一期状态（已完成 ✅）

| 主线 | 功能 | 后端测试 | 前端测试 | 说明 |
|------|:---:|:---:|:---:|------|
| A | 采购来料管理 | ✅ | ✅ | 到货→检验→入库→退货 |
| B | 返厂维修 | ✅ | ✅ | 退厂→诊断→维修→质检→入库→再出货/报废 |
| C | 出货管理 | ✅ | ✅ | 出货单 + SN 列表 + 物流 |
| D | BOM 与生产准备 | ✅ | ✅ | BOM 多级 + 生产任务 + 齐套检查 |

---

## 二、二期状态（已完成 ✅）

| 功能 | 模型 | 后端 API | 后端测试 | 前端 API | 前端页面 | 路由菜单 | 优先级 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Station（场站） | ✅ | ✅ | ✅ 11用例 | ✅ | ✅ | ✅ | P0 |
| DeviceLedger（设备台账） | ✅ | ✅ | ✅ 12用例 | ✅ | ✅ | ✅ | P0 |
| Stocktake（盘点） | ✅ | ✅ | ✅ 11用例 | ✅ | ✅ | ✅ | P0 |
| InventoryAdjustment（库存调整） | ✅ | ✅ | ✅ 6用例 | ✅ | ✅ | ✅ | P0 |
| Customer（客户扩展 8 字段） | ✅ | ✅ | ✅ 3用例 | ✅ | ❌ 无需独立页 | ❌ | P0 |
| 安卓 App（Capacitor） | ✅ 配置就绪 | ✅ 插件已装 | — | — | — | ⬜ 需SDK | P1 |
| 轮询提醒 | ✅ 后端端点 | ✅ 前端铃铛 | — | — | — | ✅ | P0 |
| 前端二期单元测试 (5文件) | — | ✅ 37用例 | — | — | — | ✅ | P0 |
| 数据看板（基础版） | — | ✅ | ✅ 合约测试 | ✅ | ✅ | ✅ | P0 |

> 二期后端：5 Model + 5 API + 5 Service + 5 Schema + 6 Contract Test（含Dashboard）+ Unit/Concurrency/Consistency/Scenario = 448用例全部通过
> 二期前端：5 API封装 + 5 Vue页面（含Dashboard）+ 路由配置 + 菜单配置 全部就绪

---

## 三、最近变更（AI 自动获取）

> 🔄 每次对话开始时由 AI 运行以下命令自动更新：

```bash
git log --oneline -3     # 最近3次提交
git branch --show-current # 当前分支
git describe --tags --abbrev=0 2>/dev/null || echo "无 Tag"  # 最近 Tag
```

**最近 3 次提交：**

```
5e0a78e (HEAD -> master) [capacitor] 安卓App集成：Capacitor初始化+Android平台+构建同步+修复MainLayout标签闭合bug
2db001d [doc] 更新PRD v2.7：二期完成状态同步、验收标准统计（24/25=96%）
108fb3a (tag: v2.0-phase2, tag: v2.0) [phase2] 二期5模块 后端+前端测试448全通
```

---

## 四、待办任务池（按执行顺序排列）

> 当前 Git 状态：40+ 修改 + 30+ 新增 未提交。**必须先提交已完成的代码，再继续新任务。**

### 🔴 第一轮：Git 提交（本次会话成果，不可跳过）

| 序号 | 任务 | 涉及文件 | 提交信息 | 优先级 |
|:---:|------|------|------|:---:|
| 1 | N+1查询修复 | `device_ledger_service.py` / `stocktake_service.py` / `inventory_adjustment_service.py` | `[perf] 修复3处N+1查询：DeviceLedger joinedload + Stocktake/Adjustment批量查询` | P0 |
| 2 | 轮询提醒 | `dashboard_service.py` / `dashboard.py` / `dashboard.js` / `usePolling.js` / `MainLayout.vue` / `schemas/dashboard.py` | `[polling] 轮询提醒实现：后端poll-status端点 + 前端usePolling composable + 铃铛徽章` | P0 |
| 3 | 前端二期测试 | `__tests__/{station,deviceLedger,stocktake,adjustment,dashboard}.test.js` + `vitest.config.js` / `vitest.setup.js` | `[test] 前端二期单元测试：5文件37用例覆盖Station/DeviceLedger/Stocktake/Adjustment/DashboardAPI` | P0 |
| 4 | Capacitor配置 | `package.json` / `capacitor.config.json` / `.gitignore` | `[capacitor] App配置完善：core→dependencies + 脚本 + gitignore排除android/ios/` | P0 |
| 5 | 检测清单更新 | `检测项目清单.md` / `PROJECT_STATE.md` | `[doc] 检测清单v2.8：Capacitor App方案（6阶段+5类检查）+ 工作序列` | P0 |
| 6 | 数据看板 | `Dashboard.vue` | `[dashboard] 数据看板：二期看板页面完成` | P0 |

### 🟡 第二轮：打印模块（P1）

| 序号 | 任务 | 涉及文件 | 提交信息 |
|:---:|------|------|------|
| 7 | 打印模块 | `backend/app/api/print.py` / `schemas/print.py` / `frontend/src/api/print.js` / `print/` 组件 / `excel_export.py` / `excel_import.py` | `[print] 打印模块：6种单据打印 + Excel导出导入` |

### 🟢 第三轮：周边工作（P1-P2）

| 序号 | 任务 | 说明 | 优先级 |
|:---:|------|------|:---:|
| 8 | 数据字典生成 | 运行 `generate_data_dict.py` 更新至 44 表 | P1 |
| 9 | Capacitor 插件安装 | `npm install @capacitor/{preferences,status-bar,camera}` | P1 |
| 10 | doc/ 目录整理 | 确认 `主线B完成报告.md` / `主线C完成报告.md` / `二期开发方案.md` 等是否需提交 | P2 |
| 11 | 根目录临时文件清理 | `test_*.py` / `debug_*.py` / `check_*.py` 等移至 tests/ 或删除 | P2 |
| 12 | E2E 测试验证 | 启动前端服务后运行 `tests/e2e/` | P2 |
| 13 | Capacitor 打包 | 需 Android SDK → `cap:add:android` → `cap:sync` → 打 APK | P2 |

---

## 五、已知问题

当前无阻塞性问题。

---

## 六、下次对话建议任务

1. **第一优先级**：按四.1 顺序提交 6 批代码（`git add` + `git commit` + `git push`）
2. 提交打印模块（四.2）
3. 安装 Capacitor 3 个插件（`npm install @capacitor/preferences @capacitor/status-bar @capacitor/camera`）
4. 运行数据字典生成脚本更新至 44 表
5. 清理根目录临时脚本文件

> 维护方式：每个里程碑完成后，由 AI 更新本文件，人工审核确认。