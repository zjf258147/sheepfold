<script setup>
import { onMounted, ref } from 'vue'
import { listRmaReturns, createRmaReturn, createRmaDiagnosis, createRmaRepair, createRmaScrap, approveRmaScrap, assignRmaReturn, createRmaReship } from '@/api/rma'
import { listSkus, listCategories } from '@/api/product'
import { listPartners } from '@/api/partner'
import { RMA_STATUS_MAP, RMA_STATUS_TAG, DIAGNOSIS_RESULT_MAP, SCRAP_STATUS_MAP } from '@/constants/enums'
import { dateTimeColumnFormatter } from '@/utils/datetime'
import { ElMessage } from 'element-plus'

const loading = ref(false)
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
const assignForm = ref({ assigned_to: null, change_reason: '' })
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
  repair_date: '',
  change_reason: '',
})
const repairLoading = ref(false)

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
  assignForm.value = { assigned_to: null, change_reason: '' }
  assignDialog.value = true
}

async function submitAssign() {
  if (!assignForm.value.assigned_to || !assignForm.value.change_reason) {
    ElMessage.warning('请选择分配人和填写变更原因')
    return
  }
  assignLoading.value = true
  try {
    await assignRmaReturn(currentReturn.value.id, assignForm.value)
    ElMessage.success('分配成功')
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
    new_sn: row.sn,
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
    <div class="page-header">
      <h2>返厂维修管理</h2>
      <el-button type="primary" @click="openCreate">退货登记</el-button>
    </div>

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
    </div>

    <el-table :data="returns" v-loading="loading" stripe border style="width:100%">
      <el-table-column prop="return_no" label="返厂单号" width="150" />
      <el-table-column prop="sn" label="设备SN" width="150" />
      <el-table-column prop="sku_name" label="物料名称" width="180" show-overflow-tooltip />
      <el-table-column prop="customer_name" label="客户" width="120" />
      <el-table-column prop="return_reason" label="退货原因" width="160" show-overflow-tooltip />
      <el-table-column label="状态" width="110" align="center">
        <template #default="{ row }">
          <el-tag :type="RMA_STATUS_TAG[row.status] || 'info'">{{ RMA_STATUS_MAP[row.status] || row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="assignee_name" label="负责人" width="100" />
      <el-table-column prop="return_date" label="退货日期" width="110" />
      <el-table-column label="操作" width="400" fixed="right" align="center">
        <template #default="{ row }">
          <el-button v-if="row.status === 'PENDING_DIAGNOSIS'" type="primary" link size="small" @click="openDiagnosis(row)">诊断</el-button>
          <el-button v-if="row.status === 'DIAGNOSED' || row.status === 'REPAIRED'" type="warning" link size="small" @click="openAssign(row)">分配</el-button>
          <el-button v-if="row.status === 'ASSIGNED' || row.status === 'REPAIRING'" type="primary" link size="small" @click="openRepair(row)">维修</el-button>
          <el-button v-if="row.status === 'REPAIRED'" type="danger" link size="small" @click="openScrap(row)">报废</el-button>
          <el-button v-if="row.status === 'REPAIRED'" type="success" link size="small" @click="openReship(row)">再出货</el-button>
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
          <el-input v-model="createForm.sn" placeholder="请输入设备SN" />
        </el-form-item>
        <el-form-item label="数量"><el-input-number v-model="createForm.quantity" :min="1" /></el-form-item>
        <el-form-item label="客户名称"><el-input v-model="createForm.customer_name" placeholder="选填" /></el-form-item>
        <el-form-item label="退货原因" required>
          <el-input v-model="createForm.return_reason" placeholder="请填写退货原因" />
        </el-form-item>
        <el-form-item label="退货日期" required>
          <el-date-picker v-model="createForm.return_date" type="date" placeholder="选择日期" style="width:100%" />
        </el-form-item>
        <el-form-item label="备注"><el-input v-model="createForm.remark" type="textarea" :rows="2" placeholder="选填" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialog = false">取消</el-button>
        <el-button type="primary" :loading="createLoading" @click="submitCreate">提交</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="diagnosisDialog" title="诊断报告" width="550px">
      <el-form label-width="100px">
        <el-form-item label="返厂单号">{{ currentReturn?.return_no }}</el-form-item>
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

    <el-dialog v-model="assignDialog" title="分配任务" width="450px">
      <el-form label-width="100px">
        <el-form-item label="返厂单号">{{ currentReturn?.return_no }}</el-form-item>
        <el-form-item label="分配给" required>
          <el-input-number v-model="assignForm.assigned_to" :min="1" placeholder="用户ID" style="width:100%" />
        </el-form-item>
        <el-form-item label="变更原因" required>
          <el-input v-model="assignForm.change_reason" placeholder="必填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="assignDialog = false">取消</el-button>
        <el-button type="primary" :loading="assignLoading" :disabled="!assignForm.change_reason" @click="submitAssign">确认分配</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="repairDialog" title="维修工单" width="550px">
      <el-form label-width="100px">
        <el-form-item label="返厂单号">{{ currentReturn?.return_no }}</el-form-item>
        <el-form-item label="原SN"><el-input v-model="repairForm.old_sn" disabled /></el-form-item>
        <el-form-item label="新SN"><el-input v-model="repairForm.new_sn" placeholder="换码时填写，留空则不变" /></el-form-item>
        <el-form-item label="维修人" required>
          <el-input-number v-model="repairForm.repair_by" :min="1" placeholder="维修人ID" style="width:100%" />
        </el-form-item>
        <el-form-item label="故障码"><el-input v-model="repairForm.fault_code" placeholder="选填" /></el-form-item>
        <el-form-item label="维修描述" required>
          <el-input v-model="repairForm.repair_description" type="textarea" :rows="3" placeholder="描述维修过程" />
        </el-form-item>
        <el-form-item label="维修用料"><el-input v-model="repairForm.materials_used" type="textarea" :rows="2" placeholder="填写用料清单" /></el-form-item>
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
          <el-input v-model="reshipForm.new_sn" placeholder="请输入出货SN" />
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
</template>

<style scoped>
.rma-page { padding: 0 4px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-header h2 { margin: 0; font-size: 18px; }
.search-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; align-items: center; }
</style>