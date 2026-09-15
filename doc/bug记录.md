# 敦临 IMS Bug 记录

> 每次发现 Bug 即时记录，供后续排查参考。

---

## Bug #001：来料管理列表页数据不显示（空白）

| 字段 | 内容 |
|------|------|
| **编号** | BUG-001 |
| **发现日期** | 2026-09-04 |
| **严重程度** | 🔴 高（功能不可用） |
| **模块** | 主线A·来料管理 |
| **状态** | ✅ 已修复 |

### 现象
进入「来料管理」页面，表格区域为空白，列表不显示任何数据。后端 API 返回5条记录正常，前端无报错提示。

### 根因
后端 API 返回格式不统一：
- 其他模块 API 使用 `R.ok(data=PageResult(...))` 包装，返回 `{ code: 0, data: { total, items } }`
- 来料模块 API 直接返回 `{ total, items }`，缺少 `code` 和 `data` 包装层
- 前端统一使用 `res.data.items` 取值，来料模块的 `res.data` 为 `undefined`，导致表格无数据

### 修复
在 `backend/app/api/incoming.py` 的 `list_receipts` 接口中，使用 `R.ok()` + `PageResult` 包装，与其他 API 保持一致。

### 涉及文件
- `backend/app/api/incoming.py` (L38-41)

### 教训
**新增 API 返回列表数据时，必须统一使用 `R.ok(data=PageResult(...))` 格式。**

---

## Bug #002：到货登记/检验 500 错误（created_at 无默认值）

| 字段 | 内容 |
|------|------|
| **编号** | BUG-002 |
| **发现日期** | 2026-09-04 |
| **严重程度** | 🔴 高（Create 操作不可用） |
| **模块** | 主线A·来料管理 |
| **状态** | ✅ 已修复 |

### 现象
点击「到货登记」提交时报 500 错误，来料检验同样报 500。后端日志：`Field 'created_at' doesn't have a default value`。

### 根因
Alembic 迁移脚本创建 `incoming_receipt`/`incoming_inspection`/`incoming_return` 三张表时，`created_at` 和 `updated_at` 列只写了 `nullable=False`，没有设置 `server_default`。模型中的 `TimestampMixin` 使用了 `server_default=func.now()`，但迁移脚本未同步。

### 修复
1. 迁移脚本三张表统一添加 `server_default=sa.text("CURRENT_TIMESTAMP")` 和 `server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")`
2. 对已存在的表执行 `ALTER TABLE ... MODIFY` 补充默认值

### 涉及文件
- `backend/alembic/versions/q1r2s3t4u5v6_create_incoming_tables.py`

### 教训
**所有新表迁移脚本，created_at/updated_at 必须带 server_default。**

---

## Bug #003：退货提交 422 错误（operator_id 必填）

| 字段 | 内容 |
|------|------|
| **编号** | BUG-003 |
| **发现日期** | 2026-09-04 |
| **严重程度** | 🟡 中（功能不可用） |
| **模块** | 主线A·来料管理 |
| **状态** | ✅ 已修复 |

### 现象
点击「退货」提交时报 422 错误：`Field required: operator_id`。前端表单没有 operator_id 输入框。

### 根因
`IncomingReturnCreate` 的 `operator_id` 字段类型为 `int`（必填），但前端未传递该字段，后端也未像其他 API 一样从 `current_user` 自动填充。

### 修复
1. Schema 中 `operator_id` 改为 `int | None = None`（可选）
2. API 中 `create_return` 增加 `if data.operator_id is None: data.operator_id = current_user.id`

### 涉及文件
- `backend/app/schemas/incoming.py` (L86)
- `backend/app/api/incoming.py` (L95-96)

### 教训
**操作人 ID 应从 `current_user` 自动填充，Schema 中设为 Optional，前端不传。**

---

## Bug #004：audit_log 写入报错（created_at 无默认值）

| 字段 | 内容 |
|------|------|
| **编号** | BUG-004 |
| **发现日期** | 2026-09-04 |
| **严重程度** | 🔴 高（审计日志写入失败） |
| **模块** | 主线A·审计日志 |
| **状态** | ✅ 已修复 |

### 现象
到货登记/检验/退货操作时，后台报 500 错误：`Column 'created_at' cannot be null`。`sys_audit_log` 表写入失败。

