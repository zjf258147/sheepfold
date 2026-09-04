# 敦临 IMS 参考数据

> 此文件为宪法（project_rules.md）的补充参考数据，包含权限矩阵、表结构、业务逻辑等。
> 宪法中通过引用链接指向此文件，AI 按需读取。

---

## 5. 权限矩阵

### 5.1 角色枚举（6个角色）

| 角色 | 枚举值 | 说明 |
|------|--------|------|
| 总经理 | `ADMIN` | 全权限 |
| 仓库管理员 | `WAREHOUSE` | 库存管理、到货登记、出货登记、报废审批 |
| 来料检/质量负责人 | `QUALITY` | 来料检验、诊断、维修、报废发起 |
| 生产主管 | `PRODUCTION` | BOM管理、来料检验、出货登记 |
| 测试工程师 | `TEST_ENGINEER` | 诊断、维修（仅自己名下设备） |
| 普通员工 | `STAFF` | 保留，向后兼容 |

### 5.2 权限矩阵

| 操作功能 | 来料检/质量 | 生产主管 | 测试工程师 | 仓库管理员 | 总经理 |
|----------|:---:|:---:|:---:|:---:|:---:|
| **全局** | | | | | |
| 查看所有数据 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 查看自己名下的设备 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Excel导出（所有模块） | ✅ | ✅ | ✅ | ✅ | ✅ |
| **主线A：来料** | | | | | |
| 到货登记 | ✅ | ❌ | ❌ | ✅ | ✅ |
| 来料检验/审核 | ✅ | ✅ | ❌ | ❌ | ✅ |
| 确认入库 | ✅ | ✅ | ❌ | ✅ | ✅ |
| 原材料退货（发起） | ✅ | ✅ | ❌ | 可发起 | ✅ |
| **主线B：返厂维修** | | | | | |
| 退货登记 | ✅ | ❌ | ❌ | ✅ | ✅ |
| 分配设备给测试工程师/生产 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 流转设备到下一人 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 诊断报告（自己名下） | ✅ | ❌ | ✅ | ❌ | ✅ |
| 维修工单（自己名下） | ✅ | ❌ | ✅ | ❌ | ✅ |
| 维修用料填报 | ✅ | ❌ | ✅（填） | ✅（扣库存） | ✅ |
| 手动填入新SN | ✅ | ❌ | ✅ | ✅ | ✅ |
| 报废发起 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 报废最终审批 | ❌ | ❌ | ❌ | ✅ | ✅ |
| **主线C：出货** | | | | | |
| 出货登记 | ✅ | ✅ | ❌ | ✅ | ✅ |
| 填写物流信息 | ✅ | ✅ | ❌ | ✅ | ✅ |
| **主线D：BOM** | | | | | |
| 创建/编辑BOM | ❌ | ✅ | ❌ | ✅ | ✅ |
| 导入BOM | ❌ | ✅ | ❌ | ✅ | ✅ |
| 导出BOM | ✅ | ✅ | ✅ | ✅ | ✅ |
| 对比库存/齐套分析 | ❌ | ✅ | ❌ | ✅ | ✅ |
| 生成采购建议 | ❌ | ✅ | ❌ | ❌ | ✅ |
| **系统** | | | | | |
| 审计日志查看 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 用户管理/系统设置 | ❌ | ❌ | ❌ | ❌ | **✅ 唯一** |

---

## 6. 数据库表清单

### 6.1 需新增的业务表（16张）

