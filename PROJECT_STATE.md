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
| 安卓 App（Capacitor） | — | — | — | — | — | ❌ | P1 |
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
108fb3a (HEAD -> master, tag: v2.0-phase2, tag: v2.0) [phase2] 二期5模块 后端+前端测试448全通：Station/DeviceLedger/Stocktake/InventoryAdjustment/Customer前后端完成，合约/场景/单元/安全测试全通过
0843e95 [doc] 完整重写 reference.md：基于实际代码同步更新全部9章
7013195 [doc] 修正 VibeCoding 手册：24条规则、19个Skill、修正PROJECT_STATE位置
```

---

## 四、待办任务池

| # | 任务 | 改动范围 | 优先级 |
|---|------|----------|:---:|
| 1 | 数据看板提交与验收（当前未提交） | 前后端 6 文件 | P0 |
| 2 | 前端二期单元测试（Phase2 专测） | `frontend/src/__tests__/` | P1 |
| 3 | 数据字典重新生成（44表） | `backend/scripts/generate_data_dict.py` | P1 |
| 4 | E2E测试验证（需启动前端） | `backend/tests/e2e/` | P2 |
| 5 | Capacitor 安卓 App 搭建 | `frontend/` + capacitor | P1 |
| 6 | 轮询提醒功能实现 | `frontend/src/composables/` | P2 |
| 7 | 打印模块提交与验收 | `backend/app/api/print.py` + 前端 | P1 |

---

## 五、已知问题

当前无阻塞性问题。

---

## 六、下次对话建议任务

1. 提交数据看板代码（前后端 6 文件已修改，未提交）
2. 提交打印模块代码（`backend/app/api/print.py` + `schemas/print.py` + 前端 `api/print.js` + `print/`）
3. 创建前端二期单元测试（Phase2 模块：station/stocktake/deviceLedger 等）
4. 运行数据字典生成脚本更新至 44 表
5. 启动前端服务验证 E2E + 跨浏览器测试

> 维护方式：每个里程碑完成后，由 AI 更新本文件，人工审核确认。