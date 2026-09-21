<script setup>
import { onMounted, ref, reactive } from 'vue'
import { Edit, Delete, Search, Checked } from '@element-plus/icons-vue'
import PermissionButton from '@/components/PermissionButton.vue'
import { listDevices, createDevice, updateDevice, removeDevice, checkWarranty } from '@/api/deviceLedger'
import { listAllActiveStations } from '@/api/station'

const loading = ref(false)
const devices = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(15)

const keyword = ref('')
const statusFilter = ref('')
const stationFilter = ref(null)
const stations = ref([])

const statusOptions = [
  { label: '运行中', value: 'RUNNING' },
  { label: '故障', value: 'FAULT' },
  { label: '已回收', value: 'RECOVERED' },
]

function statusLabel(status) {
  const found = statusOptions.find((o) => o.value === status)
  return found ? found.label : status
}

function statusTagType(status) {
  if (status === 'RUNNING') return 'success'
  if (status === 'FAULT') return 'danger'
  return 'info'
}

const dialogVisible = ref(false)
const dialogTitle = ref('登记设备')
const formRef = ref()
const form = reactive({
  id: null,
  item_sn: '',
  station_id: null,
  installed_date: '',
  warranty_start: '',
  warranty_end: '',
  software_version: '',
  status: '',
  remark: '',
})

const formRules = {
  item_sn: [{ required: true, message: '设备SN不能为空', trigger: 'blur' }],
  station_id: [{ required: true, message: '请选择场站', trigger: 'change' }],
  installed_date: [{ required: true, message: '请选择安装日期', trigger: 'change' }],
}

const removeDialogVisible = ref(false)
const removeForm = reactive({ id: null, sn: '', removed_date: '' })

const warrantyVisible = ref(false)
const warrantySn = ref('')
const warrantyResult = ref(null)
const warrantyChecking = ref(false)

onMounted(() => {
  loadStations()
  loadDevices()
})

async function loadStations() {
  try {
    const res = await listAllActiveStations()
    stations.value = res.data || []
  } catch { /* noop */ }
}

async function loadDevices() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (keyword.value.trim()) params.keyword = keyword.value.trim()
    if (statusFilter.value) params.status = statusFilter.value
    if (stationFilter.value) params.station_id = stationFilter.value
    const res = await listDevices(params)
    devices.value = res.data.items || []
    total.value = res.data.total || 0
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  loadDevices()
}

function handleReset() {
  keyword.value = ''
  statusFilter.value = ''
  stationFilter.value = null
  page.value = 1
  loadDevices()
}

function handlePageChange(p) {
  page.value = p
  loadDevices()
}

function openDialog(row = null) {
  if (row) {
    dialogTitle.value = '编辑设备'
    Object.assign(form, {
      id: row.id,
      item_sn: row.item_sn,
      station_id: row.station_id,
      installed_date: row.installed_date,
      warranty_start: row.warranty_start || '',
      warranty_end: row.warranty_end || '',
      software_version: row.software_version || '',
      status: row.status,
      remark: row.remark || '',
    })
  } else {
    dialogTitle.value = '登记设备'
    Object.assign(form, {
      id: null,
      item_sn: '',
      station_id: stations.value[0]?.id || null,
      installed_date: new Date().toISOString().slice(0, 10),
      warranty_start: '',
      warranty_end: '',
      software_version: '',
      status: '',
      remark: '',
    })
  }
  dialogVisible.value = true
}

async function handleSave() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  const { id, ...data } = form
  if (id) {
    const payload = { ...data }
    if (!payload.status) delete payload.status
    await updateDevice(id, payload)
    ElMessage.success('更新成功')
  } else {
    await createDevice(data)
    ElMessage.success('登记成功')
  }
  dialogVisible.value = false
  loadDevices()
}

function openRemoveDialog(row) {
  removeForm.id = row.id
  removeForm.sn = row.item_sn
  removeForm.removed_date = new Date().toISOString().slice(0, 10)
  removeDialogVisible.value = true
}

async function handleRemove() {
  if (!removeForm.removed_date) {
    ElMessage.warning('请选择移除日期')
    return
  }
  await removeDevice(removeForm.id, { removed_date: removeForm.removed_date })
  ElMessage.success('设备已回收')
  removeDialogVisible.value = false
  loadDevices()
}

async function handleWarrantyCheck() {
  if (!warrantySn.value.trim()) {
    ElMessage.warning('请输入设备SN')
    return
  }
  warrantyChecking.value = true
  try {
    const res = await checkWarranty(warrantySn.value.trim())
    warrantyResult.value = res.data
    warrantyVisible.value = true
  } finally {
    warrantyChecking.value = false
  }
}

function formatDate(v) {
  if (!v) return '-'
  return v
}
</script>

