<script setup>
import { onMounted, ref, watch } from 'vue'
import { listBoms, createBom, updateBom, deleteBom, checkAvailability, listTasks, createTask, updateTask, deleteTask, exportBoms } from '@/api/bom'
import { listSkus, listCategories } from '@/api/product'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getBomPrintData, getBomBatchPrintData } from '@/api/print'
import PrintPreview from '@/print/components/PrintPreview.vue'
import BomPrint from '@/print/components/BomPrint.vue'

const loading = ref(false)
const boms = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(15)
const query = ref({ keyword: '', status: '' })

const categories = ref([])
const rawMaterials = ref([])

const createDialog = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = ref({
  bom_name: '', version: '', product_sku_id: null,
  product_sku_code: '', product_sku_name: '', plan_quantity: 1,
  status: 'DRAFT', remark: '', change_reason: '',
})
const formDetails = ref([])
const formLoading = ref(false)

const formSkuCategory = ref(null)
const dialogSkus = ref([])

const detailDialog = ref(false)
const detailBom = ref(null)
const detailLoading = ref(false)

const availabilityDialog = ref(false)
const availabilityData = ref(null)
const availabilityLoading = ref(false)

const printVisible = ref(false)
const printData = ref(null)
const printLoading = ref(false)
const batchPrintLoading = ref(false)
const printBoms = ref([])
const selectedBoms = ref([])

async function handlePrint(row) {
  printLoading.value = true
  try {
    const res = await getBomPrintData(row.id)
    printData.value = res.data
    printBoms.value = []
    printVisible.value = true
  } catch {
    ElMessage.error('获取BOM打印数据失败')
  } finally {
    printLoading.value = false
  }
}

async function handleBatchPrint() {
  if (selectedBoms.value.length === 0) {
    ElMessage.warning('请先选择要打印的BOM')
    return
  }
  batchPrintLoading.value = true
  try {
    const ids = selectedBoms.value.map(r => r.id)
    const results = await getBomBatchPrintData(ids)
    printBoms.value = results.map(r => r.data)
    printData.value = null
    printVisible.value = true
  } catch {
    ElMessage.error('批量获取BOM打印数据失败')
  } finally {
    batchPrintLoading.value = false
  }
}

function handleSelectionChange(rows) {
  selectedBoms.value = rows
}

const taskDialog = ref(false)
const taskForm = ref({ bom_id: null, plan_quantity: 1, start_date: '', end_date: '', change_reason: '' })
const taskLoading = ref(false)
const selectedBomForTask = ref(null)

const exportLoading = ref(false)

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value, page_size: pageSize.value,
      keyword: query.value.keyword || undefined,
      status: query.value.status || undefined,
    }
    const res = await listBoms(params)
    boms.value = res.data?.items || []
    total.value = res.data?.total || 0
  } finally { loading.value = false }
}

const fetchCategories = async () => {
  try {
    const res = await listCategories()
    categories.value = res.data || []
    const rmRes = await listSkus({ sku_type: 'RAW_MATERIAL', page_size: 1000 })
    rawMaterials.value = rmRes.data?.items || []
  } catch {}
}

watch(() => query.value.category_id, async (val) => {
  query.value.sku_id = null
})

const handleSearch = () => { page.value = 1; fetchData() }
const handleReset = () => { query.value = { keyword: '', status: '' }; page.value = 1; fetchData() }
const handlePageChange = (p) => { page.value = p; fetchData() }
const handleSizeChange = (s) => { pageSize.value = s; page.value = 1; fetchData() }

const onSkuCategoryChange = async (val) => {
  form.value.product_sku_id = null
  dialogSkus.value = []
  if (val) {
    try {
      const res = await listSkus({ category_id: val, sku_type: 'FINISHED_GOODS' })
      dialogSkus.value = res.data || []
    } catch {}
  }
}

const handleSkuChange = (val) => {
  const sku = dialogSkus.value.find(s => s.id === val)
  if (sku) {
    form.value.product_sku_code = sku.sku_code || ''
    form.value.product_sku_name = sku.name || ''
  }
}

const addDetailRow = () => {
  formDetails.value.push({
    material_sku_id: null, material_sku_code: '', material_sku_name: '',
    spec: '', unit: '个', quantity_per_unit: 1, wastage_rate: null, remark: '',
  })
}

const removeDetailRow = (index) => {
  formDetails.value.splice(index, 1)
}

const onDetailMaterialChange = (index, val) => {
  const mat = rawMaterials.value.find(m => m.id === val)
  if (mat) {
    formDetails.value[index].material_sku_code = mat.sku_code || ''
    formDetails.value[index].material_sku_name = mat.name || ''
    formDetails.value[index].spec = mat.spec || ''
    formDetails.value[index].unit = mat.unit || '个'
  }
}

