<script setup>
import { onMounted, ref } from 'vue'
import { listIncomingReceipts, createIncomingReceipt, createIncomingInspection, createIncomingReturn, confirmIncomingReceipt, exportIncomingReceipts } from '@/api/incoming'
import { listSkus, listCategories } from '@/api/product'
import { listPartners } from '@/api/partner'
import { INCOMING_STATUS_MAP, INCOMING_STATUS_TAG, INSPECTION_RESULT_MAP } from '@/constants/enums'
import { dateTimeColumnFormatter } from '@/utils/datetime'
import { Download } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getIncomingReceiptPrintData, getIncomingReceiptBatchPrintData, getIncomingInspectionPrintData, getIncomingReturnPrintData } from '@/api/print'
import PrintPreview from '@/print/components/PrintPreview.vue'
import IncomingReceiptPrint from '@/print/components/IncomingReceiptPrint.vue'
import IncomingInspectionPrint from '@/print/components/IncomingInspectionPrint.vue'
import IncomingReturnPrint from '@/print/components/IncomingReturnPrint.vue'

const loading = ref(false)
const exportLoading = ref(false)
const receipts = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(15)
const query = ref({
  keyword: '',
  category_id: null,
  sku_id: null,
  supplier_id: null,
  status: '',
  dateRange: [],
})

const categories = ref([])
const skus = ref([])
const suppliers = ref([])

const createDialog = ref(false)
const createForm = ref({
  supplier_id: null,
  sku_id: null,
  batch_no: '',
  quantity: 1,
  unit: '个',
  delivery_date: '',
  remark: '',
})
const createLoading = ref(false)

const inspectionDialog = ref(false)
const inspectionForm = ref({
  receipt_id: null,
  inspector_id: null,
  inspection_date: '',
  result: 'ACCEPTED',
  sample_qty: 0,
  defect_qty: 0,
  defect_description: '',
  change_reason: '',
})
const inspectionLoading = ref(false)

const returnDialog = ref(false)
const returnForm = ref({
  receipt_id: null,
  return_qty: 1,
  return_reason: '',
  return_date: '',
  change_reason: '',
})
const returnLoading = ref(false)

const confirmDialog = ref(false)
const confirmForm = ref({ receipt_id: null, change_reason: '' })
const confirmLoading = ref(false)

const currentReceipt = ref(null)

const printVisible = ref(false)
const printData = ref(null)
const printReceipts = ref([])
const printLoading = ref(false)
const batchPrintLoading = ref(false)
const selectedReceipts = ref([])

const inspectionPrintVisible = ref(false)
const inspectionPrintData = ref(null)
const inspectionPrintLoading = ref(false)

const returnPrintVisible = ref(false)
const returnPrintData = ref(null)
const returnPrintLoading = ref(false)

async function handlePrint(row) {
  printLoading.value = true
  try {
    const res = await getIncomingReceiptPrintData(row.id)
    printData.value = res.data
    printReceipts.value = []
    printVisible.value = true
  } catch {
    ElMessage.error('获取打印数据失败')
  } finally {
    printLoading.value = false
  }
}

async function handleBatchPrint() {
  if (selectedReceipts.value.length === 0) {
    ElMessage.warning('请先选择要打印的收货单')
    return
  }
  batchPrintLoading.value = true
  try {
    const ids = selectedReceipts.value.map(r => r.id)
    const results = await getIncomingReceiptBatchPrintData(ids)
    printReceipts.value = results.map(r => r.data)
    printData.value = null
    printVisible.value = true
  } catch {
    ElMessage.error('批量获取打印数据失败')
  } finally {
    batchPrintLoading.value = false
  }
}

async function handleInspectionPrint(row) {
  if (!row.inspection_id) {
    ElMessage.warning('该记录没有检验报告')
    return
  }
  inspectionPrintLoading.value = true
  try {
    const res = await getIncomingInspectionPrintData(row.inspection_id)
    inspectionPrintData.value = res.data
    inspectionPrintVisible.value = true
  } catch {
    ElMessage.error('获取检验报告打印数据失败')
  } finally {
    inspectionPrintLoading.value = false
  }
}

async function handleReturnPrint(row) {
  if (!row.return_id) {
    ElMessage.warning('该记录没有退货单')
    return
  }
  returnPrintLoading.value = true
  try {
    const res = await getIncomingReturnPrintData(row.return_id)
    returnPrintData.value = res.data
    returnPrintVisible.value = true
  } catch {
    ElMessage.error('获取退货单打印数据失败')
  } finally {
    returnPrintLoading.value = false
  }
}

function handleSelectionChange(rows) {
  selectedReceipts.value = rows
}

