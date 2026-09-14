<script setup>
import { onMounted, ref } from 'vue'
import { listTasks, createTask, updateTask, deleteTask, exportTasks } from '@/api/bom'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Download } from '@element-plus/icons-vue'

const loading = ref(false)
const exportLoading = ref(false)
const tasks = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(15)
const query = ref({ keyword: '', status: '' })

const editDialog = ref(false)
const editForm = ref({ plan_quantity: 1, status: '', start_date: '', end_date: '', change_reason: '' })
const editId = ref(null)
const formLoading = ref(false)

const fetchData = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value, keyword: query.value.keyword || undefined, status: query.value.status || undefined }
    const res = await listTasks(params)
    tasks.value = res.data?.items || []
    total.value = res.data?.total || 0
  } finally { loading.value = false }
}

const handleSearch = () => { page.value = 1; fetchData() }
const handleReset = () => { query.value = { keyword: '', status: '' }; page.value = 1; fetchData() }

const handleExport = async () => {
  exportLoading.value = true
  try {
    const blob = await exportTasks(query.value)
    const d = new Date()
    const dateStr = `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `IMS-生产任务-${dateStr}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  } finally { exportLoading.value = false }
}
const handlePageChange = (p) => { page.value = p; fetchData() }
const handleSizeChange = (s) => { pageSize.value = s; page.value = 1; fetchData() }

const openEdit = (row) => {
  editId.value = row.id
  editForm.value = { plan_quantity: row.plan_quantity, status: row.status, start_date: row.start_date || '', end_date: row.end_date || '', change_reason: '' }
  editDialog.value = true
}

const handleEditSubmit = async () => {
  formLoading.value = true
  try {
    await updateTask(editId.value, editForm.value)
    ElMessage.success('更新成功')
    editDialog.value = false
    fetchData()
  } finally { formLoading.value = false }
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定删除任务 ${row.task_no}？`, '确认删除', { type: 'warning' })
    .then(async () => { await deleteTask(row.id); ElMessage.success('已删除'); fetchData() })
    .catch(() => {})
}

const statusMap = { PENDING: '待生产', IN_PROGRESS: '生产中', COMPLETED: '已完成' }
const availabilityMap = { COMPLETE: '齐套', SHORTAGE: '缺料', FULFILLED: '已齐套' }

onMounted(() => { fetchData() })
</script>

<template>
  <div class="task-page">
    <el-card class="search-card">
      <el-form :inline="true" :model="query" size="default">
        <el-form-item label="搜索">
          <el-input v-model="query.keyword" placeholder="任务编号" clearable style="width:200px" @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="query.status" placeholder="全部" clearable style="width:130px">
            <el-option label="待生产" value="PENDING" />
            <el-option label="生产中" value="IN_PROGRESS" />
            <el-option label="已完成" value="COMPLETED" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" :icon="Download" :loading="exportLoading" @click="handleExport">导出</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table :data="tasks" v-loading="loading" border stripe>
        <el-table-column prop="task_no" label="任务编号" width="150" />
        <el-table-column prop="bom_no" label="BOM编号" width="150" />
        <el-table-column prop="bom_name" label="BOM名称" min-width="160" show-overflow-tooltip />
        <el-table-column prop="plan_quantity" label="计划数量" width="90" />
        <el-table-column prop="material_availability" label="齐套状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.material_availability === 'COMPLETE' ? 'success' : row.material_availability === 'SHORTAGE' ? 'danger' : 'warning'" size="small">
              {{ availabilityMap[row.material_availability] || row.material_availability }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 'COMPLETED' ? 'success' : row.status === 'IN_PROGRESS' ? 'warning' : ''" size="small">
              {{ statusMap[row.status] || row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="110" />
        <el-table-column prop="end_date" label="完成日期" width="110" />
        <el-table-column prop="created_by" label="创建人" width="90" />
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="openEdit(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="page" v-model:page-size="pageSize" :total="total"
        :page-sizes="[15, 30, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 16px; justify-content: flex-end"
        @current-change="handlePageChange" @size-change="handleSizeChange"
      />
    </el-card>

    <el-dialog v-model="editDialog" title="编辑生产任务" width="500px" :close-on-click-modal="false">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="计划数量"><el-input-number v-model="editForm.plan_quantity" :min="1" style="width:100%" /></el-form-item>
        <el-form-item label="状态">
          <el-select v-model="editForm.status" style="width:100%">
            <el-option label="待生产" value="PENDING" />
            <el-option label="生产中" value="IN_PROGRESS" />
            <el-option label="已完成" value="COMPLETED" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期"><el-date-picker v-model="editForm.start_date" type="date" value-format="YYYY-MM-DD" style="width:100%" /></el-form-item>
        <el-form-item label="完成日期"><el-date-picker v-model="editForm.end_date" type="date" value-format="YYYY-MM-DD" style="width:100%" /></el-form-item>
        <el-form-item label="变更原因"><el-input v-model="editForm.change_reason" placeholder="变更原因" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialog = false">取消</el-button>
        <el-button type="primary" :loading="formLoading" @click="handleEditSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.task-page { padding: 16px; }
.search-card { margin-bottom: 16px; }
</style>