const openCreate = () => {
  isEdit.value = false; editId.value = null
  form.value = {
    bom_name: '', version: '', product_sku_id: null,
    product_sku_code: '', product_sku_name: '', plan_quantity: 1,
    status: 'DRAFT', remark: '', change_reason: '',
  }
  formDetails.value = []
  formSkuCategory.value = null
  dialogSkus.value = []
  createDialog.value = true
}

const openEdit = async (row) => {
  isEdit.value = true; editId.value = row.id
  detailLoading.value = true
  try {
    const res = await import('@/api/bom').then(m => m.getBom(row.id))
    const data = res.data
    form.value = {
      bom_name: data.bom_name, version: data.version,
      product_sku_id: data.product_sku_id, product_sku_code: data.product_sku_code,
      product_sku_name: data.product_sku_name, plan_quantity: data.plan_quantity,
      status: data.status, remark: data.remark || '', change_reason: '',
    }
    formDetails.value = (data.details || []).map(d => ({
      material_sku_id: d.material_sku_id,
      material_sku_code: d.material_sku_code,
      material_sku_name: d.material_sku_name,
      spec: d.spec || '', unit: d.unit,
      quantity_per_unit: d.quantity_per_unit,
      wastage_rate: d.wastage_rate,
      remark: d.remark || '',
    }))
    createDialog.value = true
  } finally { detailLoading.value = false }
}

