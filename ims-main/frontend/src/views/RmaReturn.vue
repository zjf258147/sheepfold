<script setup>
import { onMounted, ref } from 'vue'
import { listRmaReturns, createRmaReturn, createRmaDiagnosis, createRmaRepair, createRmaScrap, assignRmaReturn, createRmaReship, createRmaQualityCheck, createRmaWarehouseIn, exportRmaReturns } from '@/api/rma'
import { listSkus, listCategories } from '@/api/product'
import { RMA_STATUS_MAP, RMA_STATUS_TAG, DIAGNOSIS_RESULT_MAP, ASSIGN_TYPE_MAP, QUALITY_CHECK_RESULT_MAP, WAREHOUSE_TYPE_MAP } from '@/constants/enums'
import { ElMessage } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import { getRmaRepairPrintData } from '@/api/print'
import PrintPreview from '@/print/components/PrintPreview.vue'
import RmaRepairPrint from '@/print/components/RmaRepairPrint.vue'

const loading = ref(false)
const exportLoading = ref(false)
const returns = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(15)
const query = ref({
  keyword: '',
  category_id: null,
  sku_id: null,
  status: '',
  dateRange: [],
})

const printVisible = ref(false)
const printData = ref(null)
const printLoading = ref(false)

async function handlePrintRepair(row) {
  if (!row.repair_id) {
    ElMessage.warning('该记录没有维修工单')
    return
  }
  printLoading.value = true
  try {
    const res = await getRmaRepairPrintData(row.repair_id)
    printData.value = res.data
    printVisible.value = true
  } catch {
    ElMessage.error('获取维修工单打印数据失败')
  } finally {
    printLoading.value = false
  }
}

const categories = ref([])
const skus = ref([])

const createDialog = ref(false)
const createForm = ref({
  sku_id: null,
  sn: '',
  quantity: 1,
  unit: '个',
  customer_name: '',
  return_reason: '',
  return_date: '',
  remark: '',
})
const createLoading = ref(false)

const diagnosisDialog = ref(false)
const diagnosisForm = ref({
  return_id: null,
  diagnosed_by: null,
  diagnosis_date: '',
  fault_description: '',
  diagnosis_result: 'REPAIRABLE',
  change_reason: '',
})
const diagnosisLoading = ref(false)

const assignDialog = ref(false)
const assignForm = ref({ assigned_to: null, assign_type: 'PRODUCTION', assign_reason: '', scrap_reason: '', change_reason: '' })
const assignLoading = ref(false)

const repairDialog = ref(false)
const repairForm = ref({
  return_id: null,
  repair_by: null,
  old_sn: '',
  new_sn: '',
  repair_description: '',
  materials_used: '',
  fault_code: '',
  start_time: '',
  end_time: '',
  repair_date: '',
  change_reason: '',
})
const repairLoading = ref(false)

const qualityCheckDialog = ref(false)
const qualityCheckForm = ref({
  return_id: null,
  checked_by: null,
  check_date: '',
  check_result: 'PASS',
  check_description: '',
  change_reason: '',
})
const qualityCheckLoading = ref(false)

const warehouseInDialog = ref(false)
const warehouseInForm = ref({
  return_id: null,
  new_sn: '',
  repair_count: 1,
  repair_reason: '',
  warehouse_type: 'ZERO_COST_FINISHED',
  change_reason: '',
})
const warehouseInLoading = ref(false)

const scrapDialog = ref(false)
const scrapForm = ref({ return_id: null, scrap_reason: '', change_reason: '' })
const scrapLoading = ref(false)

const reshipDialog = ref(false)
const reshipForm = ref({
  return_id: null,
  new_sn: '',
  software_version: '',
  ship_date: '',
  recipient: '',
  change_reason: '',
})
const reshipLoading = ref(false)

const currentReturn = ref(null)

async function loadData() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value,
      keyword: query.value.keyword || undefined,
      sku_id: query.value.sku_id || undefined,
      status: query.value.status || undefined,
    }
    if (query.value.dateRange?.length === 2) {
      params.start_date = query.value.dateRange[0]
      params.end_date = query.value.dateRange[1]
    }
    const res = await listRmaReturns(params)
    returns.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

async function loadOptions() {
  const [catRes] = await Promise.all([listCategories()])
  categories.value = catRes.data
}

