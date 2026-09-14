# 敦临 IMS 参考数据

> 此文件为宪法（project_rules.md）的补充参考数据，AI 按需读取。
> **最后更新**：2026-09-14 | **来源**：基于实际代码生成，非设计文档

---

## 1. 项目当前状态

| 项目 | 值 |
|------|-----|
| 当前版本 | v2.6 |
| 当前阶段 | 二期开发中 |
| 一期状态 | 主线 A/B/C/D 全部完成 ✅ |
| 二期状态 | 5 个模块模型/API 已完成，前端待开发 🔄 |

---

## 2. 权限矩阵

### 2.1 角色枚举（6个）

| 角色 | 枚举值 | 说明 |
|------|--------|------|
| 管理员/总经理 | `ADMIN` | 全权限，唯一可管理系统设置 |
| 仓库管理员 | `WAREHOUSE` | 库存管理、到货登记、出货登记、报废审批 |
| 来料检/质量负责人 | `QUALITY` | 来料检验、诊断、维修、报废发起 |
| 生产主管 | `PRODUCTION` | BOM管理、来料检验、出货登记 |
| 测试工程师 | `TEST_ENGINEER` | 诊断、维修（仅自己名下设备） |
| 普通员工 | `STAFF` | 保留，向后兼容 |

### 2.2 权限矩阵

| 操作功能 | QUALITY | PRODUCTION | TEST_ENGINEER | WAREHOUSE | ADMIN |
|----------|:---:|:---:|:---:|:---:|:---:|
| **全局** | | | | | |
| 查看所有数据 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 查看自己名下的设备 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Excel导出（所有模块） | ✅ | ✅ | ✅ | ✅ | ✅ |
| **主线A：来料管理** | | | | | |
| 到货登记 | ✅ | ❌ | ❌ | ✅ | ✅ |
| 来料检验/审核 | ✅ | ✅ | ❌ | ❌ | ✅ |
| 确认入库 | ✅ | ✅ | ❌ | ✅ | ✅ |
| 原材料退货（发起） | ✅ | ✅ | ❌ | 可发起 | ✅ |
| **主线B：返厂维修** | | | | | |
| 退货登记 | ✅ | ❌ | ❌ | ✅ | ✅ |
| 分配设备给测试/生产 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 流转设备到下一人 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 诊断报告（自己名下） | ✅ | ❌ | ✅ | ❌ | ✅ |
| 维修工单（自己名下） | ✅ | ❌ | ✅ | ❌ | ✅ |
| 维修用料填报 | ✅ | ❌ | ✅（填） | ✅（扣库存） | ✅ |
| 质量检验 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 入库审核 | ✅ | ❌ | ❌ | ✅ | ✅ |
| 手动填入新SN | ✅ | ❌ | ✅ | ✅ | ✅ |
| 报废发起 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 报废最终审批 | ❌ | ❌ | ❌ | ✅ | ✅ |
| **主线C：出货管理** | | | | | |
| 出货登记 | ✅ | ✅ | ❌ | ✅ | ✅ |
| 填写物流信息 | ✅ | ✅ | ❌ | ✅ | ✅ |
| **主线D：BOM** | | | | | |
| 创建/编辑BOM | ❌ | ✅ | ❌ | ✅ | ✅ |
| 导入BOM | ❌ | ✅ | ❌ | ✅ | ✅ |
| 导出BOM | ✅ | ✅ | ✅ | ✅ | ✅ |
| 对比库存/齐套分析 | ❌ | ✅ | ❌ | ✅ | ✅ |
| 生成采购建议 | ❌ | ✅ | ❌ | ❌ | ✅ |
| **二期模块（模型/API已完成，前端待开发）** | | | | | |
| 场站管理 | ❌ | ❌ | ❌ | ✅ | ✅ |
| 设备台账 | ❌ | ❌ | ❌ | ✅ | ✅ |
| 盘点 | ❌ | ❌ | ❌ | ✅ | ✅ |
| 库存调整 | ❌ | ❌ | ❌ | ✅ | ✅ |
| 客户管理 | ❌ | ✅ | ❌ | ✅ | ✅ |
| **系统** | | | | | |
| 审计日志查看 | ✅ | ❌ | ❌ | ❌ | ✅ |
| 用户管理/系统设置 | ❌ | ❌ | ❌ | ❌ | **✅ 唯一** |