### 根因
`AuditLog` 模型继承 `Base`（非 `TimestampMixin`），`created_at` 字段无 `server_default`。来料模块新增审计日志写入时，未显式设置 `created_at` 值，导致插入 NULL。

### 修复
1. `AuditLog` 模型 `created_at` 添加 `server_default=func.now()`
2. `_write_audit` 函数中显式设置 `created_at=datetime.now()`
3. 数据库 `ALTER TABLE` 补充默认值

### 涉及文件
- `backend/app/models/audit_log.py` (L29)
- `backend/app/service/incoming_service.py` (L75)

### 教训
**所有模型的时间戳字段必须有 server_default，审计日志写入时显式设置 created_at 兜底。**

---

## Bug #005：来料操作未写入审计日志

| 字段 | 内容 |
|------|------|
| **编号** | BUG-005 |
| **发现日期** | 2026-09-04 |
| **严重程度** | 🟡 中（审计追溯缺失） |
| **模块** | 主线A·审计日志 |
| **状态** | ✅ 已修复 |

### 现象
执行到货登记、来料检验、退货操作后，`sys_audit_log` 表中无对应记录。仅有登录日志，无法追溯谁在何时做了什么操作。

### 根因
`incoming_service` 中 `create_receipt`/`create_inspection`/`create_return` 均未调用审计日志写入逻辑。

### 修复
新增 `_write_audit` 通用函数，在四个操作（到货登记、检验、退货、确认入库）中均写入审计日志，包含操作人、模块、资源类型、单号、摘要、变更原因、IP 地址。

### 涉及文件
- `backend/app/service/incoming_service.py` (L47-L75, L96-L105, L225-L235, L268-L278, L307-L317)
- `backend/app/api/incoming.py` (所有 create 端点增加 `request: Request` 参数)

### 教训
**新增模块必须同步接入审计日志，不可遗漏。**

---

## Bug #006：来料关键字搜索仅匹配单号/批次号

| 字段 | 内容 |
|------|------|
| **编号** | BUG-006 |
| **发现日期** | 2026-09-04 |
| **严重程度** | 🟢 低（功能不完善） |
| **模块** | 主线A·来料管理 |
| **状态** | ✅ 已修复 |

### 现象
在搜索框输入物料名称"空开"，搜索结果为 0。用户无法通过物料名称或编码查找来料记录。

### 根因
`get_receipts` 关键字过滤仅匹配 `receipt_no`（到货单号）和 `batch_no`（批次号），未 JOIN `product_sku` 表匹配物料名称和编码。

### 修复
关键字搜索增加 `ProductSku.name.like()` 和 `ProductSku.sku_code.like()` 条件，同时将 JOIN 逻辑提前到关键字过滤阶段。

### 涉及文件
- `backend/app/service/incoming_service.py` (L142-L148)

### 教训
**列表页关键字搜索应覆盖所有用户可能输入的字段：单号、名称、编码。**

---

## 模板（新 Bug 复制此格式）

| 字段 | 内容 |
|------|------|
| **编号** | BUG-XXX |
| **发现日期** | YYYY-MM-DD |
| **严重程度** | 🔴高 / 🟡中 / 🟢低 |
| **模块** | 主线X·XXX |
| **状态** | 🔴未修复 / 🟡进行中 / ✅已修复 |

### 现象
（描述用户看到的现象）

### 根因
（分析根本原因）

### 修复
（修复方案）

### 涉及文件
- `path/to/file`

### 教训
**列表页关键字搜索应覆盖所有用户可能输入的字段：单号、名称、编码。**

---

## Bug #007：返厂维修Alembic迁移缺少新表和字段

| 字段 | 内容 |
|------|------|
| **编号** | BUG-007 |
| **发现日期** | 2026-09-04 |
| **严重程度** | 🔴 高（数据库缺表/缺字段） |
| **模块** | 主线B·返厂维修 |
| **状态** | ✅ 已修复 |

### 现象
`rma_quality_check`、`rma_warehouse_in` 两张表不存在，`rma_return` 表缺少 `spec`/`assign_type`/`diagnosis_result` 等13个字段，`rma_diagnosis` 缺少 `repair_plan`/`inspection_report_no`，`rma_repair` 缺少 `start_time`/`end_time`。

