# 主线B（返厂维修）完成报告

> 完成日期：2026-09-07
> 收尾检查：7 步全部通过

---

## 一、新增数据库表（7 张）

| 表名 | 说明 | 关键外键 |
|------|------|----------|
| `rma_return` | 返厂退货单 | `sku_id` → `product_sku.id`, `assigned_to` → `sys_user.id` |
| `rma_diagnosis` | 诊断报告 | `return_id` → `rma_return.id`, `diagnosed_by` → `sys_user.id` |
| `rma_repair` | 维修工单 | `return_id` → `rma_return.id`, `repair_by` → `sys_user.id` |
| `rma_quality_check` | 质量检验 | `return_id` → `rma_return.id`, `checked_by` → `sys_user.id` |
| `rma_warehouse_in` | 入库审核 | `return_id` → `rma_return.id`, `warehouse_by` → `sys_user.id` |
| `rma_scrap` | 报废申请审批单 | `return_id` → `rma_return.id`, `requested_by` → `sys_user.id`, `approved_by` → `sys_user.id` |
| `rma_reship` | 再出货单 | `return_id` → `rma_return.id`, `operator_id` → `sys_user.id` |

### rma_return 核心字段

| 字段 | 类型 | 说明 |
|------|------|------|
| return_no | VARCHAR(50) UNIQUE | 返厂单号（FC前缀） |
| sku_id | INT FK | 物料SKU |
| sn | VARCHAR(50) | 设备SN |
| status | VARCHAR(30) | 状态（9种状态流转） |
| assigned_to | INT FK | 分配人 |
| assign_type | VARCHAR(20) | 分配类型（PRODUCTION/TEST） |
| problem_description | TEXT | 问题描述 |
| repair_plan | TEXT | 维修方案 |
| new_sn | VARCHAR(50) | 维修后新SN |
| materials_used | TEXT | 维修用料 |
| repair_time_hours | FLOAT | 修复耗时（小时） |
| turnaround_days | INT | 周转周期（天） |
| repair_count | INT | 累计维修次数 |
| diagnosis_result | VARCHAR(30) | 诊断结果 |

---

## 二、新增枚举（5 个）

| 枚举 | 值 |
|------|-----|
| `RmaStatus` | PENDING_DIAGNOSIS / DIAGNOSED / ASSIGNED / REPAIRING / REPAIRED / QUALITY_CHECK / WAREHOUSED / RESHIPPED / SCRAPPED / PENDING_SCRAP |
| `ScrapStatus` | PENDING / APPROVED / REJECTED |
| `DiagnosisResult` | REPAIRABLE |
| `AssignType` | PRODUCTION / TEST / SCRAP |
| `QualityCheckResult` | PASS / FAIL |

文件：`backend/app/models/enums.py`

---

## 三、新增编号生成器

| 函数 | 前缀 | 格式 | 示例 |
|------|------|------|------|
| `generate_return_no()` | FC | FC{YYYYMMDD}{序号} | FC20260907001 |
| `generate_diagnosis_no()` | DG | DG{YYYYMMDD}{序号} | DG20260907001 |
| `generate_repair_no()` | WX | WX{YYYYMMDD}{序号} | WX20260907001 |
| `generate_scrap_no()` | BF | BF{YYYYMMDD}{序号} | BF20260907001 |
| `generate_reship_no()` | RH | RH{YYYYMMDD}{序号} | RH20260907001 |

文件：`backend/app/utils/order_no.py`

---

## 四、新增后端文件

| 文件 | 行数 | 说明 |
|------|:----:|------|
| `backend/app/models/rma.py` | ~200 | 7 个 SQLAlchemy 模型 + relationship |
| `backend/app/schemas/rma.py` | ~120 | Pydantic Schema（Create/Response） |
| `backend/app/api/rma.py` | ~180 | 18 个 API 端点 |
| `backend/app/service/rma_service.py` | ~570 | 业务逻辑（含审计日志） |