async function onCategoryChange(catId) {
  query.value.sku_id = null
  if (catId) {
    const res = await listSkus({ category_id: catId, page_size: 200 })
    skus.value = res.data.items || []
  } else {
    skus.value = []
  }
}

function search() {
  page.value = 1
  loadData()
}

async function handleExport() {
  exportLoading.value = true
  try {
    const params = {
      keyword: query.value.keyword,
      status: query.value.status,
    }
    if (query.value.dateRange && query.value.dateRange.length === 2) {
      params.start_date = query.value.dateRange[0]
      params.end_date = query.value.dateRange[1]
    }
    const blob = await exportRmaReturns(params)
    const d = new Date()
    const dateStr = `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `IMS-返修记录-${dateStr}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  } finally { exportLoading.value = false }
}

function reset() {
  query.value = { keyword: '', category_id: null, sku_id: null, status: '', dateRange: [] }
  skus.value = []
  search()
}

function openCreate() {
  createForm.value = {
    sku_id: null,
    sn: '',
    quantity: 1,
    unit: '个',
    customer_name: '',
    return_reason: '',
    return_date: '',
    remark: '',
  }
  createDialog.value = true
}

async function submitCreate() {
  if (!createForm.value.sku_id || !createForm.value.sn || !createForm.value.return_reason || !createForm.value.return_date) {
    ElMessage.warning('请填写必填项')
    return
  }
  createLoading.value = true
  try {
    await createRmaReturn(createForm.value)
    ElMessage.success('退货登记成功')
    createDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  } finally {
    createLoading.value = false
  }
}

function openDiagnosis(row) {
  currentReturn.value = row
  diagnosisForm.value = {
    return_id: row.id,
    diagnosed_by: null,
    diagnosis_date: '',
    fault_description: '',
    diagnosis_result: 'REPAIRABLE',
    change_reason: '',
  }
  diagnosisDialog.value = true
}

async function submitDiagnosis() {
  if (!diagnosisForm.value.fault_description || !diagnosisForm.value.diagnosis_date || !diagnosisForm.value.change_reason) {
    ElMessage.warning('请填写故障描述、诊断日期和变更原因')
    return
  }
  diagnosisLoading.value = true
  try {
    await createRmaDiagnosis(diagnosisForm.value)
    ElMessage.success('诊断完成')
    diagnosisDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  } finally {
    diagnosisLoading.value = false
  }
}

function openAssign(row) {
  currentReturn.value = row
  assignForm.value = { assigned_to: null, assign_type: 'PRODUCTION', assign_reason: '', scrap_reason: '', change_reason: '' }
  assignDialog.value = true
}

async function submitAssign() {
  if (assignForm.value.assign_type === 'SCRAP') {
    if (!assignForm.value.assign_reason || !assignForm.value.change_reason) {
      ElMessage.warning('请填写报废原因和变更原因')
      return
    }
  } else {
    if (!assignForm.value.assigned_to || !assignForm.value.assign_reason || !assignForm.value.change_reason) {
      ElMessage.warning('请选择分配人、填写分配原因和变更原因')
      return
    }
  }
  assignLoading.value = true
  try {
    await assignRmaReturn(currentReturn.value.id, assignForm.value)
    ElMessage.success(assignForm.value.assign_type === 'SCRAP' ? '报废申请已提交，等待仓库审核' : '分配成功')
    assignDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  } finally {
    assignLoading.value = false
  }
}

function openRepair(row) {
  currentReturn.value = row
  repairForm.value = {
    return_id: row.id,
    repair_by: null,
    old_sn: row.sn,
    new_sn: '',
    repair_description: '',
    materials_used: '',
    fault_code: '',
    start_time: '',
    end_time: '',
    repair_date: '',
    change_reason: '',
  }
  repairDialog.value = true
}

async function submitRepair() {
  if (!repairForm.value.repair_description || !repairForm.value.change_reason) {
    ElMessage.warning('请填写维修描述和变更原因')
    return
  }
  repairLoading.value = true
  try {
    await createRmaRepair(repairForm.value)
    ElMessage.success('维修完成')
    repairDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  } finally {
    repairLoading.value = false
  }
}

function openQualityCheck(row) {
  currentReturn.value = row
  qualityCheckForm.value = {
    return_id: row.id,
    checked_by: null,
    check_date: '',
    check_result: 'PASS',
    check_description: '',
    change_reason: '',
  }
  qualityCheckDialog.value = true
}

