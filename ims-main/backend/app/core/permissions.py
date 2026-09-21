"""
统一权限字典与依赖注入。
前后端权限键语义一致，所有写操作通过 require_permission 校验。
ADMIN 自动放行，不在任何映射中显式校验。
"""

from fastapi import Depends
from app.core.deps import require_roles
from app.models.user import User

# ============================================================
# 权限映射表
# ============================================================

PERMISSION_MAP = {
    # ---- 来料管理 ----
    "incoming.create":      ["ADMIN", "WAREHOUSE"],
    "incoming.inspect":     ["ADMIN", "QUALITY"],
    "incoming.return":      ["ADMIN", "WAREHOUSE", "QUALITY"],
    "incoming.confirm":     ["ADMIN", "WAREHOUSE"],

    # ---- 入库管理 ----
    "inbound.create":       ["ADMIN", "WAREHOUSE"],
    "inbound.edit":         ["ADMIN", "WAREHOUSE"],
    "inbound.submit":       ["ADMIN", "WAREHOUSE"],
    "inbound.approve":      ["ADMIN", "WAREHOUSE"],
    "inbound.cancel":       ["ADMIN", "WAREHOUSE"],

    # ---- 出库管理 ----
    "outbound.create":      ["ADMIN", "WAREHOUSE"],
    "outbound.edit":        ["ADMIN", "WAREHOUSE"],
    "outbound.submit":      ["ADMIN", "WAREHOUSE"],
    "outbound.approve":     ["ADMIN", "WAREHOUSE"],
    "outbound.cancel":      ["ADMIN", "WAREHOUSE"],

    # ---- 返厂维修 ----
    "rma.create_return":    ["ADMIN", "WAREHOUSE"],
    "rma.diagnose":         ["ADMIN", "QUALITY", "TEST_ENGINEER"],
    "rma.assign":           ["ADMIN", "QUALITY"],
    "rma.repair":           ["ADMIN", "PRODUCTION", "TEST_ENGINEER"],
    "rma.quality_check":    ["ADMIN", "QUALITY"],
    "rma.warehouse_in":     ["ADMIN", "WAREHOUSE"],
    "rma.reship":           ["ADMIN", "WAREHOUSE"],
    "rma.knowledge_base":   ["ADMIN", "TEST_ENGINEER", "QUALITY"],
    "rma.request_scrap":    ["ADMIN", "QUALITY", "TEST_ENGINEER"],
    "rma.approve_scrap":    ["ADMIN"],

    # ---- 出货管理 ----
    "shipment.create":      ["ADMIN", "WAREHOUSE"],
    "shipment.edit":        ["ADMIN", "WAREHOUSE"],

    # ---- BOM 与生产 ----
    "bom.create_edit":      ["ADMIN", "WAREHOUSE", "PRODUCTION"],
    "bom.create":           ["ADMIN", "WAREHOUSE", "PRODUCTION"],
    "bom.edit":             ["ADMIN", "WAREHOUSE", "PRODUCTION"],
    "bom.import":           ["ADMIN", "WAREHOUSE", "PRODUCTION"],
    "production_task.create_edit": ["ADMIN", "WAREHOUSE", "PRODUCTION"],
    "production.create":    ["ADMIN", "WAREHOUSE", "PRODUCTION"],
    "production.edit":      ["ADMIN", "WAREHOUSE", "PRODUCTION"],
    "production.start":     ["ADMIN", "WAREHOUSE", "PRODUCTION"],
    "production.complete":  ["ADMIN", "WAREHOUSE", "PRODUCTION"],
    "production.fulfill":   ["ADMIN", "WAREHOUSE", "PRODUCTION"],

    # ---- 库存 ----
    "inventory.import":     ["ADMIN", "WAREHOUSE"],

    # ---- 盘点 ----
    "stocktake.create":     ["ADMIN", "WAREHOUSE"],
    "stocktake.scan":       ["ADMIN", "WAREHOUSE"],
    "stocktake.complete":   ["ADMIN", "WAREHOUSE"],
    "stocktake.cancel":     ["ADMIN", "WAREHOUSE"],

    # ---- 库存调整 ----
    "adjustment.confirm":   ["ADMIN", "WAREHOUSE"],

    # ---- 场站 ----
    "station.create_edit":  ["ADMIN", "WAREHOUSE"],

    # ---- 设备台账 ----
    "device_ledger.create_edit": ["ADMIN", "WAREHOUSE"],

    # ---- 基础数据 ----
    "product.manage":       ["ADMIN", "WAREHOUSE"],
    "partner.manage":       ["ADMIN", "WAREHOUSE"],
    "customer.manage":      ["ADMIN", "WAREHOUSE"],
}


# ============================================================
# 依赖注入函数
# ============================================================

def require_permission(permission_key: str):
    """
    统一权限依赖注入。
    - ADMIN 自动放行，不检查 PERMISSION_MAP。
    - 未知权限键降级为仅 ADMIN 可访问。
    - 前端同名权限键（如 incoming.create）与此完全对应。
    """
    roles = PERMISSION_MAP.get(permission_key, [])
    return require_roles(*roles)