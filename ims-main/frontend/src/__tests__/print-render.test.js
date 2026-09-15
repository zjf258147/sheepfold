import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import IncomingReceiptPrint from '@/print/components/IncomingReceiptPrint.vue'
import ShipmentPrint from '@/print/components/ShipmentPrint.vue'
import IncomingInspectionPrint from '@/print/components/IncomingInspectionPrint.vue'
import IncomingReturnPrint from '@/print/components/IncomingReturnPrint.vue'
import RmaRepairPrint from '@/print/components/RmaRepairPrint.vue'
import BomPrint from '@/print/components/BomPrint.vue'
import PrintPreview from '@/print/components/PrintPreview.vue'

const makeReceiptData = () => ({
  data: {
    batch_no: 'BATCH-2026-001',
    supplier_name: '测试供应商',
    receipt_date: '2026-09-01',
    receipt_no: 'RC-20260901-001',
    sku_code: 'SKU-001',
    sku_name: '测试物料',
    spec: '100mm×200mm',
    quantity: 100,
    unit: '个',
    remark: '测试备注',
  },
})

const makeShipmentData = () => ({
  data: {
    shipment_no: 'JOUT-20260901-001',
    ship_date: '2026-09-01',
    customer_name: '测试客户',
    address: '测试地址',
    logistics_provider: '顺丰快递',
    tracking_no: 'SF1234567890',
    total_amount: 12345.67,
    tf_version: 'v2.1.0',
    host_version: 'v3.0.0',
  },
  items: [
    { row_no: 1, sku_code: 'SKU-001', sku_name: '测试物料A', spec: '100mm', quantity: 10, unit: '个', remark: '' },
    { row_no: 2, sku_code: 'SKU-002', sku_name: '测试物料B', spec: '200mm', quantity: 20, unit: '个', remark: '备注' },
  ],
})

const makeInspectionData = () => ({
  data: {
    inspection_no: 'JC-20260901-001',
    inspection_date: '2026-09-01',
    supplier_name: '测试供应商',
    receipt_no: 'RC-20260901-001',
    batch_no: 'BATCH-2026-001',
    sku_code: 'SKU-001',
    sku_name: '测试物料',
    spec: '100mm×200mm',
    quantity: 100,
    unit: '个',
    sample_qty: 20,
    defect_qty: 0,
    result: 'ACCEPTED',
    result_cn: '合格',
    inspector_name: '质检员',
    defect_description: null,
  },
})

const makeReturnData = () => ({
  data: {
    return_no: 'JIN-20260901-001',
    return_date: '2026-09-01',
    supplier_name: '测试供应商',
    receipt_no: 'RC-20260901-001',
    batch_no: 'BATCH-2026-001',
    sku_code: 'SKU-001',
    sku_name: '测试物料',
    spec: '100mm×200mm',
    quantity: 100,
    return_qty: 10,
    unit: '个',
    return_reason: '外观不良',
    remark: '',
  },
})

const makeRepairData = () => ({
  data: {
    repair_no: 'WX-20260901-001',
    repair_date: '2026-09-01',
    return_no: 'FH-20260901-001',
    customer_name: '测试客户',
    sku_code: 'SKU-001',
    sku_name: '测试物料',
    spec: '100mm×200mm',
    old_sn: 'SN-OLD-001',
    new_sn: 'SN-NEW-001',
    problem_description: '无法开机',
    diagnosis_result: '电源模块损坏',
    repair_description: '更换电源模块',
    materials_used: '电源模块 ×1',
    repairer_name: '维修员',
  },
})

const makeBomData = () => ({
  data: {
    bom_no: 'BOM-20260901-001',
    bom_name: '测试BOM',
    version: 'v1.0',
    product_sku_code: 'PROD-001',
    product_sku_name: '成品物料',
    plan_quantity: 100,
    status: '已发布',
    created_by: '管理员',
  },
  items: [
    { row_no: 1, level: 0, material_sku_code: 'MAT-001', material_sku_name: '子物料A', spec: '100mm', quantity_per_unit: 2, unit: '个', wastage_rate: 1.5, remark: '' },
    { row_no: 2, level: 1, material_sku_code: 'MAT-002', material_sku_name: '子物料B', spec: '200mm', quantity_per_unit: 1, unit: '个', wastage_rate: 0, remark: '备注' },
  ],
})

