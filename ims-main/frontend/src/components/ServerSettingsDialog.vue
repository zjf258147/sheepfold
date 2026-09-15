<script setup>
import { ref, onMounted } from 'vue'
import { getApiBaseUrl, getDefaultBaseUrl, setApiBaseUrl, clearApiBaseUrl, resetBaseUrlCache, getCachedBaseUrl } from '@/utils/apiConfig'
import request from '@/utils/request'
import { ElMessage, ElMessageBox } from 'element-plus'

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
    const res = await request.post('/api/v1/settings/test-connection', {
      url: url.value.trim(),
    })
    testResult.value = { ok: res.data.data.ok, msg: res.data.data.msg }
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
      await ElMessageBox.confirm(
        '服务器地址已更改，需要刷新页面才能生效。是否立即刷新？',
        '提示',
        { confirmButtonText: '刷新', cancelButtonText: '稍后', type: 'info' }
      )
      resetBaseUrlCache()
      window.location.reload()
    }
  } finally {
    saving.value = false
  }
}

async function resetDefault() {
  try {
    await ElMessageBox.confirm('将恢复为默认地址，确定吗？', '确认', {
      type: 'warning',
      appendTo: document.body,
      customClass: 'server-settings-msgbox',
    })
  } catch {
    return
  }
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