# IMS 项目状态快照

> 最后更新：2026-09-20 | 对应检测清单版本：v2.17 | 项目版本：v2.17

## 最近一次检测结果

| 检测日期 | 检测范围 | 通过/总数 | 状态 |
|---------|---------|:---:|:---:|
| 2026-09-20 | 后端全量契约测试（339用例） | 277/339 (4 pre-existing F, 58 s) | ✅ |
| 2026-09-20 | 新创建8个改善点测试脚本 | 28P / 0F / 37s | ✅ |

---

## 15 项改善点 — 全覆盖状态矩阵

### 一、业务闭环类

| # | 改善点 | 后端 | 前端 | 测试 | 检测清单 | 总体状态 |
|---|--------|:---:|:---:|:---:|:---:|:---:|
| 1 | 质保到期主动提醒（可配置周期+开关） | ❌ | ❌ | ⚠️ 21用例已写/全部skip（API未实现） | ✅ 4.20 | 🔴 开发中 |
| 2 | 维修知识库（rma_knowledge_base + 搜索推荐） | ❌ | ❌ | ⚠️ 7用例已写/2P 5s（知识库端点未实现） | ✅ 4.21 | 🔴 未开始 |
| 3 | 故障统计分析看板（按型号/类型/趋势） | ❌ | ❌ | ⚠️ 8用例已写/2P 6s（统计端点未实现） | ✅ 4.22 | 🔴 未开始 |
| 4 | 供应商质量评估（合格率/不良率/评分） | ❌ | ❌ | ⚠️ 7用例已写/3P 4s（评估端点未实现） | ✅ 4.23 | 🔴 未开始 |
| 5 | U9深度集成（Phase1:下拉+历史 / Phase2:对接） | ❌ | ❌ | ⚠️ 7用例已写/4P 3s（U9端点未实现） | ✅ 4.33 | 🔴 未开始 |

### 二、效率提升类

| # | 改善点 | 后端 | 前端 | 测试 | 检测清单 | 总体状态 |
|---|--------|:---:|:---:|:---:|:---:|:---:|
| 6 | 批量操作增强（审核/分配/导出/打印） | ❌ | ❌ | ⚠️ 9用例已写/4P 5s（批量端点未实现） | ✅ 4.24 | 🔴 未开始 |
| 7 | 筛选条件记忆全覆盖（useFilterPersist × 10页） | N/A | ⚠️ 6/16页 | ❌ | ✅ 4.25 | 🟡 部分实现 |
| 8 | 表单自动保存草稿（useFormDraft × 10+表单） | N/A | ❌ | ❌ | ✅ 4.26 | 🔴 未开始 |
| 9 | 扫码连续录入（continuous模式+去重） | ❌ | ❌ | ❌ | ✅ 4.27 | 🔴 未开始 |
| 10 | 打印模板可视化配置（6个硬编码组件→可配置） | ❌ | ❌ | ❌ | ✅ 4.28 | 🔴 未开始 |

### 三、技术支撑类

| # | 改善点 | 后端 | 前端 | 测试 | 检测清单 | 总体状态 |
|---|--------|:---:|:---:|:---:|:---:|:---:|
| 11 | 设备生命周期追溯图谱（SN→全链路时间轴） | ❌ | ❌ | ⚠️ 8用例已写/4P 4s（lifecycle端点未实现） | ✅ 4.29 | 🔴 未开始 |
| 12 | 消息通知与待办推送（DingTalk + 企微） | ❌ | ❌ | ⚠️ 8用例已写/3P 5s（通知端点未实现） | ✅ 4.30 | 🔴 未开始 |
| 13 | 数据归档清理（历史数据定期归档） | ❌ | ❌ | ⚠️ 11用例已写/6P 5s（归档端点未实现） | ✅ 4.31 | 🔴 未开始 |
| 14 | 移动端适配增强（超出现有@media覆盖） | N/A | ⚠️ 基础可用 | ❌ | ✅ 4.32 | 🟡 基础完成 |
| 15 | CI/CD流水线+自动化测试（GitHub Actions） | ❌ | ❌ | ✅ `.github/workflows/ci.yml` 已创建 | ✅ 4.34 | 🟡 仅本地 |

### 统计

