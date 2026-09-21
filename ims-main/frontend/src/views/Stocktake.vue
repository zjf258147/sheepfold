<script setup>
import { onMounted, ref, reactive } from 'vue'
import { Search, Edit, Check, Close } from '@element-plus/icons-vue'
import PermissionButton from '@/components/PermissionButton.vue'
import {
  listStocktakes, getStocktakeLines, createStocktake,
  scanItems, updateLineReason, completeStocktake, cancelStocktake
} from '@/api/stocktake'
import { dateTimeColumnFormatter } from '@/utils/datetime'

const loading = ref(false)
const creating = ref(false)
const completing = ref(false)
const cancelling = ref(false)
const scanning = ref(false)
const savingReason = ref(false)
const tasks = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(15)
const statusFilter = ref('')

const statusOptions = [
  { label: '进行中', value: 'IN_PROGRESS' },
  { label: '已完成', value: 'COMPLETED' },
  { label: '已取消', value: 'CANCELLED' },
]

const modeOptions = [
  { label: '循环盘点', value: 'CYCLE' },
  { label: '全量盘点', value: 'FULL' },
]

function statusLabel(s) {
  return statusOptions.find(o => o.value === s)?.label || s
}

function statusTagType(s) {
  if (s === 'IN_PROGRESS') return 'warning'
  if (s === 'COMPLETED') return 'success'
  return 'info'
}

function modeLabel(m) {
  return modeOptions.find(o => o.value === m)?.label || m
}

const createVisible = ref(false)
const createForm = reactive({ mode: 'CYCLE', warehouse: '', remark: '' })
const createRef = ref()

const detailVisible = ref(false)
const detailTask = ref(null)
const detailLines = ref([])
const detailLoading = ref(false)

const scanVisible = ref(false)
const scanItem = reactive({ item_sn: '', actual_qty: 1 })
const scanLines = ref([])

const reasonVisible = ref(false)
const reasonForm = reactive({ line_id: null, diff_reason: '' })

onMounted(() => loadTasks())

async function loadTasks() {
  loading.value = true
  try {
    const p = { page: page.value, page_size: pageSize.value }
    if (statusFilter.value) p.status = statusFilter.value
    const res = await listStocktakes(p)
    tasks.value = res.data.items || []
    total.value = res.data.total || 0
  } finally { loading.value = false }
}

function handleSearch() { page.value = 1; loadTasks() }
function handleReset() { statusFilter.value = ''; page.value = 1; loadTasks() }
function handlePageChange(p) { page.value = p; loadTasks() }
function handleSizeChange(s) { pageSize.value = s; page.value = 1; loadTasks() }

function openCreate() {
  Object.assign(createForm, { mode: 'CYCLE', warehouse: '', remark: '' })
  createVisible.value = true
}

async function handleCreate() {
  const valid = await createRef.value?.validate().catch(() => false)
  if (!valid) return
  creating.value = true
  try {
    await createStocktake({ ...createForm })
    ElMessage.success('盘点任务已创建')
    createVisible.value = false
    loadTasks()
  } finally { creating.value = false }
}

async function openDetail(row) {
  detailTask.value = row
  detailLoading.value = true
  detailVisible.value = true
  try {
    const res = await getStocktakeLines(row.id)
    detailLines.value = res.data || []
  } finally { detailLoading.value = false }
}

function openScan() {
  Object.assign(scanItem, { item_sn: '', actual_qty: 1 })
  scanLines.value = []
  scanVisible.value = true
}

function addScanLine() {
  if (!scanItem.item_sn.trim()) {
    ElMessage.warning('请输入设备SN')
    return
  }
  scanLines.value.push({ item_sn: scanItem.item_sn.trim(), actual_qty: scanItem.actual_qty })
  scanItem.item_sn = ''
  scanItem.actual_qty = 1
}

function removeScanLine(idx) {
  scanLines.value.splice(idx, 1)
}

async function handleScan() {
  if (scanLines.value.length === 0) {
    ElMessage.warning('请添加盘点设备')
    return
  }
  scanning.value = true
  try {
    await scanItems(detailTask.value.id, { items: scanLines.value })
    ElMessage.success('扫码完成')
    scanVisible.value = false
    openDetail(detailTask.value)
  } finally { scanning.value = false }
}

