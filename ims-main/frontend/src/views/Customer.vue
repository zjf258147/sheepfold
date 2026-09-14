<script setup>
import { onMounted, ref, reactive } from 'vue'
import { Search, Edit } from '@element-plus/icons-vue'
import { listCustomers, createCustomer, updateCustomer } from '@/api/customer'

const loading = ref(false)
const customers = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(15)
const keyword = ref('')

onMounted(() => loadData())

async function loadData() {
  loading.value = true
  try {
    const p = { page: page.value, page_size: pageSize.value }
    if (keyword.value.trim()) p.keyword = keyword.value.trim()
    const res = await listCustomers(p)
    customers.value = res.data.items || []
    total.value = res.data.total || 0
  } finally { loading.value = false }
}

function handleSearch() { page.value = 1; loadData() }
function handleReset() { keyword.value = ''; page.value = 1; loadData() }
function handlePageChange(p) { page.value = p; loadData() }

const dialogVisible = ref(false)
const dialogTitle = ref('新增客户')
const formRef = ref()
const form = reactive({
  id: null,
  name: '',
  weight: 0,
  contact_person: '',
  contact_phone: '',
  contact_email: '',
  address: '',
  contract_no: '',
  contract_start: '',
  contract_end: '',
  remark: '',
})

const formRules = {
  name: [{ required: true, message: '客户名称不能为空', trigger: 'blur' }],
}

function openDialog(row = null) {
  if (row) {
    dialogTitle.value = '编辑客户'
    Object.assign(form, {
      id: row.id,
      name: row.name,
      weight: row.weight || 0,
      contact_person: row.contact_person || '',
      contact_phone: row.contact_phone || '',
      contact_email: row.contact_email || '',
      address: row.address || '',
      contract_no: row.contract_no || '',
      contract_start: row.contract_start || '',
      contract_end: row.contract_end || '',
      remark: row.remark || '',
    })
  } else {
    dialogTitle.value = '新增客户'
    Object.assign(form, {
      id: null,
      name: '',
      weight: 0,
      contact_person: '',
      contact_phone: '',
      contact_email: '',
      address: '',
      contract_no: '',
      contract_start: '',
      contract_end: '',
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
    await updateCustomer(id, data)
    ElMessage.success('更新成功')
  } else {
    await createCustomer(data)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadData()
}

function formatDate(v) {
  if (!v) return '-'
  return v
}
</script>

<template>
  <el-card shadow="never">
    <el-form :inline="true" class="search-bar">
      <el-form-item label="客户名称">
        <el-input
          v-model="keyword" placeholder="搜索客户名称" clearable
          @keyup.enter="handleSearch" style="width: 200px"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">新增客户</el-button>
    </div>

    <el-table :data="customers" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="客户名称" min-width="140" show-overflow-tooltip />
      <el-table-column prop="weight" label="权重" width="70" align="center" />
      <el-table-column prop="contact_person" label="联系人" width="90" />
      <el-table-column prop="contact_phone" label="联系电话" width="120" />
      <el-table-column prop="contact_email" label="邮箱" width="140" show-overflow-tooltip />
      <el-table-column label="合同编号" width="120" show-overflow-tooltip>
        <template #default="{ row }">{{ row.contract_no || '-' }}</template>
      </el-table-column>
      <el-table-column label="合同起始" width="110">
        <template #default="{ row }">{{ formatDate(row.contract_start) }}</template>
      </el-table-column>
      <el-table-column label="合同到期" width="110">
        <template #default="{ row }">{{ formatDate(row.contract_end) }}</template>
      </el-table-column>
      <el-table-column prop="address" label="地址" min-width="140" show-overflow-tooltip />
      <el-table-column prop="remark" label="备注" min-width="120" show-overflow-tooltip />
      <el-table-column label="操作" width="70" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link :icon="Edit" @click="openDialog(row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0" class="list-pagination" background
      layout="total, prev, pager, next" :total="total"
      :page-size="pageSize" :current-page="page" @current-change="handlePageChange"
    />
  </el-card>

  <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" destroy-on-close>
    <el-form ref="formRef" :model="form" :rules="formRules" label-width="90px">
      <el-form-item label="客户名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入客户名称" maxlength="200" />
      </el-form-item>
      <el-form-item label="权重">
        <el-input-number v-model="form.weight" :min="0" />
      </el-form-item>
      <el-row :gutter="12">
        <el-col :span="12">
          <el-form-item label="联系人">
            <el-input v-model="form.contact_person" placeholder="联系人" maxlength="50" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="联系电话">
            <el-input v-model="form.contact_phone" placeholder="联系电话" maxlength="20" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="邮箱">
        <el-input v-model="form.contact_email" placeholder="邮箱" maxlength="100" />
      </el-form-item>
      <el-form-item label="地址">
        <el-input v-model="form.address" placeholder="地址" type="textarea" :rows="2" />
      </el-form-item>
      <el-divider content-position="left">合同信息</el-divider>
      <el-form-item label="合同编号">
        <el-input v-model="form.contract_no" placeholder="合同编号" maxlength="50" />
      </el-form-item>
      <el-row :gutter="12">
        <el-col :span="12">
          <el-form-item label="合同起始">
            <el-date-picker v-model="form.contract_start" type="date" placeholder="选择日期" style="width:100%" value-format="YYYY-MM-DD" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="合同到期">
            <el-date-picker v-model="form.contract_end" type="date" placeholder="选择日期" style="width:100%" value-format="YYYY-MM-DD" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="备注">
        <el-input v-model="form.remark" placeholder="备注" type="textarea" :rows="2" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSave">保存</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.search-bar { margin-bottom: 4px; }
.toolbar { margin-bottom: 12px; }
.list-pagination { margin-top: 16px; justify-content: flex-end; }
</style>