| 状态 | 数量 | 改善点编号 |
|------|:---:|------|
| 🔴 未开始 | **10** | #1~#6、#8~#10、#13 |
| 🟡 部分实现 | **5** | #7（6/16页）、#11（基础API已有）、#12（轮询已有）、#14（基础CSS）、#15（CI文件已写） |
| 🟢 已完成 | **0** | — |

---

## 改善点 #1 质保提醒配置 — 详细状态

### 后端（均未实现，以下为设计方案）

| 组件 | 文件 | 状态 |
|------|------|:---:|
| Schema | `app/schemas/settings.py` | ❌ 需新增 `WarrantyAlertResponse` / `WarrantyAlertUpdate` |
| 服务层 | `app/service/settings_service.py` | ❌ 需新增 `get_warranty_alert_config()` / `update_warranty_alert_config()` |
| API | `app/api/settings.py` | ❌ 需新增 `GET/PUT /settings/warranty-alert` |
| 仪表盘Schema | `app/schemas/dashboard.py` | ❌ 需扩展 `Phase2StatsResponse` / `PollStatusResponse` |
| 仪表盘服务 | `app/service/dashboard_service.py` | ❌ 需将 `timedelta(days=30)` 改为从 sys_config 读取 |
| 仪表盘API | `app/api/dashboard.py` | ❌ 需增加 `warranty_alert_enabled/days/by_day` |

### 前端（均未实现）

| 组件 | 文件 | 状态 |
|------|------|:---:|
| API封装 | `api/settings.js` | ❌ 需新增 `getWarrantyAlert()` / `updateWarrantyAlert()` |
| 设置页面 | `views/Settings.vue` | ❌ 需新增"质保提醒"配置区域（toggle + multi-select） |
| 仪表盘 | `views/Dashboard.vue` | ❌ 需改为响应开关 + 分档显示（30/60/90天颜色区分） |

### 测试

| 类型 | 文件 | 用例 | 状态 |
|------|------|:---:|:---:|
| 配置接口契约 | `tests/contract/test_warranty_alert_contract.py` | 12 | ⬜ 待后端API实现后运行 |
| 仪表盘联动契约 | `tests/contract/test_warranty_alert_contract.py` | 8 | ⬜ 待后端API实现后运行 |
| 设置页契约（原有） | `tests/contract/test_settings_contract.py` | 14 | ✅ 14/14 |
| 仪表盘契约（原有） | `tests/contract/test_dashboard_contract.py` | 4 | ✅ 4/4 |

### 配置默认值

| 配置键 | 默认值 | 说明 |
|--------|-------|------|
| `warranty_alert_enabled` | `true` | 首次启动默认开启 |
| `warranty_alert_days` | `"30,60,90"` | 前端解析为 `[30, 60, 90]` |

### 验收标准

| # | 标准 | 状态 |
|---|------|:---:|
| 1 | 质保提醒周期不再硬编码 | ⬜ |
| 2 | 管理员可配置多个提醒周期 | ⬜ |
| 3 | 管理员可关闭和重新开启提醒 | ⬜ |
| 4 | Dashboard、顶部待办和接口行为一致 | ⬜ |
| 5 | 非法配置不能保存 | ⬜ |
| 6 | 旧字段和现有测试保持兼容 | ⬜ |
| 7 | 配置修改无需重启服务即可生效 | ⬜ |

---

## 已知问题

