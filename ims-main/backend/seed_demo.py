"""种子演示数据 — 填充所有业务模块的示例记录。"""

import random
import sys
from datetime import date, timedelta, datetime as dt
from decimal import Decimal

from app.db.database import SessionLocal
from app.models.bom import BomDetail, BomHeader, ProductionTask
from app.models.customer import Customer
from app.models.enums import (
    AssignType,
    BomStatus,
    DiagnosisResult,
    InboundMode,
    IncomingStatus,
    MaterialAvailability,
    OperationStatus,
    OutboundType,
    PartnerType,
    QualityCheckResult,
    RawMaterialSnStatus,
    RmaStatus,
    ScrapStatus,
    SkuType,
    SnMode,
    StockCondition,
    StockStatus,
    TaskStatus,
)
from app.models.inbound import InboundOrder, InboundOrderItem, InboundOrderLine
from app.models.incoming import IncomingInspection, IncomingReceipt, IncomingReturn
from app.models.inventory import InventoryDailySummary, InventoryItem, InventoryItemHistory
from app.models.outbound import OutboundOrder, OutboundOrderItem
from app.models.partner import Partner, PartnerGroup
from app.models.product import ProductCategory, ProductSku
from app.models.raw_material import RawMaterialInventory, RawMaterialInventoryLog
from app.models.rma import (
    RmaDiagnosis,
    RmaQualityCheck,
    RmaRepair,
    RmaReship,
    RmaReturn,
    RmaScrap,
    RmaWarehouseIn,
)
from app.models.user import User
from app.models.shipment import Shipment


def random_date(days_back=90):
    return date.today() - timedelta(days=random.randint(1, days_back))


