<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, Connection, Download, Loading } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useBrandStore } from '@/stores/brand'
import { getApiBaseUrl, getCachedBaseUrl, getFrontendUrl } from '@/utils/apiConfig'
import ServerSettingsDialog from '@/components/ServerSettingsDialog.vue'

const router = useRouter()
const auth = useAuthStore()
const brand = useBrandStore()
const loading = ref(false)
const switchingToOnline = ref(false)
const form = ref({ username: '', password: '' })
const serverRef = ref(null)
const showServerTip = ref(false)
const serverUrl = ref('')
const isApp = ref(false)
const hasServerConfig = ref(false)
const onlineAvailable = ref(false)

const downloadUrl = computed(() => {
  return serverUrl.value ? `${serverUrl.value}/download/ims-latest.apk` : ''
})

onMounted(async () => {
  if (!brand.loaded) brand.fetchBranding()
  serverUrl.value = getCachedBaseUrl() || (await getApiBaseUrl())
  isApp.value = !!(window.Capacitor?.isNativePlatform?.())

  if (isApp.value) {
    const url = getCachedBaseUrl() || (await getApiBaseUrl())
    if (!url) {
      showServerTip.value = true
      await nextTick()
      serverRef.value?.open()
    } else {
      hasServerConfig.value = true
      checkOnlineAvailability()
    }
  }
})

async function checkOnlineAvailability() {
  const url = getCachedBaseUrl() || (await getApiBaseUrl())
  if (!url) return
  try {
    const controller = new AbortController()
    setTimeout(() => controller.abort(), 3000)
    const res = await fetch(`${url}/health`, { signal: controller.signal })
    onlineAvailable.value = res.ok
  } catch {
    onlineAvailable.value = false
  }
}

async function switchToOnline() {
  const baseUrl = getCachedBaseUrl() || (await getApiBaseUrl())
  if (!baseUrl) {
    ElMessage.warning('请先配置服务器地址')
    serverRef.value?.open()
    return
  }
  switchingToOnline.value = true
  try {
    const controller = new AbortController()
    setTimeout(() => controller.abort(), 3000)
    const res = await fetch(`${baseUrl}/health`, { signal: controller.signal })
    if (res.ok) {
      const token = localStorage.getItem('token') || ''
      try {
        const { Preferences } = await import('@capacitor/preferences')
        await Promise.all([
          Preferences.set({ key: 'use_online', value: 'true' }),
          Preferences.set({ key: 'jump_token', value: token }),
        ])
      } catch { /* Capacitor 不可用时忽略 */ }
      const frontendUrl = getFrontendUrl(baseUrl)
      window.location.href = `${frontendUrl}/login?token=${encodeURIComponent(token)}`
    } else {
      ElMessage.warning('服务器不可达，请确认已连接公司WiFi')
    }
  } catch {
    ElMessage.warning('服务器不可达，请确认已连接公司WiFi')
  } finally {
    switchingToOnline.value = false
  }
}

async function handleLogin() {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <div v-if="brand.logoUrl" class="login-logo">
        <img :src="brand.logoUrl" :alt="brand.appName" />
      </div>
      <h1>{{ brand.appName }}</h1>
      <p class="subtitle">{{ brand.appSubtitle }}</p>
      <el-alert
        v-if="showServerTip"
        title="未配置服务器地址，请先设置"
        type="warning"
        show-icon
        :closable="false"
        style="margin-bottom:16px"
      >
        <template #default>
          <el-button type="warning" size="small" plain @click="serverRef?.open()" style="margin-top:8px">
            立即设置
          </el-button>
        </template>
      </el-alert>
      <el-alert
        v-if="isApp && !hasServerConfig && !showServerTip"
        title="首次使用"
        type="info"
        show-icon
        :closable="false"
        style="margin-bottom:16px"
      >
        <template #default>
          <p style="margin:0 0 8px;font-size:13px">请先配置服务器地址，或联系管理员获取</p>
          <el-button type="primary" size="small" @click="serverRef?.open()">配置服务器地址</el-button>
        </template>
      </el-alert>
      <el-alert
        v-if="isApp && hasServerConfig && !onlineAvailable"
        title="未连接公司服务器"
        type="warning"
        show-icon
        :closable="false"
        style="margin-bottom:16px"
      >
        <template #default>
          <p style="margin:0;font-size:13px">请连接公司WiFi后点击下方按钮使用在线版本</p>
        </template>
      </el-alert>
      <div v-if="isApp && hasServerConfig && onlineAvailable" style="margin-bottom:16px;text-align:center">
        <el-button
          type="success"
          :loading="switchingToOnline"
          @click="switchToOnline"
        >
          使用在线版本（最新功能）
        </el-button>
      </div>
      <el-form @submit.prevent="handleLogin">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" size="large" :prefix-icon="User" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" size="large" :prefix-icon="Lock" show-password @keyup.enter="handleLogin" />
        </el-form-item>
        <el-button type="primary" size="large" style="width:100%" :loading="loading" @click="handleLogin">登 录</el-button>
      </el-form>
      <div class="server-entry" @click="serverRef?.open()">
        <el-icon><Connection /></el-icon>
        <span>服务器设置</span>
      </div>
      <div v-if="downloadUrl" class="app-download">
        <a :href="downloadUrl" target="_blank">
          <el-icon><Download /></el-icon>
          <span>下载移动端 App</span>
        </a>
      </div>
    </div>
    <ServerSettingsDialog ref="serverRef" />

    <div v-if="switchingToOnline" class="switch-overlay">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <p>正在连接服务器...</p>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1d2b3a 0%, #2c5364 100%);
}
.login-card {
  width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,.2);
}
.login-logo {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}
.login-logo img {
  max-height: 56px;
  max-width: 220px;
  object-fit: contain;
}
h1 { text-align: center; margin: 0 0 8px; color: #1d2b3a; }
.subtitle { text-align: center; color: #909399; margin: 0 0 32px; font-size: 14px; }
.server-entry {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-top: 16px;
  padding: 8px;
  color: #909399;
  font-size: 13px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
}
.server-entry:hover {
  color: #409EFF;
  background: #ecf5ff;
}
.app-download {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 12px;
}
.app-download a {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px;
  color: #67C23A;
  font-size: 13px;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s;
}
.app-download a:hover {
  color: #5daf34;
  background: #f0f9eb;
}
.switch-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  color: #fff;
  gap: 16px;
}
.switch-overlay p {
  font-size: 16px;
  margin: 0;
}
</style>