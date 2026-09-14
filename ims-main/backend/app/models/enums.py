import enum


class StockStatus(str, enum.Enum):
    """库存状态（单品维度）。"""
    IN_STOCK = "IN_STOCK"
    SOLD = "SOLD"
    BORROWED = "BORROWED"
    GIFTED = "GIFTED"
    SCRAPPED = "SCRAPPED"
    RND = "RND"           # 研发出库
    SAMPLE = "SAMPLE"     # 样机出库
    TRIAL = "TRIAL"       # 试用出库
    REPAIR = "REPAIR"     # 维修出库
    DEPT_PROCUREMENT = "DEPT_PROCUREMENT"  # 部门采购出库
    PRESOLD = "PRESOLD"               # 准售出
    SOLD_OFFLINE = "SOLD_OFFLINE"     # 售出-线下（已完成）
    REPLACED = "REPLACED"             # 已替换（维修换码后的旧SN）


class StockCondition(str, enum.Enum):
    """库存属性（在库时的成色/来源）。"""
    NEW = "NEW"
    RETURNED_FROM_SALE = "RETURNED_FROM_SALE"
    RETURNED_FROM_SOLD_OFFLINE = "RETURNED_FROM_SOLD_OFFLINE"
    RETURNED_FROM_PRESOLD = "RETURNED_FROM_PRESOLD"
    RETURNED_FROM_BORROW = "RETURNED_FROM_BORROW"
    RETURNED_FROM_GIFT = "RETURNED_FROM_GIFT"
    RETURNED_FROM_SCRAPPED = "RETURNED_FROM_SCRAPPED"
    RETURNED_FROM_RND = "RETURNED_FROM_RND"
    RETURNED_FROM_SAMPLE = "RETURNED_FROM_SAMPLE"
    RETURNED_FROM_TRIAL = "RETURNED_FROM_TRIAL"
    RETURNED_FROM_REPAIR = "RETURNED_FROM_REPAIR"
    RETURNED_FROM_DEPT_PROCUREMENT = "RETURNED_FROM_DEPT_PROCUREMENT"


class OperationStatus(str, enum.Enum):
    """操作状态（单据 + 单品）。"""
    INITIATED = "INITIATED"
    PICKING = "PICKING"
    CHECKING = "CHECKING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class OutboundType(str, enum.Enum):
    """出库类型（顺序见 OUTBOUND_TYPE_ORDER）。"""
    SOLD = "SOLD"                     # 售出-线上
    SOLD_OFFLINE = "SOLD_OFFLINE"     # 售出-线下
    PRESOLD = "PRESOLD"               # 准售出
    GIFTED = "GIFTED"
    SCRAPPED = "SCRAPPED"
    RND = "RND"
    SAMPLE = "SAMPLE"
    TRIAL = "TRIAL"
    REPAIR = "REPAIR"
    DEPT_PROCUREMENT = "DEPT_PROCUREMENT"  # 部门采购
    BORROWED = "BORROWED"


OUTBOUND_TYPE_ORDER = [
    OutboundType.SOLD,
    OutboundType.SOLD_OFFLINE,
    OutboundType.PRESOLD,
    OutboundType.GIFTED,
    OutboundType.SCRAPPED,
    OutboundType.RND,
    OutboundType.SAMPLE,
    OutboundType.TRIAL,
    OutboundType.REPAIR,
    OutboundType.DEPT_PROCUREMENT,
]

RETURN_CONDITION_ORDER = [
    StockCondition.RETURNED_FROM_SALE,
    StockCondition.RETURNED_FROM_SOLD_OFFLINE,
    StockCondition.RETURNED_FROM_PRESOLD,
    StockCondition.RETURNED_FROM_GIFT,
    StockCondition.RETURNED_FROM_SCRAPPED,
    StockCondition.RETURNED_FROM_RND,
    StockCondition.RETURNED_FROM_SAMPLE,
    StockCondition.RETURNED_FROM_TRIAL,
    StockCondition.RETURNED_FROM_REPAIR,
    StockCondition.RETURNED_FROM_DEPT_PROCUREMENT,
]


class InboundMode(str, enum.Enum):
    """入库方式。"""
    PROCUREMENT = "PROCUREMENT"
    NON_PROCUREMENT = "NON_PROCUREMENT"


class SnSource(str, enum.Enum):
    """SN 来源。"""
    MANUAL = "MANUAL"
    AUTO = "AUTO"


class PartnerType(int, enum.Enum):
    """往来单位类型。"""
    BOTH = 0       # 供应商 & 客户
    CUSTOMER = 1   # 客户
    SUPPLIER = 2   # 供应商


class SnMode(str, enum.Enum):
    """SKU 的 SN 录入模式。"""
    MANUAL = "MANUAL"
    AUTO = "AUTO"
    BOTH = "BOTH"


class SkuType(str, enum.Enum):
    """SKU 物料类型。"""
    RAW_MATERIAL = "RAW_MATERIAL"     # 原材料
    FINISHED_GOODS = "FINISHED_GOODS" # 成品