| 类别 | 表名 | 说明 |
|------|------|------|
| 主线A | `incoming_receipt` | 到货单（外键 supplier_id → partner.id, sku_id → product_sku.id） |
| 主线A | `incoming_inspection` | 来料检验报告 |
| 主线A | `incoming_return` | 原材料退货单 |
| 主线A | `raw_material_inventory` | 原材料库存（批次管理） |
| 主线A | `raw_material_sn` | 原材料SN明细（可选SN管理） |
| 主线A | `raw_material_inventory_log` | 原材料库存流水 |
| 主线B | `rma_return` | 返厂退货单（外键 sku_id → product_sku.id） |
| 主线B | `rma_diagnosis` | 诊断报告 |
| 主线B | `rma_repair` | 维修工单 |
| 主线B | `rma_scrap` | 报废申请审批单 |
| 主线B | `rma_reship` | 再出货单 |
| 主线C | `shipment` | 出货单 |
| 主线D | `bom_header` | BOM主表 |
| 主线D | `bom_detail` | BOM明细 |
| 主线D | `production_task` | 生产任务 |
| 审计 | `audit_log` | 审计日志表（已有基础，改造扩展） |

### 6.2 IMS 现有表改造

#### inventory_item 表（成品 SN 表）新增字段

| 字段名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `replaced_by_sn` | VARCHAR(50) | NULL | 如果已替换，指向新 SN |
| `replaced_from_sn` | VARCHAR(50) | NULL | 如果是维修后新 SN，指向旧 SN |
| `current_location` | VARCHAR(50) | '库房' | 库房 / 已发出 / 维修中 / 已报废 |

#### stock_status 枚举扩展

新增 `REPLACED = "REPLACED"`（已替换，维修换码后的旧SN）

#### product_sku 表新增字段

| 字段名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `sku_code` | VARCHAR(50) | - | 物料编码（U9编码），唯一键 |
| `spec` | VARCHAR(100) | NULL | 规格型号 |
| `sku_type` | VARCHAR(20) | 'FINISHED_GOODS' | RAW_MATERIAL / FINISHED_GOODS |

#### audit_log 表改造

| 字段名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `change_reason` | VARCHAR(255) | NULL | 变更原因（必填） |

`action` 枚举扩展：新增 `APPROVE` 类型

### 6.3 审计日志表字段（audit_log）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `id` | INT | 主键 |
| `user_id` | INT | 操作人 ID |
| `username` | VARCHAR(50) | 操作人账号 |
| `action` | VARCHAR(20) | CREATE / UPDATE / DELETE / STATUS_CHANGE / APPROVE |
| `entity_type` | VARCHAR(30) | 实体类型 |
| `entity_id` | INT | 实体 ID |
| `entity_no` | VARCHAR(50) | 实体编号 |
| `field_name` | VARCHAR(50) | 变更字段名 |
| `before_value` | TEXT | 变更前值 |
| `after_value` | TEXT | 变更后值 |
| `change_reason` | VARCHAR(255) | **变更原因（必填，不填无法提交）** |
| `ip_address` | VARCHAR(50) | 操作 IP |
| `created_at` | DATETIME | 操作时间 |

---

## 7. 单据编号格式

| 单据类型 | 格式 | 示例 |
|----------|------|------|
| 到货单 | RC + 年月日 + 序号 | RC20260901001 |
| 返厂单 | FC + 年月日 + 序号 | FC20260901001 |
| 出货单 | SH + 年月日 + 序号 | SH20260901001 |
| BOM编号 | BOM + 年月日 + 序号 | BOM20260901001 |
| 生产任务 | PR + 年月日 + 序号 | PR20260901001 |

---

## 8. 验收清单摘要

### 主线A（来料管理）- 7项
A-01 到货登记 → A-02 到货列表 → A-03 来料检验 → A-04 合格入库 → A-05 让步接收 → A-06 不合格→退货 → A-07 来料导出

### 主线B（返厂维修）- 16项
B-01 退货登记 → B-02 退货列表 → B-03 诊断报告 → B-04 分配任务 → B-05 测试工程师查看自己名下 → B-06 测试工程师不能流转 → B-07 维修工单（含新SN手动输入） → B-08 新SN校验 → B-09 维修后原因/故障码 → B-10 维修用料填报 → B-11 维修用料扣库存 → B-12 流转设备 → B-13 报废发起 → B-14 报废审批通过 → B-15 报废审批驳回 → B-16 再出货（含双版本号）