async function submitQualityCheck() {
  if (!qualityCheckForm.value.check_date || !qualityCheckForm.value.change_reason) {
    ElMessage.warning('请填写检验日期和变更原因')
    return
  }
  qualityCheckLoading.value = true
  try {
    await createRmaQualityCheck(qualityCheckForm.value)
    ElMessage.success('质量检验完成')
    qualityCheckDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  } finally {
    qualityCheckLoading.value = false
  }
}

function openWarehouseIn(row) {
  currentReturn.value = row
  warehouseInForm.value = {
    return_id: row.id,
    new_sn: row.new_sn || '',
    repair_count: 1,
    repair_reason: row.repair_reason || '',
    warehouse_type: 'ZERO_COST_FINISHED',
    change_reason: '',
  }
  warehouseInDialog.value = true
}

async function submitWarehouseIn() {
  if (!warehouseInForm.value.new_sn || !warehouseInForm.value.change_reason) {
    ElMessage.warning('请填写新SN和变更原因')
    return
  }
  warehouseInLoading.value = true
  try {
    await createRmaWarehouseIn(warehouseInForm.value)
    ElMessage.success('入库审核完成')
    warehouseInDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  } finally {
    warehouseInLoading.value = false
  }
}

function openScrap(row) {
  currentReturn.value = row
  scrapForm.value = { return_id: row.id, scrap_reason: '', change_reason: '' }
  scrapDialog.value = true
}

async function submitScrap() {
  if (!scrapForm.value.scrap_reason || !scrapForm.value.change_reason) {
    ElMessage.warning('请填写报废原因和变更原因')
    return
  }
  scrapLoading.value = true
  try {
    await createRmaScrap(scrapForm.value)
    ElMessage.success('报废申请已提交')
    scrapDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  } finally {
    scrapLoading.value = false
  }
}

function openReship(row) {
  currentReturn.value = row
  reshipForm.value = {
    return_id: row.id,
    new_sn: row.new_sn || row.sn,
    software_version: '',
    ship_date: '',
    recipient: '',
    change_reason: '',
  }
  reshipDialog.value = true
}

async function submitReship() {
  if (!reshipForm.value.new_sn || !reshipForm.value.ship_date || !reshipForm.value.change_reason) {
    ElMessage.warning('请填写SN、出货日期和变更原因')
    return
  }
  reshipLoading.value = true
  try {
    await createRmaReship(reshipForm.value)
    ElMessage.success('再出货完成')
    reshipDialog.value = false
    search()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '操作失败')
  } finally {
    reshipLoading.value = false
  }
}

onMounted(() => {
  loadOptions()
  loadData()
})
</script>

