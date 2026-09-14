<script setup>
import { onMounted, ref, watch } from 'vue'
import { listShipments, createShipment, updateShipment, deleteShipment } from '@/api/shipment'
import { listSkus, listCategories } from '@/api/product'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getShipmentPrintData, getShipmentBatchPrintData } from '@/api/print'
import PrintPreview from '@/print/components/PrintPreview.vue'
import ShipmentPrint from '@/print/components/ShipmentPrint.vue'

const loading = ref(false)
const shipments = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(15)
const query = ref({
  keyword: '',
  category_id: null,
  sku_id: null,
  dateRange: [],
})

const categories = ref([])
const skus = ref([])

const createDialog = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = ref({
  sku_id: null,
  sku_code: '',
  sku_name: '',
  spec: '',
  unit: '个',
  sn_list: '',
  ship_date: '',
  address: '',
  logistics_provider: '',
  tracking_no: '',
  u9_task_no: '',
  tf_version: '',
  host_version: '',
  remark: '',
  change_reason: '',
})
const formLoading = ref(false)

const exportLoading = ref(false)

const printVisible = ref(false)
const printData = ref(null)
const printShipments = ref([])
const printLoading = ref(false)
const batchPrintLoading = ref(false)
const selectedShipments = ref([])

async function handlePrint(row) {
  printLoading.value = true
  try {
    const res = await getShipmentPrintData(row.id)
    printData.value = res.data
    printShipments.value = []
    printVisible.value = true
  } catch {
    ElMessage.error('获取打印数据失败')
  } finally {
    printLoading.value = false
  }
}

async function handleBatchPrint() {
  if (selectedShipments.value.length === 0) {
    ElMessage.warning('请先选择要打印的出货单')
    return
  }
  batchPrintLoading.value = true
  try {
    const ids = selectedShipments.value.map(r => r.id)
    const results = await getShipmentBatchPrintData(ids)
    printShipments.value = results.map(r => r.data)
    printData.value = null
    printVisible.value = true
  } catch {
    ElMessage.error('批量获取打印数据失败')
  } finally {
    batchPrintLoading.value = false
  }
}

function handleSelectionChange(rows) {
  selectedShipments.value = rows
}

const scanSn = ref('')
const appendSn = (val) => {
  const current = form.value.sn_list || ''
  form.value.sn_list = current ? current + '\n' + val : val
  scanSn.value = ''
}

const formSkuCategory = ref(null)
const dialogSkus = ref([])

const onSkuCategoryChange = async (val) => {
  form.value.sku_id = null
  dialogSkus.value = []
  if (val) {
    try {
      const res = await listSkus({ category_id: val })
      dialogSkus.value = res.data || []
    } catch {}
  }
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value,
      keyword: query.value.keyword || undefined,
      sku_id: query.value.sku_id || undefined,
      start_date: query.value.dateRange?.[0] || undefined,
      end_date: query.value.dateRange?.[1] || undefined,
    }
    const res = await listShipments(params)
    shipments.value = res.data?.items || []
    total.value = res.data?.total || 0
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const res = await listCategories()
    categories.value = res.data || []
  } catch {}
}

watch(() => query.value.category_id, async (val) => {
  query.value.sku_id = null
  skus.value = []
  if (val) {
    try {
      const res = await listSkus({ category_id: val })
      skus.value = res.data || []
    } catch {}
  }
})

const handleSearch = () => {
  page.value = 1
  fetchData()
}

const handleReset = () => {
  query.value = { keyword: '', category_id: null, sku_id: null, dateRange: [] }
  page.value = 1
  fetchData()
}

const handlePageChange = (p) => {
  page.value = p
  fetchData()
}

const handleSizeChange = (s) => {
  pageSize.value = s
  page.value = 1
  fetchData()
}

const openCreate = () => {
  isEdit.value = false
  editId.value = null
  form.value = {
    sku_id: null, sku_code: '', sku_name: '', spec: '', unit: '个',
    sn_list: '', ship_date: '', address: '', logistics_provider: '',
    tracking_no: '', u9_task_no: '', tf_version: '', host_version: '',
    remark: '', change_reason: '',
  }
  createDialog.value = true
}

const openEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  form.value = {
    sku_id: row.sku_id,
    sku_code: row.sku_code,
    sku_name: row.sku_name,
    spec: row.spec || '',
    unit: row.unit,
    sn_list: Array.isArray(row.sn_list) ? row.sn_list.join('\n') : row.sn_list,
    ship_date: row.ship_date,
    address: row.address,
    logistics_provider: row.logistics_provider,
    tracking_no: row.tracking_no,
    u9_task_no: row.u9_task_no || '',
    tf_version: row.tf_version || '',
    host_version: row.host_version || '',
    remark: row.remark || '',
    change_reason: '',
  }
  createDialog.value = true
}