async function loadData() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value,
      keyword: query.value.keyword || undefined,
      category_id: query.value.category_id || undefined,
      sku_id: query.value.sku_id || undefined,
      supplier_id: query.value.supplier_id || undefined,
      status: query.value.status || undefined,
    }
    if (query.value.dateRange?.length === 2) {
      params.start_date = query.value.dateRange[0]
      params.end_date = query.value.dateRange[1]
    }
    const res = await listIncomingReceipts(params)
    receipts.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

async function loadOptions() {
  const [catRes, supRes] = await Promise.all([listCategories(), listPartners({ type: 'SUPPLIER' })])
  categories.value = catRes.data
  suppliers.value = supRes.data.items || []
}

async function onCategoryChange(catId) {
  query.value.sku_id = null
  if (catId) {
    const res = await listSkus({ category_id: catId, page_size: 200 })
    skus.value = res.data.items
  } else {
    skus.value = []
  }
}

function search() {
  page.value = 1
  loadData()
}

function resetQuery() {
  query.value = { keyword: '', category_id: null, sku_id: null, supplier_id: null, status: '', dateRange: [] }
  skus.value = []
  search()
}

async function handleExport() {
  exportLoading.value = true
  try {
    const params = {
      keyword: query.value.keyword || undefined,
      category_id: query.value.category_id || undefined,
      sku_id: query.value.sku_id || undefined,
      supplier_id: query.value.supplier_id || undefined,
      status: query.value.status || undefined,
    }
    if (query.value.dateRange?.length === 2) {
      params.start_date = query.value.dateRange[0]
      params.end_date = query.value.dateRange[1]
    }
    const blob = await exportIncomingReceipts(params)
    const d = new Date()
    const dateStr = `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `IMS-来料管理-${dateStr}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  } finally {
    exportLoading.value = false
  }
}

function onPageChange(p) {
  page.value = p
  loadData()
}

function openCreate() {
  createForm.value = { supplier_id: null, sku_id: null, batch_no: '', quantity: 1, unit: '个', delivery_date: '', remark: '' }
  createDialog.value = true
}

async function submitCreate() {
  createLoading.value = true
  try {
    await createIncomingReceipt(createForm.value)
    ElMessage.success('到货登记成功')
    createDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '登记失败')
  } finally {
    createLoading.value = false
  }
}

function openInspection(row) {
  currentReceipt.value = row
  inspectionForm.value = {
    receipt_id: row.id,
    inspector_id: null,
    inspection_date: new Date().toISOString().slice(0, 10),
    result: 'ACCEPTED',
    sample_qty: 0,
    defect_qty: 0,
    defect_description: '',
    change_reason: '',
  }
  inspectionDialog.value = true
}

async function submitInspection() {
  if (!inspectionForm.value.change_reason) {
    ElMessage.warning('请填写变更原因')
    return
  }
  inspectionLoading.value = true
  try {
    await createIncomingInspection(inspectionForm.value)
    ElMessage.success('检验完成')
    inspectionDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '检验失败')
  } finally {
    inspectionLoading.value = false
  }
}

function openReturn(row) {
  currentReceipt.value = row
  returnForm.value = {
    receipt_id: row.id,
    return_qty: row.quantity,
    return_reason: '',
    return_date: new Date().toISOString().slice(0, 10),
    change_reason: '',
  }
  returnDialog.value = true
}

async function submitReturn() {
  if (!returnForm.value.change_reason) {
    ElMessage.warning('请填写变更原因')
    return
  }
  returnLoading.value = true
  try {
    await createIncomingReturn(returnForm.value)
    ElMessage.success('退货完成')
    returnDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '退货失败')
  } finally {
    returnLoading.value = false
  }
}

function openConfirm(row) {
  currentReceipt.value = row
  confirmForm.value = { receipt_id: row.id, change_reason: '' }
  confirmDialog.value = true
}

async function submitConfirm() {
  if (!confirmForm.value.change_reason) {
    ElMessage.warning('请填写入库确认原因')
    return
  }
  confirmLoading.value = true
  try {
    await confirmIncomingReceipt(confirmForm.value.receipt_id, { change_reason: confirmForm.value.change_reason })
    ElMessage.success('入库确认完成')
    confirmDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '确认失败')
  } finally {
    confirmLoading.value = false
  }
}

onMounted(() => {
  loadOptions()
  loadData()
})
</script>

