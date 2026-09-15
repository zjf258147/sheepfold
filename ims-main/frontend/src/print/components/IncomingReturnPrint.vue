<script setup>
import { COMPANY_INFO, formatDate } from '../print-utils'

const props = defineProps({
  data: { type: Object, default: null },
})

const doc = props.data?.data || {}
</script>

<template>
  <div class="print-document return-print">
    <div class="print-page">
      <div class="header-accent"></div>
      <div class="brand-area">
        <div class="company-full">{{ COMPANY_INFO.fullName }}</div>
        <div class="company-short">{{ COMPANY_INFO.shortName }}</div>
        <div class="doc-title">退 货 单</div>
        <div class="doc-meta-row">
          <span class="doc-meta-item">退货单号：<strong>{{ doc.return_no }}</strong></span>
          <span class="doc-meta-item">退货日期：<strong>{{ formatDate(doc.return_date) }}</strong></span>
        </div>
      </div>

      <div class="info-section">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">供应商</span>
            <span class="info-value">{{ doc.supplier_name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">原到货单号</span>
            <span class="info-value">{{ doc.receipt_no }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">批次号</span>
            <span class="info-value">{{ doc.batch_no }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">处理方式</span>
            <span class="info-value check-value">
              <span class="check-option">□ 换货</span>
              <span class="check-option">□ 退款</span>
              <span class="check-option">□ 维修</span>
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
            <th class="col-qty">收货数量</th>
            <th class="col-qty">退货数量</th>
            <th class="col-unit">单位</th>
            <th class="col-remark">备注</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="col-seq">1</td>
            <td class="col-code">{{ doc.sku_code }}</td>
            <td class="col-name">{{ doc.sku_name }}</td>
            <td class="col-spec">{{ doc.spec || '-' }}</td>
            <td class="col-qty">{{ doc.quantity }}</td>
            <td class="col-qty return-qty">{{ doc.return_qty }}</td>
            <td class="col-unit">{{ doc.unit }}</td>
            <td class="col-remark">{{ doc.remark || '' }}</td>
          </tr>
        </tbody>
      </table>

      <div class="reason-section">
        <span class="section-label">退货原因</span>
        <div class="reason-box">{{ doc.return_reason }}</div>
      </div>

      <div class="signature-area">
        <div class="signature-item">
          <div class="signature-label">经办人</div>
          <div class="signature-line"></div>
          <div class="signature-date">日期：___年___月___日</div>
        </div>
        <div class="signature-item">
          <div class="signature-label">供应商签收</div>
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
.return-print {
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

.check-value {
  display: flex;
  gap: 20px;
  border-bottom: none;
}

.check-option {
  border: 1px solid #94a3b8;
  padding: 2px 10px;
  border-radius: 2px;
  font-size: 13px;
  color: #64748b;
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
.col-code { width: 13%; }
.col-name { width: 16%; }
.col-spec { width: 14%; }
.col-qty { width: 9%; }
.col-unit { width: 7%; }
.col-remark { width: 27%; }

.return-qty {
  color: #dc2626 !important;
  font-weight: 700;
}

.reason-section {
  margin-bottom: 14px;
}

.section-label {
  font-size: 14px;
  font-weight: 700;
  color: #dc2626;
  display: block;
  margin-bottom: 6px;
}

.reason-box {
  border: 1px solid #dc2626;
  background: #fef2f2;
  padding: 12px 16px;
  font-size: 16px;
  font-weight: 700;
  color: #dc2626;
  min-height: 40px;
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
  .return-print {
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
    color: #b91c1c !important;
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