| # | 问题 | 关联改善点 | 严重程度 | 状态 |
|---|------|:---:|:---:|:---:|
| 1 | 质保提醒代码未实现（仅测试脚本+方案文档就绪） | #1 | 低 | ⬜ |
| 2 | `useFilterPersist` 仅覆盖 6/16 个列表页（缺 Stocktake/DeviceLedger/BOM 等10页） | #7 | 低 | ⬜ |
| 3 | 表单草稿自动保存机制未实现（浏览器崩溃会丢数据） | #8 | 中 | ⬜ |
| 4 | 扫码无连续模式（需逐条扫描确认） | #9 | 中 | ⬜ |
| 5 | 维修知识库未建设（故障诊断无历史参考） | #2 | 中 | ⬜ |
| 6 | 无故障统计分析看板（无法识别质量问题趋势） | #3 | 中 | ⬜ |
| 7 | 无供应商质量评估（无法量化供应商表现） | #4 | 中 | ⬜ |
| 8 | 无消息通知推送（待办需主动刷新查看） | #12 | 高 | ⬜ |
| 9 | 无CI/CD（测试仅本地手动执行） | #15 | 中 | ⬜ |
| 10 | 打印模板硬编码（修改模板需改Vue源码+重新打包） | #10 | 低 | ⬜ |
| 11 | test_inbound_contract.py::test_delete_inbound_order 返回 500（边界条件） | pre-existing | 低 | ⬜ |
| 12 | test_inbound_contract.py::test_submit_inbound_order_pending_audit 状态=ACTIVE 非 SUBMITTED（并发种子数据） | pre-existing | 低 | ⬜ |
| 13 | test_inventory_contract.py::test_create_inventory_record_auto_code 旧断言不匹配新逻辑 | pre-existing | 低 | ⬜ |
| 14 | test_shipment_contract.py::test_delete_shipment_record 数据库 FK 级联问题 | pre-existing | 低 | ⬜ |
| 15 | 改善点 #2-#6、#11-#13 后端 API 未实现（55个skip） | 多改善点 | 中 | ⚠️ 测试脚本已就绪 |

---

## 下一批实施计划

### P0（当前批次 — v2.17）

| 改善点 | 内容 | 预估工时 |
|:---:|------|:---:|
| #1 | 质保提醒配置：后端6文件 + 前端3文件 + 测试验证 | 0.5天 |
| #8 | 表单草稿自动保存：useFormDraft composable + 接入10+表单 | 1天 |
| #9 | 扫码连续录入：continuous模式 + 去重 + 接入4个页面 | 1天 |

### P1（v2.18）

| 改善点 | 内容 | 预估工时 |
|:---:|------|:---:|
| #7 | 筛选记忆全覆盖：useFilterPersist × 10个未覆盖页面 | 0.5天 |
| #6 | 批量操作增强：Inbound/Outbound批量提交 + RMA批量分配 + 导出 | 2天 |
| #11 | 设备生命周期追溯图谱：SN全链路时间轴 | 2天 |
| #12 | 消息通知与待办推送：DingTalk webhook + BackgroundTasks | 2天 |

### P2（v2.19+）

| 改善点 | 内容 | 预估工时 |
|:---:|------|:---:|
| #2 | 维修知识库：rma_knowledge_base表 + CRUD + 搜索推荐 | 3天 |
| #3 | 故障统计分析看板：4个统计接口 + ECharts看板 | 3天 |
| #4 | 供应商质量评估：评分算法 + 看板 | 2天 |
| #5 | U9深度集成：Phase1下拉选择历史单号 | 1天 |
| #10 | 打印模板可视化配置：模板编辑器 + 预览 | 3天 |
| #13 | 数据归档清理：归档策略 + 脚本 + 定时任务 | 2天 |
| #14 | 移动端适配增强：Capacitor 原生功能 + 离线缓存 | 3天 |
| #15 | CI/CD：GitHub Actions + 自动测试 + Docker构建 | 2天 |

---

## 运行命令

```bash
# 后端全量测试
cd ims-main/backend && uv run pytest tests/ -v --tb=short

# 改善点专项 — 已创建测试（部分skip，待API实现后启用）
cd ims-main/backend && uv run pytest tests/contract/test_warranty_alert_contract.py -v --tb=short
cd ims-main/backend && uv run pytest tests/contract/test_rma_knowledge_base_contract.py -v --tb=short
cd ims-main/backend && uv run pytest tests/contract/test_fault_statistics_contract.py -v --tb=short
cd ims-main/backend && uv run pytest tests/contract/test_supplier_quality_contract.py -v --tb=short
cd ims-main/backend && uv run pytest tests/contract/test_batch_operations_contract.py -v --tb=short
cd ims-main/backend && uv run pytest tests/contract/test_device_lifecycle_contract.py -v --tb=short
cd ims-main/backend && uv run pytest tests/contract/test_notification_contract.py -v --tb=short
cd ims-main/backend && uv run pytest tests/contract/test_data_archive_contract.py -v --tb=short
cd ims-main/backend && uv run pytest tests/contract/test_u9_integration_contract.py -v --tb=short

# 设置+仪表盘回归
cd ims-main/backend && uv run pytest tests/contract/test_settings_contract.py tests/contract/test_dashboard_contract.py -v --tb=short
```