<template>
  <el-card shadow="never">
    <el-form :inline="true" class="search-bar">
      <el-form-item label="设备SN">
        <el-input
          v-model="keyword"
          placeholder="搜索SN"
          clearable
          @keyup.enter="handleSearch"
          style="width: 160px"
        />
      </el-form-item>
      <el-form-item label="场站">
        <el-select v-model="stationFilter" placeholder="全部" clearable style="width: 150px">
          <el-option v-for="s in stations" :key="s.id" :label="s.name" :value="s.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="statusFilter" placeholder="全部" clearable style="width: 110px">
          <el-option v-for="opt in statusOptions" :key="opt.value" :label="opt.label" :value="opt.value" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <div class="toolbar">
      <PermissionButton permKey="device_ledger.create_edit" tip="仅仓库管理员可管理设备台账">
        <el-button type="primary" @click="openDialog()">登记设备</el-button>
      </PermissionButton>
      <el-input v-model="warrantySn" placeholder="输入SN查质保" style="width:200px;margin-left:12px" clearable />
      <el-button :icon="Checked" :loading="warrantyChecking" @click="handleWarrantyCheck">质保查询</el-button>
    </div>

    <el-table :data="devices" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="item_sn" label="设备SN" width="140" show-overflow-tooltip />
      <el-table-column label="场站" min-width="120" show-overflow-tooltip>
        <template #default="{ row }">{{ row.station_name || '-' }}</template>
      </el-table-column>
      <el-table-column label="安装日期" width="110">
        <template #default="{ row }">{{ formatDate(row.installed_date) }}</template>
      </el-table-column>
      <el-table-column label="移除日期" width="110">
        <template #default="{ row }">{{ formatDate(row.removed_date) }}</template>
      </el-table-column>
      <el-table-column label="质保起始" width="110">
        <template #default="{ row }">{{ formatDate(row.warranty_start) }}</template>
      </el-table-column>
      <el-table-column label="质保到期" width="110">
        <template #default="{ row }">{{ formatDate(row.warranty_end) }}</template>
      </el-table-column>
      <el-table-column prop="software_version" label="软件版本" width="110" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" min-width="140" show-overflow-tooltip />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <PermissionButton permKey="device_ledger.create_edit">
            <el-button type="primary" link :icon="Edit" @click="openDialog(row)">编辑</el-button>
          </PermissionButton>
          <PermissionButton permKey="device_ledger.create_edit">
            <el-button v-if="!row.removed_date" type="warning" link :icon="Delete" @click="openRemoveDialog(row)">回收</el-button>
          </PermissionButton>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0"
      class="list-pagination"
      background
      layout="total, prev, pager, next"
      :total="total"
      :page-size="pageSize"
      :current-page="page"
      @current-change="handlePageChange"
    />
  </el-card>

  <el-dialog v-model="dialogVisible" :title="dialogTitle" width="520px" destroy-on-close>
    <el-form ref="formRef" :model="form" :rules="formRules" label-width="90px">
      <el-form-item label="设备SN" prop="item_sn">
        <el-input v-model="form.item_sn" placeholder="请输入设备SN" maxlength="50" :disabled="!!form.id" />
      </el-form-item>
      <el-form-item label="场站" prop="station_id">
        <el-select v-model="form.station_id" placeholder="请选择场站" style="width:100%">
          <el-option v-for="s in stations" :key="s.id" :label="s.name" :value="s.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="安装日期" prop="installed_date">
        <el-date-picker v-model="form.installed_date" type="date" placeholder="请选择日期" style="width:100%" value-format="YYYY-MM-DD" />
      </el-form-item>
      <el-form-item label="质保起始">
        <el-date-picker v-model="form.warranty_start" type="date" placeholder="请选择日期" style="width:100%" value-format="YYYY-MM-DD" />
      </el-form-item>
      <el-form-item label="质保到期">
        <el-date-picker v-model="form.warranty_end" type="date" placeholder="请选择日期" style="width:100%" value-format="YYYY-MM-DD" />
      </el-form-item>
      <el-collapse>
        <el-collapse-item title="其他信息">
          <el-form-item label="软件版本">
            <el-input v-model="form.software_version" placeholder="请输入软件版本号" maxlength="50" />
          </el-form-item>
          <el-form-item v-if="form.id" label="状态">
            <el-select v-model="form.status" style="width:100%">
              <el-option v-for="opt in statusOptions" :key="opt.value" :label="opt.label" :value="opt.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="form.remark" placeholder="请输入备注" type="textarea" :rows="2" />
          </el-form-item>
        </el-collapse-item>
      </el-collapse>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSave">保存</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="removeDialogVisible" title="设备回收" width="400px">
    <p>确认将设备 <b>{{ removeForm.sn }}</b> 从场站回收？</p>
    <el-form-item label="移除日期">
      <el-date-picker v-model="removeForm.removed_date" type="date" placeholder="请选择日期" style="width:100%" value-format="YYYY-MM-DD" />
    </el-form-item>
    <template #footer>
      <el-button @click="removeDialogVisible = false">取消</el-button>
      <el-button type="warning" @click="handleRemove">确认回收</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="warrantyVisible" title="质保查询结果" width="420px">
    <template v-if="warrantyResult">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="设备SN">{{ warrantyResult.item_sn }}</el-descriptions-item>
        <el-descriptions-item label="质保状态">
          <el-tag :type="warrantyResult.in_warranty ? 'success' : 'danger'">
            {{ warrantyResult.in_warranty ? '质保期内' : '已过保' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="质保起始">{{ formatDate(warrantyResult.warranty_start) }}</el-descriptions-item>
        <el-descriptions-item label="质保到期">{{ formatDate(warrantyResult.warranty_end) }}</el-descriptions-item>
        <el-descriptions-item v-if="warrantyResult.in_warranty" label="剩余天数">
          {{ warrantyResult.days_remaining }} 天
        </el-descriptions-item>
        <el-descriptions-item label="运行状态">
          {{ statusLabel(warrantyResult.status) }}
        </el-descriptions-item>
      </el-descriptions>
    </template>
    <template #footer>
      <el-button @click="warrantyVisible = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.search-bar { margin-bottom: 4px; }
.toolbar { margin-bottom: 12px; display: flex; align-items: center; }
.list-pagination { margin-top: 16px; justify-content: flex-end; }
</style>