---

## 3. 数据模型总览

### 3.1 一期（已完成，共 25 张业务表）

| 模块 | 表名 | 说明 | 关联外键 |
|------|------|------|----------|
| **基础数据** | | | |
| 用户 | `sys_user` | 系统用户 | — |
| 往来单位 | `partner_group` | 往来单位分组 | — |
| 往来单位 | `partner` | 往来单位（供应商/客户） | `group_id` → partner_group |
| 商品 | `product_category` | 商品分类 | — |
| 商品 | `product_sku` | 商品SKU（物料主数据） | `category_id` → product_category |
| **A：来料管理** | | | |
| A | `incoming_receipt` | 到货单 | `supplier_id`→partner, `sku_id`→product_sku |
| A | `incoming_inspection` | 来料检验报告 | `receipt_id`→incoming_receipt |
| A | `incoming_return` | 原材料退货单 | `receipt_id`→incoming_receipt |
| A | `raw_material_inventory` | 原材料库存（批次管理） | `sku_id`→product_sku, `supplier_id`→partner |
| A | `raw_material_sn` | 原材料SN明细 | `inventory_id`→raw_material_inventory |
| A | `raw_material_inventory_log` | 原材料库存流水 | `inventory_id`→raw_material_inventory |
| **B：返厂维修** | | | |
| B | `rma_return` | 返厂退货单（主表） | `sku_id`→product_sku |
| B | `rma_diagnosis` | 诊断报告 | `return_id`→rma_return |
| B | `rma_repair` | 维修工单 | `return_id`→rma_return |
| B | `rma_quality_check` | 质量检验 | `return_id`→rma_return |
| B | `rma_warehouse_in` | 入库审核 | `return_id`→rma_return |
| B | `rma_scrap` | 报废申请审批 | `return_id`→rma_return |
| B | `rma_reship` | 再出货单 | `return_id`→rma_return |
| **C：出货管理** | | | |
| C | `shipment` | 出货单 | — |
| **D：BOM** | | | |
| D | `bom_header` | BOM主表 | `product_sku_id`→product_sku |
| D | `bom_detail` | BOM明细（多级） | `bom_id`→bom_header, `parent_detail_id`→bom_detail(自引用) |
| D | `production_task` | 生产任务 | `bom_id`→bom_header |
| **库存管理** | | | |
| 库存 | `inventory_item` | 成品库存单品（一物一码） | `sku_id`→product_sku |
| 库存 | `inventory_item_history` | 单品变动轨迹 | `item_id`→inventory_item |
| 库存 | `inventory_item_snapshot` | 单品日/月快照 | — |
| 库存 | `inventory_daily_summary` | 库存日汇总（财务） | — |
| 库存 | `inventory_sku_daily_ledger` | SKU日流水 | `sku_id`→product_sku |
| 库存 | `inbound_order` | 入库单 | `partner_id`→partner |
| 库存 | `inbound_order_line` | 入库单商品行 | `inbound_order_id`→inbound_order |
| 库存 | `inbound_order_item` | 入库单SN绑定 | `inbound_order_id`→inbound_order |
| 库存 | `outbound_order` | 出库单 | `partner_id`→partner |
| 库存 | `outbound_order_item` | 出库单SN明细 | `outbound_order_id`→outbound_order |
| **审计** | | | |
| 审计 | `sys_audit_log` | 审计日志 | `operator_id`→sys_user |
| **序列号** | | | |
| 序列 | `sequence_counter` | 单据编号序列号生成器 | — |

### 3.2 二期（模型/API已完成，前端待开发，共 6 张表）

| 模块 | 表名 | 说明 | 关联外键 |
|------|------|------|----------|
| 客户 | `customer` | 客户（扩展8字段） | — |
| 场站 | `station` | 场站档案 | `customer_id`→customer |
| 设备 | `device_ledger` | 设备安装记录（台账） | `station_id`→station, `item_sn`→inventory_item |
| 盘点 | `stocktake` | 盘点任务 | — |
| 盘点 | `stocktake_line` | 盘点明细行 | `stocktake_id`→stocktake |
| 调整 | `inventory_adjustment` | 库存调整记录 | `stocktake_id`→stocktake |

---

## 4. 核心表结构详解