### 根因
模型定义（`rma.py`）与 Alembic 迁移脚本（`bdbe653a2582`）不同步。模型新增了字段和表，但迁移脚本未同步更新。

### 修复
创建新迁移 `c1d2e3f4g5h6_add_rma_missing_fields.py`，补充：
- 新增 `rma_quality_check` 表（质量检验记录）
- 新增 `rma_warehouse_in` 表（入库审核记录）
- `rma_return` 新增13个字段
- `rma_diagnosis` 新增2个字段
- `rma_repair` 新增2个字段

### 涉及文件
- `backend/alembic/versions/c1d2e3f4g5h6_add_rma_missing_fields.py`
- `backend/app/models/rma.py`
- `backend/app/models/__init__.py`

### 教训
**模型变更后必须同步创建 Alembic 迁移脚本，不可遗漏。**

---

## Bug #008：RMA模型未导入 __init__.py

| 字段 | 内容 |
|------|------|
| **编号** | BUG-008 |
| **发现日期** | 2026-09-04 |
| **严重程度** | 🟡 中（Alembic autogenerate 无法发现） |
| **模块** | 主线B·返厂维修 |
| **状态** | ✅ 已修复 |

### 现象
`models/__init__.py` 未导入 RMA 相关模型，导致 Alembic `--autogenerate` 无法发现新增表。

### 根因
新增模型文件后忘记在 `__init__.py` 中注册导入。

### 修复
在 `models/__init__.py` 中添加 `from app.models.rma import RmaReturn, RmaDiagnosis, RmaRepair, RmaQualityCheck, RmaWarehouseIn, RmaScrap, RmaReship`。

### 涉及文件
- `backend/app/models/__init__.py`

### 教训
**新增模型文件后必须在 `__init__.py` 中导入，供 Alembic 发现。**

---

## Bug #009：API缺少质量检验/入库审核端点

| 字段 | 内容 |
|------|------|
| **编号** | BUG-009 |
| **发现日期** | 2026-09-04 |
| **严重程度** | 🔴 高（功能不可用） |
| **模块** | 主线B·返厂维修 |
| **状态** | ✅ 已修复 |

### 现象
前端无法调用质量检验和入库审核接口，404 错误。

### 根因
`api/rma.py` 缺少 `POST /quality-checks`、`POST /warehouse-ins`、`GET /returns/{id}/quality-checks`、`GET /returns/{id}/warehouse-ins` 四个端点。

### 修复
在 `api/rma.py` 中新增四个端点，并在 `schemas/rma.py` 中导入对应的 Schema。

### 涉及文件
- `backend/app/api/rma.py`
- `backend/app/schemas/rma.py`

### 教训
**Service 层函数写完后，API 路由层必须同步暴露端点。**

---

## Bug #010：前端缺少质量检验/入库审核弹窗

| 字段 | 内容 |
|------|------|
| **编号** | BUG-010 |
| **发现日期** | 2026-09-04 |
| **严重程度** | 🔴 高（用户无法操作） |
| **模块** | 主线B·返厂维修 |
| **状态** | ✅ 已修复 |

### 现象
返厂维修页面缺少"质量检验"和"入库审核"两个操作弹窗，分配弹窗缺少"分配类型"和"分配原因"字段，维修弹窗缺少"开始时间"/"结束时间"，操作按钮状态流转不正确。

### 根因
前端页面开发时未包含质量检验和入库审核环节，分配/维修弹窗字段不完整。

### 修复
1. 新增质量检验弹窗（检验人、检验日期、检验结果、检验描述、变更原因）
2. 新增入库审核弹窗（新SN、维修次数、维修原因、变更原因）
3. 分配弹窗新增"分配类型"（生产/测试）和"分配原因"字段
4. 维修弹窗新增"开始时间"/"结束时间"字段
5. 修正操作按钮状态流转：`REPAIRED→质量检验`、`QUALITY_CHECK→入库审核`、`WAREHOUSED→再出货`
6. 前端枚举新增 `QUALITY_CHECK`/`WAREHOUSED`/`DIRECT_RESHIP`/`ASSIGN_TYPE_MAP`/`QUALITY_CHECK_RESULT_MAP`

