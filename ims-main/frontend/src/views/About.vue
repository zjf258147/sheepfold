<script setup>
import { ref, computed, onMounted } from 'vue'
import { useBrandStore } from '@/stores/brand'
import { getApiBaseUrl } from '@/utils/apiConfig'
import ServerSettingsDialog from '@/components/ServerSettingsDialog.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Download } from '@element-plus/icons-vue'

const brand = useBrandStore()
const serverUrl = ref('')
const serverRef = ref(null)
const downloading = ref(false)

const appVersion = __APP_VERSION__
const buildTime = __BUILD_TIME__

const isApp = !!(window.Capacitor?.isNativePlatform?.())
const isRemote = computed(() => {
  return isApp && !window.location.href.startsWith('capacitor://')
})

const downloadUrl = computed(() => {
  return serverUrl.value ? `${serverUrl.value}/download/ims-latest.apk` : ''
})

onMounted(async () => {
  if (!brand.loaded) brand.fetchBranding()
  serverUrl.value = await getApiBaseUrl()
})

function openServerSettings() {
  serverRef.value?.open()
}

async function switchToLocal() {
  try {
    await ElMessageBox.confirm(
      '切回本地版本后，下次打开 App 将使用旧版本功能。确定吗？',
      '切回本地',
      { type: 'warning' }
    )
    const { Preferences } = await import('@capacitor/preferences')
    await Preferences.set({ key: 'use_online', value: 'false' })
    await Preferences.remove({ key: 'jump_token' })
    ElMessage.success('已切回本地版本，请重启 App')
  } catch {
    /* 用户取消 */
  }
}

function handleDownload() {
  if (!downloadUrl.value) {
    ElMessage.warning('服务器地址未配置')
    return
  }
  downloading.value = true
  window.open(downloadUrl.value, '_blank')
  setTimeout(() => { downloading.value = false }, 2000)
}

async function copyVersionInfo() {
  const info = [
    `${brand.appName} v${appVersion}`,
    `构建时间：${buildTime}`,
    `服务器：${serverUrl.value}`,
    `运行模式：${isRemote.value ? '在线版' : '本地版'}`,
  ].join('\n')
  try {
    await navigator.clipboard.writeText(info)
    ElMessage.success('版本信息已复制到剪贴板')
  } catch {
    ElMessage.info(info)
  }
}
</script>

<template>
  <div class="about-page">
    <el-card class="about-card">
      <div class="about-header">
        <img
          v-if="brand.logoUrl"
          :src="brand.logoUrl"
          :alt="brand.appName"
          class="about-logo"
        />
        <h1>{{ brand.appName }}</h1>
        <p class="about-subtitle">{{ brand.appSubtitle }}</p>
      </div>

      <div class="about-info">
        <div class="info-row">
          <span class="info-label">运行模式</span>
          <span class="info-value">
            <el-tag :type="isRemote ? 'success' : 'info'" size="small">
              {{ isRemote ? '在线版' : '本地版' }}
            </el-tag>
          </span>
        </div>
        <div class="info-row">
          <span class="info-label">App 版本</span>
          <span class="info-value">{{ appVersion }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">构建时间</span>
          <span class="info-value">{{ new Date(buildTime).toLocaleString('zh-CN') }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">服务器地址</span>
          <span class="info-value mono">{{ serverUrl }}</span>
        </div>
      </div>

      <div class="about-actions">
        <el-button type="primary" @click="handleDownload" :loading="downloading">
          <el-icon><Download /></el-icon>
          下载 Android App
        </el-button>
        <el-button v-if="isRemote" @click="switchToLocal" type="warning" plain>
          切回本地版本
        </el-button>
        <el-button type="primary" plain @click="openServerSettings">切换服务器</el-button>
        <el-button plain @click="copyVersionInfo">复制版本信息</el-button>
      </div>

      <div class="about-footer">
        <p>&copy; 2026 西安敦临计量检测有限公司</p>
      </div>
    </el-card>

    <ServerSettingsDialog ref="serverRef" />
  </div>
</template>

<style scoped>
.about-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
  padding: 20px;
}

.about-card {
  background: #fff;
  border-radius: 12px;
  padding: 40px 48px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.about-header {
  text-align: center;
  margin-bottom: 32px;
}

.about-logo {
  width: 72px;
  height: 72px;
  object-fit: contain;
  margin-bottom: 16px;
}

.about-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
  margin: 0 0 8px;
}

.about-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.about-info {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 24px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.info-row + .info-row {
  border-top: 1px solid #e4e7ed;
}

.info-label {
  font-size: 13px;
  color: #909399;
  flex-shrink: 0;
  margin-right: 16px;
}

.info-value {
  font-size: 14px;
  color: #303133;
  text-align: right;
  word-break: break-all;
}

.info-value.mono {
  font-family: 'Courier New', Consolas, monospace;
  font-size: 13px;
  color: #409eff;
}

.about-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.about-actions .el-button {
  flex: 1;
}

.about-footer {
  text-align: center;
}

.about-footer p {
  font-size: 12px;
  color: #c0c4cc;
  margin: 0;
}

@media (max-width: 480px) {
  .about-card {
    padding: 24px 20px;
  }

  .about-actions {
    flex-direction: column;
  }
}
</style>