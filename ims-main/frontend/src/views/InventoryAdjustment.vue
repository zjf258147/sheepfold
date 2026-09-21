<script setup>
import { onMounted, ref, reactive } from 'vue'
import { Search, Check } from '@element-plus/icons-vue'
import PermissionButton from '@/components/PermissionButton.vue'
import { listAdjustments, createAdjustment, confirmAdjustments } from '@/api/adjustment'
import { listStocktakes, getStocktakeLines } from '@/api/stocktake'

const loading = ref(false)
const items = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(15)

const typeFilter = ref('')
const stocktakeIdFilter = ref('')

const typeOptions = [
  { label: '盘盈', value: 'SURPLUS' },
  { label: '盘亏', value: 'SHORTAGE' },
]

function typeLabel(t) { return typeOptions.find(o => o.value === t)?.label || t }
function typeTagType(t) { return t === 'SURPLUS' ? 'success' : 'danger' }

onMounted(() => loadList())

async function loadList() {
  loading.value = true
  try {
    const p = { page: page.value, page_size: pageSize.value }
    if (typeFilter.value) p.adjustment_type = typeFilter.value
    if (stocktakeIdFilter.value) p.stocktake_id = stocktakeIdFilter.value
    const res = await listAdjustments(p)
    items.value = res.data.items || []
    total.value = res.data.total || 0
  } finally { loading.value = false }
}

function handleSearch() { page.value = 1; loadList() }
function handleReset() { typeFilter.value = ''; stocktakeIdFilter.value = ''; page.value = 1; loadList() }
function handlePageChange(p) { page.value = p; loadList() }

const createVisible = ref(false)
const createStep = ref(0)
const createRef = ref()
const stocktakes = ref([])
const stocktakeLines = ref([])
const loadingLines = ref(false)
const createForm = reactive({
  stocktake_id: null,
  stocktake_line_id: null,
  adjustment_type: 'SHORTAGE',
  reason: '',
})

async function openCreate() {
  createStep.value = 0
  Object.assign(createForm, { stocktake_id: null, stocktake_line_id: null, adjustment_type: 'SHORTAGE', reason: '' })
  stocktakeLines.value = []
  try {
    const res = await listStocktakes({ page: 1, page_size: 100, status: 'COMPLETED' })
    stocktakes.value = res.data.items || []
  } catch { /* noop */ }
  createVisible.value = true
}

async function onStocktakeChange(id) {
  createForm.stocktake_line_id = null
  stocktakeLines.value = []
  if (!id) return
  loadingLines.value = true
  try {
    const res = await getStocktakeLines(id)
    stocktakeLines.value = (res.data || []).filter(l => l.diff_qty !== 0)
    createStep.value = stocktakeLines.value.length > 0 ? 1 : 0
  } finally { loadingLines.value = false }
}

function onLineSelect(line) {
  createForm.stocktake_line_id = line.id
  createStep.value = 2
}

async function handleCreate() {
  if (!createForm.stocktake_id || !createForm.stocktake_line_id) {
    ElMessage.warning('请选择盘点任务和明细行')
    return
  }
  if (!createForm.reason.trim()) {
    ElMessage.warning('请填写调整原因')
    return
  }
  await createAdjustment({
    stocktake_id: createForm.stocktake_id,
    stocktake_line_id: createForm.stocktake_line_id,
    adjustment_type: createForm.adjustment_type,
    reason: createForm.reason,
  })
  ElMessage.success('调整记录已创建')
  createVisible.value = false
  loadList()
}

function handleConfirm(ids) {
  ElMessageBox.confirm(`确认执行选中的库存调整？此操作将实际修改库存状态。`, '确认调整', {
    confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning'
  }).then(async () => {
    await confirmAdjustments({ adjustment_ids: ids })
    ElMessage.success('库存调整已确认')
    loadList()
  }).catch(() => {})
}

function formatDate(v) {
  if (!v) return '-'
  return v
}
</script>