class UserRole(str, enum.Enum):
    """系统用户角色。"""
    ADMIN = "ADMIN"                   # 管理员/总经理
    WAREHOUSE = "WAREHOUSE"           # 仓库管理员
    QUALITY = "QUALITY"               # 来料检/质量负责人
    PRODUCTION = "PRODUCTION"         # 生产
    TEST_ENGINEER = "TEST_ENGINEER"   # 测试工程师
    STAFF = "STAFF"                   # 普通员工


class RawMaterialSnStatus(str, enum.Enum):
    """原材料 SN 状态。"""
    IN_STOCK = "IN_STOCK"       # 在库
    CONSUMED = "CONSUMED"       # 已消耗
    DEFECTIVE = "DEFECTIVE"     # 不良品
    RETURNED = "RETURNED"       # 已退货
    SCRAPPED = "SCRAPPED"       # 已报废


class IncomingStatus(str, enum.Enum):
    """到货/检验状态（主线A）。"""
    PENDING_INSPECTION = "PENDING_INSPECTION"   # 待检验
    INSPECTED = "INSPECTED"                     # 已检验
    ACCEPTED = "ACCEPTED"                       # 合格入库
    REJECTED = "REJECTED"                       # 不合格退货
    WAREHOUSED = "WAREHOUSED"                   # 已入库（仓管确认）


class RmaStatus(str, enum.Enum):
    """返厂维修状态（主线B）。"""
    PENDING_DIAGNOSIS = "PENDING_DIAGNOSIS"   # 待诊断
    DIAGNOSED = "DIAGNOSED"                   # 已诊断
    ASSIGNED = "ASSIGNED"                     # 已分配
    REPAIRING = "REPAIRING"                   # 维修中
    REPAIRED = "REPAIRED"                     # 已修复
    QUALITY_CHECK = "QUALITY_CHECK"           # 质量检验
    WAREHOUSED = "WAREHOUSED"                 # 已入库
    RESHIPPED = "RESHIPPED"                   # 已再出货
    SCRAPPED = "SCRAPPED"                     # 已报废
    PENDING_SCRAP = "PENDING_SCRAP"           # 待报废审批


class ScrapStatus(str, enum.Enum):
    """报废审批状态（主线B）。"""
    PENDING = "PENDING"       # 待审批
    APPROVED = "APPROVED"     # 已通过
    REJECTED = "REJECTED"     # 已驳回


class DiagnosisResult(str, enum.Enum):
    """诊断结果（主线B）。"""
    REPAIRABLE = "REPAIRABLE"           # 可维修


class AssignType(str, enum.Enum):
    """分配类型（主线B）。"""
    PRODUCTION = "PRODUCTION"   # 生产（外观问题）
    TEST = "TEST"               # 测试（功能问题）
    SCRAP = "SCRAP"             # 判定报废


class QualityCheckResult(str, enum.Enum):
    """质量检验结果（主线B）。"""
    PASS = "PASS"   # 通过
    FAIL = "FAIL"   # 不通过


class BomStatus(str, enum.Enum):
    """BOM状态（主线D）。"""
    DRAFT = "DRAFT"           # 草稿
    PUBLISHED = "PUBLISHED"   # 已发布
    DISCONTINUED = "DISCONTINUED"  # 已停产


class TaskStatus(str, enum.Enum):
    """生产任务状态（主线D）。"""
    PENDING = "PENDING"       # 待生产
    IN_PROGRESS = "IN_PROGRESS"  # 生产中
    COMPLETED = "COMPLETED"   # 已完成


class MaterialAvailability(str, enum.Enum):
    """物料齐套状态（主线D）。"""
    COMPLETE = "COMPLETE"     # 齐套
    SHORTAGE = "SHORTAGE"     # 缺料
    FULFILLED = "FULFILLED"   # 已齐套


class WarehouseType(str, enum.Enum):
    """仓库类型（库存归类）。"""
    RAW_MATERIAL = "RAW_MATERIAL"           # 原材料仓
    SEMI_FINISHED = "SEMI_FINISHED"         # 半成品仓
    FINISHED = "FINISHED"                   # 成品仓
    ZERO_COST_FINISHED = "ZERO_COST_FINISHED"   # 零成本仓-成品
    ZERO_COST_SEMI = "ZERO_COST_SEMI"       # 零成本仓-半成品
    RND = "RND"                             # 研发物料仓


class ProductType(str, enum.Enum):
    """产出类型（生产任务）。"""
    FINISHED_PRODUCT = "FINISHED_PRODUCT"   # 成品
    SEMI_FINISHED = "SEMI_FINISHED"         # 半成品