### 4.1 inventory_item（成品库存单品）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGINT PK | 主键 |
| `item_sn` | VARCHAR(50) UNIQUE | 单品SN（一物一码） |
| `sku_id` | INT FK→product_sku | 物料 |
| `stock_status` | VARCHAR(30) | 库存状态（IN_STOCK/SOLD/SCRAPPED/REPAIR/REPLACED...） |
| `stock_condition` | VARCHAR(30) | 库存属性（NEW/RETURNED_FROM_xxx） |
| `operation_status` | VARCHAR(30) | 操作状态（INITIATED/COMPLETED...） |
| `warehouse_type` | VARCHAR(30) | 仓库类型（见 §6.5） |
| `current_location` | VARCHAR(50) | 当前位置（库房/已发出/维修中/已报废） |
| `replaced_by_sn` | VARCHAR(50) NULL | 如果被替换，指向新SN |
| `replaced_from_sn` | VARCHAR(50) NULL | 如果是新SN，指向旧SN |
| `unit_price` | DECIMAL(12,2) NULL | 采购单价 |
| `quantity` | INT DEFAULT 1 | 数量（固定为1） |
| `last_order_no` | VARCHAR(30) NULL | 最近关联单号 |

### 4.2 rma_return（返厂退货单，主表）

返厂维修全流程围绕此表展开，一条记录贯穿：退货→诊断→维修→质检→入库→再出货/报废。

| 关键字段 | 说明 |
|----------|------|
| `return_no` | 返厂单号 FC |
| `sn` | 原始设备SN |
| `new_sn` | 维修后新SN（换码时填写） |
| `status` | 流程状态（PENDING_DIAGNOSIS→...→RESHIPPED/SCRAPPED） |
| `assigned_to` | 当前分配给谁 |
| `assign_type` | 分配类型（PRODUCTION/TEST） |
| `repair_count` | 该SN累计维修次数 |
| `repair_reason` | 维修原因（累计，用分号拼接） |
| `repair_time_hours` | 修复耗时（小时） |
| `turnaround_days` | 周转周期（天） |
| `materials_used` | 维修用料描述 |
| `reship_station` | 再出货发出场站 |

### 4.3 shipment（出货单）

| 关键字段 | 说明 |
|----------|------|
| `shipment_no` | 出货单号 SH |
| `sn_list` | JSON数组，出货SN列表 |
| `u9_task_no` | U9任务单号 |
| `tf_version` | TF卡版本号 |
| `host_version` | 上位机版本号 |
| `logistics_provider` | 物流供应商 |
| `tracking_no` | 快递单号 |

---

## 5. 核心枚举值速查

### 5.1 库存状态 StockStatus

| 枚举值 | 说明 |
|--------|------|
| `IN_STOCK` | 在库 |
| `SOLD` | 售出-线上 |
| `SOLD_OFFLINE` | 售出-线下 |
| `PRESOLD` | 准售出 |
| `BORROWED` | 借用 |
| `GIFTED` | 赠送 |
| `SCRAPPED` | 已报废 |
| `RND` | 研发出库 |
| `SAMPLE` | 样机出库 |
| `TRIAL` | 试用出库 |
| `REPAIR` | 维修出库 |
| `DEPT_PROCUREMENT` | 部门采购出库 |
| `REPLACED` | 已替换（维修换码后的旧SN） |

### 5.2 返厂维修状态 RmaStatus

| 枚举值 | 说明 |
|--------|------|
| `PENDING_DIAGNOSIS` | 待诊断 |
| `DIAGNOSED` | 已诊断 |
| `ASSIGNED` | 已分配 |
| `REPAIRING` | 维修中 |
| `REPAIRED` | 已修复 |
| `QUALITY_CHECK` | 质量检验 |
| `WAREHOUSED` | 已入库 |
| `RESHIPPED` | 已再出货 |
| `SCRAPPED` | 已报废 |
| `PENDING_SCRAP` | 待报废审批 |

### 5.3 来料状态 IncomingStatus

| 枚举值 | 说明 |
|--------|------|
| `PENDING_INSPECTION` | 待检验 |
| `INSPECTED` | 已检验 |
| `ACCEPTED` | 合格入库 |
| `REJECTED` | 不合格退货 |
| `WAREHOUSED` | 已入库（仓管确认） |

### 5.4 仓库类型 WarehouseType

