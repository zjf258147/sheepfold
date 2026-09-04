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
（避免再犯）