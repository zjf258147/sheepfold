<script setup>
import { onMounted, ref } from 'vue'
import PermissionButton from '@/components/PermissionButton.vue'
import {
  listCategories, createCategory, updateCategory, deleteCategory,
  listSkus, createSku, updateSku, deleteSku,
} from '@/api/product'
import { SNNO_IMPORT_MODE_MAP, SKU_TYPE_MAP } from '@/constants/enums'
import { Edit, Delete } from '@element-plus/icons-vue'
const activeTab = ref('sku')
const categories = ref([])
const skus = ref([])
const skuTotal = ref(0)
const loading = ref(false)

const catDialog = ref(false)
const catForm = ref({ id: null, name: '' })
const skuDialog = ref(false)
const skuForm = ref({ id: null, name: '', category_id: null, barcode: '', unit: '', sku_code: '', spec: '', sku_type: 'FINISHED_GOODS', sn_mode: 'MANUAL', status: 1, remark: '' })

const unitOptions = ['个', '台', '件', '套', '张', '份', '副', '盒', '箱', '袋', '包', '卷', '米', '千克', '升']

onMounted(() => { loadCategories(); loadSkus() })

async function loadCategories() {
  const res = await listCategories()
  categories.value = res.data
}

async function loadSkus() {
  loading.value = true
  try {
    const res = await listSkus({ page: 1, page_size: 100 })
    skus.value = res.data.items
    skuTotal.value = res.data.total
  } finally { loading.value = false }
}

function openCatDialog(row = null) {
  catForm.value = row ? { id: row.id, name: row.name } : { id: null, name: '' }
  catDialog.value = true
}

async function saveCategory() {
  if (!catForm.value.name?.trim()) {
    ElMessage.warning('分类名称不能为空')
    return
  }
  if (catForm.value.id) {
    await updateCategory(catForm.value.id, { name: catForm.value.name })
  } else {
    await createCategory({ name: catForm.value.name })
  }
  ElMessage.success('保存成功')
  catDialog.value = false
  loadCategories()
}

async function removeCategory(row) {
  await ElMessageBox.confirm('确认删除该分类？', '提示', { type: 'warning' })
  await deleteCategory(row.id)
  ElMessage.success('删除成功')
  loadCategories()
}

function openSkuDialog(row = null) {
  skuForm.value = row
    ? { id: row.id, name: row.name, category_id: row.category_id, barcode: row.barcode, unit: row.unit || '', sku_code: row.sku_code || '', spec: row.spec || '', sku_type: row.sku_type || 'FINISHED_GOODS', sn_mode: row.sn_mode, status: row.status, remark: row.remark || '' }
    : { id: null, name: '', category_id: categories.value[0]?.id || null, barcode: '', unit: '', sku_code: '', spec: '', sku_type: 'FINISHED_GOODS', sn_mode: 'MANUAL', status: 1, remark: '' }
  skuDialog.value = true
}

async function saveSku() {
  if (!skuForm.value.name?.trim()) {
    ElMessage.warning('商品名称不能为空')
    return
  }
  const { id, ...data } = skuForm.value
  if (id) await updateSku(id, data)
  else await createSku(data)
  ElMessage.success('保存成功')
  skuDialog.value = false
  loadSkus()
}

async function removeSku(row) {
  await ElMessageBox.confirm('确认删除该 SKU？', '提示', { type: 'warning' })
  await deleteSku(row.id)
  ElMessage.success('删除成功')
  loadSkus()
}
</script>