class StationStatus(str, enum.Enum):
    """场站状态。"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class StocktakeMode(str, enum.Enum):
    """盘点模式。"""
    CYCLE = "CYCLE"
    FULL = "FULL"


class StocktakeStatus(str, enum.Enum):
    """盘点状态。"""
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class AdjustmentType(str, enum.Enum):
    """库存调整类型。"""
    SURPLUS = "SURPLUS"
    SHORTAGE = "SHORTAGE"


class DeviceLedgerStatus(str, enum.Enum):
    """设备台账状态。"""
    RUNNING = "RUNNING"
    FAULT = "FAULT"
    RECOVERED = "RECOVERED"


# 出库类型 → 审核后单品库存状态
OUTBOUND_TO_STOCK_STATUS = {
    OutboundType.SOLD: StockStatus.SOLD,
    OutboundType.SOLD_OFFLINE: StockStatus.SOLD_OFFLINE,
    OutboundType.PRESOLD: StockStatus.PRESOLD,
    OutboundType.GIFTED: StockStatus.GIFTED,
    OutboundType.SCRAPPED: StockStatus.SCRAPPED,
    OutboundType.RND: StockStatus.RND,
    OutboundType.SAMPLE: StockStatus.SAMPLE,
    OutboundType.TRIAL: StockStatus.TRIAL,
    OutboundType.REPAIR: StockStatus.REPAIR,
    OutboundType.DEPT_PROCUREMENT: StockStatus.DEPT_PROCUREMENT,
    OutboundType.BORROWED: StockStatus.BORROWED,
}

# 历史出库类型 code 兼容
OUTBOUND_TYPE_ALIASES: dict[str, OutboundType] = {
    "OFFLINE_SOLD": OutboundType.SOLD_OFFLINE,
}


def parse_outbound_type(code: str) -> OutboundType:
    """解析出库类型 code，兼容历史别名。"""
    if code in OUTBOUND_TYPE_ALIASES:
        return OUTBOUND_TYPE_ALIASES[code]
    return OutboundType(code)


# 非采购入库类型 → 默认关联的出库类型
RETURN_CONDITION_TO_OUTBOUND = {
    StockCondition.RETURNED_FROM_SALE: OutboundType.SOLD,
    StockCondition.RETURNED_FROM_SOLD_OFFLINE: OutboundType.SOLD_OFFLINE,
    StockCondition.RETURNED_FROM_PRESOLD: OutboundType.PRESOLD,
    StockCondition.RETURNED_FROM_BORROW: OutboundType.BORROWED,
    StockCondition.RETURNED_FROM_GIFT: OutboundType.GIFTED,
    StockCondition.RETURNED_FROM_SCRAPPED: OutboundType.SCRAPPED,
    StockCondition.RETURNED_FROM_RND: OutboundType.RND,
    StockCondition.RETURNED_FROM_SAMPLE: OutboundType.SAMPLE,
    StockCondition.RETURNED_FROM_TRIAL: OutboundType.TRIAL,
    StockCondition.RETURNED_FROM_REPAIR: OutboundType.REPAIR,
    StockCondition.RETURNED_FROM_DEPT_PROCUREMENT: OutboundType.DEPT_PROCUREMENT,
}

# 非采购入库类型 → 允许的关联出库类型
RETURN_CONDITION_ALLOWED_OUTBOUND: dict[StockCondition, list[OutboundType]] = {
    StockCondition.RETURNED_FROM_SALE: [OutboundType.SOLD],
    StockCondition.RETURNED_FROM_SOLD_OFFLINE: [OutboundType.SOLD_OFFLINE],
    StockCondition.RETURNED_FROM_PRESOLD: [OutboundType.PRESOLD],
    StockCondition.RETURNED_FROM_BORROW: [OutboundType.BORROWED],
    StockCondition.RETURNED_FROM_GIFT: [OutboundType.GIFTED],
    StockCondition.RETURNED_FROM_SCRAPPED: [OutboundType.SCRAPPED],
    StockCondition.RETURNED_FROM_RND: [OutboundType.RND],
    StockCondition.RETURNED_FROM_SAMPLE: [OutboundType.SAMPLE],
    StockCondition.RETURNED_FROM_TRIAL: [OutboundType.TRIAL],
    StockCondition.RETURNED_FROM_REPAIR: [OutboundType.REPAIR],
    StockCondition.RETURNED_FROM_DEPT_PROCUREMENT: [OutboundType.DEPT_PROCUREMENT],
}

# 非采购入库类型 → 单品当前应处的库存状态
RETURN_CONDITION_EXPECTED_STOCK: dict[StockCondition, list[StockStatus]] = {
    StockCondition.RETURNED_FROM_SALE: [StockStatus.SOLD],
    StockCondition.RETURNED_FROM_SOLD_OFFLINE: [StockStatus.SOLD_OFFLINE],
    StockCondition.RETURNED_FROM_PRESOLD: [StockStatus.PRESOLD],
    StockCondition.RETURNED_FROM_BORROW: [StockStatus.BORROWED],
    StockCondition.RETURNED_FROM_GIFT: [StockStatus.GIFTED],
    StockCondition.RETURNED_FROM_SCRAPPED: [StockStatus.SCRAPPED],
    StockCondition.RETURNED_FROM_RND: [StockStatus.RND],
    StockCondition.RETURNED_FROM_SAMPLE: [StockStatus.SAMPLE],
    StockCondition.RETURNED_FROM_TRIAL: [StockStatus.TRIAL],
    StockCondition.RETURNED_FROM_REPAIR: [StockStatus.REPAIR],
    StockCondition.RETURNED_FROM_DEPT_PROCUREMENT: [StockStatus.DEPT_PROCUREMENT],
}