### 涉及文件
- `frontend/src/views/RmaReturn.vue`
- `frontend/src/api/rma.js`
- `frontend/src/constants/enums.js`

### 教训
**前端页面必须与后端流程完全对齐，每个状态节点都要有对应的操作按钮和弹窗。**

---

## Bug #011：返厂维修时间选择器宽度不一致

| 字段 | 内容 |
|------|------|
| **编号** | BUG-011 |
| **发现日期** | 2026-09-07 |
| **严重程度** | 🟢 低（UI 样式问题） |
| **模块** | 主线B·返厂维修 |
| **状态** | ✅ 已修复 |

### 现象
维修工单弹窗中「开始时间」和「结束时间」日期选择器宽度小于其他表单项控件，视觉上不协调。

### 根因
`el-date-picker` 组件未设置 `style="width:100%"`，默认宽度与其他 `el-input` 不一致。

### 修复
在维修工单弹窗的开始时间和结束时间 `el-date-picker` 中添加 `style="width:100%"`。

### 涉及文件
- `frontend/src/views/RmaReturn.vue`

### 教训
**所有表单控件应统一宽度，对 `el-date-picker`、`el-select` 等非 `el-input` 组件也需显式设置 `width:100%`。**

---

## Bug #012：seed_demo.py 枚举值名称错误

| 字段 | 内容 |
|------|------|
| **编号** | BUG-012 |
| **发现日期** | 2026-09-07 |
| **严重程度** | 🟡 中（数据填充失败） |
| **模块** | 开发工具·数据种子 |
| **状态** | ✅ 已修复 |

### 现象
运行 `seed_demo.py` 填充演示数据时报错：
```
AttributeError: type object 'MaterialAvailability' has no attribute 'AVAILABLE'
```

### 根因
`enums.py` 中 `MaterialAvailability` 的枚举值定义为 `COMPLETE`（齐套）/ `SHORTAGE`（缺料）/ `FULFILLED`（已齐套），`seed_demo.py` 中错误写为 `AVAILABLE`。

### 修复
将 `seed_demo.py` 中两处 `MaterialAvailability.AVAILABLE.value` 改为 `MaterialAvailability.COMPLETE.value`。

### 涉及文件
- `backend/seed_demo.py` (L580, L591)

### 教训
**写种子数据前必须核对枚举定义，不能凭记忆猜测枚举值名称。**

---

## Bug #013：RawMaterialInventory created_at/updated_at 无默认值

| 字段 | 内容 |
|------|------|
| **编号** | BUG-013 |
| **发现日期** | 2026-09-07 |
| **严重程度** | 🔴 高（插入失败） |
| **模块** | 主线D·原材料管理 |
| **状态** | ✅ 已修复 |

### 现象
插入 `raw_material_inventory` 时报错：
```
OperationalError: (1364 "Field 'created_at' doesn't have a default value")
```

### 根因
模型虽然继承 `TimestampMixin`（声明 `created_at/updated_at` + `server_default=func.now()`），但实际数据库表结构迁移时没有加上 `DEFAULT CURRENT_TIMESTAMP`，导致无法自动获取默认值。

### 修复
在 `seed_demo.py` 插入 `RawMaterialInventory` 时，显式传入 `created_at` 和 `updated_at` 值。

### 涉及文件
- `backend/seed_demo.py` (L672-L675)

### 教训
**模型定义与数据库实际结构可能不一致，种子脚本插入时显式设置时间戳可避免此类问题。**

---

## Bug #014：dt 名称覆盖导致 UnboundLocalError

| 字段 | 内容 |
|------|------|
| **编号** | BUG-014 |
| **发现日期** | 2026-09-07 |
| **严重程度** | 🟡 中（数据填充失败） |
| **模块** | 开发工具·数据种子 |
| **状态** | ✅ 已修复 |

### 现象
运行 `seed_demo.py` 报错：
```
UnboundLocalError: cannot access local variable 'dt' where it is not associated with a value
```

### 根因
1. 全局导入 `from datetime import datetime as dt`
2. 在 `seed` 函数内部又定义 `dt = today - timedelta(days=d)`
3. Python 将整个函数中的 `dt` 视为局部变量，导致在前面使用 `dt.combine()` 时报错