function openReason(line) {
  reasonForm.line_id = line.id
  reasonForm.diff_reason = line.diff_reason || ''
  reasonVisible.value = true
}

async function handleReason() {
  savingReason.value = true
  try {
    await updateLineReason(reasonForm.line_id, { diff_reason: reasonForm.diff_reason })
    ElMessage.success('已更新')
    reasonVisible.value = false
    openDetail(detailTask.value)
  } finally { savingReason.value = false }
}

async function handleComplete(row) {
  try {
    const { value: remark } = await ElMessageBox.prompt('请输入完成备注（可选）', '完成盘点', {
      confirmButtonText: '确认', cancelButtonText: '取消'
    })
    completing.value = true
    try {
      await completeStocktake(row.id, { remark: remark || '' })
      ElMessage.success('盘点已完成')
      loadTasks()
    } finally { completing.value = false }
  } catch (e) {
    if (e !== 'cancel' && e !== 'close') throw e
  }
}

async function handleCancel(row) {
  try {
    await ElMessageBox.confirm(`确认取消盘点任务 ${row.stocktake_no}？`, '取消盘点', {
      confirmButtonText: '确认取消', cancelButtonText: '返回', type: 'warning'
    })
    cancelling.value = true
    try {
      await cancelStocktake(row.id)
      ElMessage.success('已取消')
      loadTasks()
    } finally { cancelling.value = false }
  } catch (e) {
    if (e !== 'cancel' && e !== 'close') throw e
  }
}
</script>

