<script setup>
import { computed } from 'vue'
import { COMPANY_INFO, formatDate, amountToChinese, formatAmount, paginateItems, PAGE_SIZE } from '../print-utils'

const props = defineProps({
  data: { type: Object, default: null },
  shipments: { type: Array, default: () => [] },
})

const allDocs = computed(() => {
  if (props.shipments && props.shipments.length > 0) {
    return props.shipments.map(s => s.data || s)
  }
  if (props.data) {
    return [props.data.data || props.data]
  }
  return []
})

const allItems = computed(() => {
  if (props.shipments && props.shipments.length > 0) {
    return props.shipments.map(s => ({
      doc: s.data || s,
      items: s.items || [],
    }))
  }
  if (props.data) {
    return [{
      doc: props.data.data || props.data,
      items: props.data.items || [],
    }]
  }
  return []
})

const allPages = computed(() => {
  const result = []
  allItems.value.forEach((shipment, shipmentIndex) => {
    const rawItems = shipment.items || []
    const pages = paginateItems(rawItems, PAGE_SIZE)
    pages.forEach((pageItems, pageIndex) => {
      result.push({
        shipmentIndex,
        pageIndex,
        doc: shipment.doc,
        pageItems,
        totalPagesInShipment: pages.length,
        isLastPageOfShipment: pageIndex === pages.length - 1,
      })
    })
  })
  return result
})

const globalPageIndex = (entry) => {
  return allPages.value.indexOf(entry) + 1
}

const totalGlobalPages = computed(() => allPages.value.length)

const totalQuantity = (doc, items) => {
  return items.reduce((sum, item) => sum + (item.quantity || 0), 0)
}
</script>