<template>
  <el-card>
    <el-form :inline="true" class="list-search">
      <el-form-item label="关键词">
        <el-input v-model="query.keyword" clearable placeholder="到货单号/批次号" style="width:180px" @keyup.enter="search" />
      </el-form-item>
      <el-form-item label="分类">
        <el-select v-model="query.category_id" clearable placeholder="全部分类" style="width:140px" @change="onCategoryChange">
          <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="物料">
        <el-select v-model="query.sku_id" clearable placeholder="全部物料" style="width:160px">
          <el-option v-for="s in skus" :key="s.id" :label="`${s.name}${s.spec ? ' (' + s.spec + ')' : ''}`" :value="s.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="供应商">
        <el-select v-model="query.supplier_id" clearable placeholder="全部供应商" style="width:160px">
          <el-option v-for="s in suppliers" :key="s.id" :label="s.name" :value="s.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" clearable placeholder="全部状态" style="width:130px">
          <el-option v-for="[k, v] in Object.entries(INCOMING_STATUS_MAP)" :key="k" :label="v" :value="k" />
        </el-select>
      </el-form-item>
      <el-form-item label="日期">
        <el-date-picker
          v-model="query.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始"
          end-placeholder="结束"
          value-format="YYYY-MM-DD"
          style="width:240px"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="search">搜索</el-button>
        <el-button @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <div class="toolbar">
      <el-button type="primary" @click="openCreate">到货登记</el-button>
      <el-button type="success" :icon="Download" :loading="exportLoading" @click="handleExport">导出</el-button>
      <el-button type="warning" :loading="batchPrintLoading" :disabled="selectedReceipts.length === 0" @click="handleBatchPrint">
        批量打印 {{ selectedReceipts.length > 0 ? `(${selectedReceipts.length})` : '' }}
      </el-button>
    </div>

    <el-table :data="receipts" v-loading="loading" stripe @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="50" />
      <el-table-column prop="receipt_no" label="到货单号" width="150" show-overflow-tooltip />
      <el-table-column prop="batch_no" label="批次号" width="140" show-overflow-tooltip />
      <el-table-column prop="supplier_name" label="供应商" width="160" show-overflow-tooltip />
      <el-table-column prop="sku_name" label="物料名称" width="140" show-overflow-tooltip />
      <el-table-column prop="spec" label="规格型号" width="120" show-overflow-tooltip />
      <el-table-column label="数量" width="80" align="center">
        <template #default="{ row }">{{ row.quantity }} {{ row.unit }}</template>
      </el-table-column>
      <el-table-column label="到货日期" width="110" :formatter="dateTimeColumnFormatter" prop="delivery_date" />
      <el-table-column label="状态" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="INCOMING_STATUS_TAG[row.status] || 'info'" size="small">{{ INCOMING_STATUS_MAP[row.status] || row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" width="140" show-overflow-tooltip align="center" />
      <el-table-column label="创建时间" width="160" :formatter="dateTimeColumnFormatter" prop="created_at" align="center" />
      <el-table-column label="操作" width="360" fixed="right" align="center">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="handlePrint(row)" :loading="printLoading">收货单</el-button>
          <el-button v-if="row.inspection_id" type="success" link size="small" @click="handleInspectionPrint(row)" :loading="inspectionPrintLoading">检验报告</el-button>
          <el-button v-if="row.return_id" type="danger" link size="small" @click="handleReturnPrint(row)" :loading="returnPrintLoading">退货单</el-button>
          <el-button v-if="row.status === 'PENDING_INSPECTION' || row.status === 'INSPECTED'" type="primary" link size="small" @click="openInspection(row)">检验</el-button>
          <el-button v-if="row.status === 'INSPECTED'" type="danger" link size="small" @click="openReturn(row)">退货</el-button>
          <el-button v-if="row.status === 'ACCEPTED'" type="success" link size="small" @click="openConfirm(row)">确认入库</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      class="list-pagination"
      layout="total, prev, pager, next"
      :total="total"
      :page-size="pageSize"
      :current-page="page"
      @current-change="onPageChange"
    />
  </el-card>

  <el-dialog v-model="createDialog" title="到货登记" width="500px">
    <el-form label-width="80px">
      <el-form-item label="供应商" required>
        <el-select v-model="createForm.supplier_id" style="width:100%" placeholder="请选择供应商">
          <el-option v-for="s in suppliers" :key="s.id" :label="s.name" :value="s.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="物料" required>
        <el-select v-model="createForm.sku_id" style="width:100%" placeholder="请选择物料" filterable>
          <el-option v-for="s in skus" :key="s.id" :label="`${s.name}${s.spec ? ' (' + s.spec + ')' : ''}`" :value="s.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="批次号" required><el-input v-model="createForm.batch_no" placeholder="请输入批次号" /></el-form-item>
      <el-form-item label="数量" required>
        <el-input-number v-model="createForm.quantity" :min="1" style="width:100%" />
      </el-form-item>
      <el-form-item label="单位"><el-input v-model="createForm.unit" placeholder="个" /></el-form-item>
      <el-form-item label="到货日期" required>
        <el-date-picker v-model="createForm.delivery_date" type="date" value-format="YYYY-MM-DD" style="width:100%" />
      </el-form-item>
      <el-form-item label="备注"><el-input v-model="createForm.remark" type="textarea" :rows="2" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="createDialog = false">取消</el-button>
      <el-button type="primary" :loading="createLoading" @click="submitCreate">提交</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="inspectionDialog" title="来料检验" width="550px">
    <el-form label-width="100px">
      <el-form-item label="到货单号">{{ currentReceipt?.receipt_no }}</el-form-item>
      <el-form-item label="检验日期" required>
        <el-date-picker v-model="inspectionForm.inspection_date" type="date" value-format="YYYY-MM-DD" style="width:100%" />
      </el-form-item>
      <el-form-item label="检验结果" required>
        <el-select v-model="inspectionForm.result" style="width:100%">
          <el-option v-for="[k, v] in Object.entries(INSPECTION_RESULT_MAP)" :key="k" :label="v" :value="k" />
        </el-select>
      </el-form-item>
      <el-form-item label="抽样数量">
        <el-input-number v-model="inspectionForm.sample_qty" :min="0" style="width:100%" />
      </el-form-item>
      <el-form-item label="不良数量">
        <el-input-number v-model="inspectionForm.defect_qty" :min="0" style="width:100%" />
      </el-form-item>
      <el-form-item label="不良描述"><el-input v-model="inspectionForm.defect_description" type="textarea" :rows="2" /></el-form-item>
      <el-form-item label="变更原因" required>
        <el-input v-model="inspectionForm.change_reason" placeholder="请填写变更原因（必填）" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="inspectionDialog = false">取消</el-button>
      <el-button type="primary" :loading="inspectionLoading" :disabled="!inspectionForm.change_reason" @click="submitInspection">提交</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="returnDialog" title="退货" width="500px">
    <el-form label-width="100px">
      <el-form-item label="到货单号">{{ currentReceipt?.receipt_no }}</el-form-item>
      <el-form-item label="退货数量" required>
        <el-input-number v-model="returnForm.return_qty" :min="1" :max="currentReceipt?.quantity" style="width:100%" />
      </el-form-item>
      <el-form-item label="退货日期" required>
        <el-date-picker v-model="returnForm.return_date" type="date" value-format="YYYY-MM-DD" style="width:100%" />
      </el-form-item>
      <el-form-item label="退货原因" required>
        <el-input v-model="returnForm.return_reason" type="textarea" :rows="2" placeholder="请填写退货原因" />
      </el-form-item>
      <el-form-item label="变更原因" required>
        <el-input v-model="returnForm.change_reason" placeholder="请填写变更原因（必填）" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="returnDialog = false">取消</el-button>
      <el-button type="primary" :loading="returnLoading" :disabled="!returnForm.change_reason" @click="submitReturn">提交</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="confirmDialog" title="确认入库" width="500px">
    <el-form label-width="100px">
      <el-form-item label="到货单号">{{ currentReceipt?.receipt_no }}</el-form-item>
      <el-form-item label="物料名称">{{ currentReceipt?.sku_name }}</el-form-item>
      <el-form-item label="数量">{{ currentReceipt?.quantity }} {{ currentReceipt?.unit }}</el-form-item>
      <el-form-item label="入库原因" required>
        <el-input v-model="confirmForm.change_reason" type="textarea" :rows="2" placeholder="请填写入库确认原因（必填）" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="confirmDialog = false">取消</el-button>
      <el-button type="primary" :loading="confirmLoading" :disabled="!confirmForm.change_reason" @click="submitConfirm">确认入库</el-button>
    </template>
  </el-dialog>

  <PrintPreview v-model:visible="printVisible" title="采购收货单">
    <IncomingReceiptPrint v-if="printData || printReceipts.length > 0" :data="printData" :receipts="printReceipts" />
  </PrintPreview>

  <PrintPreview v-model:visible="inspectionPrintVisible" title="来料检验报告">
    <IncomingInspectionPrint v-if="inspectionPrintData" :data="inspectionPrintData" />
  </PrintPreview>

  <PrintPreview v-model:visible="returnPrintVisible" title="退货单">
    <IncomingReturnPrint v-if="returnPrintData" :data="returnPrintData" />
  </PrintPreview>
</template>

<style scoped>
.toolbar { margin-bottom: 12px; }
.list-search { margin-bottom: 4px; }
.list-search :deep(.el-form-item) { margin-bottom: 12px; }
.list-pagination { margin-top: 16px; justify-content: flex-end; }
</style>