<template>
  <el-card shadow="never" style="position: relative;">
    <PermissionButton v-if="activeTab === 'sku'" permKey="product.manage">
      <el-button type="primary" style="position: absolute; right: 20px; top: 12px; z-index: 1000;" @click="openSkuDialog()">新增商品</el-button>
    </PermissionButton>
    <PermissionButton v-if="activeTab === 'category'" permKey="product.manage">
      <el-button type="primary" style="position: absolute; right: 20px; top: 12px; z-index: 1000;" @click="openCatDialog()">新增分类</el-button>
    </PermissionButton>
    <el-tabs v-model="activeTab">

      <el-tab-pane label="商品列表" name="sku">
        <el-table :data="skus" v-loading="loading" stripe style="margin-top:12px">
          <el-table-column prop="id" label="商品ID" />
          <el-table-column prop="name" label="商品名称" />
          <el-table-column prop="barcode" label="条码编码" />
          <el-table-column label="分类">
            <template #default="{ row }">{{ categories.find(c => c.id === row.category_id)?.name || row.category_id }}</template>
          </el-table-column>
          <el-table-column prop="unit" label="计量单位" />
          <el-table-column prop="sku_code" label="物料编码" />
          <el-table-column prop="spec" label="规格型号" />
          <el-table-column label="物料类型">
            <template #default="{ row }">{{ SKU_TYPE_MAP[row.sku_type] || row.sku_type }}</template>
          </el-table-column>
          <el-table-column label="SN号模式" >
            <template #default="{ row }">{{ SNNO_IMPORT_MODE_MAP[row.sn_mode] }}</template>
          </el-table-column>
          <el-table-column label="状态">
            <template #default="{ row }">
              <el-tag :type="row.status === 1 ? 'success' : 'info'" size="small">{{ row.status === 1 ? '启用' : '停用' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="{ row }">
              <PermissionButton permKey="product.manage">
                <el-button type="primary" link :icon="Edit" title="编辑" @click="openSkuDialog(row)" />
              </PermissionButton>
              <PermissionButton permKey="product.manage">
                <el-button type="danger" link :icon="Delete" title="删除" @click="removeSku(row)" />
              </PermissionButton>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="商品分类" name="category">
        <el-table :data="categories" stripe style="margin-top:12px">
          <el-table-column prop="id" label="分类ID" />
          <el-table-column prop="name" label="分类名称" />
          <el-table-column label="操作">
            <template #default="{ row }">
              <PermissionButton permKey="product.manage">
                <el-button type="primary" link :icon="Edit" title="编辑" @click="openCatDialog(row)" />
              </PermissionButton>
              <PermissionButton permKey="product.manage">
                <el-button type="danger" link :icon="Delete" title="删除" @click="removeCategory(row)" />
              </PermissionButton>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </el-card>

  <el-dialog v-model="catDialog" :title="catForm.id ? '编辑分类' : '新增分类'">
    <el-form label-width="80px">
      <el-form-item label="分类名称" required >
        <el-input v-model="catForm.name" placeholder="请输入分类名称" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="catDialog = false">取消</el-button>
      <el-button type="primary" @click="saveCategory">保存</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="skuDialog" :title="skuForm.id ? '编辑商品' : '新增商品'">
    <el-form label-width="90px">
      <el-form-item label="商品名称" required ><el-input v-model="skuForm.name" /></el-form-item>
      <el-form-item label="分类">
        <el-select v-model="skuForm.category_id" style="width:100%">
          <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="条码编码"><el-input v-model="skuForm.barcode" placeholder="如:691414123456" /></el-form-item>
      <el-form-item label="物料编码"><el-input v-model="skuForm.sku_code" placeholder="U9物料编码" /></el-form-item>
      <el-form-item label="规格型号"><el-input v-model="skuForm.spec" placeholder="规格型号" /></el-form-item>
      <el-form-item label="物料类型">
        <el-select v-model="skuForm.sku_type" style="width:100%">
          <el-option label="成品" value="FINISHED_GOODS" />
          <el-option label="原材料" value="RAW_MATERIAL" />
        </el-select>
      </el-form-item>
      <el-form-item label="计量单位">
        <el-select v-model="skuForm.unit" filterable allow-create default-first-option placeholder="请选择或输入" style="width:100%">
          <el-option v-for="u in unitOptions" :key="u" :label="u" :value="u" />
        </el-select>
      </el-form-item>
      <el-form-item label="SN模式">
        <el-select v-model="skuForm.sn_mode" style="width:100%">
          <el-option label="人工录入" value="MANUAL" />
          <el-option label="系统生成" value="AUTO" />
        </el-select>
      </el-form-item>
      <el-form-item label="备注"><el-input v-model="skuForm.remark" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="skuDialog = false">取消</el-button>
      <el-button type="primary" @click="saveSku">保存</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.toolbar { margin-bottom: 4px; }
</style>