describe('IncomingReceiptPrint 采购收货单渲染', () => {
  it('正确渲染公司名称和文档标题', () => {
    const wrapper = mount(IncomingReceiptPrint, { props: { data: makeReceiptData() } })
    expect(wrapper.text()).toContain('西安敦临计量检测有限公司')
    expect(wrapper.text()).toContain('采 购 收 货 单')
  })

  it('正确渲染批次号和到货日期', () => {
    const wrapper = mount(IncomingReceiptPrint, { props: { data: makeReceiptData() } })
    expect(wrapper.text()).toContain('BATCH-2026-001')
    expect(wrapper.text()).toContain('2026-09-01')
  })

  it('正确渲染物料信息表格', () => {
    const wrapper = mount(IncomingReceiptPrint, { props: { data: makeReceiptData() } })
    expect(wrapper.text()).toContain('SKU-001')
    expect(wrapper.text()).toContain('测试物料')
    expect(wrapper.text()).toContain('100mm×200mm')
  })

  it('空数据时不崩溃', () => {
    const wrapper = mount(IncomingReceiptPrint, { props: { data: null } })
    expect(wrapper.exists()).toBe(true)
  })

  it('支持 receipts 数组模式渲染', () => {
    const wrapper = mount(IncomingReceiptPrint, {
      props: {
        receipts: [makeReceiptData()],
      },
    })
    expect(wrapper.text()).toContain('采 购 收 货 单')
    expect(wrapper.text()).toContain('BATCH-2026-001')
  })

  it('多页数据正确分页', () => {
    const items = []
    for (let i = 0; i < 25; i++) {
      items.push({
        batch_no: 'BATCH-2026-001',
        supplier_name: '测试供应商',
        receipt_date: '2026-09-01',
        receipt_no: `RC-20260901-${String(i + 1).padStart(3, '0')}`,
        sku_code: `SKU-${String(i + 1).padStart(3, '0')}`,
        sku_name: `物料${i + 1}`,
        spec: '100mm',
        quantity: 10,
        unit: '个',
        remark: '',
      })
    }
    const wrapper = mount(IncomingReceiptPrint, {
      props: { receipts: items.map(r => ({ data: r })) },
    })
    expect(wrapper.text()).toContain('第 1 页')
    expect(wrapper.text()).toContain('第 2 页')
  })
})

describe('ShipmentPrint 出货单渲染', () => {
  it('正确渲染公司名称和出货单标题', () => {
    const wrapper = mount(ShipmentPrint, { props: { data: makeShipmentData() } })
    expect(wrapper.text()).toContain('西安敦临计量检测有限公司')
    expect(wrapper.text()).toContain('出 货 单')
  })

  it('正确渲染出货单号和发货日期', () => {
    const wrapper = mount(ShipmentPrint, { props: { data: makeShipmentData() } })
    expect(wrapper.text()).toContain('JOUT-20260901-001')
    expect(wrapper.text()).toContain('2026-09-01')
  })

  it('正确渲染物流信息', () => {
    const wrapper = mount(ShipmentPrint, { props: { data: makeShipmentData() } })
    expect(wrapper.text()).toContain('顺丰快递')
    expect(wrapper.text()).toContain('SF1234567890')
  })

  it('正确渲染物料表格', () => {
    const wrapper = mount(ShipmentPrint, { props: { data: makeShipmentData() } })
    expect(wrapper.text()).toContain('SKU-001')
    expect(wrapper.text()).toContain('测试物料A')
    expect(wrapper.text()).toContain('SKU-002')
  })

  it('正确渲染金额合计（大写和小写）', () => {
    const wrapper = mount(ShipmentPrint, { props: { data: makeShipmentData() } })
    expect(wrapper.text()).toContain('合计金额')
    expect(wrapper.text()).toContain('壹万贰仟叁佰肆拾伍元陆角柒分')
  })

  it('空数据时不崩溃', () => {
    const wrapper = mount(ShipmentPrint, { props: { data: null } })
    expect(wrapper.exists()).toBe(true)
  })

  it('金额为0时正确显示', () => {
    const data = makeShipmentData()
    data.data.total_amount = 0
    const wrapper = mount(ShipmentPrint, { props: { data } })
    expect(wrapper.text()).toContain('零元整')
    expect(wrapper.text()).toContain('合计金额')
  })

  it('shipments 数组模式渲染', () => {
    const wrapper = mount(ShipmentPrint, {
      props: {
        shipments: [makeShipmentData()],
      },
    })
    expect(wrapper.text()).toContain('出 货 单')
    expect(wrapper.text()).toContain('JOUT-20260901-001')
  })
})