### API 端点清单（18 个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/rma/returns` | 返厂单列表（分页+筛选） |
| GET | `/rma/returns/{id}` | 返厂单详情 |
| POST | `/rma/returns` | 创建返厂单 |
| POST | `/rma/returns/{id}/assign` | 分配返厂单 |
| POST | `/rma/returns/{id}/transfer` | 流转返厂单 |
| GET | `/rma/returns/{id}/diagnoses` | 诊断列表 |
| POST | `/rma/diagnoses` | 创建诊断报告 |
| GET | `/rma/returns/{id}/repairs` | 维修工单列表 |
| POST | `/rma/repairs` | 创建维修工单 |
| GET | `/rma/returns/{id}/scraps` | 报废单列表 |
| POST | `/rma/scraps` | 创建报废申请 |
| POST | `/rma/scraps/{id}/approve` | 审批报废单 |
| GET | `/rma/returns/{id}/reships` | 再出货列表 |
| POST | `/rma/reships` | 创建再出货单 |
| GET | `/rma/returns/{id}/quality-checks` | 质检列表 |
| POST | `/rma/quality-checks` | 创建质检报告 |
| GET | `/rma/returns/{id}/warehouse-ins` | 入库记录列表 |
| POST | `/rma/warehouse-ins` | 创建入库审核 |

---

## 五、状态流转

```
待诊断(PENDING_DIAGNOSIS)
  └─ 诊断 → 已诊断(DIAGNOSED)
             └─ 质量负责人判定分配：
                   ├─ 外观问题 → 分配给生产 → 已分配(ASSIGNED)
                   ├─ 功能问题 → 分配给测试 → 已分配(ASSIGNED)
                   └─ 判定报废 → 待报废审批(PENDING_SCRAP)
                                  ├─ 仓库管理员审核通过 → 已报废(SCRAPPED)
                                  └─ 仓库管理员驳回 → 已诊断(DIAGNOSED)

已分配(ASSIGNED)
  └─ 创建维修工单 → 维修中(REPAIRING) → 已修复(REPAIRED)
                                            ├─ 质检通过 → 质量检验(QUALITY_CHECK)
                                            │              └─ 入库审核(零成本仓-成品/半成品) → 已入库(WAREHOUSED)
                                            │                                                   └─ 再出货 → 已再出货(RESHIPPED)
                                            └─ 质检不通过 → 已分配(ASSIGNED) [退回维修]
```

---

## 六、新增前端文件

| 文件 | 说明 |
|------|------|
| `frontend/src/views/RmaReturn.vue` | 返厂维修页面（含退货登记、诊断、分配、维修、质检、入库、报废、再出货全流程） |
| `frontend/src/router/index.js` | 新增路由 `/rma` → `RmaReturn` |

---

## 七、Bug 修复

| 编号 | 问题 | 修复 |
|:----:|------|------|
| BUG-003 | 返厂维修页面中「开始时间」和「结束时间」日期选择器宽度与其他控件不一致 | 添加 `style="width:100%"` 到维修工单弹窗中的开始时间和结束时间 `el-date-picker` 组件 |

---

## 八、收尾检查结果

| 步骤 | 检查项 | 结果 |
|:---:|--------|:----:|
| ① | 代码质量检查（code-quality-skill） | ✅ 通过 |
| ② | 代码异味检测（detect-code-smells） | ✅ 通过 |
| ③ | 技术栈专项检查（fastapi + vue + sqlalchemy） | ✅ 通过 |
| ④ | 浏览器验证（webapp-testing） | ✅ 通过 |
| ⑤ | 后端启动验证（uvicorn） | ✅ 通过 |
| ⑥ | 前端启动验证（vite） | ✅ 通过 |
| ⑦ | 结果记录（本文档） | ✅ 完成 |

### 检查详情

**① 代码质量**：所有函数参数和返回值均有类型提示，API 使用 R.ok() + PageResult 统一封装，审计日志使用 `_write_audit` 统一记录，异常处理使用 ValueError 提供明确错误信息。

**② 代码异味**：函数长度适中（最长约 50 行），模型字段合理（无过度冗余），审计日志模式统一复用，无重复代码。

**③ 技术栈**：FastAPI 路由使用 APIRouter 模块化，SQLAlchemy 使用 Mapped + mapped_column 新式声明，Vue 3 使用 Composition API + script setup。

**④ 浏览器验证**：登录后导航到 `/rma` 页面，确认包含「返厂维修」「退货登记」「返厂单号」等关键元素，页面正常渲染。

**⑤ 后端**：`uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000` 启动成功，日志显示数据库连接正常、定时任务调度器已启动。

**⑥ 前端**：`npm run dev` 启动成功，运行在 `http://localhost:5174/`（5173 被占用，自动切换）。

---

## 九、后续优化建议

1. 对返厂单列表查询添加 Redis 缓存（高频查询）
2. 对返厂单列表添加游标分页支持（大数据量场景）
3. 为 `rma_return.sn` 和 `rma_return.status` 添加复合索引