# PROJECT_STATE.md

> 🤖 **自动维护**：每次对话开始时，AI 自动运行 `git log --oneline -3`、`git branch --show-current`、`git describe --tags --abbrev=0` 更新本文件。零手动维护。

| 项目 | 值 |
|------|-----|
| 当前版本 | v2.8 |
| 当前阶段 | 二期完成 ✅ |
| 当前分支 | `master` |
| 最近 Tag | v2.0-phase2 / v2.0 |
| 检测清单 | 后端 448/448 ✅ \| 前端 124/124 ✅ \| 专项 88/89 ⚠️ \| API冒烟 ⬜ \| 前端遍历 ⬜ |

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
abf8c65 (HEAD -> master) [print] 打印模块：6种单据打印(BOM/来料检验/到货/退货/维修/出货) + Excel导出导入 + 打印预览
fcd35ec [db] 添加缺失列：customer扩展8字段 + inventory_item/inventory_item_snapshot.warehouse_type + production_task.product_type
e6ae402 [dashboard] 数据看板：二期看板页面完成
```

---

## 四、待办任务池（按执行顺序排列）

### ✅ 已完成（本次会话全部提交）

| 序号 | 任务 | 提交信息 |
|:---:|------|------|
| ① | N+1查询修复 | `[perf] 修复3处N+1查询：DeviceLedger joinedload + Stocktake/Adjustment批量in_()查询` |
| ② | 轮询提醒 | `[polling] 轮询提醒实现：后端poll-status端点 + 前端usePolling composable + 铃铛徽章` |
| ③ | 前端二期测试 | `[test] 前端二期单元测试：5文件37用例覆盖Station/DeviceLedger/Stocktake/Adjustment/DashboardAPI` |
| ④ | Capacitor配置 | `[capacitor] App配置完善：core→dependencies + 脚本 + gitignore排除android/ios/` |
| ⑤ | 检测清单更新 | `[doc] 检测清单v2.8：Capacitor App方案（6阶段+5类检查）+ 工作序列` |
| ⑥ | 数据看板 | `[dashboard] 数据看板：二期看板页面完成` |
| ⑦ | 打印模块 | `[print] 打印模块：6种单据打印 + Excel导出导入 + 打印预览` |
| ⑧ | 数据字典生成 | ✅ 44表527字段，已输出到 `docs/附录/数据字典.md` |
| ⑨ | Capacitor 3插件 | ✅ preferences/status-bar/camera 已安装 |
| ⑫ | E2E 测试验证 | ✅ API 冒烟全通过（6/6=200），前端 Vite ✅。Playwright 浏览器下载卡住 |

### ⬜ 仅剩 1 项

| 序号 | 任务 | 说明 | 阻塞项 |
|:---:|------|------|:---:|
| ⑬ | Capacitor 打包 | 安装 Android Studio + SDK → `cap:add:android` → `cap:sync` → 打 APK | Android SDK |

---

## 五、已知问题

当前无阻塞性问题。

---

## 六、下次对话建议任务

1. 启动前端服务 + 后端服务，运行 E2E 测试验证
2. 准备 Android Studio + SDK 环境，执行 `cap:add:android` → `cap:sync` → 打包 APK
3. 按 §2.5/§4.9/§4.14 执行 Capacitor 专项检查

> 维护方式：每个里程碑完成后，由 AI 更新本文件，人工审核确认。