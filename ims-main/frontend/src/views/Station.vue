<script setup>
import { onMounted, ref, reactive } from 'vue'
import { Edit, Delete, Search } from '@element-plus/icons-vue'
import PermissionButton from '@/components/PermissionButton.vue'
import { listStations, createStation, updateStation, deleteStation } from '@/api/station'
import { listCustomers } from '@/api/customer'

const loading = ref(false)
const stations = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(15)

const keyword = ref('')
const statusFilter = ref('')
const customers = ref([])

const dialogVisible = ref(false)
const dialogTitle = ref('新增场站')
const formRef = ref()
const form = reactive({
  id: null,
  name: '',
  customer_id: null,
  address: '',
  contact_person: '',
  contact_phone: '',
  status: 'ACTIVE',
  remark: '',
})

const formRules = {
  name: [{ required: true, message: '场站名称不能为空', trigger: 'blur' }],
  customer_id: [{ required: true, message: '请选择客户', trigger: 'change' }],
}

const statusOptions = [
  { label: '启用', value: 'ACTIVE' },
  { label: '停用', value: 'INACTIVE' },
]

function statusLabel(status) {
  const found = statusOptions.find((o) => o.value === status)
  return found ? found.label : status
}

function statusTagType(status) {
  return status === 'ACTIVE' ? 'success' : 'info'
}

onMounted(() => {
  loadCustomers()
  loadStations()
})

async function loadCustomers() {
  try {
    const res = await listCustomers({ page_size: 1000 })
    customers.value = res.data.items || []
  } catch { /* noop */ }
}

async function loadStations() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (keyword.value.trim()) params.keyword = keyword.value.trim()
    if (statusFilter.value) params.status = statusFilter.value
    const res = await listStations(params)
    stations.value = res.data.items || []
    total.value = res.data.total || 0
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  loadStations()
}

function handleReset() {
  keyword.value = ''
  statusFilter.value = ''
  page.value = 1
  loadStations()
}

function handlePageChange(p) {
  page.value = p
  loadStations()
}

function openDialog(row = null) {
  if (row) {
    dialogTitle.value = '编辑场站'
    Object.assign(form, {
      id: row.id,
      name: row.name,
      customer_id: row.customer_id,
      address: row.address || '',
      contact_person: row.contact_person || '',
      contact_phone: row.contact_phone || '',
      status: row.status,
      remark: row.remark || '',
    })
  } else {
    dialogTitle.value = '新增场站'
    Object.assign(form, {
      id: null,
      name: '',
      customer_id: customers.value[0]?.id || null,
      address: '',
      contact_person: '',
      contact_phone: '',
      status: 'ACTIVE',
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
    await updateStation(id, data)
    ElMessage.success('更新成功')
  } else {
    await createStation(data)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadStations()
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确认删除场站"${row.name}"？`, '提示', { type: 'warning' })
  await deleteStation(row.id)
  ElMessage.success('删除成功')
  loadStations()
}
</script>

<template>
  <el-card shadow="never">
    <el-form :inline="true" class="search-bar">
      <el-form-item label="关键词">
        <el-input
          v-model="keyword"
          placeholder="场站名称"
          clearable
          @keyup.enter="handleSearch"
          style="width: 200px"
        />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="statusFilter" placeholder="全部" clearable style="width: 120px">
          <el-option
            v-for="opt in statusOptions"
            :key="opt.value"
            :label="opt.label"
            :value="opt.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <div style="margin-bottom: 12px">
      <PermissionButton permKey="station.create_edit" tip="仅仓库管理员可管理场站">
        <el-button type="primary" @click="openDialog()">新增场站</el-button>
      </PermissionButton>
    </div>

    <el-table :data="stations" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="场站名称" min-width="150" show-overflow-tooltip />
      <el-table-column label="关联客户" min-width="120" show-overflow-tooltip>
        <template #default="{ row }">
          {{ row.customer_name || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="address" label="地址" min-width="180" show-overflow-tooltip />
      <el-table-column prop="contact_person" label="联系人" width="100" />
      <el-table-column prop="contact_phone" label="联系电话" width="130" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)" size="small">
            {{ statusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
      <el-table-column label="操作" width="140">
        <template #default="{ row }">
          <PermissionButton permKey="station.create_edit">
            <el-button type="primary" link :icon="Edit" @click="openDialog(row)">编辑</el-button>
          </PermissionButton>
          <PermissionButton permKey="station.create_edit">
            <el-button type="danger" link :icon="Delete" @click="handleDelete(row)">删除</el-button>
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
      <el-form-item label="场站名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入场站名称" maxlength="200" />
      </el-form-item>
      <el-form-item label="关联客户" prop="customer_id">
        <el-select v-model="form.customer_id" placeholder="请选择客户" style="width: 100%">
          <el-option
            v-for="c in customers"
            :key="c.id"
            :label="c.name"
            :value="c.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="地址">
        <el-input v-model="form.address" placeholder="请输入地址" type="textarea" :rows="2" />
      </el-form-item>
      <el-form-item label="联系人">
        <el-input v-model="form.contact_person" placeholder="请输入联系人" maxlength="50" />
      </el-form-item>
      <el-form-item label="联系电话">
        <el-input v-model="form.contact_phone" placeholder="请输入联系电话" maxlength="20" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="form.status" style="width: 100%">
          <el-option
            v-for="opt in statusOptions"
            :key="opt.value"
            :label="opt.label"
            :value="opt.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="form.remark" placeholder="请输入备注" type="textarea" :rows="2" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSave">保存</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.search-bar {
  margin-bottom: 4px;
}
.list-pagination {
  margin-top: 16px;
  justify-content: flex-end;
}
</style>