### 修复
将局部变量 `dt` 重命名为 `summary_date`，避免覆盖全局导入名称。

### 涉及文件
- `backend/seed_demo.py` (L1079-L1085)

### 教训
**全局导入的短名称（如 dt、pd、np）不要在函数内部作为局部变量名重用，否则 Python 会将整个函数中的该名称标记为局部变量，导致 UnboundLocalError。**

---

## Bug #015：日期相减可能产生负数 day

| 字段 | 内容 |
|------|------|
| **编号** | BUG-015 |
| **发现日期** | 2026-09-07 |
| **严重程度** | 🟢 低（可能异常） |
| **模块** | 开发工具·数据种子 |
| **状态** | ✅ 已修复 |

### 现象
构造 `created_at` 时用 `today.day - random.randint(5, 20)`，如果 `today.day` < 20 会得到负数日期。

### 根因
直接对 `day` 做减法不处理跨月，可能生成非法日期（如 `2026-09-00` 或 `2026-09--5`）。

### 修复
改用 `dt.combine(today - timedelta(days=random.randint(5, 20)), dt.min.time())`，利用 `timedelta` 自动处理跨月。

### 涉及文件
- `backend/seed_demo.py` (L672-L675, L692)

### 教训
**生成过去日期优先使用 `timedelta` 从 `today` 往前推，不要直接对 `day` 做减法，否则遇到月初会得到非法日期。**

---

## Bug #016：GET /incoming/receipts/{id} 不存在时返回 500

| 字段 | 内容 |
|------|------|
| **编号** | BUG-016 |
| **发现日期** | 2026-09-15 |
| **严重程度** | 🔴 高（API 500） |
| **模块** | 主线A·来料管理 |
| **状态** | 🔴 待修复 |
| **发现方式** | API 全量冒烟测试（自动发现） |

### 现象
`GET /api/v1/incoming/receipts/99999` → 500，响应体 `{"code":500,"msg":"服务器内部错误","data":null}`。期望返回 404。

### 根因
- `incoming_service.py:159` — `get_receipt()` 未找到到货单时 `raise ValueError(f"到货单不存在：{receipt_id}")`
- `incoming.py:101` — API 层 `get_receipt` 没有 `except ValueError` 包装
- `incoming.py` 是整个项目中唯二缺少 `except ValueError` 的 API 模块（另一个是 `rma.py`）

### 修复
在 `incoming.py` 的 `get_receipt` 函数中包裹 `try/except ValueError`，返回 `HTTPException(status_code=404)`。

### 涉及文件
- `backend/app/api/incoming.py` (L101-108)
- `backend/app/service/incoming_service.py` (L159)

### 教训
**API 层必须 `except ValueError` 转换为 HTTPException。所有其他模块（14个）都有此模式，仅 `incoming.py` 和 `rma.py` 遗漏。**

---

## Bug #017：POST /incoming/receipts/{id}/confirm 不存在时返回 500

| 字段 | 内容 |
|------|------|
| **编号** | BUG-017 |
| **发现日期** | 2026-09-15 |
| **严重程度** | 🔴 高（API 500） |
| **模块** | 主线A·来料管理 |
| **状态** | 🔴 待修复 |
| **发现方式** | API 全量冒烟测试（自动发现） |

### 现象
`POST /api/v1/incoming/receipts/99999/confirm` → 500。期望返回 404。

### 根因
- `incoming_service.py:267` — `confirm_receipt()` 未找到到货单时 `raise ValueError(f"到货单不存在：{receipt_id}")`
- `incoming.py:120` — API 层 `confirm_receipt` 没有 `except ValueError` 包装

### 修复
在 `incoming.py` 的 `confirm_receipt` 函数中包裹 `try/except ValueError`。

### 涉及文件
- `backend/app/api/incoming.py` (L119-127)
- `backend/app/service/incoming_service.py` (L267)

---

## Bug #018：POST /rma/scraps 返厂单不存在时返回 500

| 字段 | 内容 |
|------|------|
| **编号** | BUG-018 |
| **发现日期** | 2026-09-15 |
| **严重程度** | 🔴 高（API 500） |
| **模块** | 主线B·返厂维修 |
| **状态** | 🔴 待修复 |
| **发现方式** | API 全量冒烟测试（自动发现） |