| 枚举值 | 说明 |
|--------|------|
| `RAW_MATERIAL` | 原材料仓 |
| `SEMI_FINISHED` | 半成品仓 |
| `FINISHED` | 成品仓 |
| `ZERO_COST_FINISHED` | 零成本仓-成品（维修后入库） |
| `ZERO_COST_SEMI` | 零成本仓-半成品 |
| `RND` | 研发物料仓 |

### 5.5 物料类型 SkuType

| 枚举值 | 说明 |
|--------|------|
| `RAW_MATERIAL` | 原材料 |
| `FINISHED_GOODS` | 成品 |

### 5.6 盘点相关

| 枚举 | 值 | 说明 |
|------|-----|------|
| StocktakeMode | `CYCLE` / `FULL` | 循环盘点 / 全盘 |
| StocktakeStatus | `IN_PROGRESS` / `COMPLETED` / `CANCELLED` | 盘点状态 |
| AdjustmentType | `SURPLUS` / `SHORTAGE` | 盘盈 / 盘亏 |

### 5.7 二期模块枚举

| 枚举 | 值 | 说明 |
|------|-----|------|
| StationStatus | `ACTIVE` / `INACTIVE` | 场站状态 |
| DeviceLedgerStatus | `RUNNING` / `FAULT` / `RECOVERED` | 设备运行状态 |
| BomStatus | `DRAFT` / `PUBLISHED` / `DISCONTINUED` | BOM状态 |
| TaskStatus | `PENDING` / `IN_PROGRESS` / `COMPLETED` | 生产任务状态 |
| MaterialAvailability | `COMPLETE` / `SHORTAGE` / `FULFILLED` | 齐套状态 |
| QualityCheckResult | `PASS` / `FAIL` | 质检结果 |

---

## 6. 单据编号格式

| 单据类型 | 前缀 | 格式 | 示例 |
|----------|:---:|------|------|
| 到货单 | RC | RC + 年月日 + 3位序号 | RC20260901001 |
| 返厂单 | FC | FC + 年月日 + 3位序号 | FC20260901001 |
| 诊断编号 | DG | DG + 年月日 + 3位序号 | DG20260901001 |
| 维修工单 | WX | WX + 年月日 + 3位序号 | WX20260901001 |
| 报废单 | BF | BF + 年月日 + 3位序号 | BF20260901001 |
| 再出货单 | RH | RH + 年月日 + 3位序号 | RH20260901001 |
| 出货单 | SH | SH + 年月日 + 3位序号 | SH20260901001 |
| BOM编号 | BOM | BOM + 年月日 + 3位序号 | BOM20260901001 |
| 生产任务 | PR | PR + 年月日 + 3位序号 | PR20260901001 |
| 入库单 | JIN | JIN-前缀 | JIN-20260901001 |
| 出库单 | JOUT | JOUT-前缀 | JOUT-20260901001 |
| 盘点单 | PD | PD-前缀 | PD-20260901001 |
| 调整单 | TZ | TZ-前缀 | TZ-20260901001 |

---

## 7. 核心业务逻辑

### 7.1 返厂维修全流程（主线B）

```
退货登记（rma_return: PENDING_DIAGNOSIS）
  ↓
诊断报告（rma_diagnosis: 故障描述 + 诊断结果 REPAIRABLE/SCRAP/DIRECT_RESHIP）
  ↓
分配任务（rma_return: ASSIGNED, assign_type=PRODUCTION/TEST/SCRAP）
  ↓
维修工单（rma_repair: 维修描述 + 新SN + 故障码 + 用料）
  ↓  状态→ REPAIRED
质量检验（rma_quality_check: PASS/FAIL）
  ├→ FAIL → 回到维修
  └→ PASS → 状态→ QUALITY_CHECK
        ↓
入库审核（rma_warehouse_in: 仓库类型 ZERO_COST_FINISHED/ZERO_COST_SEMI）
  ↓  状态→ WAREHOUSED
再出货（rma_reship）或 报废（rma_scrap）
```

### 7.2 新旧SN关联机制

维修换码时：
1. 测试工程师在维修工单中填写 `new_sn`
2. 系统创建新 `inventory_item`（new_sn），设置 `replaced_from_sn`=旧SN
3. 旧SN的 `replaced_by_sn`=新SN，`stock_status`=`REPLACED`
4. 入库审核时更新 `rma_return.new_sn`，记录 `repair_count`、`repair_reason`

