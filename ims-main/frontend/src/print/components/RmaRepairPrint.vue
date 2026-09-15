<script setup>
import { COMPANY_INFO, formatDate } from '../print-utils'

const props = defineProps({
  data: { type: Object, default: null },
})

const doc = props.data?.data || {}
</script>

<template>
  <div class="print-document repair-print">
    <div class="print-page">
      <div class="header-accent"></div>
      <div class="brand-area">
        <div class="company-full">{{ COMPANY_INFO.fullName }}</div>
        <div class="company-short">{{ COMPANY_INFO.shortName }}</div>
        <div class="doc-title">维修工单</div>
        <div class="doc-subtitle">Repair Work Order</div>
        <div class="doc-meta-row">
          <span class="doc-meta-item">工单编号：<strong>{{ doc.repair_no }}</strong></span>
          <span class="doc-meta-item">完工日期：<strong>{{ formatDate(doc.repair_date) }}</strong></span>
        </div>
      </div>

      <div class="info-section">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">返厂单号</span>
            <span class="info-value">{{ doc.return_no }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">客户</span>
            <span class="info-value">{{ doc.customer_name || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">物料编码</span>
            <span class="info-value">{{ doc.sku_code }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">物料名称</span>
            <span class="info-value">{{ doc.sku_name }}</span>
          </div>
        </div>
      </div>

      <div class="sn-section">
        <span class="section-label">设备信息</span>
        <div class="sn-row">
          <span class="sn-label">原SN码</span>
          <span class="sn-value">{{ doc.old_sn }}</span>
          <span v-if="doc.new_sn" class="sn-label">新SN码</span>
          <span v-if="doc.new_sn" class="sn-value sn-new">{{ doc.new_sn }}</span>
        </div>
        <div class="spec-row">
          <span class="sn-label">规格型号</span>
          <span>{{ doc.spec || '-' }}</span>
        </div>
      </div>

      <div class="problem-section" v-if="doc.problem_description">
        <span class="section-label">故障现象</span>
        <div class="problem-box">{{ doc.problem_description }}</div>
      </div>

      <div class="diagnosis-section" v-if="doc.diagnosis_result">
        <span class="section-label">诊断结论</span>
        <div class="diagnosis-box">{{ doc.diagnosis_result }}</div>
      </div>

      <div class="repair-section">
        <span class="section-label">维修方案</span>
        <div class="repair-box">{{ doc.repair_description || '（待填写）' }}</div>
      </div>

      <div class="materials-section" v-if="doc.materials_used">
        <span class="section-label">更换零件</span>
        <div class="materials-box">{{ doc.materials_used }}</div>
      </div>

      <div class="signature-area">
        <div class="signature-item">
          <div class="signature-label">维修人</div>
          <div class="signature-value">{{ doc.repairer_name }}</div>
          <div class="signature-date">日期：___年___月___日</div>
        </div>
        <div class="signature-item">
          <div class="signature-label">审核人</div>
          <div class="signature-line"></div>
          <div class="signature-date">日期：___年___月___日</div>
        </div>
      </div>

      <div class="page-footer">
        <span>第 1 页 / 共 1 页</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.repair-print {
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

.sn-section {
  margin-bottom: 10px;
}

.sn-row, .spec-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 6px;
  font-size: 13px;
}

.sn-label {
  font-weight: 600;
  color: #475569;
  white-space: nowrap;
}

.sn-label::after {
  content: '：';
}

.sn-value {
  font-size: 14px;
  font-weight: 700;
  color: #2563eb;
  font-family: 'Consolas', 'Courier New', monospace;
  background: #eff6ff;
  padding: 2px 10px;
  border-radius: 3px;
  border: 1px solid #bfdbfe;
}

.sn-new {
  color: #16a34a;
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.problem-section, .diagnosis-section, .repair-section, .materials-section {
  margin-bottom: 10px;
}

.problem-box {
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  padding: 12px 16px;
  min-height: 50px;
  font-size: 13px;
  color: #475569;
  border-radius: 4px;
  line-height: 1.6;
}

.diagnosis-box {
  border: 1px solid #1a3c6e;
  background: #f1f5f9;
  padding: 12px 16px;
  min-height: 40px;
  font-size: 14px;
  font-weight: 600;
  color: #1a3c6e;
  border-radius: 4px;
  line-height: 1.6;
}

.repair-box {
  border: 1px solid #cbd5e1;
  padding: 12px 16px;
  min-height: 80px;
  font-size: 13px;
  color: #1e293b;
  border-radius: 4px;
  line-height: 1.6;
}

.materials-box {
  border: 1px solid #cbd5e1;
  padding: 12px 16px;
  min-height: 40px;
  font-size: 13px;
  color: #1e293b;
  border-radius: 4px;
  line-height: 1.6;
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
  .repair-print {
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

  .sn-value {
    color: #3a6ca0 !important;
    background: #f0f4f8 !important;
    border-color: #a0bcd0 !important;
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