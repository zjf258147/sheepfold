<script setup>
import { ref, onMounted } from 'vue'
import { getApiBaseUrl, getDefaultBaseUrl, setApiBaseUrl, clearApiBaseUrl, resetBaseUrlCache, getCachedBaseUrl } from '@/utils/apiConfig'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['saved'])

const visible = ref(false)
const url = ref('')
const originalUrl = ref('')
const testing = ref(false)
const saving = ref(false)
const testResult = ref(null)
const isCapacitor = ref(false)

onMounted(() => {
  isCapacitor.value = !!(window.Capacitor?.isNativePlatform?.())
})

async function open() {
  visible.value = true
  testResult.value = null
  const current = getCachedBaseUrl() || (await getApiBaseUrl())
  url.value = current
  originalUrl.value = current
}

function close() {
  visible.value = false
}

async function testConnection() {
  if (!url.value.trim()) {
    ElMessage.warning('请输入服务器地址')
    return
  }
  testing.value = true
  testResult.value = null
  try {
    const baseUrl = url.value.trim().replace(/\/+$/, '')
    const resp = await fetch(baseUrl + '/api/v1/settings/test-connection', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: baseUrl }),
    })
    const data = await resp.json()
    testResult.value = { ok: data.ok ?? true, msg: data.msg || '连接成功' }
  } catch (e) {
    testResult.value = { ok: false, msg: e.message || '请求失败' }
  } finally {
    testing.value = false
  }
}

async function save() {
  if (!url.value.trim()) {
    ElMessage.warning('请输入服务器地址')
    return
  }
  saving.value = true
  try {
    await setApiBaseUrl(url.value.trim())
    ElMessage.success('服务器地址已保存')
    visible.value = false

    if (url.value.trim() !== originalUrl.value) {
      resetBaseUrlCache()
      window.location.reload()
    }
  } finally {
    saving.value = false
  }
}

async function resetDefault() {
  await clearApiBaseUrl()
  const defaultUrl = getDefaultBaseUrl()
  url.value = defaultUrl
  testResult.value = null
  ElMessage.success('已恢复默认地址，请点击保存')
}

defineExpose({ open })
</script>

<template>
  <el-dialog
    v-model="visible"
    title="服务器设置"
    width="460px"
    destroy-on-close
    :close-on-click-modal="false"
  >
    <div class="server-settings">
      <el-alert
        v-if="isCapacitor"
        title="当前运行在 App 环境中，修改地址后无需重新打包即可生效"
        type="info"
        show-icon
        :closable="false"
        style="margin-bottom: 16px"
      />

      <el-form label-width="90px" @submit.prevent="save">
        <el-form-item label="服务器地址">
          <el-input
            v-model="url"
            placeholder="例如: http://192.168.1.100:8000"
            clearable
          >
            <template #prefix>🔗</template>
          </el-input>
        </el-form-item>

        <el-form-item v-if="testResult" label="测试结果">
          <el-tag :type="testResult.ok ? 'success' : 'danger'" effect="plain">
            {{ testResult.ok ? '✓' : '✗' }} {{ testResult.msg }}
          </el-tag>
        </el-form-item>
      </el-form>

      <div class="server-actions">
        <el-button @click="resetDefault" :disabled="testing || saving">恢复默认</el-button>
        <el-button @click="testConnection" :loading="testing" :disabled="!url.trim()">
          测试连接
        </el-button>
        <el-button type="primary" @click="save" :loading="saving">
          保存并刷新
        </el-button>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
.server-settings {
  padding: 4px 0;
}

.server-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}
</style>