const handleSubmit = async () => {
  if (!form.value.sku_id) { ElMessage.warning('请选择物料'); return }
  if (!form.value.ship_date) { ElMessage.warning('请选择发货日期'); return }
  if (!form.value.address) { ElMessage.warning('请输入收货地址'); return }
  if (!form.value.logistics_provider) { ElMessage.warning('请输入物流供应商'); return }
  if (!form.value.tracking_no) { ElMessage.warning('请输入快递单号'); return }

  const snList = (form.value.sn_list || '').split('\n').map(s => s.trim()).filter(Boolean)
  if (snList.length === 0) { ElMessage.warning('请输入至少一个SN'); return }

  formLoading.value = true
  try {
    const data = {
      ...form.value,
      sn_list: snList,
      quantity: snList.length,
    }
    if (isEdit.value) {
      await updateShipment(editId.value, data)
      ElMessage.success('更新成功')
    } else {
      await createShipment(data)
      ElMessage.success('创建成功')
    }
    createDialog.value = false
    fetchData()
  } finally {
    formLoading.value = false
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定删除出货单 ${row.shipment_no}？`, '确认删除', { type: 'warning' })
    .then(async () => {
      await deleteShipment(row.id)
      ElMessage.success('已删除')
      fetchData()
    })
    .catch(() => {})
}

const handleExport = async () => {
  exportLoading.value = true
  try {
    const params = {
      page: 1,
      page_size: 10000,
      keyword: query.value.keyword || undefined,
      sku_id: query.value.sku_id || undefined,
      start_date: query.value.dateRange?.[0] || undefined,
      end_date: query.value.dateRange?.[1] || undefined,
    }
    const res = await listShipments(params)
    const items = res.data?.items || []
    if (!items || items.length === 0) { ElMessage.warning('无数据可导出'); return }

    const headers = ['出货单号', '物料编码', '物料名称', '规格', '单位', 'SN列表', '数量', '发货日期', '收货地址', '物流供应商', '快递单号', 'U9任务单号', 'TF版本', '上位机版本', '备注', '创建人', '创建时间']
    const rows = items.map(r => [
      r.shipment_no, r.sku_code, r.sku_name, r.spec || '', r.unit,
      (r.sn_list || []).join(';'), r.quantity, r.ship_date, r.address,
      r.logistics_provider, r.tracking_no, r.u9_task_no || '',
      r.tf_version || '', r.host_version || '', r.remark || '',
      r.created_by, r.created_at,
    ])

    const csvContent = [headers, ...rows].map(row => row.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n')
    const BOM = '\uFEFF'
    const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `IMS-出货记录-${new Date().toISOString().slice(0, 10)}.csv`
    link.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } finally {
    exportLoading.value = false
  }
}

const handleSkuChange = (val) => {
  const sku = skus.value.find(s => s.id === val)
  if (sku) {
    form.value.sku_code = sku.sku_code || ''
    form.value.sku_name = sku.name || ''
    form.value.spec = sku.spec || ''
    form.value.unit = sku.unit || '个'
  }
}

onMounted(() => {
  fetchCategories()
  fetchData()
})
</script>

<template>
  <div class="shipment-page">
    <el-card class="search-card">
      <el-form :inline="true" :model="query" size="default">
        <el-form-item label="搜索">
          <el-input v-model="query.keyword" placeholder="单号/物料/快递单号/U9" clearable style="width:200px" @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="query.category_id" placeholder="全部" clearable style="width:150px">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="物料">
          <el-select v-model="query.sku_id" placeholder="全部" clearable filterable style="width:180px">
            <el-option v-for="s in skus" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="发货日期">
          <el-date-picker v-model="query.dateRange" type="daterange" range-separator="至" start-placeholder="开始" end-placeholder="结束" value-format="YYYY-MM-DD" style="width:240px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <div class="toolbar">
        <el-button type="primary" @click="openCreate">出货登记</el-button>
        <el-button :loading="exportLoading" @click="handleExport">导出CSV</el-button>
        <el-button type="warning" :loading="batchPrintLoading" :disabled="selectedShipments.length === 0" @click="handleBatchPrint">
          批量打印 {{ selectedShipments.length > 0 ? `(${selectedShipments.length})` : '' }}
        </el-button>
      </div>

      <el-table :data="shipments" v-loading="loading" border stripe @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="50" />
        <el-table-column prop="shipment_no" label="出货单号" width="160" />
        <el-table-column prop="sku_code" label="物料编码" width="120" />
        <el-table-column prop="sku_name" label="物料名称" min-width="140" show-overflow-tooltip />
        <el-table-column prop="spec" label="规格" width="120" show-overflow-tooltip />
        <el-table-column prop="unit" label="单位" width="60" />
        <el-table-column prop="quantity" label="数量" width="70" />
        <el-table-column label="SN列表" width="140" show-overflow-tooltip>
          <template #default="{ row }">
            <span>{{ (row.sn_list || []).join(', ') }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="ship_date" label="发货日期" width="110" />
        <el-table-column prop="logistics_provider" label="物流供应商" width="110" />
        <el-table-column prop="tracking_no" label="快递单号" width="140" show-overflow-tooltip />
        <el-table-column prop="u9_task_no" label="U9任务单号" width="130" show-overflow-tooltip />
        <el-table-column prop="tf_version" label="TF版本" width="100" />
        <el-table-column prop="host_version" label="上位机版本" width="110" />
        <el-table-column prop="created_by" label="创建人" width="90" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handlePrint(row)" :loading="printLoading">打印</el-button>
            <el-button type="primary" link size="small" @click="openEdit(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[15, 30, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 16px; justify-content: flex-end"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
      />
    </el-card>

    <el-dialog v-model="createDialog" :title="isEdit ? '编辑出货单' : '出货登记'" width="700px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px">
        <el-form-item label="物料分类">
          <el-select v-model="formSkuCategory" placeholder="选择分类" clearable style="width:100%" @change="onSkuCategoryChange">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="物料" required>
          <el-select v-model="form.sku_id" placeholder="选择物料" filterable style="width:100%" @change="handleSkuChange">
            <el-option v-for="s in dialogSkus" :key="s.id" :label="`${s.sku_code || ''} ${s.name}`" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="物料编码"><el-input v-model="form.sku_code" disabled /></el-form-item>
        <el-form-item label="物料名称"><el-input v-model="form.sku_name" disabled /></el-form-item>
        <el-form-item label="规格"><el-input v-model="form.spec" disabled /></el-form-item>
        <el-form-item label="单位"><el-input v-model="form.unit" disabled /></el-form-item>
        <el-form-item label="SN列表" required>
          <div style="display:flex;gap:8px;align-items:flex-start">
            <BarcodeScanner v-model="scanSn" placeholder="扫码添加SN" @scan="appendSn" style="flex:1" />
          </div>
          <el-input v-model="form.sn_list" type="textarea" :rows="4" placeholder="每行一个SN，或点击上方扫码按钮添加" style="margin-top:8px" />
        </el-form-item>
        <el-form-item label="发货日期" required>
          <el-date-picker v-model="form.ship_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width:100%" />
        </el-form-item>
        <el-form-item label="收货地址" required>
          <el-input v-model="form.address" placeholder="详细收货地址" />
        </el-form-item>
        <el-form-item label="物流供应商" required>
          <el-input v-model="form.logistics_provider" placeholder="如：顺丰速运" />
        </el-form-item>
        <el-form-item label="快递单号" required>
          <el-input v-model="form.tracking_no" placeholder="快递单号" />
        </el-form-item>
        <el-form-item label="U9任务单号">
          <el-input v-model="form.u9_task_no" placeholder="关联U9任务单号" />
        </el-form-item>
        <el-form-item label="TF卡版本">
          <el-input v-model="form.tf_version" placeholder="TF卡版本号" />
        </el-form-item>
        <el-form-item label="上位机版本">
          <el-input v-model="form.host_version" placeholder="上位机版本号" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="备注" />
        </el-form-item>
        <el-form-item label="变更原因">
          <el-input v-model="form.change_reason" placeholder="变更原因" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialog = false">取消</el-button>
        <el-button type="primary" :loading="formLoading" @click="handleSubmit">{{ isEdit ? '保存' : '登记' }}</el-button>
      </template>
    </el-dialog>
  </div>

  <PrintPreview v-model:visible="printVisible" title="出货单">
    <ShipmentPrint v-if="printData || printShipments.length > 0" :data="printData" :shipments="printShipments" />
  </PrintPreview>
</template>

<style scoped>
.shipment-page { padding: 16px; }
.search-card { margin-bottom: 16px; }
.table-card { }
.toolbar { margin-bottom: 16px; display: flex; gap: 8px; }
</style>