describe('IncomingInspectionPrint 来料检验报告渲染', () => {
  it('正确渲染公司名称和报告标题', () => {
    const wrapper = mount(IncomingInspectionPrint, { props: { data: makeInspectionData() } })
    expect(wrapper.text()).toContain('西安敦临计量检测有限公司')
    expect(wrapper.text()).toContain('来料检验报告')
  })

  it('正确渲染报告编号和检验日期', () => {
    const wrapper = mount(IncomingInspectionPrint, { props: { data: makeInspectionData() } })
    expect(wrapper.text()).toContain('JC-20260901-001')
    expect(wrapper.text()).toContain('2026-09-01')
  })

  it('正确渲染物料信息', () => {
    const wrapper = mount(IncomingInspectionPrint, { props: { data: makeInspectionData() } })
    expect(wrapper.text()).toContain('SKU-001')
    expect(wrapper.text()).toContain('测试物料')
    expect(wrapper.text()).toContain('100mm×200mm')
  })

  it('ACCEPTED 结果正确显示为合格', () => {
    const wrapper = mount(IncomingInspectionPrint, { props: { data: makeInspectionData() } })
    expect(wrapper.text()).toContain('合格')
  })

  it('REJECTED 结果正确显示为不合格', () => {
    const data = makeInspectionData()
    data.data.result = 'REJECTED'
    data.data.result_cn = '不合格'
    const wrapper = mount(IncomingInspectionPrint, { props: { data } })
    expect(wrapper.text()).toContain('不合格')
  })

  it('有缺陷描述时渲染缺陷描述区域', () => {
    const data = makeInspectionData()
    data.data.defect_description = '外观划痕'
    const wrapper = mount(IncomingInspectionPrint, { props: { data } })
    expect(wrapper.text()).toContain('外观划痕')
  })

  it('空数据时不崩溃', () => {
    const wrapper = mount(IncomingInspectionPrint, { props: { data: null } })
    expect(wrapper.exists()).toBe(true)
  })
})

describe('IncomingReturnPrint 退货单渲染', () => {
  it('正确渲染公司名称和退货单标题', () => {
    const wrapper = mount(IncomingReturnPrint, { props: { data: makeReturnData() } })
    expect(wrapper.text()).toContain('西安敦临计量检测有限公司')
    expect(wrapper.text()).toContain('退 货 单')
  })

  it('正确渲染退货单号和退货日期', () => {
    const wrapper = mount(IncomingReturnPrint, { props: { data: makeReturnData() } })
    expect(wrapper.text()).toContain('JIN-20260901-001')
    expect(wrapper.text()).toContain('2026-09-01')
  })

  it('正确渲染退货数量和退货原因', () => {
    const wrapper = mount(IncomingReturnPrint, { props: { data: makeReturnData() } })
    expect(wrapper.text()).toContain('10')
    expect(wrapper.text()).toContain('外观不良')
  })

  it('空数据时不崩溃', () => {
    const wrapper = mount(IncomingReturnPrint, { props: { data: null } })
    expect(wrapper.exists()).toBe(true)
  })
})

