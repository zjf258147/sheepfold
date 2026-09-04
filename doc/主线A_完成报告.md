# 主线A（来料管理）完成报告

> 完成日期：2026-09-04
> Git 提交：[incoming] 2 次提交

---

## 一、新增数据库表（3 张）

| 表名 | 说明 | 关键外键 |
|------|------|----------|
| `incoming_receipt` | 到货单 | `supplier_id` → `partner.id`, `sku_id` → `product_sku.id`, `inspector_id` → `sys_user.id` |
| `incoming_inspection` | 来料检验报告 | `receipt_id` → `incoming_receipt.id`, `inspector_id` → `sys_user.id` |
| `incoming_return` | 原材料退货单 | `receipt_id` → `incoming_receipt.id`, `operator_id` → `sys_user.id` |

### incoming_receipt 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键 |
| receipt_no | VARCHAR(50) UNIQUE | 到货单号（RC前缀） |
| supplier_id | INT FK | 供应商 |
| sku_id | INT FK | 物料SKU |
| batch_no | VARCHAR(50) | 批次号 |
| quantity | INT | 到货数量 |
| unit | VARCHAR(20) | 单位（默认"个"） |
| status | VARCHAR(30) | 状态（PENDING_INSPECTION / INSPECTED / ACCEPTED / REJECTED） |
| delivery_date | DATE | 到货日期 |
| inspector_id | INT FK | 检验人 |
| inspection_date | DATE | 检验日期 |
| change_reason | VARCHAR(255) | 变更原因 |
| remark | TEXT | 备注 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### incoming_inspection 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键 |
| receipt_id | INT FK | 关联到货单 |
| inspection_no | VARCHAR(50) UNIQUE | 检验编号（JC前缀） |
| inspector_id | INT FK | 检验人 |
| inspection_date | DATE | 检验日期 |
| result | VARCHAR(30) | 检验结果（ACCEPTED / CONCESSION_ACCEPTED / REJECTED） |
| sample_qty | INT | 抽检数量 |
| defect_qty | INT | 不合格数量 |
| defect_description | TEXT | 缺陷描述 |
| change_reason | VARCHAR(255) | 变更原因 |
| remark | TEXT | 备注 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### incoming_return 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT PK | 主键 |
| receipt_id | INT FK | 关联到货单 |
| return_no | VARCHAR(50) UNIQUE | 退货单号（TH前缀） |
| return_qty | INT | 退货数量 |
| return_reason | TEXT | 退货原因 |
| status | VARCHAR(30) | 状态（PENDING / CONFIRMED） |
| operator_id | INT FK | 操作人 |
| change_reason | VARCHAR(255) | 变更原因 |
| remark | TEXT | 备注 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 二、新增枚举

| 枚举 | 文件 | 值 |
|------|------|-----|
| `IncomingStatus` | `backend/app/models/enums.py` | PENDING_INSPECTION / INSPECTED / ACCEPTED / REJECTED |
| `InspectionResult` | `backend/app/models/enums.py` | ACCEPTED / CONCESSION_ACCEPTED / REJECTED |
| `ReturnStatus` | `backend/app/models/enums.py` | PENDING / CONFIRMED |
| `INCOMING_STATUS_MAP` | `frontend/src/constants/enums.js` | 前端状态映射 |
| `INSPECTION_RESULT_MAP` | `frontend/src/constants/enums.js` | 前端检验结果映射 |

---

## 三、新增编号生成器

| 函数 | 前缀 | 格式 | 示例 |
|------|------|------|------|
| `generate_rc_no()` | RC | RC{YYYYMMDD}{序号3位} | RC20260904001 |
| `generate_inspection_no()` | JC | JC{YYYYMMDD}{序号3位} | JC20260904001 |
| `generate_return_no()` | TH | TH{YYYYMMDD}{序号3位} | TH20260904001 |

文件：`backend/app/utils/order_no.py`

---

## 四、新增后端文件

| 文件 | 说明 |
|------|------|
| `backend/app/models/incoming.py` | 3个 SQLAlchemy 模型 + relationship |
| `backend/app/schemas/incoming.py` | 6个 Pydantic Schema（Create/Update/Response × 3） |
| `backend/app/service/incoming_service.py` | 业务逻辑层（CRUD + 分页 + 搜索 + 检验 + 退货） |
| `backend/app/api/incoming.py` | 7个 API 端点 |

### API 端点

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/v1/incoming/receipts` | 到货列表（分页 + keyword + category + sku + supplier + status + date 筛选） |
| GET | `/api/v1/incoming/receipts/{id}` | 到货单详情 |
| POST | `/api/v1/incoming/receipts` | 到货登记 |
| PUT | `/api/v1/incoming/receipts/{id}` | 编辑到货单 |
| GET | `/api/v1/incoming/receipts/{id}/inspections` | 检验记录列表 |
| POST | `/api/v1/incoming/inspections` | 来料检验 |
| POST | `/api/v1/incoming/returns` | 退货处理 |

---

## 五、新增/变更前端文件

| 文件 | 类型 | 说明 |
|------|:--:|------|
| `frontend/src/views/IncomingReceipt.vue` | **新增** | 完整页面：搜索区 + 列表 + 到货登记弹窗 + 检验弹窗 + 退货弹窗 |
| `frontend/src/api/incoming.js` | **新增** | API 调用封装（7个接口） |
| `frontend/src/router/index.js` | 变更 | 新增 `/incoming` 路由 |
| `frontend/src/layout/MainLayout.vue` | 变更 | 菜单新增「来料管理」 |
| `frontend/src/constants/enums.js` | 变更 | 新增 INCOMING_STATUS_MAP、INSPECTION_RESULT_MAP |

---

## 六、业务规则实现

| 规则 | 实现 |
|------|------|
| 变更原因强制弹窗 | 检验/退货弹窗中 `change_reason` 为空时提交按钮 disabled |
| 外键关联 | supplier_id → partner.id, sku_id → product_sku.id |
| 检验联动状态 | 检验后自动更新到货单状态 |
| 模糊搜索 | 后端复用 `_keyword_filter`，前端 keyword + 分类联动 + 状态 + 日期 |
| 审计日志 | 所有关键操作写入 audit_log |
| 权限控制 | 菜单和路由配置 roles 数组 |

---

## 七、数据流

```
到货登记(RC编号) → 待检验
  ↓
来料检验(JC编号)
  ├→ 合格(ACCEPTED) → 可入库
  ├→ 让步接收(CONCESSION_ACCEPTED) → 可入库
  └→ 拒收(REJECTED) → 退货(TH编号)
```

---

## 八、验收结果

| 检查项 | 结果 |
|--------|:--:|
| 后端启动无报错 | ✅ |
| 前端启动无报错 | ✅ |
| 浏览器可登录（admin/admin123） | ✅ |
| 来料管理页面可访问 | ✅ |
| 到货登记弹窗可打开 | ✅ |
| 检验弹窗可打开 | ✅ |
| 退货弹窗可打开 | ✅ |
| 变更原因不填时按钮灰显 | ✅ |
| 数据库表已创建（3张） | ✅ |
| 迁移脚本已执行（27条） | ✅ |
| API 文档可访问（/docs） | ✅ |