### 现象
`POST /api/v1/rma/scraps` → 500（return_id=99999 不存在）。期望返回 404。

### 根因
- `rma_service.py:288` — `create_scrap()` 未找到返厂单时 `raise ValueError(f"返厂单不存在：{data.return_id}")`
- `rma.py:131` — API 层 `create_scrap` 没有 `except ValueError` 包装

### 修复
在 `rma.py` 的 `create_scrap` 函数中包裹 `try/except ValueError`。

### 涉及文件
- `backend/app/api/rma.py` (L131-138)
- `backend/app/service/rma_service.py` (L288)

---

## Bug #019：POST /rma/scraps/{id}/approve 报废单不存在时返回 500

| 字段 | 内容 |
|------|------|
| **编号** | BUG-019 |
| **发现日期** | 2026-09-15 |
| **严重程度** | 🔴 高（API 500） |
| **模块** | 主线B·返厂维修 |
| **状态** | 🔴 待修复 |
| **发现方式** | API 全量冒烟测试（自动发现） |

### 现象
`POST /api/v1/rma/scraps/99999/approve` → 500。期望返回 404。

### 根因
- `rma_service.py:324` — `approve_scrap()` 未找到报废单时 `raise ValueError(f"报废单不存在：{scrap_id}")`
- `rma.py:141` — API 层 `approve_scrap` 没有 `except ValueError` 包装

### 修复
在 `rma.py` 的 `approve_scrap` 函数中包裹 `try/except ValueError`。

### 涉及文件
- `backend/app/api/rma.py` (L141-148)
- `backend/app/service/rma_service.py` (L324)

---

## Bug #020：incoming.py / rma.py 全模块缺少 ValueError 异常捕获（系统性问题）

| 字段 | 内容 |
|------|------|
| **编号** | BUG-020 |
| **发现日期** | 2026-09-15 |
| **严重程度** | 🔴 高（系统性风险） |
| **模块** | 主线A + 主线B |
| **状态** | 🔴 待修复 |
| **发现方式** | API 全量冒烟测试 + 全局代码审查 |

### 现象
`incoming.py`（来料管理）和 `rma.py`（返厂维修）两个 API 模块中，**所有** POST/PUT 端点都没有 `except ValueError` 异常捕获。这意味着任意 ValueError（不存在、状态不符、业务校验失败）都会变成 500。

其他 14 个 API 模块（`user.py`, `stocktake.py`, `station.py`, `snapshot.py`, `shipment.py`, `settings.py`, `product.py`, `partner.py`, `outbound.py`, `inventory_adjustment.py`, `inventory.py`, `inbound.py`, `device_ledger.py`, `bom.py`）均已正确添加 `except ValueError as e` 模式。

### 根因
开发 incoming 和 rma 模块时遗漏了 `except ValueError` 的包装模式，其他模块后续补全时未同步修复这两个模块。

### 涉及端点（共 ~25 个）

| 模块 | 缺少异常捕获的端点 |
|------|-------------------|
| `incoming.py` | `get_receipt`, `create_receipt`, `update_receipt`, `confirm_receipt`, `create_inspection`, `create_return` |
| `rma.py` | `create_return`, `get_return`, `assign_return`, `transfer_return`, `create_diagnosis`, `create_repair`, `create_scrap`, `approve_scrap`, `create_reship`, `create_quality_check`, `create_warehouse_in` |

### 修复方案
在每个端点函数中包裹 `try/except ValueError as e: raise HTTPException(status_code=400, detail=str(e))`（参考其他14个模块的写法）。

### 涉及文件
- `backend/app/api/incoming.py` (6个端点)
- `backend/app/api/rma.py` (11个端点)


---

## Bug #021：Capacitor Gradle 构建因项目路径含中文失败

| 字段 | 内容 |
|------|------|
| **编号** | BUG-021 |
| **发现日期** | 2026-09-14 |
| **严重程度** | 🔴 高（APK构建阻塞） |
| **模块** | Capacitor / Android 构建 |
| **状态** | ✅ 已修复 |

### 现象
`./gradlew.bat assembleDebug` 构建失败，错误：
```
Your project path contains non-ASCII characters. This will most likely cause
the build to fail on Windows. Please move your project to a different directory.
```