### 7.3 报废审批流程

```
质量负责人发起报废申请（rma_scrap: PENDING）
  ↓
总经理 或 仓库管理员 审批
  ├→ APPROVED → rma_return.status = SCRAPPED → inventory_item.stock_status = SCRAPPED
  └→ REJECTED → rma_return.status 回退
```

### 7.4 原材料库存双轨制

| 模式 | 表 | 扣减方式 |
|------|-----|----------|
| 无SN批次 | `raw_material_inventory` | 按数量扣减 |
| 有SN批次 | `raw_material_inventory` + `raw_material_sn` | 按SN逐件扣减 |

流水记录在 `raw_material_inventory_log`（变更类型 INCREASE/DECREASE + 变更前后数量）。

### 7.5 原材料SN状态 RawMaterialSnStatus

| 状态 | 说明 |
|------|------|
| `IN_STOCK` | 在库 |
| `CONSUMED` | 已消耗（用于生产） |
| `DEFECTIVE` | 不良品 |
| `RETURNED` | 已退货 |
| `SCRAPPED` | 已报废 |

### 7.6 仓库类型体系

| 仓库类型 | 说明 | 入库来源 |
|----------|------|----------|
| `RAW_MATERIAL` | 原材料仓 | 来料检验合格入库 |
| `SEMI_FINISHED` | 半成品仓 | 生产任务产出半成品 |
| `FINISHED` | 成品仓 | 生产任务产出成品 |
| `ZERO_COST_FINISHED` | 零成本仓-成品 | 维修后入库（无成本） |
| `ZERO_COST_SEMI` | 零成本仓-半成品 | 维修后入库（无成本） |
| `RND` | 研发物料仓 | 研发专用 |

---

## 8. 一期验收清单（全部通过 ✅）

### 主线A：来料管理（7项）
A-01 到货登记 → A-02 到货列表 → A-03 来料检验 → A-04 合格入库 → A-05 让步接收 → A-06 不合格→退货 → A-07 来料导出

### 主线B：返厂维修（16项）
B-01 退货登记 → B-02 退货列表 → B-03 诊断报告 → B-04 分配任务 → B-05 测试查看自己名下 → B-06 测试不能流转 → B-07 维修工单（含新SN） → B-08 新SN校验 → B-09 故障码 → B-10 维修用料 → B-11 用料扣库存 → B-12 流转设备 → B-13 报废发起 → B-14 报废审批 → B-15 报废驳回 → B-16 再出货

### 主线C：出货管理（4项）
C-01 出货登记 → C-02 软件版本号录入 → C-03 U9任务单号关联 → C-04 出货导出

### 主线D：BOM（8项）
D-01 BOM导入 → D-02 BOM编辑 → D-03 BOM版本管理 → D-04 BOM导出 → D-05 齐套分析 → D-06 采购建议 → D-07 采购转主线A → D-08 BOM权限

### 审计日志（5项）
L-01 操作记录 → L-02 变更前后值 → L-03 变更原因强制 → L-04 审计查看 → L-05 不可删除

### 权限（5项）
P-01 管理员全权限 → P-02 质量无系统设置 → P-03 测试仅见自己设备 → P-04 测试不能流转 → P-05 仓管可审核来料

---

## 9. 数据迁移说明

### 9.1 现有 SN 的 current_location 自动填充

```sql
UPDATE inventory_item
SET current_location = CASE
    WHEN stock_status = 'IN_STOCK' THEN '库房'
    WHEN stock_status IN ('SOLD','SOLD_OFFLINE','BORROWED','GIFTED','RND','SAMPLE','TRIAL','PRESOLD','DEPT_PROCUREMENT') THEN '已发出'
    WHEN stock_status = 'SCRAPPED' THEN '已报废'
    WHEN stock_status = 'REPAIR' THEN '维修中'
    ELSE '库房'
END
WHERE current_location IS NULL;
```

### 9.2 现有 SKU 的 sku_type 默认值

新增字段时设置 `default='FINISHED_GOODS'`，现有数据自动填充。

### 9.3 现有 STAFF 用户迁移

上线后由管理员在系统设置页面手动修改角色，不做自动化迁移。