const handleSubmit = async () => {
  if (!form.value.bom_name) { ElMessage.warning('请输入BOM名称'); return }
  if (!form.value.product_sku_id) { ElMessage.warning('请选择成品物料'); return }
  if (formDetails.value.length === 0) { ElMessage.warning('请添加至少一条BOM明细'); return }
  for (let i = 0; i < formDetails.value.length; i++) {
    const d = formDetails.value[i]
    if (!d.material_sku_id) { ElMessage.warning(`第${i + 1}行请选择原材料物料`); return }
    if (!d.quantity_per_unit || d.quantity_per_unit <= 0) { ElMessage.warning(`第${i + 1}行单台用量必须大于0`); return }
  }

  formLoading.value = true
  try {
    const data = { ...form.value, details: formDetails.value }
    if (isEdit.value) {
      await updateBom(editId.value, data)
      ElMessage.success('更新成功')
    } else {
      await createBom(data)
      ElMessage.success('创建成功')
    }
    createDialog.value = false
    fetchData()
  } finally { formLoading.value = false }
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定删除BOM ${row.bom_no}？`, '确认删除', { type: 'warning' })
    .then(async () => { await deleteBom(row.id); ElMessage.success('已删除'); fetchData() })
    .catch(() => {})
}

const openDetail = async (row) => {
  detailLoading.value = true
  detailDialog.value = true
  try {
    const res = await import('@/api/bom').then(m => m.getBom(row.id))
    detailBom.value = res.data
  } finally { detailLoading.value = false }
}

const openAvailability = async (row) => {
  availabilityLoading.value = true
  availabilityDialog.value = true
  try {
    const res = await checkAvailability(row.id)
    availabilityData.value = res.data
  } finally { availabilityLoading.value = false }
}

const openTaskCreate = (row) => {
  selectedBomForTask.value = row
  taskForm.value = { bom_id: row.id, plan_quantity: row.plan_quantity, start_date: '', end_date: '', change_reason: '' }
  taskDialog.value = true
}

const handleTaskSubmit = async () => {
  if (!taskForm.value.plan_quantity || taskForm.value.plan_quantity <= 0) {
    ElMessage.warning('请输入计划生产数量'); return
  }
  taskLoading.value = true
  try {
    await createTask(taskForm.value)
    ElMessage.success('生产任务创建成功')
    taskDialog.value = false
  } finally { taskLoading.value = false }
}

const handleExport = async () => {
  exportLoading.value = true
  try {
    const blob = await exportBoms({ keyword: query.value.keyword || undefined, status: query.value.status || undefined })
    const d = new Date()
    const dateStr = `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `IMS-BOM清单-${dateStr}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  } finally { exportLoading.value = false }
}

const statusMap = { DRAFT: '草稿', PUBLISHED: '已发布', DISCONTINUED: '已停产' }
const availabilityMap = { COMPLETE: '齐套', SHORTAGE: '缺料', FULFILLED: '已齐套' }

onMounted(() => { fetchCategories(); fetchData() })
</script>

<template>
  <div class="bom-page">
    <el-card class="search-card">
      <el-form :inline="true" :model="query" size="default">
        <el-form-item label="搜索">
          <el-input v-model="query.keyword" placeholder="BOM编号/名称/成品" clearable style="width:220px" @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="query.status" placeholder="全部" clearable style="width:130px">
            <el-option label="草稿" value="DRAFT" />
            <el-option label="已发布" value="PUBLISHED" />
            <el-option label="已停产" value="DISCONTINUED" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <div class="toolbar">
        <el-button type="primary" @click="openCreate">创建BOM</el-button>
        <el-button :loading="exportLoading" @click="handleExport">导出Excel</el-button>
        <el-button type="warning" :loading="batchPrintLoading" :disabled="selectedBoms.length === 0" @click="handleBatchPrint">
          批量打印 {{ selectedBoms.length > 0 ? `(${selectedBoms.length})` : '' }}
        </el-button>
      </div>

      <el-table :data="boms" v-loading="loading" border stripe @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="50" />
        <el-table-column prop="bom_no" label="BOM编号" width="150" />
        <el-table-column prop="bom_name" label="BOM名称" min-width="160" show-overflow-tooltip />
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="product_sku_code" label="成品编码" width="120" />
        <el-table-column prop="product_sku_name" label="成品名称" min-width="140" show-overflow-tooltip />
        <el-table-column prop="plan_quantity" label="计划数量" width="90" />
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 'PUBLISHED' ? 'success' : row.status === 'DISCONTINUED' ? 'info' : ''" size="small">
              {{ statusMap[row.status] || row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_by" label="创建人" width="90" />
        <el-table-column label="操作" width="340">
            <template #default="{ row }">
              <el-button type="primary" link size="small" @click="handlePrint(row)" :loading="printLoading">打印</el-button>
              <el-button type="primary" link size="small" @click="openEdit(row)">编辑</el-button>
            <el-button type="success" link size="small" @click="openDetail(row)">明细</el-button>
            <el-button type="warning" link size="small" @click="openAvailability(row)">齐套</el-button>
            <el-button type="info" link size="small" @click="openTaskCreate(row)">任务</el-button>
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

    <el-dialog v-model="createDialog" :title="isEdit ? '编辑BOM' : '创建BOM'" width="900px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="BOM名称" required><el-input v-model="form.bom_name" placeholder="BOM名称" /></el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="版本" required><el-input v-model="form.version" placeholder="如 V1.0" /></el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="状态"><el-select v-model="form.status" style="width:100%"><el-option label="草稿" value="DRAFT" /><el-option label="已发布" value="PUBLISHED" /><el-option label="已停产" value="DISCONTINUED" /></el-select></el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="物料分类"><el-select v-model="formSkuCategory" placeholder="选择分类" clearable style="width:100%" @change="onSkuCategoryChange"><el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" /></el-select></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="成品物料" required><el-select v-model="form.product_sku_id" placeholder="选择成品物料" filterable style="width:100%" @change="handleSkuChange"><el-option v-for="s in dialogSkus" :key="s.id" :label="`${s.sku_code || ''} ${s.name}`" :value="s.id" /></el-select></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="计划数量" required><el-input-number v-model="form.plan_quantity" :min="1" style="width:100%" /></el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="成品编码"><el-input v-model="form.product_sku_code" disabled /></el-form-item>
        <el-form-item label="成品名称"><el-input v-model="form.product_sku_name" disabled /></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" placeholder="备注" /></el-form-item>
        <el-form-item label="变更原因"><el-input v-model="form.change_reason" placeholder="变更原因" /></el-form-item>

        <el-divider content-position="left">BOM明细</el-divider>
        <div style="margin-bottom: 8px">
          <el-button type="success" size="small" @click="addDetailRow">+ 添加物料</el-button>
        </div>
        <el-table :data="formDetails" border size="small">
          <el-table-column label="原材料物料" width="200">
            <template #default="{ row: r, $index }">
              <el-select v-model="r.material_sku_id" placeholder="选择原材料" filterable size="small" style="width:100%" @change="(v) => onDetailMaterialChange($index, v)">
                <el-option v-for="m in rawMaterials" :key="m.id" :label="`${m.sku_code || ''} ${m.name}`" :value="m.id" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="编码" width="110">
            <template #default="{ row: r }"><el-input v-model="r.material_sku_code" size="small" disabled /></template>
          </el-table-column>
          <el-table-column label="规格" width="100">
            <template #default="{ row: r }"><el-input v-model="r.spec" size="small" disabled /></template>
          </el-table-column>
          <el-table-column label="单位" width="70">
            <template #default="{ row: r }"><el-input v-model="r.unit" size="small" disabled /></template>
          </el-table-column>
          <el-table-column label="单台用量" width="120">
            <template #default="{ row: r }"><el-input-number v-model="r.quantity_per_unit" :min="0.001" :precision="3" size="small" style="width:100%" /></template>
          </el-table-column>
          <el-table-column label="损耗率(%)" width="110">
            <template #default="{ row: r }"><el-input-number v-model="r.wastage_rate" :min="0" :max="100" :precision="2" size="small" style="width:100%" /></template>
          </el-table-column>
          <el-table-column label="备注" min-width="120">
            <template #default="{ row: r }"><el-input v-model="r.remark" size="small" placeholder="备注" /></template>
          </el-table-column>
          <el-table-column label="操作" width="60">
            <template #default="{ $index }"><el-button type="danger" link size="small" @click="removeDetailRow($index)">删除</el-button></template>
          </el-table-column>
        </el-table>
      </el-form>
      <template #footer>
        <el-button @click="createDialog = false">取消</el-button>
        <el-button type="primary" :loading="formLoading" @click="handleSubmit">{{ isEdit ? '保存' : '创建' }}</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="detailDialog" title="BOM明细" width="800px">
      <div v-if="detailBom" v-loading="detailLoading">
        <p><strong>BOM编号：</strong>{{ detailBom.bom_no }} &nbsp; <strong>名称：</strong>{{ detailBom.bom_name }} &nbsp; <strong>版本：</strong>{{ detailBom.version }}</p>
        <el-table :data="detailBom.details" border size="small">
          <el-table-column prop="material_sku_code" label="物料编码" width="120" />
          <el-table-column prop="material_sku_name" label="物料名称" min-width="140" />
          <el-table-column prop="spec" label="规格" width="100" />
          <el-table-column prop="unit" label="单位" width="60" />
          <el-table-column prop="quantity_per_unit" label="单台用量" width="90" />
          <el-table-column prop="wastage_rate" label="损耗率(%)" width="90" />
          <el-table-column prop="remark" label="备注" min-width="100" />
        </el-table>
      </div>
    </el-dialog>

    <el-dialog v-model="availabilityDialog" title="齐套分析" width="900px">
      <div v-if="availabilityData" v-loading="availabilityLoading">
        <p>
          <strong>BOM：</strong>{{ availabilityData.bom_no }} {{ availabilityData.bom_name }} &nbsp;
          <strong>计划数量：</strong>{{ availabilityData.plan_quantity }} &nbsp;
          <el-tag :type="availabilityData.overall_sufficient ? 'success' : 'danger'" size="small">
            {{ availabilityData.overall_sufficient ? '物料齐套' : '物料缺料' }}
          </el-tag>
        </p>
        <el-table :data="availabilityData.items" border size="small">
          <el-table-column prop="material_sku_code" label="物料编码" width="120" />
          <el-table-column prop="material_sku_name" label="物料名称" min-width="140" />
          <el-table-column prop="spec" label="规格" width="100" />
          <el-table-column prop="required_qty" label="需求数量" width="90" />
          <el-table-column prop="stock_qty" label="库存数量" width="90" />
          <el-table-column prop="shortage_qty" label="缺料数量" width="90">
            <template #default="{ row }">
              <span :style="{ color: row.shortage_qty > 0 ? 'red' : 'green', fontWeight: 'bold' }">{{ row.shortage_qty }}</span>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="80">
            <template #default="{ row }">
              <el-tag :type="row.is_sufficient ? 'success' : 'danger'" size="small">{{ row.is_sufficient ? '充足' : '缺料' }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
        <div v-if="!availabilityData.overall_sufficient" style="margin-top: 12px; color: #e6a23c">
          提示：部分物料库存不足，建议创建采购计划或调整生产数量。
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="taskDialog" title="创建生产任务" width="500px" :close-on-click-modal="false">
      <el-form :model="taskForm" label-width="100px">
        <el-form-item label="关联BOM"><el-input :value="selectedBomForTask?.bom_no + ' ' + selectedBomForTask?.bom_name" disabled /></el-form-item>
        <el-form-item label="计划数量" required>
          <el-input-number v-model="taskForm.plan_quantity" :min="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker v-model="taskForm.start_date" type="date" placeholder="计划开始日期" value-format="YYYY-MM-DD" style="width:100%" />
        </el-form-item>
        <el-form-item label="完成日期">
          <el-date-picker v-model="taskForm.end_date" type="date" placeholder="计划完成日期" value-format="YYYY-MM-DD" style="width:100%" />
        </el-form-item>
        <el-form-item label="变更原因"><el-input v-model="taskForm.change_reason" placeholder="变更原因" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="taskDialog = false">取消</el-button>
        <el-button type="primary" :loading="taskLoading" @click="handleTaskSubmit">创建</el-button>
      </template>
    </el-dialog>

    <PrintPreview v-model:visible="printVisible" title="BOM清单">
      <BomPrint v-if="printData || printBoms.length > 0" :data="printData" :boms="printBoms" />
    </PrintPreview>
  </div>
</template>

<style scoped>
.bom-page { padding: 16px; }
.search-card { margin-bottom: 16px; }
.toolbar { margin-bottom: 16px; display: flex; gap: 8px; }
</style>