<template>
  <div class="rma-page">
    <div class="search-bar">
      <el-input v-model="query.keyword" placeholder="搜索单号/SN/物料名" clearable style="width:220px" @clear="search" @keyup.enter="search" />
      <el-select v-model="query.category_id" placeholder="物料分类" clearable style="width:160px" @change="onCategoryChange">
        <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
      </el-select>
      <el-select v-model="query.sku_id" placeholder="物料" clearable style="width:180px">
        <el-option v-for="s in skus" :key="s.id" :label="s.name" :value="s.id" />
      </el-select>
      <el-select v-model="query.status" placeholder="状态" clearable style="width:140px">
        <el-option v-for="(label, key) in RMA_STATUS_MAP" :key="key" :label="label" :value="key" />
      </el-select>
      <el-date-picker v-model="query.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width:260px" />
      <el-button type="primary" @click="search">搜索</el-button>
      <el-button @click="reset">重置</el-button>
      <el-button type="primary" plain @click="openCreate">退货登记</el-button>
      <el-button type="success" :icon="Download" :loading="exportLoading" @click="handleExport">导出</el-button>
    </div>

    <el-table :data="returns" v-loading="loading" stripe border style="width:100%">
      <el-table-column prop="return_no" label="返厂单号" width="150" />
      <el-table-column prop="sn" label="设备SN" width="150" />
      <el-table-column prop="sku_code" label="物料编码" width="120" show-overflow-tooltip />
      <el-table-column prop="sku_name" label="物料名称" width="150" show-overflow-tooltip />
      <el-table-column prop="spec" label="规格" width="100" />
      <el-table-column prop="customer_name" label="客户" width="120" />
      <el-table-column prop="return_reason" label="退货原因" width="140" show-overflow-tooltip />
      <el-table-column label="状态" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="RMA_STATUS_TAG[row.status] || 'info'">{{ RMA_STATUS_MAP[row.status] || row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="assignee_name" label="负责人" width="90" />
      <el-table-column prop="new_sn" label="新SN" width="130" show-overflow-tooltip />
      <el-table-column prop="repair_time_hours" label="修复耗时(h)" width="100" align="center" />
      <el-table-column prop="turnaround_days" label="周转(天)" width="90" align="center" />
      <el-table-column prop="return_date" label="退货日期" width="110" />
      <el-table-column label="操作" width="260" align="center">
        <template #default="{ row }">
          <el-button v-if="row.repair_id" type="warning" link size="small" @click="handlePrintRepair(row)" :loading="printLoading">维修单</el-button>
          <el-button v-if="row.status === 'PENDING_DIAGNOSIS'" type="primary" link size="small" @click="openDiagnosis(row)">诊断</el-button>
          <el-button v-if="row.status === 'DIAGNOSED'" type="warning" link size="small" @click="openAssign(row)">分配</el-button>
          <el-button v-if="row.status === 'ASSIGNED' || row.status === 'REPAIRING'" type="primary" link size="small" @click="openRepair(row)">维修</el-button>
          <el-button v-if="row.status === 'REPAIRED'" type="success" link size="small" @click="openQualityCheck(row)">质量检验</el-button>
          <el-button v-if="row.status === 'QUALITY_CHECK'" type="primary" link size="small" @click="openWarehouseIn(row)">入库审核</el-button>
          <el-button v-if="row.status === 'WAREHOUSED'" type="success" link size="small" @click="openReship(row)">再出货</el-button>
          <el-button v-if="row.status === 'REPAIRED'" type="danger" link size="small" @click="openScrap(row)">报废</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="page"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[10, 15, 20, 50]"
      layout="total, sizes, prev, pager, next"
      style="margin-top:16px; justify-content:flex-end"
      @change="loadData"
    />

    <el-dialog v-model="createDialog" title="退货登记" width="550px">
      <el-form label-width="100px">
        <el-form-item label="物料" required>
          <el-select v-model="createForm.sku_id" placeholder="选择物料" filterable style="width:100%">
            <el-option v-for="s in skus" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="设备SN" required>
          <BarcodeScanner v-model="createForm.sn" placeholder="扫码或输入设备SN" />
        </el-form-item>
        <el-form-item label="数量"><el-input-number v-model="createForm.quantity" :min="1" /></el-form-item>
        <el-form-item label="客户名称"><el-input v-model="createForm.customer_name" placeholder="选填" /></el-form-item>
        <el-form-item label="退货原因" required>
          <el-input v-model="createForm.return_reason" placeholder="请填写退货原因（必填）" />
        </el-form-item>
        <el-form-item label="退货日期" required>
          <el-date-picker v-model="createForm.return_date" type="date" placeholder="选择日期" style="width:100%" />
        </el-form-item>
        <el-form-item label="备注"><el-input v-model="createForm.remark" type="textarea" :rows="2" placeholder="选填" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialog = false">取消</el-button>
        <el-button type="primary" :loading="createLoading" :disabled="!createForm.return_reason" @click="submitCreate">提交</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="diagnosisDialog" title="诊断报告" width="550px">
      <el-form label-width="100px">
        <el-form-item label="返厂单号">{{ currentReturn?.return_no }}</el-form-item>
        <el-form-item label="设备SN">{{ currentReturn?.sn }}</el-form-item>
        <el-form-item label="诊断日期" required>
          <el-date-picker v-model="diagnosisForm.diagnosis_date" type="date" placeholder="选择日期" style="width:100%" />
        </el-form-item>
        <el-form-item label="诊断人" required>
          <el-input-number v-model="diagnosisForm.diagnosed_by" :min="1" placeholder="诊断人ID" style="width:100%" />
        </el-form-item>
        <el-form-item label="诊断结果" required>
          <el-select v-model="diagnosisForm.diagnosis_result" style="width:100%">
            <el-option v-for="(label, key) in DIAGNOSIS_RESULT_MAP" :key="key" :label="label" :value="key" />
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" required>
          <el-input v-model="diagnosisForm.fault_description" type="textarea" :rows="3" placeholder="请详细描述故障现象" />
        </el-form-item>
        <el-form-item label="变更原因" required>
          <el-input v-model="diagnosisForm.change_reason" placeholder="必填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="diagnosisDialog = false">取消</el-button>
        <el-button type="primary" :loading="diagnosisLoading" :disabled="!diagnosisForm.change_reason" @click="submitDiagnosis">提交诊断</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="assignDialog" :title="assignForm.assign_type === 'SCRAP' ? '判定报废' : '分配任务'" width="500px">
      <el-form label-width="100px">
        <el-form-item label="返厂单号">{{ currentReturn?.return_no }}</el-form-item>
        <el-form-item label="设备SN">{{ currentReturn?.sn }}</el-form-item>
        <el-form-item label="分配类型" required>
          <el-select v-model="assignForm.assign_type" style="width:100%">
            <el-option v-for="(label, key) in ASSIGN_TYPE_MAP" :key="key" :label="label" :value="key" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="assignForm.assign_type !== 'SCRAP'" label="分配给" required>
          <el-input-number v-model="assignForm.assigned_to" :min="1" placeholder="用户ID" style="width:100%" />
        </el-form-item>
        <el-form-item :label="assignForm.assign_type === 'SCRAP' ? '报废原因' : '分配原因'" required>
          <el-input v-model="assignForm.assign_reason" :placeholder="assignForm.assign_type === 'SCRAP' ? '请填写报废原因（必填）' : '请填写分配原因（必填）'" />
        </el-form-item>
        <el-form-item label="变更原因" required>
          <el-input v-model="assignForm.change_reason" placeholder="必填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="assignDialog = false">取消</el-button>
        <el-button type="primary" :loading="assignLoading" :disabled="!assignForm.change_reason || !assignForm.assign_reason" @click="submitAssign">{{ assignForm.assign_type === 'SCRAP' ? '判定报废' : '确认分配' }}</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="repairDialog" title="维修工单" width="550px">
      <el-form label-width="100px">
        <el-form-item label="返厂单号">{{ currentReturn?.return_no }}</el-form-item>
        <el-form-item label="原SN"><el-input v-model="repairForm.old_sn" disabled /></el-form-item>
        <el-form-item label="新SN"><BarcodeScanner v-model="repairForm.new_sn" placeholder="换码时扫码，留空则不变" /></el-form-item>
        <el-form-item label="维修人" required>
          <el-input-number v-model="repairForm.repair_by" :min="1" placeholder="维修人ID" style="width:100%" />
        </el-form-item>
        <el-form-item label="故障码"><el-input v-model="repairForm.fault_code" placeholder="选填" /></el-form-item>
        <el-form-item label="开始时间"><el-date-picker v-model="repairForm.start_time" type="datetime" placeholder="选择开始时间" style="width:100%" /></el-form-item>
        <el-form-item label="结束时间"><el-date-picker v-model="repairForm.end_time" type="datetime" placeholder="选择结束时间" style="width:100%" /></el-form-item>
        <el-form-item label="维修描述" required>
          <el-input v-model="repairForm.repair_description" type="textarea" :rows="3" placeholder="描述维修过程" />
        </el-form-item>
        <el-form-item label="维修用料"><el-input v-model="repairForm.materials_used" type="textarea" :rows="2" placeholder="填写用料清单（仓库管理员可选消耗物料）" /></el-form-item>
        <el-form-item label="完成日期"><el-date-picker v-model="repairForm.repair_date" type="date" placeholder="选填" style="width:100%" /></el-form-item>
        <el-form-item label="变更原因" required>
          <el-input v-model="repairForm.change_reason" placeholder="必填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="repairDialog = false">取消</el-button>
        <el-button type="primary" :loading="repairLoading" :disabled="!repairForm.change_reason" @click="submitRepair">提交维修</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="qualityCheckDialog" title="质量检验" width="500px">
      <el-form label-width="100px">
        <el-form-item label="返厂单号">{{ currentReturn?.return_no }}</el-form-item>
        <el-form-item label="设备SN">{{ currentReturn?.new_sn || currentReturn?.sn }}</el-form-item>
        <el-form-item label="检验人" required>
          <el-input-number v-model="qualityCheckForm.checked_by" :min="1" placeholder="检验人ID" style="width:100%" />
        </el-form-item>
        <el-form-item label="检验日期" required>
          <el-date-picker v-model="qualityCheckForm.check_date" type="date" placeholder="选择日期" style="width:100%" />
        </el-form-item>
        <el-form-item label="检验结果" required>
          <el-select v-model="qualityCheckForm.check_result" style="width:100%">
            <el-option v-for="(label, key) in QUALITY_CHECK_RESULT_MAP" :key="key" :label="label" :value="key" />
          </el-select>
        </el-form-item>
        <el-form-item label="检验描述"><el-input v-model="qualityCheckForm.check_description" type="textarea" :rows="2" placeholder="选填" /></el-form-item>
        <el-form-item label="变更原因" required>
          <el-input v-model="qualityCheckForm.change_reason" placeholder="必填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="qualityCheckDialog = false">取消</el-button>
        <el-button type="primary" :loading="qualityCheckLoading" :disabled="!qualityCheckForm.change_reason" @click="submitQualityCheck">提交检验</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="warehouseInDialog" title="入库审核（零成本仓）" width="500px">
      <el-form label-width="100px">
        <el-form-item label="返厂单号">{{ currentReturn?.return_no }}</el-form-item>
        <el-form-item label="新SN" required>
          <BarcodeScanner v-model="warehouseInForm.new_sn" placeholder="扫码或输入新SN" />
        </el-form-item>
        <el-form-item label="入库仓库" required>
          <el-select v-model="warehouseInForm.warehouse_type" style="width:100%">
            <el-option v-for="(label, key) in WAREHOUSE_TYPE_MAP" :key="key" :label="label" :value="key" />
          </el-select>
        </el-form-item>
        <el-form-item label="维修次数">
          <el-input-number v-model="warehouseInForm.repair_count" :min="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="维修原因"><el-input v-model="warehouseInForm.repair_reason" type="textarea" :rows="2" placeholder="累计维修原因" /></el-form-item>
        <el-form-item label="变更原因" required>
          <el-input v-model="warehouseInForm.change_reason" placeholder="必填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="warehouseInDialog = false">取消</el-button>
        <el-button type="primary" :loading="warehouseInLoading" :disabled="!warehouseInForm.change_reason || !warehouseInForm.new_sn" @click="submitWarehouseIn">确认入库</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="scrapDialog" title="报废申请" width="500px">
      <el-form label-width="100px">
        <el-form-item label="返厂单号">{{ currentReturn?.return_no }}</el-form-item>
        <el-form-item label="报废原因" required>
          <el-input v-model="scrapForm.scrap_reason" type="textarea" :rows="3" placeholder="请填写报废原因" />
        </el-form-item>
        <el-form-item label="变更原因" required>
          <el-input v-model="scrapForm.change_reason" placeholder="必填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="scrapDialog = false">取消</el-button>
        <el-button type="danger" :loading="scrapLoading" :disabled="!scrapForm.change_reason" @click="submitScrap">提交报废申请</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="reshipDialog" title="再出货" width="500px">
      <el-form label-width="100px">
        <el-form-item label="返厂单号">{{ currentReturn?.return_no }}</el-form-item>
        <el-form-item label="出货SN" required>
          <BarcodeScanner v-model="reshipForm.new_sn" placeholder="扫码或输入出货SN" />
        </el-form-item>
        <el-form-item label="软件版本号"><el-input v-model="reshipForm.software_version" placeholder="选填" /></el-form-item>
        <el-form-item label="出货日期" required>
          <el-date-picker v-model="reshipForm.ship_date" type="date" placeholder="选择日期" style="width:100%" />
        </el-form-item>
        <el-form-item label="收货人"><el-input v-model="reshipForm.recipient" placeholder="选填" /></el-form-item>
        <el-form-item label="变更原因" required>
          <el-input v-model="reshipForm.change_reason" placeholder="必填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reshipDialog = false">取消</el-button>
        <el-button type="primary" :loading="reshipLoading" :disabled="!reshipForm.change_reason" @click="submitReship">确认再出货</el-button>
    </template>
  </el-dialog>

  </div>

  <PrintPreview v-model:visible="printVisible" title="维修工单">
    <RmaRepairPrint v-if="printData" :data="printData" />
  </PrintPreview>
</template>

<style scoped>
.rma-page { padding: 0 4px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h2 { margin: 0; font-size: 18px; }
.search-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; align-items: center; }
</style>