### 根因
项目路径 `C:\Users\25075\Desktop\IMS生产物料与产品追溯管理系统\` 包含中文字符「生产物料与产品追溯管理系统」，Android Gradle Plugin 默认拒绝非 ASCII 路径。

### 修复
在 `android/gradle.properties` 中添加：
```properties
android.overridePathCheck=true
```

### 涉及文件
- `ims-main/frontend/android/gradle.properties`

### 教训
**创建项目时应使用全英文路径。如果无法避免（现有项目），需在 gradle.properties 中显式开启 overridePathCheck。**


---

## Bug #022：Capacitor Camera 插件编译要求 JDK 21（JDK 17 不满足）

| 字段 | 内容 |
|------|------|
| **编号** | BUG-022 |
| **发现日期** | 2026-09-14 |
| **严重程度** | 🔴 高（APK构建阻塞） |
| **模块** | Capacitor / Android 构建 |
| **状态** | ✅ 已修复 |

### 现象
Gradle 构建失败，`capacitor-camera` 模块报错：
```
Cannot find a Java installation on your machine matching:
{languageVersion=21 vendor=any vendor implementation=vendor-specific}
```

JDK 17 已安装但不满足插件的 toolchain 要求。

### 根因
Capacitor 8.x + Android Gradle Plugin 8.x 的 `capacitor-camera` 插件使用 Gradle toolchain 机制自动检测 Java 版本，其 `compileDebugJavaWithJavac` 任务要求 JDK 21。项目中配置的 JDK 17 不满足此要求。

### 修复
通过 winget 安装 Microsoft OpenJDK 21：
```bash
winget install --id Microsoft.OpenJDK.21 --accept-source-agreements --accept-package-agreements --silent
```
构建时设置 `JAVA_HOME=C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot`。

### 涉及文件
- 无代码文件（仅环境配置）
- `capacitor-camera` AAR 依赖的 `bundleLibCompileToJarDebug` 任务

### 教训
**Capacitor 8 + AGP 8 的 toolchain 要求 JDK 21，旧版 JDK 17 不满足。安装新 JDK 后需同时修改 JAVA_HOME 环境变量。**

---

## Bug #023：测试连接 fetch 被 CORS 拦截导致 "failed to fetch"

| 字段 | 内容 |
|------|------|
| **编号** | BUG-023 |
| **发现日期** | 2026-09-15 |
| **严重程度** | 🟡 中（服务器设置功能不可用） |
| **模块** | 方式B·运行时配置 / ServerSettingsDialog |
| **状态** | ✅ 已修复 |

### 现象
浏览器中打开「服务器设置」弹窗，点击「测试连接」按钮，提示 `failed to fetch`，无法验证服务器地址是否可达。

### 根因
`ServerSettingsDialog.vue` 中使用浏览器原生 `fetch()` 直连后端 `/health`：
```js
const res = await fetch(testUrl, { method: 'GET', signal: AbortSignal.timeout(5000) })
```
该请求从 `http://localhost:5175`（Vite dev）发往 `http://192.168.10.77:8000`，属于跨域请求。而后端 `.env` 中 `CORS_ORIGINS` 仅配置了 `http://localhost:5173,http://localhost:8080,http://127.0.0.1:8080`，缺少 `localhost:5175`，导致浏览器 CORS 拦截，`fetch` 抛出网络错误。

**注意**：常规 API 请求不受影响，因为它们走的是 Vite proxy（`/api/v1/*`），不存在跨域问题。

### 修复
在 `backend/.env` 的 `CORS_ORIGINS` 中追加 `http://localhost:5175`：
```
CORS_ORIGINS=http://localhost:5173,http://localhost:5175,http://localhost:8080,http://127.0.0.1:8080
```
然后重启后端使配置生效。

### 涉及文件
- `backend/.env` (CORS_ORIGINS 追加 `localhost:5175`)
- `frontend/src/components/ServerSettingsDialog.vue` (测试连接逻辑，无需改动)

### 教训
**直接使用 `fetch()` 发出的请求绕过 Vite proxy，必须确保后端 CORS 白名单包含当前前端端口。后续如有端口变更需同步更新 CORS_ORIGINS。**