<template>
  <div class="print-document shipment-print">
    <div v-for="(entry, entryIdx) in allPages" :key="`${entry.shipmentIndex}-${entry.pageIndex}`" class="print-page">
      <div class="header-accent"></div>
      <div class="brand-area">
        <div class="company-full">{{ COMPANY_INFO.fullName }}</div>
        <div class="doc-title">出 货 单</div>
        <div class="doc-meta-row">
          <span class="doc-meta-item">出货单号：<strong>{{ entry.doc.shipment_no }}</strong></span>
          <span class="doc-meta-item">发货日期：<strong>{{ formatDate(entry.doc.ship_date) }}</strong></span>
        </div>
      </div>

      <div class="info-section">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">收货场站</span>
            <span class="info-value">{{ entry.doc.customer_name || entry.doc.address }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">收货地址</span>
            <span class="info-value">{{ entry.doc.address }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">物流供应商</span>
            <span class="info-value">{{ entry.doc.logistics_provider }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">快递单号</span>
            <span class="info-value">{{ entry.doc.tracking_no }}</span>
          </div>
          <div class="info-item" v-if="entry.doc.u9_task_no">
            <span class="info-label">U9任务单号</span>
            <span class="info-value">{{ entry.doc.u9_task_no }}</span>
          </div>
        </div>
      </div>

      <table class="print-table">
        <thead>
          <tr>
            <th class="col-seq">序号</th>
            <th class="col-code">物料编码</th>
            <th class="col-name">物料名称</th>
            <th class="col-spec">规格型号</th>
            <th class="col-qty">数量</th>
            <th class="col-unit">单位</th>
            <th class="col-tf">TF卡版本</th>
            <th class="col-host">上位机版本</th>
            <th class="col-remark">备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in entry.pageItems" :key="item.row_no">
            <td class="col-seq">{{ item.row_no }}</td>
            <td class="col-code">{{ item.sku_code }}</td>
            <td class="col-name">{{ item.sku_name }}</td>
            <td class="col-spec">{{ item.spec || '-' }}</td>
            <td class="col-qty">{{ item.quantity }}</td>
            <td class="col-unit">{{ item.unit }}</td>
            <td class="col-tf">{{ entry.pageIndex === 0 ? (entry.doc.tf_version || '-') : '-' }}</td>
            <td class="col-host">{{ entry.pageIndex === 0 ? (entry.doc.host_version || '-') : '-' }}</td>
            <td class="col-remark">{{ item.remark || '' }}</td>
          </tr>
        </tbody>
      </table>

      <div v-if="entry.isLastPageOfShipment" class="summary-area">
        <div class="summary-row">
          <div class="amount-arabic">
            <span class="summary-label">合计金额</span>
            <span class="summary-value">¥ {{ formatAmount(entry.doc.total_amount || 0) }}</span>
          </div>
          <div class="amount-chinese">
            <span class="summary-label">大写</span>
            <span class="summary-value chinese-amount">{{ amountToChinese(entry.doc.total_amount || 0) }}</span>
          </div>
        </div>
        <div class="summary-row">
          <span class="summary-label">合计数量</span>
          <span class="summary-value">{{ totalQuantity(entry.doc, allItems[entry.shipmentIndex]?.items || []) }} {{ allItems[entry.shipmentIndex]?.items?.[0]?.unit || '个' }}</span>
        </div>
      </div>

      <div v-if="entry.isLastPageOfShipment" class="signature-area">
        <div class="signature-item">
          <div class="signature-label">客户签收</div>
          <div class="signature-line-large"></div>
          <div class="signature-date">日期：___年___月___日</div>
        </div>
        <div class="signature-item">
          <div class="signature-label">经办人</div>
          <div class="signature-line"></div>
          <div class="signature-date">日期：___年___月___日</div>
        </div>
      </div>

      <div class="page-footer">
        <span>第 {{ globalPageIndex(entry) }} 页 / 共 {{ totalGlobalPages }} 页</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.shipment-print {
  font-family: 'Microsoft YaHei', 'PingFang SC', SimHei, sans-serif;
  font-size: 13px;
  color: #1e293b;
  background: #fff;
}

.print-page {
  padding: 12mm 14mm;
  min-height: 297mm;
  width: 210mm;
  margin: 0 auto 0;
  box-sizing: border-box;
  page-break-after: always;
  position: relative;
}

.print-page:last-child {
  page-break-after: auto;
}

.header-accent {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #3a6ca0 0%, #5a9ad4 50%, #3a6ca0 100%);
}

.brand-area {
  text-align: center;
  padding: 18px 0 14px 0;
  margin-bottom: 14px;
  border-bottom: 1px solid #1a3c6e;
  position: relative;
}

.brand-area::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 1px;
  background: #1a3c6e;
}

.company-full {
  font-size: 22px;
  font-weight: 700;
  color: #1a3c6e;
  letter-spacing: 3px;
  margin-bottom: 12px;
}

.doc-title {
  font-size: 26px;
  font-weight: 700;
  color: #1a3c6e;
  letter-spacing: 10px;
  margin-bottom: 10px;
}

.doc-meta-row {
  display: flex;
  justify-content: center;
  gap: 60px;
  font-size: 13px;
  color: #475569;
}

.doc-meta-item strong {
  color: #1e293b;
  font-weight: 600;
}

.info-section {
  margin-bottom: 12px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px 40px;
  margin-bottom: 8px;
}

.info-item {
  display: flex;
  align-items: center;
}

.info-label {
  font-weight: 600;
  color: #475569;
  white-space: nowrap;
  min-width: 80px;
  font-size: 13px;
}

.info-label::after {
  content: '：';
}

.info-value {
  flex: 1;
  border-bottom: 1px solid #cbd5e1;
  padding: 3px 8px;
  font-size: 13px;
  color: #1e293b;
}

.print-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 14px;
  font-size: 12px;
}

.print-table thead th {
  background: #1a3c6e;
  color: #fff;
  padding: 10px 4px;
  font-size: 11px;
  font-weight: 600;
  border: 1px solid #1a3c6e;
  letter-spacing: 1px;
}

.print-table tbody td {
  border: 1px solid #cbd5e1;
  padding: 8px 4px;
  text-align: center;
  color: #1e293b;
  font-size: 12px;
}

.print-table tbody tr:nth-child(even) td {
  background: #f8fafc;
}

.col-seq { width: 4%; }
.col-code { width: 11%; }
.col-name { width: 13%; }
.col-spec { width: 11%; }
.col-qty { width: 6%; }
.col-unit { width: 5%; }
.col-tf { width: 9%; }
.col-host { width: 10%; }
.col-remark { width: 31%; }

.summary-area {
  margin-top: 10px;
  margin-bottom: 14px;
  padding: 10px 14px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  font-size: 14px;
}

.summary-row:last-child {
  margin-bottom: 0;
}

.amount-arabic {
  flex: 1;
}

.amount-chinese {
  flex: 1;
  text-align: right;
}

.summary-label {
  font-weight: 600;
  color: #475569;
  font-size: 13px;
}

.summary-label::after {
  content: '：';
}

.summary-value {
  font-weight: 700;
  font-size: 15px;
  color: #1e293b;
}

.chinese-amount {
  font-size: 14px;
}

.signature-area {
  margin-top: 30px;
  display: flex;
  gap: 80px;
}

.signature-item {
  flex: 1;
}

.signature-label {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
}

.signature-line {
  border-bottom: 1px solid #94a3b8;
  height: 36px;
}

.signature-line-large {
  border-bottom: 1px solid #94a3b8;
  height: 52px;
}

.signature-date {
  font-size: 13px;
  margin-top: 8px;
  color: #94a3b8;
}

.page-footer {
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
  margin-top: 20px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

@media print {
  .shipment-print {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .print-page {
    padding: 10mm 12mm;
    margin: 0;
    width: 100%;
    min-height: auto;
    background: #fff !important;
  }

  .header-accent {
    background: linear-gradient(90deg, #5a7fa8 0%, #7ab0d8 50%, #5a7fa8 100%) !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .brand-area {
    border-bottom-color: #5a7fa8 !important;
  }

  .brand-area::after {
    background: #5a7fa8 !important;
  }

  .company-full,
  .doc-title {
    color: #3a6ca0 !important;
  }

  .print-table thead th {
    background: #5a7fa8 !important;
    color: #fff !important;
    border-color: #5a7fa8 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .print-table tbody tr:nth-child(even) td {
    background: #f5f7fa !important;
  }
}
</style>

<style>
@media print {
  @page {
    size: A4;
    margin: 0;
  }
}
</style>