<template>
  <el-card shadow="never">
    <el-form :inline="true" class="search-bar">
      <el-form-item label="盘点任务ID">
        <el-input v-model="stocktakeIdFilter" placeholder="按任务筛选" clearable style="width:130px" @keyup.enter="handleSearch" />
      </el-form-item>
      <el-form-item label="类型">
        <el-select v-model="typeFilter" placeholder="全部" clearable style="width:110px">
          <el-option v-for="o in typeOptions" :key="o.value" :label="o.label" :value="o.value" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <div class="toolbar">
      <PermissionButton permKey="adjustment.confirm" tip="仅仓库管理员可创建调整">
        <el-button type="primary" @click="openCreate">创建调整</el-button>
      </PermissionButton>
    </div>

    <el-table :data="items" v-loading="loading" stripe @selection-change="v => selected = v">
      <el-table-column prop="adjustment_no" label="调整单号" width="150" />
      <el-table-column prop="stocktake_no" label="盘点单号" width="150" />
      <el-table-column prop="item_sn" label="设备SN" width="140" show-overflow-tooltip />
      <el-table-column label="类型" width="80">
        <template #default="{ row }">
          <el-tag :type="typeTagType(row.adjustment_type)" size="small">{{ typeLabel(row.adjustment_type) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="before_status" label="调整前状态" width="100" />
      <el-table-column prop="after_status" label="调整后状态" width="100" />
      <el-table-column prop="reason" label="原因" min-width="140" show-overflow-tooltip />
      <el-table-column prop="operator_name" label="操作人" width="90" />
      <el-table-column label="创建时间" width="160">
        <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0" class="list-pagination" background
      layout="total, prev, pager, next" :total="total"
      :page-size="pageSize" :current-page="page" @current-change="handlePageChange"
    />
  </el-card>

  <el-dialog v-model="createVisible" title="创建库存调整" width="600px" destroy-on-close>
    <el-steps :active="createStep" simple class="create-steps">
      <el-step title="选盘点任务" />
      <el-step title="选差异行" />
      <el-step title="填调整信息" />
    </el-steps>

    <div v-show="createStep === 0" class="step-content">
      <el-form label-width="90px">
        <el-form-item label="盘点任务" required>
          <el-select v-model="createForm.stocktake_id" placeholder="请选择已完成的盘点" style="width:100%" @change="onStocktakeChange">
            <el-option v-for="s in stocktakes" :key="s.id" :label="s.stocktake_no + ' - ' + s.warehouse" :value="s.id" />
          </el-select>
        </el-form-item>
      </el-form>
    </div>

    <div v-show="createStep === 1" class="step-content">
      <el-table :data="stocktakeLines" v-loading="loadingLines" max-height="250" highlight-current-row @row-click="onLineSelect">
        <el-table-column prop="item_sn" label="设备SN" width="150" />
        <el-table-column prop="system_qty" label="系统数量" width="80" align="center" />
        <el-table-column prop="actual_qty" label="实盘数量" width="80" align="center" />
        <el-table-column label="差异" width="80" align="center">
          <template #default="{ row }">
            <span :style="{ color: row.diff_qty > 0 ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
              {{ row.diff_qty > 0 ? '+' : '' }}{{ row.diff_qty }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="diff_reason" label="差异原因" min-width="120" show-overflow-tooltip />
      </el-table>
      <div v-if="stocktakeLines.length === 0 && !loadingLines" class="empty-hint">该盘点任务无差异行</div>
    </div>

    <div v-show="createStep === 2" class="step-content">
      <el-form ref="createRef" :model="createForm" label-width="90px">
        <el-form-item label="盘点单">
          <el-input :value="stocktakes.find(s=>s.id===createForm.stocktake_id)?.stocktake_no" disabled />
        </el-form-item>
        <el-form-item label="设备SN">
          <el-input :value="stocktakeLines.find(l=>l.id===createForm.stocktake_line_id)?.item_sn" disabled />
        </el-form-item>
        <el-form-item label="调整类型" required>
          <el-radio-group v-model="createForm.adjustment_type">
            <el-radio v-for="o in typeOptions" :key="o.value" :value="o.value">{{ o.label }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="原因" required>
          <el-input v-model="createForm.reason" placeholder="请输入调整原因" maxlength="500" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
    </div>

    <template #footer>
      <el-button @click="createVisible = false">取消</el-button>
      <el-button v-if="createStep > 0" @click="createStep--">上一步</el-button>
      <el-button v-if="createStep < 2 && createStep === 1 && createForm.stocktake_line_id" type="primary" @click="createStep = 2">下一步</el-button>
      <el-button v-if="createStep === 2" type="primary" @click="handleCreate">创建</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.search-bar { margin-bottom: 4px; }
.toolbar { margin-bottom: 12px; }
.list-pagination { margin-top: 16px; justify-content: flex-end; }
.create-steps { margin-bottom: 20px; }
.step-content { min-height: 120px; }
.empty-hint { text-align: center; color: #909399; padding: 40px 0; }
</style>