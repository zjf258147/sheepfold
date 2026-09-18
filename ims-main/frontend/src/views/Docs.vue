<template>
  <div class="docs-page">
    <h2>文档下载中心</h2>
    <p class="subtitle">提供 IMS 系统相关文档的在线阅读与下载</p>

    <el-divider />

    <div v-for="(group, cat) in groupedDocs" :key="cat" class="doc-category">
      <h3>{{ cat }}</h3>
      <el-row :gutter="20">
        <el-col v-for="doc in group" :key="doc.id" :xs="24" :sm="12" :lg="8" :xl="6">
          <el-card shadow="hover" class="doc-card">
            <div class="doc-card-body">
              <el-icon :size="36" color="#409EFF">
                <component :is="iconMap[doc.icon] || Document" />
              </el-icon>
              <h4>{{ doc.name }}</h4>
              <p class="doc-desc">{{ doc.description }}</p>
              <div class="doc-meta">
                <el-tag v-if="doc.exists" size="small" type="success">可下载</el-tag>
                <el-tag v-else size="small" type="danger">文件缺失</el-tag>
                <span v-if="doc.size" class="doc-size">{{ doc.size }}</span>
              </div>
            </div>
            <div class="doc-card-footer">
              <el-button
                type="primary"
                :disabled="!doc.exists"
                @click="downloadDoc(doc)"
              >
                <el-icon><Download /></el-icon>
                下载 .docx
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div v-if="loading" class="loading-block">
      <el-icon class="is-loading" :size="24"><Loading /></el-icon>
      <span>加载中...</span>
    </div>
    <el-empty v-if="!loading && allDocs.length === 0" description="暂无可用文档" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Notebook, EditPen, Download, Loading } from '@element-plus/icons-vue'
import axios from 'axios'

const loading = ref(true)
const allDocs = ref([])

const iconMap = { Document, Notebook, EditPen }

const groupedDocs = computed(() => {
  const groups = {}
  for (const doc of allDocs.value) {
    const cat = doc.category || '其他'
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(doc)
  }
  return groups
})

onMounted(async () => {
  try {
    const { data } = await axios.get('/api/v1/docs')
    allDocs.value = data.items || []
  } catch (e) {
    ElMessage.error('获取文档列表失败')
  } finally {
    loading.value = false
  }
})

function downloadDoc(doc) {
  const a = document.createElement('a')
  a.href = doc.downloadUrl
  a.download = `${doc.name}.docx`
  a.click()
  ElMessage.success(`正在下载: ${doc.name}`)
}
</script>

<style scoped>
.docs-page {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.subtitle {
  color: #909399;
  margin-top: -8px;
}

.doc-category {
  margin-bottom: 32px;
}

.doc-category h3 {
  font-size: 16px;
  color: #303133;
  border-left: 3px solid #409EFF;
  padding-left: 10px;
  margin-bottom: 16px;
}

.doc-card {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 220px;
}

.doc-card-body {
  text-align: center;
  padding: 12px 0;
}

.doc-card-body h4 {
  font-size: 16px;
  margin: 10px 0 6px;
  color: #303133;
}

.doc-desc {
  font-size: 13px;
  color: #909399;
  line-height: 1.5;
  min-height: 36px;
}

.doc-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
}

.doc-size {
  font-size: 12px;
  color: #c0c4cc;
}

.doc-card-footer {
  text-align: center;
  padding-top: 8px;
  border-top: 1px solid #ebeef5;
}

.loading-block {
  text-align: center;
  padding: 40px;
  color: #909399;
}
</style>