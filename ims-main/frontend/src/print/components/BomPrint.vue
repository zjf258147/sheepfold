<script setup>
import { computed } from 'vue'
import { COMPANY_INFO, paginateItems, PAGE_SIZE } from '../print-utils'

const props = defineProps({
  data: { type: Object, default: null },
  boms: { type: Array, default: () => [] },
})

const allBoms = computed(() => {
  if (props.boms && props.boms.length > 0) {
    return props.boms.map(r => r.data || r)
  }
  if (props.data) {
    return [props.data.data || props.data]
  }
  return []
})

const allPages = computed(() => {
  const result = []
  allBoms.value.forEach((bom, bomIdx) => {
    const rawItems = bom.items || []
    const pageItems = paginateItems(rawItems, PAGE_SIZE)
    pageItems.forEach((page, pageIdx) => {
      result.push({
        bom,
        bomIdx,
        pageIdx,
        pageItems: page,
        isFirstBomPage: pageIdx === 0,
      })
    })
  })
  return result
})

function indentStyle(level) {
  const px = (level || 0) * 20
  return px > 0 ? { paddingLeft: px + 'px' } : {}
}
</script>

<template>
  <div class="print-document bom-print">
    <div v-for="(page, globalIdx) in allPages" :key="globalIdx" class="print-page" :class="{ 'bom-separator': page.bomIdx > 0 && page.pageIdx === 0 }">
      <div class="header-accent"></div>
      <div class="brand-area">
        <div class="company-full">{{ COMPANY_INFO.fullName }}</div>
        <div class="company-short">{{ COMPANY_INFO.shortName }}</div>
        <div class="doc-title">物料清单</div>
        <div class="doc-subtitle">Bill of Materials</div>
        <div class="doc-meta-row">
          <span class="doc-meta-item">BOM编号：<strong>{{ page.bom.bom_no }}</strong></span>
          <span class="doc-meta-item version-tag">版本：{{ page.bom.version }}</span>
        </div>
      </div>

      <div class="info-section">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">BOM名称</span>
            <span class="info-value">{{ page.bom.bom_name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">成品物料</span>
            <span class="info-value">{{ page.bom.product_sku_code }} / {{ page.bom.product_sku_name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">计划数量</span>
            <span class="info-value">{{ page.bom.plan_quantity }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">状态</span>
            <span class="info-value">{{ page.bom.status }}</span>
          </div>
        </div>
      </div>

      <table class="print-table">
        <thead>
          <tr>
            <th class="col-seq">序号</th>
            <th class="col-level">层级</th>
            <th class="col-code">物料编码</th>
            <th class="col-name">物料名称</th>
            <th class="col-spec">规格型号</th>
            <th class="col-qty">单台用量</th>
            <th class="col-unit">单位</th>
            <th class="col-waste">损耗率</th>
            <th class="col-remark">备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in page.pageItems" :key="item.row_no">
            <td class="col-seq">{{ item.row_no }}</td>
            <td class="col-level">{{ item.level }}</td>
            <td class="col-code" :style="indentStyle(item.level)">{{ item.material_sku_code }}</td>
            <td class="col-name" :style="indentStyle(item.level)">{{ item.material_sku_name }}</td>
            <td class="col-spec">{{ item.spec || '-' }}</td>
            <td class="col-qty">{{ item.quantity_per_unit }}</td>
            <td class="col-unit">{{ item.unit }}</td>
            <td class="col-waste">{{ item.wastage_rate != null ? item.wastage_rate + '%' : '-' }}</td>
            <td class="col-remark">{{ item.remark || '' }}</td>
          </tr>
        </tbody>
      </table>

      <div class="info-section bottom-info">
        <div class="info-item">
          <span class="info-label">制单人</span>
          <span class="info-value">{{ page.bom.created_by }}</span>
        </div>
      </div>

      <div class="page-footer">
        <span>第 {{ globalIdx + 1 }} 页 / 共 {{ allPages.length }} 页</span>
        <span v-if="allBoms.length > 1" style="margin-left: 16px">| BOM #{{ page.bomIdx + 1 }}/{{ allBoms.length }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bom-print {
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
}

.bom-separator {
  page-break-before: always;
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
  margin-bottom: 4px;
}

.company-short {
  font-size: 14px;
  color: #94a3b8;
  margin-bottom: 12px;
}

.doc-title {
  font-size: 26px;
  font-weight: 700;
  color: #1a3c6e;
  letter-spacing: 10px;
  margin-bottom: 4px;
}

.doc-subtitle {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 10px;
  font-style: italic;
}

.doc-meta-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 60px;
  font-size: 13px;
  color: #475569;
}

.doc-meta-item strong {
  color: #1e293b;
  font-weight: 600;
}

.version-tag {
  background: #1a3c6e;
  color: #fff;
  padding: 1px 10px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: 600;
}

.info-section {
  margin-bottom: 12px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 40px;
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

.bottom-info {
  margin-top: 20px;
}

.print-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 10px;
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
  padding: 7px 4px;
  text-align: center;
  color: #1e293b;
  font-size: 12px;
}

.print-table tbody tr:nth-child(even) td {
  background: #f8fafc;
}

.col-seq { width: 4%; }
.col-level { width: 5%; }
.col-code { width: 13%; text-align: left !important; }
.col-name { width: 16%; text-align: left !important; }
.col-spec { width: 12%; }
.col-qty { width: 8%; }
.col-unit { width: 6%; }
.col-waste { width: 7%; }
.col-remark { width: 29%; }

.page-footer {
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
  margin-top: 20px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

@media print {
  .bom-print {
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

  .company-full, .doc-title {
    color: #3a6ca0 !important;
  }

  .version-tag {
    background: #5a7fa8 !important;
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