describe('RmaRepairPrint 维修工单渲染', () => {
  it('正确渲染公司名称和维修工单标题', () => {
    const wrapper = mount(RmaRepairPrint, { props: { data: makeRepairData() } })
    expect(wrapper.text()).toContain('西安敦临计量检测有限公司')
    expect(wrapper.text()).toContain('维修工单')
  })

  it('正确渲染工单编号和完工日期', () => {
    const wrapper = mount(RmaRepairPrint, { props: { data: makeRepairData() } })
    expect(wrapper.text()).toContain('WX-20260901-001')
    expect(wrapper.text()).toContain('2026-09-01')
  })

  it('正确渲染SN信息（旧SN和新SN）', () => {
    const wrapper = mount(RmaRepairPrint, { props: { data: makeRepairData() } })
    expect(wrapper.text()).toContain('SN-OLD-001')
    expect(wrapper.text()).toContain('SN-NEW-001')
  })

  it('正确渲染故障现象和诊断结论', () => {
    const wrapper = mount(RmaRepairPrint, { props: { data: makeRepairData() } })
    expect(wrapper.text()).toContain('无法开机')
    expect(wrapper.text()).toContain('电源模块损坏')
  })

  it('正确渲染维修方案和更换零件', () => {
    const wrapper = mount(RmaRepairPrint, { props: { data: makeRepairData() } })
    expect(wrapper.text()).toContain('更换电源模块')
    expect(wrapper.text()).toContain('电源模块 ×1')
  })

  it('无新SN时不显示新SN区域', () => {
    const data = makeRepairData()
    data.data.new_sn = null
    const wrapper = mount(RmaRepairPrint, { props: { data } })
    expect(wrapper.text()).toContain('SN-OLD-001')
    expect(wrapper.text()).not.toContain('新SN码')
  })

  it('空数据时不崩溃', () => {
    const wrapper = mount(RmaRepairPrint, { props: { data: null } })
    expect(wrapper.exists()).toBe(true)
  })
})

describe('BomPrint 物料清单渲染', () => {
  it('正确渲染公司名称和BOM标题', () => {
    const wrapper = mount(BomPrint, { props: { data: makeBomData() } })
    expect(wrapper.text()).toContain('西安敦临计量检测有限公司')
    expect(wrapper.text()).toContain('物料清单')
  })

  it('正确渲染BOM编号和版本', () => {
    const wrapper = mount(BomPrint, { props: { data: makeBomData() } })
    expect(wrapper.text()).toContain('BOM-20260901-001')
    expect(wrapper.text()).toContain('v1.0')
  })

  it('正确渲染BOM层级物料表格', () => {
    const wrapper = mount(BomPrint, { props: { data: makeBomData() } })
    expect(wrapper.text()).toContain('MAT-001')
    expect(wrapper.text()).toContain('子物料A')
    expect(wrapper.text()).toContain('MAT-002')
    expect(wrapper.text()).toContain('子物料B')
  })

  it('空数据时不崩溃', () => {
    const wrapper = mount(BomPrint, { props: { data: null } })
    expect(wrapper.exists()).toBe(true)
  })

  it('多页数据正确显示分页', () => {
    const items = []
    for (let i = 1; i <= 25; i++) {
      items.push({
        row_no: i,
        level: 0,
        material_sku_code: `MAT-${String(i).padStart(3, '0')}`,
        material_sku_name: `物料${i}`,
        spec: '100mm',
        quantity_per_unit: 1,
        unit: '个',
        wastage_rate: 0,
        remark: '',
      })
    }
    const wrapper = mount(BomPrint, {
      props: { data: { data: makeBomData().data, items } },
    })
    expect(wrapper.text()).toContain('第 1 页')
    expect(wrapper.text()).toContain('第 2 页')
  })
})

describe('PrintPreview 打印预览容器', () => {
  it('visible=false 时不渲染 dialog', () => {
    const wrapper = mount(PrintPreview, {
      props: { visible: false, title: '测试打印' },
      slots: { default: '<div class="test-slot">测试内容</div>' },
    })
    const dialog = wrapper.findComponent({ name: 'ElDialog' })
    expect(dialog.exists()).toBe(true)
  })

  it('visible=true 时渲染内容', async () => {
    const wrapper = mount(PrintPreview, {
      props: { visible: true, title: '测试打印' },
      slots: { default: '<div class="test-slot">测试内容</div>' },
    })
    await nextTick()
    expect(wrapper.findComponent({ name: 'ElDialog' }).exists()).toBe(true)
  })

  it('渲染打印和导出PDF按钮', async () => {
    const wrapper = mount(PrintPreview, {
      props: { visible: true, title: '测试' },
      slots: { default: '<div>内容</div>' },
    })
    await nextTick()
    const dialog = wrapper.findComponent({ name: 'ElDialog' })
    expect(dialog.exists()).toBe(true)
    expect(dialog.props('title')).toBe('测试')
  })

  it('update:visible 事件正确处理', async () => {
    const wrapper = mount(PrintPreview, {
      props: { visible: true, title: '测试' },
      slots: { default: '<div>内容</div>' },
    })
    const dialog = wrapper.findComponent({ name: 'ElDialog' })
    expect(dialog.exists()).toBe(true)
  })
})