### 主线C（出货管理）- 4项
C-01 出货登记 → C-02 软件版本号录入 → C-03 U9任务单号关联 → C-04 出货导出

### 主线D（BOM）- 8项
D-01 BOM导入 → D-02 BOM编辑 → D-03 BOM版本管理 → D-04 BOM导出 → D-05 对比库存/齐套分析 → D-06 生成采购建议 → D-07 采购建议转入主线A → D-08 BOM查看权限

### 审计日志 - 5项
L-01 操作记录生成 → L-02 变更前后值记录 → L-03 变更原因强制 → L-04 审计日志查看 → L-05 日志不可删除

### 权限 - 5项
P-01 总经理管理员权限 → P-02 质量负责人无系统设置 → P-03 测试工程师仅见自己名下设备 → P-04 测试工程师不能流转 → P-05 仓库管理员可审核来料检验

### 扫码功能 - 2项
S-01 扫码录入SN → S-02 手动输入SN

---

## 9. 核心业务逻辑

### 9.1 新旧SN关联机制

维修完成后：
1. 测试工程师手动输入新 SN（支持扫码）
2. 系统校验新 SN 是否已存在（重复则拦截）
3. 系统自动建立关联：
   - 旧 SN 的 `replaced_by_sn` = 新 SN
   - 旧 SN 的 `stock_status` = `REPLACED`
   - 新 SN 的 `replaced_from_sn` = 旧 SN
   - 新 SN 的 `stock_status` = `IN_STOCK`
   - 新 SN 的 `current_location` = '库房'
4. 审计日志记录完整变更链路

### 9.2 报废审批流程

```
质量负责人发起报废申请
  ↓
状态：待审批
  ↓
总经理 或 仓库管理员（任意一人）
  ├→ 通过 → 状态：已报废
  └→ 驳回 → 状态：回退到待维修
```

### 9.3 维修用料扣库存流程

```
测试工程师在维修工单中填写"维修用料描述"
  ↓
仓库管理员在"库存调整"模块中：
  ├→ 选择扣减原因："维修领料"
  ├→ 关联维修工单号
  ├→ 输入扣减物料和数量
  └→ 提交 → 库存扣减 + 库存流水记录
```

### 9.4 原材料库存管理（批次 + 可选SN双轨制）

- **无 SN 批次**：只在 `raw_material_inventory` 记录数量，扣减时按数量扣减
- **有 SN 批次**：`raw_material_inventory` 记录总数量 + `raw_material_sn` 逐条记录每个 SN，扣减时按 SN 逐件扣减

### 9.5 原材料SN状态枚举

| 状态 | 枚举值 | 说明 |
|------|--------|------|
| 在库 | `IN_STOCK` | 来料检验合格 |
| 已消耗 | `CONSUMED` | 用于生产 |
| 不良品 | `DEFECTIVE` | 来料检验发现 |
| 已退货 | `RETURNED` | 退货给供应商 |
| 已报废 | `SCRAPPED` | 生产过程报废 |

---

## 10. 数据迁移说明

### 10.1 现有 SN 的 current_location 自动填充

```sql
UPDATE inventory_item
SET current_location = CASE
    WHEN stock_status = 'IN_STOCK' THEN '库房'
    WHEN stock_status IN ('SOLD', 'SOLD_OFFLINE', 'BORROWED', 'GIFTED', 'RND', 'SAMPLE', 'TRIAL', 'PRESOLD', 'DEPT_PROCUREMENT') THEN '已发出'
    WHEN stock_status = 'SCRAPPED' THEN '已报废'
    WHEN stock_status = 'REPAIR' THEN '维修中'
    ELSE '库房'
END
WHERE current_location IS NULL;
```

### 10.2 现有 SKU 的 sku_type 默认值

新增字段时设置 `default='FINISHED_GOODS'`，现有数据自动填充。

### 10.3 现有 STAFF 用户迁移

上线后由管理员在系统设置页面手动修改角色，不做自动化迁移。