<template>
  <div class="not-found-container">
    <div class="not-found-card">
      <div class="not-found-icon">404</div>
      <h2>页面未找到</h2>
      <p class="not-found-desc">您访问的页面不存在或已被移除。</p>
      <p class="not-found-path">路径：<code>{{ currentPath }}</code></p>
      <el-button type="primary" @click="goHome">返回首页</el-button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const currentPath = computed(() => route.path)

function goHome() {
  router.push('/dashboard')
}
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 60px);
  background: #f5f7fa;
}
.not-found-card {
  text-align: center;
  padding: 60px 80px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}
.not-found-icon {
  font-size: 80px;
  font-weight: 700;
  color: #e6e8ed;
  line-height: 1;
  margin-bottom: 16px;
  user-select: none;
}
.not-found-card h2 {
  font-size: 20px;
  color: #303133;
  margin: 0 0 12px;
  font-weight: 500;
}
.not-found-desc {
  color: #909399;
  font-size: 14px;
  margin: 0 0 8px;
}
.not-found-path {
  color: #c0c4cc;
  font-size: 13px;
  margin: 0 0 24px;
}
.not-found-path code {
  background: #f5f7fa;
  padding: 2px 8px;
  border-radius: 3px;
  font-family: monospace;
}
</style>