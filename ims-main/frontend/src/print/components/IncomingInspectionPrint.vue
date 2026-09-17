<script setup>
import { computed } from 'vue'
import { COMPANY_INFO, formatDate } from '../print-utils'

const props = defineProps({
  data: { type: Object, default: null },
  inspections: { type: Array, default: () => [] },
})

const allDocs = computed(() => {
  if (props.inspections && props.inspections.length > 0) {
    return props.inspections.map(r => r.data || r)
  }
  if (props.data) {
    return [props.data.data || props.data]
  }
  return []
})
</script>

<template>
  <div class="print-document inspection-print">
    <template v-for="(doc, idx) in allDocs" :key="doc.inspection_no || idx">
    <div class="print-page" :class="{ 'batch-page': idx < allDocs.length - 1 }">
      <div class="header-accent"></div>
      <div class="brand-area">
        <div class="company-full">{{ COMPANY_INFO.fullName }}</div>
        <div class="company-short">{{ COMPANY_INFO.shortName }}</div>
        <div class="doc-title">来料检验报告</div>
        <div class="doc-subtitle">Incoming Inspection Report</div>
        <div class="doc-meta-row">
          <span class="doc-meta-item">报告编号：<strong>{{ doc.inspection_no }}</strong></span>
          <span class="doc-meta-item">检验日期：<strong>{{ formatDate(doc.inspection_date) }}</strong></span>
        </div>
      </div>

      <div class="info-section">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">供应商</span>
            <span class="info-value">{{ doc.supplier_name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">到货单号</span>
            <span class="info-value">{{ doc.receipt_no }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">批次号</span>
            <span class="info-value">{{ doc.batch_no }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">检验依据</span>
            <span class="info-value">GB/T 2828.1-2012</span>
          </div>
        </div>
      </div>

      <div class="material-info">
        <span class="section-label">物料信息</span>
        <table class="info-table">
        <tbody>
          <tr>
            <td class="info-td-label">物料编码</td>
            <td>{{ doc.sku_code }}</td>
            <td class="info-td-label">物料名称</td>
            <td>{{ doc.sku_name }}</td>
          </tr>
          <tr>
            <td class="info-td-label">规格型号</td>
            <td>{{ doc.spec || '-' }}</td>
            <td class="info-td-label">来料数量</td>
            <td>{{ doc.quantity }} {{ doc.unit }}</td>
          </tr>
        </tbody>
        </table>
      </div>

      <div class="inspection-items">
        <span class="section-label">检验项目</span>
        <table class="print-table">
          <thead>
            <tr>
              <th>序号</th>
              <th>检验项目</th>
              <th>标准要求</th>
              <th>实测值</th>
              <th>单项判定</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>外观检查</td>
              <td>无破损、无划痕、标签清晰</td>
              <td>符合</td>
              <td class="result-pass">合格</td>
            </tr>
            <tr>
              <td>2</td>
              <td>尺寸检查</td>
              <td>符合图纸要求</td>
              <td>符合</td>
              <td class="result-pass">合格</td>
            </tr>
            <tr>
              <td>3</td>
              <td>性能测试</td>
              <td>功能正常</td>
              <td>符合</td>
              <td class="result-pass">合格</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="defect-section" v-if="doc.defect_description">
        <span class="section-label">缺陷描述</span>
        <div class="defect-box">{{ doc.defect_description }}</div>
      </div>

      <div class="result-section">
        <div class="result-row">
          <span class="section-label">抽样信息</span>
          <span>抽样数量：{{ doc.sample_qty }}  |  不良数量：{{ doc.defect_qty }}</span>
        </div>
        <div class="result-row">
          <span class="section-label">综合判定</span>
          <span class="result-badge" :class="{
            'result-accept': doc.result === 'ACCEPTED',
            'result-concession': doc.result === 'CONCESSION_ACCEPTED',
            'result-reject': doc.result === 'REJECTED',
          }">{{ doc.result_cn }}</span>
        </div>
      </div>

      <div class="signature-area">
        <div class="signature-item">
          <div class="signature-label">检验员</div>
          <div class="signature-value">{{ doc.inspector_name }}</div>
          <div class="signature-date">日期：___年___月___日</div>
        </div>
        <div class="signature-item">
          <div class="signature-label">审核人</div>
          <div class="signature-line"></div>
          <div class="signature-date">日期：___年___月___日</div>
        </div>
      </div>

      <div class="page-footer">
        <span>{{ allDocs.length > 1 ? `第 ${idx + 1} 页 / 共 ${allDocs.length} 页（检验报告）` : '第 1 页 / 共 1 页' }}</span>
      </div>
    </div>
    </template>
  </div>
</template>

<style scoped>
.inspection-print {
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

.batch-page {
  page-break-after: always;
  margin-bottom: 20px;
  border-bottom: 2px dashed #cbd5e1;
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

.section-label {
  font-size: 14px;
  font-weight: 700;
  color: #1a3c6e;
  display: block;
  margin: 12px 0 6px 0;
  padding-left: 4px;
  border-left: 3px solid #1a3c6e;
}

.material-info {
  margin-bottom: 10px;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.info-table td {
  border: 1px solid #cbd5e1;
  padding: 6px 10px;
}

.info-td-label {
  background: #f1f5f9;
  font-weight: 600;
  color: #475569;
  width: 15%;
  text-align: right;
}

.inspection-items {
  margin-bottom: 10px;
}

.print-table {
  width: 100%;
  border-collapse: collapse;
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

.result-pass {
  color: #16a34a !important;
  font-weight: 600;
}

.defect-section {
  margin-bottom: 10px;
}

.defect-box {
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  padding: 10px 14px;
  min-height: 50px;
  font-size: 13px;
  color: #dc2626;
  border-radius: 4px;
}

.result-section {
  margin-bottom: 20px;
}

.result-row {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 8px;
  font-size: 13px;
}

.result-badge {
  font-size: 20px;
  font-weight: 700;
  padding: 4px 24px;
  border-radius: 4px;
  border: 2px solid;
}

.result-accept {
  color: #16a34a;
  border-color: #16a34a;
  background: #f0fdf4;
}

.result-concession {
  color: #d97706;
  border-color: #d97706;
  background: #fffbeb;
}

.result-reject {
  color: #dc2626;
  border-color: #dc2626;
  background: #fef2f2;
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

.signature-value {
  font-size: 13px;
  color: #1e293b;
  margin-bottom: 4px;
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
  .inspection-print {
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

  .section-label {
    color: #3a6ca0 !important;
    border-left-color: #5a7fa8 !important;
  }

  .print-table thead th {
    background: #5a7fa8 !important;
    color: #fff !important;
    border-color: #5a7fa8 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
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