def seed(db):
    if db.query(ProductCategory).count() > 0:
        print("[跳过] 数据库已有数据，跳过填充。")
        return

    # ─── 动态查询用户 ID，与用户数据解耦 ───────────────────────
    all_users = db.query(User).all()
    U = {u.username: u.id for u in all_users}
    # 角色 → 第一个用户名（给种子数据用的快捷引用）
    _role_first = {}
    for u in all_users:
        if u.role not in _role_first:
            _role_first[u.role] = u.username
    A = _role_first  # 简写：A["ADMIN"] → "zwf"
    print(f"[OK] 用户映射: {len(U)} 个账号, 角色: {list(_role_first.keys())}")

    # ============================================================
    # 1. 商品分类
    # ============================================================
    cats = [
        ProductCategory(name="成品—智能设备"),
        ProductCategory(name="成品—配件"),
        ProductCategory(name="原材料—电子元器件"),
        ProductCategory(name="原材料—结构件"),
        ProductCategory(name="原材料—包装材料"),
    ]
    db.add_all(cats)
    db.flush()
    print(f"[OK] 商品分类: {len(cats)} 条")

    # ============================================================
    # 2. 商品 SKU
    # ============================================================
    skus = [
        ProductSku(name="AIoT 智能网关 XG-200", category_id=cats[0].id, barcode="CP00001",
                   sn_mode=SnMode.BOTH, unit="台", sku_code="FG-GW-200", spec="XG-200",
                   sku_type=SkuType.FINISHED_GOODS, remark="旗舰款智能网关"),
        ProductSku(name="AIoT 智能网关 XG-100", category_id=cats[0].id, barcode="CP00002",
                   sn_mode=SnMode.BOTH, unit="台", sku_code="FG-GW-100", spec="XG-100",
                   sku_type=SkuType.FINISHED_GOODS, remark="标准款智能网关"),
        ProductSku(name="4G 通信模块 M-4G", category_id=cats[1].id, barcode="CP00003",
                   sn_mode=SnMode.MANUAL, unit="个", sku_code="FG-4G-01", spec="M-4G-v2",
                   sku_type=SkuType.FINISHED_GOODS, remark="4G通信配件"),
        ProductSku(name="MCU 主控芯片 STM32H7", category_id=cats[2].id, barcode="RM00001",
                   sn_mode=SnMode.MANUAL, unit="颗", sku_code="RM-MCU-H7", spec="STM32H743",
                   sku_type=SkuType.RAW_MATERIAL),
        ProductSku(name="电源管理芯片 PMIC-12V", category_id=cats[2].id, barcode="RM00002",
                   sn_mode=SnMode.MANUAL, unit="颗", sku_code="RM-PMIC-12", spec="PMIC-12V-3A",
                   sku_type=SkuType.RAW_MATERIAL),
        ProductSku(name="Flash 存储芯片 16MB", category_id=cats[2].id, barcode="RM00003",
                   sn_mode=SnMode.MANUAL, unit="颗", sku_code="RM-FLASH-16", spec="W25Q128",
                   sku_type=SkuType.RAW_MATERIAL),
        ProductSku(name="WiFi/BT 模组", category_id=cats[2].id, barcode="RM00004",
                   sn_mode=SnMode.MANUAL, unit="个", sku_code="RM-WIFI-01", spec="ESP32-C3",
                   sku_type=SkuType.RAW_MATERIAL),
        ProductSku(name="铝合金外壳 XG-200", category_id=cats[3].id, barcode="RM00005",
                   sn_mode=SnMode.MANUAL, unit="套", sku_code="RM-CASE-200", spec="XG-200-Housing",
                   sku_type=SkuType.RAW_MATERIAL),
        ProductSku(name="铝合金外壳 XG-100", category_id=cats[3].id, barcode="RM00006",
                   sn_mode=SnMode.MANUAL, unit="套", sku_code="RM-CASE-100", spec="XG-100-Housing",
                   sku_type=SkuType.RAW_MATERIAL),
        ProductSku(name="PCB 主板 V2.0", category_id=cats[3].id, barcode="RM00007",
                   sn_mode=SnMode.MANUAL, unit="块", sku_code="RM-PCB-20", spec="PCB-V2.0-4L",
                   sku_type=SkuType.RAW_MATERIAL),
        ProductSku(name="彩盒包装", category_id=cats[4].id, barcode="RM00008",
                   sn_mode=SnMode.MANUAL, unit="个", sku_code="RM-BOX-01", spec="350x250x80mm",
                   sku_type=SkuType.RAW_MATERIAL),
        ProductSku(name="说明书/保修卡", category_id=cats[4].id, barcode="RM00009",
                   sn_mode=SnMode.MANUAL, unit="套", sku_code="RM-MANUAL", spec="A5-双语",
                   sku_type=SkuType.RAW_MATERIAL),
    ]
    db.add_all(skus)
    db.flush()

    # ─── TES-600 变压器状态综合监测装置产品 ───────────────────
    tes600 = ProductSku(name="TES-600变压器状态综合监测装置", category_id=cats[0].id, barcode="CP00010",
                        sn_mode=SnMode.BOTH, unit="台", sku_code="303-019", spec="TES-600",
                        sku_type=SkuType.FINISHED_GOODS, remark="变压器（电抗器）状态综合在线监测装置")
    b_dw = ProductSku(name="TES-600变压器状态综合监测装置 B相DW", category_id=cats[1].id, barcode="CP00011",
                      sn_mode=SnMode.MANUAL, unit="台", sku_code="201-018", spec="B-DW",
                      sku_type=SkuType.FINISHED_GOODS, remark="B相监测单元")
    ac_dw = ProductSku(name="TES-600变压器状态综合监测装置 AC相DW", category_id=cats[1].id, barcode="CP00012",
                       sn_mode=SnMode.MANUAL, unit="台", sku_code="201-019", spec="AC-DW",
                       sku_type=SkuType.FINISHED_GOODS, remark="AC相监测单元")
    hd_au = ProductSku(name="HD-AU902V1.0.0型采集单元", category_id=cats[1].id, barcode="CP00013",
                       sn_mode=SnMode.MANUAL, unit="台", sku_code="305-016", spec="HD-AU902V1.0.0",
                       sku_type=SkuType.FINISHED_GOODS, remark="采集单元")
    db.add_all([tes600, b_dw, ac_dw, hd_au])
    db.flush()

    # ─── TES-600 原材料 SKU ──────────────────────────────────
    rm_air_switch = ProductSku(name="2P/10A空开", category_id=cats[2].id, barcode="RM00020",
                               sn_mode=SnMode.MANUAL, unit="个", sku_code="RM-AIR-10A", spec="2P/10A",
                               sku_type=SkuType.RAW_MATERIAL)
    rm_power_24v = ProductSku(name="24V电源模块", category_id=cats[2].id, barcode="RM00021",
                              sn_mode=SnMode.MANUAL, unit="个", sku_code="RM-PWR-24V", spec="24V/5A",
                              sku_type=SkuType.RAW_MATERIAL)
    rm_industrial_pc = ProductSku(name="工控机", category_id=cats[2].id, barcode="RM00022",
                                  sn_mode=SnMode.MANUAL, unit="台", sku_code="RM-IPC-01", spec="IPC-610L",
                                  sku_type=SkuType.RAW_MATERIAL)
    rm_ribbon_cable = ProductSku(name="排线", category_id=cats[2].id, barcode="RM00023",
                                 sn_mode=SnMode.MANUAL, unit="条", sku_code="RM-CABLE-01", spec="FC-16P",
                                 sku_type=SkuType.RAW_MATERIAL)
    rm_terminal_block = ProductSku(name="接线端子排", category_id=cats[2].id, barcode="RM00024",
                                   sn_mode=SnMode.MANUAL, unit="个", sku_code="RM-TERM-01", spec="TB-12P",
                                   sku_type=SkuType.RAW_MATERIAL)
    rm_atom_wire_y = ProductSku(name="原子线(黄)", category_id=cats[2].id, barcode="RM00025",
                                sn_mode=SnMode.MANUAL, unit="米", sku_code="RM-WIRE-Y", spec="AWG24-黄",
                                sku_type=SkuType.RAW_MATERIAL)
    rm_atom_wire_b = ProductSku(name="原子线(蓝)", category_id=cats[2].id, barcode="RM00026",
                                sn_mode=SnMode.MANUAL, unit="米", sku_code="RM-WIRE-B", spec="AWG24-蓝",
                                sku_type=SkuType.RAW_MATERIAL)
    rm_cabinet = ProductSku(name="机柜", category_id=cats[3].id, barcode="RM00027",
                            sn_mode=SnMode.MANUAL, unit="台", sku_code="RM-CAB-01", spec="600x800x2200",
                            sku_type=SkuType.RAW_MATERIAL)
    rm_display = ProductSku(name="显示屏", category_id=cats[3].id, barcode="RM00028",
                            sn_mode=SnMode.MANUAL, unit="个", sku_code="RM-LCD-01", spec="15.6寸",
                            sku_type=SkuType.RAW_MATERIAL)
    db.add_all([rm_air_switch, rm_power_24v, rm_industrial_pc, rm_ribbon_cable,
                rm_terminal_block, rm_atom_wire_y, rm_atom_wire_b, rm_cabinet, rm_display])
    db.flush()

    print(f"[OK] 商品 SKU: {len(skus) + 4 + 9} 条 (含 TES-600 系列)")

    # ============================================================
    # 3. 往来单位分组 & 往来单位
    # ============================================================
    groups = [
        PartnerGroup(name="芯片供应商"),
        PartnerGroup(name="结构件供应商"),
        PartnerGroup(name="包装供应商"),
        PartnerGroup(name="经销商"),
        PartnerGroup(name="终端客户"),
    ]
    db.add_all(groups)
    db.flush()

    partners = [
        Partner(name="深圳华强电子有限公司", group_id=groups[0].id, partner_type=PartnerType.SUPPLIER.value),
        Partner(name="上海芯源微电子有限公司", group_id=groups[0].id, partner_type=PartnerType.SUPPLIER.value),
        Partner(name="东莞精密五金制品有限公司", group_id=groups[1].id, partner_type=PartnerType.SUPPLIER.value),
        Partner(name="苏州博世包装材料有限公司", group_id=groups[2].id, partner_type=PartnerType.SUPPLIER.value),
        Partner(name="北京智联科技有限公司", group_id=groups[3].id, partner_type=PartnerType.CUSTOMER.value),
        Partner(name="广州云创数据有限公司", group_id=groups[3].id, partner_type=PartnerType.CUSTOMER.value),
        Partner(name="华为技术有限公司", group_id=groups[4].id, partner_type=PartnerType.CUSTOMER.value),
        Partner(name="中国移动通信集团", group_id=groups[4].id, partner_type=PartnerType.CUSTOMER.value),
        Partner(name="深圳赛格电子市场有限公司", group_id=groups[0].id, partner_type=PartnerType.BOTH.value),
        Partner(name="杭州海康威视数字技术有限公司", group_id=groups[4].id, partner_type=PartnerType.CUSTOMER.value),
    ]
    db.add_all(partners)
    db.flush()
    print(f"[OK] 往来单位分组: {len(groups)} 条, 往来单位: {len(partners)} 条")

    # ============================================================
    # 3.5 客户
    # ============================================================
    customers = [
        Customer(name="北京智联科技有限公司", weight=100),
        Customer(name="广州云创数据有限公司", weight=90),
        Customer(name="华为技术有限公司", weight=95),
        Customer(name="中国移动通信集团", weight=85),
        Customer(name="杭州海康威视数字技术有限公司", weight=80),
        Customer(name="深圳腾讯计算机系统有限公司", weight=75),
        Customer(name="阿里巴巴集团", weight=70),
        Customer(name="上海商汤科技开发有限公司", weight=60),
    ]
    db.add_all(customers)
    db.flush()
    print(f"[OK] 客户: {len(customers)} 条")

    # ============================================================
    # 4. 库存单品 + 入库单
    # ============================================================
    # XG-200 在库 30 台
    xg200_items = []
    for i in range(1, 31):
        sn = f"XG200-{date.today().strftime('%y%m')}-{i:04d}"
        item = InventoryItem(
            item_sn=sn, sku_id=skus[0].id,
            stock_status=StockStatus.IN_STOCK.value,
            stock_condition=StockCondition.NEW.value,
            operation_status=OperationStatus.COMPLETED.value,
            current_location="A区-01架",
            unit_price=2850.00,
            quantity=1,
        )
        xg200_items.append(item)
    db.add_all(xg200_items)
    db.flush()

    # XG-100 在库 20 台
    xg100_items = []
    for i in range(1, 21):
        sn = f"XG100-{date.today().strftime('%y%m')}-{i:04d}"
        item = InventoryItem(
            item_sn=sn, sku_id=skus[1].id,
            stock_status=StockStatus.IN_STOCK.value,
            stock_condition=StockCondition.NEW.value,
            operation_status=OperationStatus.COMPLETED.value,
            current_location="A区-02架",
            unit_price=1680.00,
            quantity=1,
        )
        xg100_items.append(item)
    db.add_all(xg100_items)
    db.flush()

    # 4G 模块 在库 50 个
    m4g_items = []
    for i in range(1, 51):
        sn = f"M4G-{date.today().strftime('%y%m')}-{i:04d}"
        item = InventoryItem(
            item_sn=sn, sku_id=skus[2].id,
            stock_status=StockStatus.IN_STOCK.value,
            stock_condition=StockCondition.NEW.value,
            operation_status=OperationStatus.COMPLETED.value,
            current_location="B区-03架",
            unit_price=320.00,
            quantity=1,
        )
        m4g_items.append(item)
    db.add_all(m4g_items)
    db.flush()

    # 已售出的 XG-200 (售出5台)
    sold_items = []
    for i in range(31, 36):
        sn = f"XG200-{date.today().strftime('%y%m')}-{i:04d}"
        item = InventoryItem(
            item_sn=sn, sku_id=skus[0].id,
            stock_status=StockStatus.SOLD.value,
            stock_condition=StockCondition.NEW.value,
            operation_status=OperationStatus.COMPLETED.value,
            current_location="已发出",
            unit_price=2850.00,
            quantity=1,
        )
        sold_items.append(item)
    db.add_all(sold_items)
    db.flush()

    print(f"[OK] 库存单品: {len(xg200_items) + len(xg100_items) + len(m4g_items) + len(sold_items)} 条")

    # ============================================================
    # 5. 入库单 (采购入库)
    # ============================================================
    today = date.today()
    inbound = InboundOrder(
        order_no=f"JIN-{today.strftime('%y%m%d')}-001",
        inbound_mode=InboundMode.PROCUREMENT.value,
        stock_condition=StockCondition.NEW.value,
        partner_id=partners[0].id,
        operation_status=OperationStatus.COMPLETED.value,
        total_qty=30,
        submitted_by=2,
        reviewed_by=1,
        submitted_at=today - timedelta(days=7),
        reviewed_at=today - timedelta(days=6),
        remark="XG-200 首批量产入库",
    )
    db.add(inbound)
    db.flush()

    line = InboundOrderLine(
        inbound_order_id=inbound.id,
        sku_id=skus[0].id,
        quantity=30,
        unit_price=2850.00,
    )
    db.add(line)
    db.flush()

    for item in xg200_items:
        db.add(InboundOrderItem(
            inbound_order_id=inbound.id,
            line_id=line.id,
            item_sn=item.item_sn,
            item_id=item.id,
            sn_source="MANUAL",
        ))

    # XG-100 入库
    inbound2 = InboundOrder(
        order_no=f"JIN-{today.strftime('%y%m%d')}-002",
        inbound_mode=InboundMode.PROCUREMENT.value,
        stock_condition=StockCondition.NEW.value,
        partner_id=partners[1].id,
        operation_status=OperationStatus.COMPLETED.value,
        total_qty=20,
        submitted_by=2,
        reviewed_by=1,
        submitted_at=today - timedelta(days=5),
        reviewed_at=today - timedelta(days=4),
        remark="XG-100 入库",
    )
    db.add(inbound2)
    db.flush()

    line2 = InboundOrderLine(
        inbound_order_id=inbound2.id,
        sku_id=skus[1].id,
        quantity=20,
        unit_price=1680.00,
    )
    db.add(line2)
    db.flush()

    for item in xg100_items:
        db.add(InboundOrderItem(
            inbound_order_id=inbound2.id,
            line_id=line2.id,
            item_sn=item.item_sn,
            item_id=item.id,
            sn_source="MANUAL",
        ))

    # 4G 模块入库
    inbound3 = InboundOrder(
        order_no=f"JIN-{today.strftime('%y%m%d')}-003",
        inbound_mode=InboundMode.PROCUREMENT.value,
        stock_condition=StockCondition.NEW.value,
        partner_id=partners[2].id,
        operation_status=OperationStatus.COMPLETED.value,
        total_qty=50,
        submitted_by=2,
        reviewed_by=1,
        submitted_at=today - timedelta(days=3),
        reviewed_at=today - timedelta(days=2),
        remark="4G通信模块入库",
    )
    db.add(inbound3)
    db.flush()

    line3 = InboundOrderLine(
        inbound_order_id=inbound3.id,
        sku_id=skus[2].id,
        quantity=50,
        unit_price=320.00,
    )
    db.add(line3)
    db.flush()

    for item in m4g_items:
        db.add(InboundOrderItem(
            inbound_order_id=inbound3.id,
            line_id=line3.id,
            item_sn=item.item_sn,
            item_id=item.id,
            sn_source="MANUAL",
        ))

    print(f"[OK] 入库单: 3 条")

    # ============================================================
    # 6. 出库单 (售出)
    # ============================================================
    outbound = OutboundOrder(
        order_no=f"JOUT-{today.strftime('%y%m%d')}-001",
        outbound_type=OutboundType.SOLD.value,
        partner_id=partners[4].id,
        customer_name="北京智联科技有限公司",
        operation_status=OperationStatus.COMPLETED.value,
        total_qty=5,
        submitted_by=2,
        reviewed_by=1,
        submitted_at=today - timedelta(days=2),
        reviewed_at=today - timedelta(days=1),
        remark="XG-200 首批出货",
    )
    db.add(outbound)
    db.flush()

    for item in sold_items:
        db.add(OutboundOrderItem(
            outbound_order_id=outbound.id,
            item_id=item.id,
            sku_id=skus[0].id,
            quantity=1,
        ))

    print(f"[OK] 出库单(售出): 1 条")

    # 更多出库类型 — 样机出库 (XG-200 2台)
    sample_items = []
    for i in range(36, 38):
        sn = f"XG200-{today.strftime('%y%m')}-{i:04d}"
        item = InventoryItem(
            item_sn=sn, sku_id=skus[0].id,
            stock_status=StockStatus.SAMPLE.value,
            stock_condition=StockCondition.NEW.value,
            operation_status=OperationStatus.COMPLETED.value,
            current_location="已发出",
            unit_price=2850.00,
            quantity=1,
        )
        sample_items.append(item)
    db.add_all(sample_items)
    db.flush()

    outbound_sample = OutboundOrder(
        order_no=f"JOUT-{today.strftime('%y%m%d')}-002",
        outbound_type=OutboundType.SAMPLE.value,
        partner_id=partners[6].id,
        customer_name="华为技术有限公司",
        operation_status=OperationStatus.COMPLETED.value,
        total_qty=2,
        submitted_by=2,
        reviewed_by=1,
        submitted_at=today - timedelta(days=10),
        reviewed_at=today - timedelta(days=9),
        remark="XG-200 样机送测华为",
    )
    db.add(outbound_sample)
    db.flush()
    for item in sample_items:
        db.add(OutboundOrderItem(
            outbound_order_id=outbound_sample.id,
            item_id=item.id,
            sku_id=skus[0].id,
            quantity=1,
        ))

    # 研发出库 (XG-100 3台)
    rnd_items = []
    for i in range(21, 24):
        sn = f"XG100-{today.strftime('%y%m')}-{i:04d}"
        item = InventoryItem(
            item_sn=sn, sku_id=skus[1].id,
            stock_status=StockStatus.RND.value,
            stock_condition=StockCondition.NEW.value,
            operation_status=OperationStatus.COMPLETED.value,
            current_location="研发部",
            unit_price=1680.00,
            quantity=1,
        )
        rnd_items.append(item)
    db.add_all(rnd_items)
    db.flush()

    outbound_rnd = OutboundOrder(
        order_no=f"JOUT-{today.strftime('%y%m%d')}-003",
        outbound_type=OutboundType.RND.value,
        partner_id=partners[8].id,
        customer_name="深圳赛格电子市场有限公司",
        operation_status=OperationStatus.COMPLETED.value,
        total_qty=3,
        submitted_by=4,
        reviewed_by=1,
        submitted_at=today - timedelta(days=8),
        reviewed_at=today - timedelta(days=7),
        remark="XG-100 研发测试用机",
    )
    db.add(outbound_rnd)
    db.flush()
    for item in rnd_items:
        db.add(OutboundOrderItem(
            outbound_order_id=outbound_rnd.id,
            item_id=item.id,
            sku_id=skus[1].id,
            quantity=1,
        ))

    # 借用出库 (XG-200 1台)
    borrow_items = []
    sn = f"XG200-{today.strftime('%y%m')}-0038"
    item = InventoryItem(
        item_sn=sn, sku_id=skus[0].id,
        stock_status=StockStatus.BORROWED.value,
        stock_condition=StockCondition.NEW.value,
        operation_status=OperationStatus.COMPLETED.value,
        current_location="已借出",
        unit_price=2850.00,
        quantity=1,
    )
    borrow_items.append(item)
    db.add_all(borrow_items)
    db.flush()

    outbound_borrow = OutboundOrder(
        order_no=f"JOUT-{today.strftime('%y%m%d')}-004",
        outbound_type=OutboundType.BORROWED.value,
        partner_id=partners[7].id,
        customer_name="中国移动通信集团",
        operation_status=OperationStatus.PICKING.value,
        total_qty=1,
        submitted_by=2,
        submitted_at=today - timedelta(days=3),
        remark="借用XG-200 1台用于现场演示",
    )
    db.add(outbound_borrow)
    db.flush()
    for item in borrow_items:
        db.add(OutboundOrderItem(
            outbound_order_id=outbound_borrow.id,
            item_id=item.id,
            sku_id=skus[0].id,
            quantity=1,
        ))

    print(f"[OK] 出库单: 4 条 (售出/样机/研发/借用)")

    # ============================================================
    # 7. BOM 管理 — TES-600 真实多层级 BOM
    # ============================================================
    # Level 0: TES-600 整机
    bom_tes600 = BomHeader(
        bom_no=f"BOM-{today.strftime('%y%m')}-001",
        bom_name="TES-600变压器状态综合监测系统 BOM",
        version="V1.0",
        product_sku_id=tes600.id,
        product_sku_code=tes600.sku_code,
        product_sku_name=tes600.name,
        plan_quantity=50,
        status=BomStatus.PUBLISHED,
        created_by=U[A["ADMIN"]],
        remark="2026年Q3量产版本，含4个子组件",
    )
    db.add(bom_tes600)
    db.flush()

    # Level 1: B相DW 子组件 (作为明细行)
    b_dw_detail = BomDetail(
        bom_id=bom_tes600.id, level=1, parent_detail_id=None,
        material_sku_id=b_dw.id, material_sku_code=b_dw.sku_code,
        material_sku_name=b_dw.name, spec=b_dw.spec,
        unit="台", quantity_per_unit=1, wastage_rate=0,
        item_version="A00", process_note="B相监测单元装配",
        remark="201-018",
    )
    db.add(b_dw_detail)
    db.flush()

    # Level 2: B相DW 零件明细
    b_dw_parts = [
        BomDetail(bom_id=bom_tes600.id, level=2, parent_detail_id=b_dw_detail.id,
                  material_sku_id=rm_air_switch.id, material_sku_code=rm_air_switch.sku_code,
                  material_sku_name=rm_air_switch.name, spec=rm_air_switch.spec,
                  unit="个", quantity_per_unit=1, wastage_rate=0,
                  item_version="A00", process_note="B相DW 空开"),
        BomDetail(bom_id=bom_tes600.id, level=2, parent_detail_id=b_dw_detail.id,
                  material_sku_id=rm_terminal_block.id, material_sku_code=rm_terminal_block.sku_code,
                  material_sku_name=rm_terminal_block.name, spec=rm_terminal_block.spec,
                  unit="个", quantity_per_unit=2, wastage_rate=0,
                  item_version="A00", process_note="B相DW 接线端子"),
        BomDetail(bom_id=bom_tes600.id, level=2, parent_detail_id=b_dw_detail.id,
                  material_sku_id=rm_ribbon_cable.id, material_sku_code=rm_ribbon_cable.sku_code,
                  material_sku_name=rm_ribbon_cable.name, spec=rm_ribbon_cable.spec,
                  unit="条", quantity_per_unit=3, wastage_rate=0,
                  item_version="A00", process_note="B相DW 排线连接"),
    ]
    db.add_all(b_dw_parts)

    # Level 1: AC相DW 子组件
    ac_dw_detail = BomDetail(
        bom_id=bom_tes600.id, level=1, parent_detail_id=None,
        material_sku_id=ac_dw.id, material_sku_code=ac_dw.sku_code,
        material_sku_name=ac_dw.name, spec=ac_dw.spec,
        unit="台", quantity_per_unit=1, wastage_rate=0,
        item_version="A00", process_note="AC相监测单元装配",
        remark="201-019",
    )
    db.add(ac_dw_detail)
    db.flush()

    # Level 2: AC相DW 零件明细
    ac_dw_parts = [
        BomDetail(bom_id=bom_tes600.id, level=2, parent_detail_id=ac_dw_detail.id,
                  material_sku_id=rm_air_switch.id, material_sku_code=rm_air_switch.sku_code,
                  material_sku_name=rm_air_switch.name, spec=rm_air_switch.spec,
                  unit="个", quantity_per_unit=1, wastage_rate=0,
                  item_version="A00", process_note="AC相DW 空开"),
        BomDetail(bom_id=bom_tes600.id, level=2, parent_detail_id=ac_dw_detail.id,
                  material_sku_id=rm_terminal_block.id, material_sku_code=rm_terminal_block.sku_code,
                  material_sku_name=rm_terminal_block.name, spec=rm_terminal_block.spec,
                  unit="个", quantity_per_unit=2, wastage_rate=0,
                  item_version="A00", process_note="AC相DW 接线端子"),
        BomDetail(bom_id=bom_tes600.id, level=2, parent_detail_id=ac_dw_detail.id,
                  material_sku_id=rm_ribbon_cable.id, material_sku_code=rm_ribbon_cable.sku_code,
                  material_sku_name=rm_ribbon_cable.name, spec=rm_ribbon_cable.spec,
                  unit="条", quantity_per_unit=3, wastage_rate=0,
                  item_version="A00", process_note="AC相DW 排线连接"),
    ]
    db.add_all(ac_dw_parts)

    # Level 1: HD-AU902 采集单元
    hd_au_detail = BomDetail(
        bom_id=bom_tes600.id, level=1, parent_detail_id=None,
        material_sku_id=hd_au.id, material_sku_code=hd_au.sku_code,
        material_sku_name=hd_au.name, spec=hd_au.spec,
        unit="台", quantity_per_unit=1, wastage_rate=0,
        item_version="V1.0.0", process_note="采集单元装配",
        remark="305-016",
    )
    db.add(hd_au_detail)
    db.flush()

    # Level 2: HD-AU902 零件明细
    hd_au_parts = [
        BomDetail(bom_id=bom_tes600.id, level=2, parent_detail_id=hd_au_detail.id,
                  material_sku_id=rm_ribbon_cable.id, material_sku_code=rm_ribbon_cable.sku_code,
                  material_sku_name=rm_ribbon_cable.name, spec=rm_ribbon_cable.spec,
                  unit="条", quantity_per_unit=4, wastage_rate=5.0,
                  item_version="V1.0.0", process_note="采集单元 排线连接"),
        BomDetail(bom_id=bom_tes600.id, level=2, parent_detail_id=hd_au_detail.id,
                  material_sku_id=rm_atom_wire_y.id, material_sku_code=rm_atom_wire_y.sku_code,
                  material_sku_name=rm_atom_wire_y.name, spec=rm_atom_wire_y.spec,
                  unit="米", quantity_per_unit=0.5, wastage_rate=0,
                  item_version="V1.0.0", process_note="采集单元 原子线黄"),
        BomDetail(bom_id=bom_tes600.id, level=2, parent_detail_id=hd_au_detail.id,
                  material_sku_id=rm_atom_wire_b.id, material_sku_code=rm_atom_wire_b.sku_code,
                  material_sku_name=rm_atom_wire_b.name, spec=rm_atom_wire_b.spec,
                  unit="米", quantity_per_unit=0.5, wastage_rate=0,
                  item_version="V1.0.0", process_note="采集单元 原子线蓝"),
    ]
    db.add_all(hd_au_parts)

    # Level 1: 整机级零件 (直接挂在整机下)
    level1_parts = [
        BomDetail(bom_id=bom_tes600.id, level=1, parent_detail_id=None,
                  material_sku_id=rm_cabinet.id, material_sku_code=rm_cabinet.sku_code,
                  material_sku_name=rm_cabinet.name, spec=rm_cabinet.spec,
                  unit="台", quantity_per_unit=1, wastage_rate=0,
                  item_version="A00", process_note="标准机柜"),
        BomDetail(bom_id=bom_tes600.id, level=1, parent_detail_id=None,
                  material_sku_id=rm_display.id, material_sku_code=rm_display.sku_code,
                  material_sku_name=rm_display.name, spec=rm_display.spec,
                  unit="个", quantity_per_unit=1, wastage_rate=0,
                  item_version="A00", process_note="监控显示屏"),
        BomDetail(bom_id=bom_tes600.id, level=1, parent_detail_id=None,
                  material_sku_id=rm_industrial_pc.id, material_sku_code=rm_industrial_pc.sku_code,
                  material_sku_name=rm_industrial_pc.name, spec=rm_industrial_pc.spec,
                  unit="台", quantity_per_unit=1, wastage_rate=0,
                  item_version="A00", process_note="工控主机"),
        BomDetail(bom_id=bom_tes600.id, level=1, parent_detail_id=None,
                  material_sku_id=rm_power_24v.id, material_sku_code=rm_power_24v.sku_code,
                  material_sku_name=rm_power_24v.name, spec=rm_power_24v.spec,
                  unit="个", quantity_per_unit=1, wastage_rate=0,
                  item_version="A00", process_note="24V供电模块"),
    ]
    db.add_all(level1_parts)

    total_details = len(b_dw_parts) + len(ac_dw_parts) + len(hd_au_parts) + len(level1_parts) + 3
    print(f"[OK] BOM: 1 条主表 (TES-600), {total_details} 条明细 (3级层级结构)")

    # ============================================================
    # 7.5 生产任务 (主线D)
    # ============================================================
    tasks = [
        ProductionTask(
            task_no=f"TASK-{today.strftime('%y%m')}-001",
            bom_id=bom_tes600.id,
            plan_quantity=50,
            material_availability=MaterialAvailability.COMPLETE.value,
            status=TaskStatus.COMPLETED.value,
            start_date=today - timedelta(days=20),
            end_date=today - timedelta(days=10),
            created_by=U[A["PRODUCTION"]],
        ),
        ProductionTask(
            task_no=f"TASK-{today.strftime('%y%m')}-002",
            bom_id=bom_tes600.id,
            plan_quantity=30,
            material_availability=MaterialAvailability.COMPLETE.value,
            status=TaskStatus.IN_PROGRESS.value,
            start_date=today - timedelta(days=5),
            end_date=today + timedelta(days=10),
            created_by=U[A["PRODUCTION"]],
        ),
        ProductionTask(
            task_no=f"TASK-{today.strftime('%y%m')}-003",
            bom_id=bom_tes600.id,
            plan_quantity=20,
            material_availability=MaterialAvailability.SHORTAGE.value,
            status=TaskStatus.PENDING.value,
            start_date=today + timedelta(days=5),
            end_date=today + timedelta(days=20),
            created_by=U[A["PRODUCTION"]],
        ),
    ]
    db.add_all(tasks)
    db.flush()
    print(f"[OK] 生产任务: {len(tasks)} 条 (已完成/生产中/待生产)")

    # ============================================================
    # 8. 来料管理 (主线A)
    # ============================================================
    receipts = []
    for i, (sku, qty, supplier) in enumerate([
        (skus[3], 500, partners[0]),   # MCU 芯片
        (skus[4], 1000, partners[1]),  # 电源芯片
        (skus[5], 800, partners[0]),   # Flash
        (skus[6], 600, partners[1]),   # WiFi模组
        (skus[7], 300, partners[2]),   # 外壳200
        (skus[9], 200, partners[2]),   # PCB
    ]):
        receipt = IncomingReceipt(
            receipt_no=f"RC-{today.strftime('%y%m%d')}-{i+1:03d}",
            supplier_id=supplier.id,
            sku_id=sku.id,
            batch_no=f"BATCH-{today.strftime('%y%m')}-{random.randint(100, 999)}",
            quantity=qty,
            unit=sku.unit or "个",
            status=IncomingStatus.ACCEPTED.value if i < 5 else IncomingStatus.PENDING_INSPECTION.value,
            delivery_date=random_date(30),
            inspector_id=3,
            inspection_date=random_date(25) if i < 5 else None,
            confirmed_at=random_date(24) if i < 5 else None,
            confirmed_by=1 if i < 5 else None,
            remark=f"{sku.name} 来料批次",
        )
        receipts.append(receipt)
    db.add_all(receipts)
    db.flush()

    # 检验报告
    for i, receipt in enumerate(receipts[:5]):
        dq = random.randint(0, 2)
        db.add(IncomingInspection(
            receipt_id=receipt.id,
            inspection_no=f"INSP-{today.strftime('%y%m%d')}-{i+1:03d}",
            inspector_id=3,
            inspection_date=receipt.inspection_date or today,
            result="ACCEPTED",
            sample_qty=min(20, receipt.quantity // 10),
            defect_qty=dq,
            defect_description="外观无异常，电气性能合格" if dq == 0 else "少量引脚氧化",
            remark="检验通过",
        ))

    print(f"[OK] 来料到货单: {len(receipts)} 条, 检验报告: 5 条")

    # ============================================================
    # 8.5 原材料批次库存 (基于到货数据)
    # ============================================================
    raw_inventories = []
    for i, receipt in enumerate(receipts[:5]):
        inv = RawMaterialInventory(
            sku_id=receipt.sku_id,
            batch_no=receipt.batch_no,
            quantity=receipt.quantity // 2,
            unit=receipt.unit,
            status=RawMaterialSnStatus.IN_STOCK.value,
            supplier_id=receipt.supplier_id,
            receipt_no=receipt.receipt_no,
            remark=f"{receipt.remark} — 库存批次",
            created_at=dt.combine(today - timedelta(days=random.randint(5, 20)), dt.min.time()),
            updated_at=dt.combine(today - timedelta(days=random.randint(5, 20)), dt.min.time()),
        )
        raw_inventories.append(inv)
    db.add_all(raw_inventories)
    db.flush()

    raw_logs = []
    for inv in raw_inventories:
        raw_logs.append(RawMaterialInventoryLog(
            inventory_id=inv.id,
            change_type="INCREASE",
            change_qty=inv.quantity,
            before_qty=0,
            after_qty=inv.quantity,
            change_reason="来料检验合格入库",
            related_order_no=inv.receipt_no,
            operator_id=U[A["QUALITY"]],
            remark="来料入库",
            created_at=dt.combine(today - timedelta(days=random.randint(5, 20)), dt.min.time()),
        ))
    db.add_all(raw_logs)
    print(f"[OK] 原材料批次库存: {len(raw_inventories)} 条, 流水: {len(raw_logs)} 条")

    # ============================================================
    # 8.6 来料退货 (主线A)
    # ============================================================
    return_receipts = [
        IncomingReturn(
            receipt_id=receipts[3].id,
            return_no=f"RT-{today.strftime('%y%m%d')}-001",
            return_qty=10,
            return_reason="WiFi模组部分批次信号强度不达标",
            return_date=today - timedelta(days=12),
            status="CONFIRMED",
            operator_id=U[A["QUALITY"]],
            remark="供应商已确认退货",
        ),
        IncomingReturn(
            receipt_id=receipts[4].id,
            return_no=f"RT-{today.strftime('%y%m%d')}-002",
            return_qty=5,
            return_reason="外壳表面有轻微划痕，不符合外观标准",
            return_date=today - timedelta(days=5),
            status="PENDING",
            operator_id=U[A["QUALITY"]],
            remark="待供应商确认",
        ),
    ]
    db.add_all(return_receipts)
    db.flush()
    print(f"[OK] 来料退货: {len(return_receipts)} 条")

    # ============================================================
    # 9. 返厂维修 (主线B)
    # ============================================================
    rma1 = RmaReturn(
        return_no=f"FC-{today.strftime('%y%m%d')}-001",
        sku_id=skus[0].id,
        sn="XG200-2509-0015",
        quantity=1,
        unit="台",
        spec=skus[0].spec,
        customer_name="北京智联科技有限公司",
        return_reason="设备无法正常启动，电源指示灯不亮",
        return_date=today - timedelta(days=15),
        status=RmaStatus.PENDING_DIAGNOSIS.value,
        problem_description="客户反馈设备上电后无任何反应，怀疑电源模块故障",
        repair_count=1,
        remark="客户急修",
    )
    db.add(rma1)
    db.flush()

    rma2 = RmaReturn(
        return_no=f"FC-{today.strftime('%y%m%d')}-002",
        sku_id=skus[0].id,
        sn="XG200-2509-0022",
        quantity=1,
        unit="台",
        spec=skus[0].spec,
        customer_name="广州云创数据有限公司",
        return_reason="4G信号频繁掉线",
        return_date=today - timedelta(days=10),
        status=RmaStatus.DIAGNOSED.value,
        diagnosis_result="REPAIRABLE",
        problem_description="4G模块间歇性断连，已更换4G通信模块",
        repair_plan="更换4G通信模块 M-4G，重新烧录固件",
        repair_time_hours=2.5,
        turnaround_days=5,
        repair_count=1,
        assigned_to=U[A["TEST_ENGINEER"]],
        assign_type="TEST",
        assign_reason="需要测试工程师诊断4G模块问题",
        remark="已修复，待测试验证",
    )
    db.add(rma2)
    db.flush()

    rma3 = RmaReturn(
        return_no=f"FC-{today.strftime('%y%m%d')}-003",
        sku_id=skus[1].id,
        sn="XG100-2509-0008",
        quantity=1,
        unit="台",
        spec=skus[1].spec,
        customer_name="杭州海康威视数字技术有限公司",
        return_reason="外壳变形，疑似运输损坏",
        return_date=today - timedelta(days=5),
        status=RmaStatus.REPAIRED.value,
        diagnosis_result="REPAIRABLE",
        problem_description="外壳右下角有明显磕碰痕迹，内部PCB完好",
        repair_plan="更换铝合金外壳，重新组装测试",
        inspection_report_no=f"INSP-{today.strftime('%y%m%d')}-010",
        new_sn=f"XG100-{today.strftime('%y%m')}-0100",
        reship_station="杭州滨江站",
        materials_used="铝合金外壳 XG-100 x1",
        repair_time_hours=1.0,
        turnaround_days=3,
        repair_count=1,
        repair_reason="外壳更换",
        assigned_to=U[A["PRODUCTION"]],
        assign_type="PRODUCTION",
        assign_reason="需要生产部门更换外壳",
        remark="已完成维修，准备发回",
    )
    db.add(rma3)
    db.flush()

    # 诊断报告
    db.add(RmaDiagnosis(
        return_id=rma2.id,
        diagnosis_no=f"DG-{today.strftime('%y%m%d')}-001",
        diagnosed_by=U[A["TEST_ENGINEER"]],
        diagnosis_date=today - timedelta(days=8),
        fault_description="4G通信模块与主板连接异常，天线接口松动导致信号不稳定",
        diagnosis_result="REPAIRABLE",
        repair_plan="重新焊接天线接口，更换4G通信模块，更新固件至V2.3.1",
        inspection_report_no=f"INSP-{today.strftime('%y%m%d')}-006",
        remark="4G模块批次问题，建议同批次产品预防性检查",
    ))

    db.add(RmaDiagnosis(
        return_id=rma3.id,
        diagnosis_no=f"DG-{today.strftime('%y%m%d')}-002",
        diagnosed_by=U[A["TEST_ENGINEER"]],
        diagnosis_date=today - timedelta(days=4),
        fault_description="外壳右下角碰撞变形，内部PCB无损伤，功能正常",
        diagnosis_result="REPAIRABLE",
        repair_plan="更换外壳，重新做防水测试",
        remark="建议加强运输包装",
    ))

    print(f"[OK] 返厂维修: 3 条, 诊断报告: 2 条")

    # ============================================================
    # 9.5 RMA 维修工单 (主线B)
    # ============================================================
    repairs = [
        RmaRepair(
            return_id=rma2.id,
            repair_no=f"WX-{today.strftime('%y%m%d')}-001",
            repair_by=U[A["PRODUCTION"]],
            old_sn=rma2.sn,
            new_sn=f"XG200-{today.strftime('%y%m')}-0100",
            repair_description="更换4G通信模块，重新焊接天线接口，烧录固件V2.3.1",
            materials_used="4G通信模块 M-4G x1, 天线连接线 x1",
            fault_code="RF-001",
            start_time=today - timedelta(days=9, hours=9),
            end_time=today - timedelta(days=9, hours=11, minutes=30),
            repair_date=today - timedelta(days=9),
            remark="4G模块批次问题，更换后信号正常",
        ),
        RmaRepair(
            return_id=rma3.id,
            repair_no=f"WX-{today.strftime('%y%m%d')}-002",
            repair_by=U[A["PRODUCTION"]],
            old_sn=rma3.sn,
            new_sn=rma3.new_sn,
            repair_description="更换铝合金外壳，重新组装，防水测试通过",
            materials_used="铝合金外壳 XG-100 x1, 密封胶圈 x1",
            fault_code="MECH-003",
            start_time=today - timedelta(days=4, hours=14),
            end_time=today - timedelta(days=4, hours=15),
            repair_date=today - timedelta(days=4),
            remark="外壳更换完成，功能正常",
        ),
    ]
    db.add_all(repairs)
    db.flush()
    print(f"[OK] RMA维修工单: {len(repairs)} 条")

    # ============================================================
    # 9.6 RMA 质量检验 (主线B)
    # ============================================================
    quality_checks = [
        RmaQualityCheck(
            return_id=rma2.id,
            checked_by=U[A["QUALITY"]],
            check_date=today - timedelta(days=8),
            check_result=QualityCheckResult.PASS.value,
            check_description="4G信号测试正常，连续运行24小时无掉线，各项指标合格",
            remark="质量检验通过，可入库",
        ),
        RmaQualityCheck(
            return_id=rma3.id,
            checked_by=U[A["QUALITY"]],
            check_date=today - timedelta(days=3),
            check_result=QualityCheckResult.PASS.value,
            check_description="外观检验合格，防水测试通过，功能测试正常",
            remark="质量检验通过，可入库或再出货",
        ),
    ]
    db.add_all(quality_checks)
    db.flush()

    # 新增一条维修失败的RMA用于展示报废流程
    rma4 = RmaReturn(
        return_no=f"FC-{today.strftime('%y%m%d')}-004",
        sku_id=skus[0].id,
        sn="XG200-2509-0040",
        quantity=1,
        unit="台",
        spec=skus[0].spec,
        customer_name="深圳腾讯计算机系统有限公司",
        return_reason="设备进水，主板腐蚀严重",
        return_date=today - timedelta(days=25),
        status=RmaStatus.DIAGNOSED.value,
        diagnosis_result=DiagnosisResult.SCRAP.value,
        problem_description="设备进水导致主板多处腐蚀，MCU芯片损坏，维修成本超过新机",
        repair_count=2,
        repair_reason="首次维修：电源模块更换；本次：进水主板腐蚀",
        assigned_to=U[A["TEST_ENGINEER"]],
        assign_type="TEST",
        assign_reason="评估是否可维修",
        remark="诊断结论：建议报废",
    )
    db.add(rma4)
    db.flush()

    db.add(RmaDiagnosis(
        return_id=rma4.id,
        diagnosis_no=f"DG-{today.strftime('%y%m%d')}-003",
        diagnosed_by=U[A["TEST_ENGINEER"]],
        diagnosis_date=today - timedelta(days=20),
        fault_description="进水导致主板腐蚀，MCU主控芯片STM32H7引脚氧化断裂，PCB多层板层间短路",
        diagnosis_result=DiagnosisResult.SCRAP.value,
        repair_plan="主板更换成本￥2100，超过新机成本的70%，建议报废处理",
        remark="报废审批中",
    ))

    print(f"[OK] RMA质量检验: {len(quality_checks)} 条 (含新增报废案例)")

    # ============================================================
    # 9.7 RMA 入库审核 (主线B)
    # ============================================================
    warehouse_ins = [
        RmaWarehouseIn(
            return_id=rma2.id,
            new_sn=repairs[0].new_sn,
            warehouse_by=U[A["WAREHOUSE"]],
            warehouse_date=today - timedelta(days=7),
            repair_count=1,
            repair_reason="4G通信模块更换",
            remark="维修后新SN已入库，可重新出货",
        ),
        RmaWarehouseIn(
            return_id=rma3.id,
            new_sn=repairs[1].new_sn,
            warehouse_by=U[A["WAREHOUSE"]],
            warehouse_date=today - timedelta(days=2),
            repair_count=1,
            repair_reason="外壳更换",
            remark="维修后新SN已入库",
        ),
    ]
    db.add_all(warehouse_ins)
    db.flush()
    print(f"[OK] RMA入库审核: {len(warehouse_ins)} 条")

    # ============================================================
    # 9.8 RMA 报废申请 (主线B)
    # ============================================================
    scrap = RmaScrap(
        return_id=rma4.id,
        scrap_no=f"BF-{today.strftime('%y%m%d')}-001",
        requested_by=U[A["TEST_ENGINEER"]],
        scrap_reason="设备进水导致主板严重腐蚀，MCU芯片损坏，PCB层间短路，维修成本￥2100超过新机成本70%，建议报废处理",
        status=ScrapStatus.PENDING.value,
        remark="待管理员审批",
    )
    db.add(scrap)
    db.flush()
    print(f"[OK] RMA报废申请: 1 条")

    # ============================================================
    # 9.9 RMA 再出货 (主线B)
    # ============================================================
    reship = RmaReship(
        return_id=rma3.id,
        reship_no=f"RH-{today.strftime('%y%m%d')}-001",
        new_sn=repairs[1].new_sn,
        software_version="V3.2.1",
        ship_date=today - timedelta(days=1),
        recipient="杭州海康威视数字技术有限公司",
        operator_id=U[A["WAREHOUSE"]],
        remark="维修后重新发回客户",
    )
    db.add(reship)
    db.flush()
    print(f"[OK] RMA再出货: 1 条")

    # ============================================================
    # 10. 出货管理 (主线C)
    # ============================================================
    shipment1 = Shipment(
        shipment_no=f"SH-{today.strftime('%y%m%d')}-001",
        sku_id=skus[0].id,
        sku_code=skus[0].sku_code,
        sku_name=skus[0].name,
        spec=skus[0].spec,
        unit="台",
        sn_list=[item.item_sn for item in sold_items],
        quantity=len(sold_items),
        ship_date=today - timedelta(days=1),
        address="北京市海淀区中关村软件园 智联科技大厦 8层",
        logistics_provider="顺丰速运",
        tracking_no=f"SF{random.randint(100000000000, 999999999999)}",
        u9_task_no=f"U9-TASK-{today.strftime('%y%m')}-001",
        tf_version="V3.2.1",
        host_version="V2.8.0",
        created_by=U[A["WAREHOUSE"]],
        remark="XG-200 首批出货至北京智联",
    )
    db.add(shipment1)

    shipment2 = Shipment(
        shipment_no=f"SH-{today.strftime('%y%m%d')}-002",
        sku_id=skus[2].id,
        sku_code=skus[2].sku_code,
        sku_name=skus[2].name,
        spec=skus[2].spec,
        unit="个",
        sn_list=[m4g_items[i].item_sn for i in range(5)],
        quantity=5,
        ship_date=today - timedelta(days=3),
        address="广州市天河区珠江新城 云创数据大厦 15层",
        logistics_provider="京东物流",
        tracking_no=f"JD{random.randint(100000000000, 999999999999)}",
        u9_task_no=f"U9-TASK-{today.strftime('%y%m')}-002",
        tf_version="V3.2.0",
        host_version="V2.8.0",
        created_by=U[A["WAREHOUSE"]],
        remark="4G通信模块备件出货",
    )
    db.add(shipment2)

    print(f"[OK] 出货单: 2 条")

    # 更多出货单 — 含不同状态
    shipment3 = Shipment(
        shipment_no=f"SH-{today.strftime('%y%m%d')}-003",
        sku_id=skus[1].id,
        sku_code=skus[1].sku_code,
        sku_name=skus[1].name,
        spec=skus[1].spec,
        unit="台",
        sn_list=[rnd_items[0].item_sn],
        quantity=1,
        ship_date=today - timedelta(days=7),
        address="深圳市南山区科技园 腾讯大厦 12层",
        logistics_provider="顺丰速运",
        tracking_no=f"SF{random.randint(100000000000, 999999999999)}",
        u9_task_no=f"U9-TASK-{today.strftime('%y%m')}-003",
        tf_version="V3.2.0",
        host_version="V2.7.5",
        created_by=U[A["WAREHOUSE"]],
        remark="XG-100 研发测试样机出货",
    )
    db.add(shipment3)

    shipment4 = Shipment(
        shipment_no=f"SH-{today.strftime('%y%m%d')}-004",
        sku_id=skus[0].id,
        sku_code=skus[0].sku_code,
        sku_name=skus[0].name,
        spec=skus[0].spec,
        unit="台",
        sn_list=[sample_items[0].item_sn, sample_items[1].item_sn],
        quantity=2,
        ship_date=today - timedelta(days=9),
        address="深圳市龙岗区坂田华为基地 H区",
        logistics_provider="德邦快递",
        tracking_no=f"DB{random.randint(100000000000, 999999999999)}",
        created_by=U[A["WAREHOUSE"]],
        remark="XG-200 样机送测华为",
    )
    db.add(shipment4)

    print(f"[OK] 出货单: 4 条")

    # ============================================================
    # 11. 库存日汇总
    # ============================================================
    daily_summaries = []
    for d in [30, 25, 20, 15, 10, 7, 5, 3, 2, 1]:
        summary_date = today - timedelta(days=d)
        opening = 100 - d * 3
        closing = opening + random.randint(-5, 8)
        inbound_qty = max(0, closing - opening + random.randint(0, 3))
        outbound_qty = max(0, opening - closing + random.randint(0, 3))
        daily_summaries.append(InventoryDailySummary(
            snapshot_date=summary_date,
            opening_in_stock_qty=opening,
            inbound_qty=inbound_qty,
            outbound_qty=outbound_qty,
            closing_in_stock_qty=opening + inbound_qty - outbound_qty,
            closing_asset_amount=Decimal(str((opening + inbound_qty - outbound_qty) * 1500)),
        ))
    db.add_all(daily_summaries)
    db.flush()
    print(f"[OK] 库存日汇总: {len(daily_summaries)} 条")

    # ============================================================
    # 12. 库存流水
    # ============================================================
    histories = []
    for item in xg200_items[:5]:
        histories.append(InventoryItemHistory(
            item_id=item.id,
            event_type="INBOUND",
            order_no=inbound.order_no,
            to_stock_status=StockStatus.IN_STOCK.value,
            to_operation_status=OperationStatus.COMPLETED.value,
            operator_id=U[A["WAREHOUSE"]],
            created_at=today - timedelta(days=7),
            remark="采购入库",
        ))
    for item in sold_items:
        histories.append(InventoryItemHistory(
            item_id=item.id,
            event_type="OUTBOUND",
            order_no=outbound.order_no,
            from_stock_status=StockStatus.IN_STOCK.value,
            to_stock_status=StockStatus.SOLD.value,
            to_operation_status=OperationStatus.COMPLETED.value,
            operator_id=U[A["WAREHOUSE"]],
            created_at=today - timedelta(days=1),
            remark="售出出库",
        ))
    for item in sample_items:
        histories.append(InventoryItemHistory(
            item_id=item.id,
            event_type="OUTBOUND",
            order_no=outbound_sample.order_no,
            from_stock_status=StockStatus.IN_STOCK.value,
            to_stock_status=StockStatus.SAMPLE.value,
            to_operation_status=OperationStatus.COMPLETED.value,
            operator_id=U[A["WAREHOUSE"]],
            created_at=today - timedelta(days=9),
            remark="样机出库",
        ))
    for item in rnd_items:
        histories.append(InventoryItemHistory(
            item_id=item.id,
            event_type="OUTBOUND",
            order_no=outbound_rnd.order_no,
            from_stock_status=StockStatus.IN_STOCK.value,
            to_stock_status=StockStatus.RND.value,
            to_operation_status=OperationStatus.COMPLETED.value,
            operator_id=U[A["PRODUCTION"]],
            created_at=today - timedelta(days=7),
            remark="研发出库",
        ))
    for item in borrow_items:
        histories.append(InventoryItemHistory(
            item_id=item.id,
            event_type="OUTBOUND",
            order_no=outbound_borrow.order_no,
            from_stock_status=StockStatus.IN_STOCK.value,
            to_stock_status=StockStatus.BORROWED.value,
            to_operation_status=OperationStatus.PICKING.value,
            operator_id=U[A["WAREHOUSE"]],
            created_at=today - timedelta(days=3),
            remark="借用出库",
        ))
    db.add_all(histories)
    print(f"[OK] 库存流水: {len(histories)} 条")

    db.commit()
    print("\n========================================")
    print("  演示数据填充完成！")
    print("  包含：客户/分类/商品/往来单位/库存/入库/出库/")
    print("        BOM/生产任务/来料/原材料库存/来料退货/")
    print("        返修/诊断/维修/质检/入库审核/报废/再出货/")
    print("        出货/库存流水/库存日汇总")
    print("========================================")


def main():
    db = SessionLocal()
    try:
        seed(db)
    except Exception as e:
        db.rollback()
        print(f"[ERROR] {e}", file=sys.stderr)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()