<template>
  <el-card shadow="never">
    <el-form :inline="true" class="search-bar">
      <el-form-item label="状态">
        <el-select v-model="statusFilter" placeholder="全部" clearable style="width:120px">
          <el-option v-for="o in statusOptions" :key="o.value" :label="o.label" :value="o.value" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <div class="toolbar">
      <PermissionButton permKey="stocktake.create" tip="仅仓库管理员可创建盘点">
        <el-button type="primary" @click="openCreate">创建盘点</el-button>
      </PermissionButton>
    </div>

    <el-table :data="tasks" v-loading="loading" stripe>
      <el-table-column prop="stocktake_no" label="盘点单号" width="150" />
      <el-table-column label="盘点方式" width="100">
        <template #default="{ row }">{{ modeLabel(row.mode) }}</template>
      </el-table-column>
      <el-table-column prop="warehouse" label="仓库" width="100" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_by_name" label="创建人" width="90" />
      <el-table-column prop="started_at" label="开始时间" width="160" :formatter="dateTimeColumnFormatter" />
      <el-table-column prop="completed_at" label="完成时间" width="160" :formatter="dateTimeColumnFormatter" />
      <el-table-column prop="remark" label="备注" min-width="120" show-overflow-tooltip />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button type="primary" link :icon="Search" @click="openDetail(row)">明細</el-button>
          <PermissionButton v-if="row.status === 'IN_PROGRESS'" permKey="stocktake.complete" tip="仅仓库管理员可完成盘点">
            <el-button
              type="success" link :icon="Check" :loading="completing" @click="handleComplete(row)"
            >完成</el-button>
          </PermissionButton>
          <PermissionButton v-if="row.status !== 'CANCELLED'" permKey="stocktake.cancel" tip="仅仓库管理员可取消盘点">
            <el-button
              type="danger" link :icon="Close" :loading="cancelling" @click="handleCancel(row)"
            >取消</el-button>
          </PermissionButton>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0" class="list-pagination" background
      layout="total, sizes, prev, pager, next, jumper"
      :page-sizes="[10, 15, 20, 50]"
      :total="total"
      :page-size="pageSize" :current-page="page"
      @size-change="handleSizeChange"
      @current-change="handlePageChange"
    />
  </el-card>

  <el-dialog v-model="createVisible" title="创建盘点任务" width="450px" destroy-on-close>
    <el-form ref="createRef" :model="createForm" label-width="80px">
      <el-form-item label="盘点方式" prop="mode" required>
        <el-radio-group v-model="createForm.mode">
          <el-radio v-for="o in modeOptions" :key="o.value" :value="o.value">{{ o.label }}</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="仓库范围" prop="warehouse" required :rules="[{ required: true, message: '请输入仓库' }]">
        <el-input v-model="createForm.warehouse" placeholder="如：主仓库" maxlength="30" />
      </el-form-item>
      <el-form-item label="备注" prop="remark">
        <el-input v-model="createForm.remark" placeholder="可选" maxlength="500" type="textarea" :rows="2" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="createVisible = false">取消</el-button>
      <el-button type="primary" :loading="creating" @click="handleCreate">创建</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="detailVisible" :title="detailTask?.stocktake_no + ' 盘点明细'" width="800px" destroy-on-close>
    <div class="toolbar" v-if="detailTask?.status === 'IN_PROGRESS'">
      <PermissionButton permKey="stocktake.scan" tip="仅仓库管理员可扫码盘点">
        <el-button type="primary" @click="openScan">扫码盘点</el-button>
      </PermissionButton>
      <span class="hint">差异数量 ≠ 0 的条目可填写差异原因</span>
    </div>
    <el-table :data="detailLines" v-loading="detailLoading" stripe max-height="400">
      <el-table-column prop="item_sn" label="设备SN" width="150" show-overflow-tooltip />
      <el-table-column prop="system_qty" label="系统数量" width="90" align="center" />
      <el-table-column prop="actual_qty" label="实盘数量" width="90" align="center" />
      <el-table-column label="差异" width="80" align="center">
        <template #default="{ row }">
          <span :style="{ color: row.diff_qty === 0 ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
            {{ row.diff_qty > 0 ? '+' : '' }}{{ row.diff_qty }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="diff_reason" label="差异原因" min-width="120" show-overflow-tooltip />
      <el-table-column prop="scanned_at" label="扫码时间" width="160" :formatter="dateTimeColumnFormatter" />
      <el-table-column v-if="detailTask?.status === 'IN_PROGRESS'" label="操作" width="80">
        <template #default="{ row }">
          <el-button v-if="row.diff_qty !== 0" type="primary" link :icon="Edit" @click="openReason(row)">原因</el-button>
        </template>
      </el-table-column>
    </el-table>
    <template #footer>
      <el-button @click="detailVisible = false">关闭</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="scanVisible" title="扫码盘点" width="520px" destroy-on-close>
    <el-form :inline="true">
      <el-form-item label="设备SN">
        <el-input v-model="scanItem.item_sn" placeholder="扫描或输入SN" style="width:180px" @keyup.enter="addScanLine" />
      </el-form-item>
      <el-form-item label="数量">
        <el-input-number v-model="scanItem.actual_qty" :min="0" style="width:100px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="addScanLine">添加</el-button>
      </el-form-item>
    </el-form>
    <el-table :data="scanLines" max-height="250" v-if="scanLines.length > 0">
      <el-table-column type="index" label="#" width="50" />
      <el-table-column prop="item_sn" label="设备SN" width="200" />
      <el-table-column prop="actual_qty" label="数量" width="80" align="center" />
      <el-table-column label="操作" width="70">
        <template #default="{ $index }">
          <el-button type="danger" link :icon="Close" @click="removeScanLine($index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <template #footer>
      <el-button @click="scanVisible = false">取消</el-button>
      <el-button type="primary" :loading="scanning" :disabled="scanLines.length === 0" @click="handleScan">提交盘点</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="reasonVisible" title="填写差异原因" width="400px">
    <el-input v-model="reasonForm.diff_reason" placeholder="说明差异原因" maxlength="255" type="textarea" :rows="3" />
    <template #footer>
      <el-button @click="reasonVisible = false">取消</el-button>
      <el-button type="primary" :loading="savingReason" @click="handleReason">保存</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.search-bar { margin-bottom: 4px; }
.toolbar { margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
.hint { color: #909399; font-size: 13px; }
.list-pagination { margin-top: 16px; justify-content: flex-end; }
</style>