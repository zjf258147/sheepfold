<script setup>
import { computed } from 'vue'
import { COMPANY_INFO, formatDate } from '../print-utils'

const ITEMS_PER_PAGE = 15

const props = defineProps({
  data: { type: Object, default: null },
  receipts: { type: Array, default: () => [] },
})

const allDocs = computed(() => {
  if (props.receipts && props.receipts.length > 0) {
    return props.receipts.map(r => r.data || r)
  }
  if (props.data) {
    return [props.data.data || props.data]
  }
  return []
})

const groups = computed(() => {
  const map = new Map()
  allDocs.value.forEach(doc => {
    const key = doc.batch_no || '__no_batch__'
    if (!map.has(key)) {
      map.set(key, {
        batch_no: doc.batch_no,
        supplier_name: doc.supplier_name,
        receipt_date: doc.receipt_date,
        receipt_nos: [],
        items: [],
      })
    }
    const group = map.get(key)
    group.receipt_nos.push(doc.receipt_no)
    group.items.push(doc)
  })
  return Array.from(map.values())
})

const allPages = computed(() => {
  const result = []
  groups.value.forEach((group, groupIdx) => {
    const totalGroupPages = Math.ceil(group.items.length / ITEMS_PER_PAGE)
    for (let i = 0; i < totalGroupPages; i++) {
      result.push({
        groupIdx,
        pageInGroup: i,
        totalGroupPages,
        group,
        pageItems: group.items.slice(i * ITEMS_PER_PAGE, (i + 1) * ITEMS_PER_PAGE),
      })
    }
  })
  return result
})

const totalGlobalPages = computed(() => allPages.value.length)

const globalPageNo = (entry) => allPages.value.indexOf(entry) + 1
</script>

<template>
  <div class="print-document incoming-receipt-print">
    <div v-for="(entry, _entryIdx) in allPages" :key="`${entry.groupIdx}-${entry.pageInGroup}`" class="print-page">
      <div class="header-accent"></div>
      <div class="brand-area">
        <div class="company-full">{{ COMPANY_INFO.fullName }}</div>
        <div class="doc-title">采 购 收 货 单</div>
        <div class="doc-meta-row">
          <span class="doc-meta-item">批次号：<strong>{{ entry.group.batch_no }}</strong></span>
          <span class="doc-meta-item">到货日期：<strong>{{ formatDate(entry.group.receipt_date) }}</strong></span>
        </div>
      </div>

      <div class="info-section">
        <div class="info-row">
          <div class="info-item">
            <span class="info-label">供应商</span>
            <span class="info-value">{{ entry.group.supplier_name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">到货单号</span>
            <span class="info-value">{{ entry.group.receipt_nos.join('、') }}</span>
          </div>
        </div>
        <div class="info-row">
          <div class="info-item">
            <span class="info-label">外包装检查</span>
            <span class="info-value check-value">
              <span class="check-option">□ 完好</span>
              <span class="check-option">□ 破损</span>
            </span>
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
            <th class="col-remark">备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in entry.pageItems" :key="item.receipt_no || idx">
            <td class="col-seq">{{ entry.pageInGroup * ITEMS_PER_PAGE + idx + 1 }}</td>
            <td class="col-code">{{ item.sku_code }}</td>
            <td class="col-name">{{ item.sku_name }}</td>
            <td class="col-spec">{{ item.spec || '-' }}</td>
            <td class="col-qty">{{ item.quantity }}</td>
            <td class="col-unit">{{ item.unit }}</td>
            <td class="col-remark">{{ item.remark || '' }}</td>
          </tr>
        </tbody>
      </table>

      <div class="signature-area">
        <div class="signature-item">
          <div class="signature-label">收货人</div>
          <div class="signature-line"></div>
          <div class="signature-date">日期：___年___月___日</div>
        </div>
        <div class="signature-item">
          <div class="signature-label">供应商代表</div>
          <div class="signature-line"></div>
          <div class="signature-date">日期：___年___月___日</div>
        </div>
      </div>

      <div class="page-footer">
        <span>第 {{ globalPageNo(entry) }} 页 / 共 {{ totalGlobalPages }} 页</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.incoming-receipt-print {
  font-family: 'Microsoft YaHei', 'PingFang SC', SimHei, sans-serif;
  font-size: 13px;
  color: #1e293b;
  background: #fff;
}

.print-page {
  padding: 12mm 14mm;
  min-height: 297mm;
  width: 210mm;
  margin: 0 auto;
  box-sizing: border-box;
  position: relative;
  page-break-after: always;
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

.info-row {
  display: flex;
  gap: 50px;
  margin-bottom: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  flex: 1;
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

.check-value {
  display: flex;
  gap: 30px;
  border-bottom: none;
}

.check-option {
  border: 1px solid #94a3b8;
  padding: 2px 12px;
  border-radius: 2px;
  font-size: 13px;
  color: #64748b;
}

.print-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  font-size: 12px;
}

.print-table thead th {
  background: #1a3c6e;
  color: #fff;
  padding: 10px 6px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid #1a3c6e;
  letter-spacing: 1px;
}

.print-table tbody td {
  border: 1px solid #cbd5e1;
  padding: 9px 6px;
  text-align: center;
  color: #1e293b;
  font-size: 13px;
}

.print-table tbody tr:nth-child(even) td {
  background: #f8fafc;
}

.col-seq { width: 5%; }
.col-code { width: 14%; }
.col-name { width: 18%; }
.col-spec { width: 16%; }
.col-qty { width: 9%; }
.col-unit { width: 7%; }
.col-remark { width: 31%; }

.signature-area {
  margin-top: 40px;
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

.signature-date {
  font-size: 13px;
  margin-top: 8px;
  color: #94a3b8;
}

.page-footer {
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
  margin-top: 30px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

@media print {
  .incoming-receipt-print {
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