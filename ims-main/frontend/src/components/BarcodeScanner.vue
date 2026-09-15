<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { Camera, PictureFilled, Sunny, Refresh, Aim } from '@element-plus/icons-vue'
import { Html5Qrcode } from 'html5-qrcode'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: '扫码或输入SN' },
})

const emit = defineEmits(['update:modelValue', 'scan', 'scanEnter', 'photo'])

const visible = ref(false)
const scanValue = ref('')
const cameraError = ref('')
const scanResult = ref('')
const isScanning = ref(false)
const scanMode = ref(true)
const photoUrl = ref('')
const flashOn = ref(false)
const hasFlash = ref(false)
const dialogFullscreen = ref(false)
const focusing = ref(false)
const photoCodes = ref([])
const scanningPhoto = ref(false)
const selectedCode = ref('')

let html5QrCode = null

onMounted(() => {
  dialogFullscreen.value = window.innerWidth < 768
})

async function open() {
  scanValue.value = ''
  cameraError.value = ''
  scanResult.value = ''
  photoUrl.value = ''
  photoCodes.value = []
  selectedCode.value = ''
  scanningPhoto.value = false
  scanMode.value = true
  isScanning.value = false
  dialogFullscreen.value = window.innerWidth < 768
  visible.value = true
  await nextTick()
  startScan()
}

function close() {
  stopScan()
  visible.value = false
}

async function stopScan() {
  if (html5QrCode) {
    try {
      await html5QrCode.stop()
    } catch (e) { /* ignore */ }
    html5QrCode = null
  }
  isScanning.value = false
}

async function startScan() {
  await stopScan()
  scanMode.value = true
  cameraError.value = ''
  scanResult.value = ''
  photoUrl.value = ''
  photoCodes.value = []
  selectedCode.value = ''

  try {
    html5QrCode = new Html5Qrcode('scanner-video')
    const config = {
      fps: 10,
      qrbox: { width: 250, height: 250 },
      aspectRatio: 1.0,
      formatsToSupport: [
        'CODE_128', 'CODE_39', 'CODE_93', 'CODABAR',
        'EAN_13', 'EAN_8', 'UPC_A', 'UPC_E',
        'ITF', 'RSS_14', 'RSS_EXPANDED',
        'QR_CODE', 'DATA_MATRIX', 'AZTEC', 'PDF_417',
      ],
    }

    await html5QrCode.start(
      { facingMode: 'environment' },
      config,
      onScanSuccess,
      onScanFailure,
    )

    isScanning.value = true
    checkFlash()
    applyFocusConstraints()
  } catch (err) {
    cameraError.value = '无法访问摄像头，请手动输入'
  }
}

function onScanSuccess(decodedText) {
  scanResult.value = decodedText
  if (navigator.vibrate) navigator.vibrate(200)
  nextTick(() => {
    confirmScan()
  })
}

function onScanFailure() {
  // 持续扫描，不做处理
}

function confirmScan() {
  if (scanResult.value) {
    emit('update:modelValue', scanResult.value)
    emit('scan', scanResult.value)
    close()
  }
}

async function switchToPhoto() {
  await stopScan()
  scanMode.value = false
  cameraError.value = ''
  photoUrl.value = ''
  photoCodes.value = []
  selectedCode.value = ''
  scanningPhoto.value = false

  try {
    html5QrCode = new Html5Qrcode('scanner-video')
    const config = {
      fps: 10,
      qrbox: { width: 250, height: 250 },
      aspectRatio: 1.0,
    }

    await html5QrCode.start(
      { facingMode: 'environment' },
      config,
      () => {},
      () => {},
    )
    isScanning.value = true
    applyFocusConstraints()
  } catch (err) {
    cameraError.value = '无法访问摄像头，请手动输入'
  }
}

async function switchToScan() {
  await stopScan()
  startScan()
}

function getVideoTrack() {
  const videoEl = document.querySelector('#scanner-video video')
  if (videoEl && videoEl.srcObject) {
    return videoEl.srcObject.getVideoTracks()[0] || null
  }
  return null
}

async function applyFocusConstraints() {
  try {
    const track = getVideoTrack()
    if (!track) return
    const capabilities = track.getCapabilities()
    if (capabilities.focusMode) {
      await track.applyConstraints({
        advanced: [{ focusMode: 'continuous' }],
      })
    }
  } catch (e) {
    // 忽略
  }
}

async function tapToFocus(e) {
  const videoEl = document.querySelector('#scanner-video video')
  if (!videoEl) return
  const rect = videoEl.getBoundingClientRect()
  const x = (e.clientX - rect.left) / rect.width
  const y = (e.clientY - rect.top) / rect.height

  try {
    const track = getVideoTrack()
    if (!track) return
    const capabilities = track.getCapabilities()

    // 优先用 pointsOfInterest 定点对焦
    if (capabilities.pointsOfInterest) {
      await track.applyConstraints({
        advanced: [{ pointsOfInterest: [{ x, y }] }],
      })
    }

    // 触发一次自动对焦
    if (capabilities.focusMode) {
      if (capabilities.focusMode.includes('auto')) {
        await track.applyConstraints({ advanced: [{ focusMode: 'auto' }] })
      }
      // 再切回连续对焦
      if (capabilities.focusMode.includes('continuous')) {
        setTimeout(async () => {
          try {
            await track.applyConstraints({ advanced: [{ focusMode: 'continuous' }] })
          } catch (e) { /* ignore */ }
        }, 1500)
      }
    }

    if (navigator.vibrate) navigator.vibrate(30)
  } catch (e) {
    // 忽略
  }
}

async function triggerFocus() {
  if (focusing.value) return
  focusing.value = true
  try {
    const track = getVideoTrack()
    if (!track) return
    const capabilities = track.getCapabilities()
    if (capabilities.focusMode && capabilities.focusMode.includes('auto')) {
      // 先切到 auto 触发一次对焦，再切回 continuous
      await track.applyConstraints({ advanced: [{ focusMode: 'auto' }] })
      if (capabilities.focusMode.includes('continuous')) {
        setTimeout(async () => {
          try {
            await track.applyConstraints({ advanced: [{ focusMode: 'continuous' }] })
          } catch (e) { /* ignore */ }
        }, 1500)
      }
    } else if (capabilities.focusMode && capabilities.focusMode.includes('continuous')) {
      await track.applyConstraints({ advanced: [{ focusMode: 'continuous' }] })
    }
    if (navigator.vibrate) navigator.vibrate(50)
  } catch (e) {
    // 对焦不支持
  }
  setTimeout(() => { focusing.value = false }, 800)
}

function capturePhoto() {
  const videoEl = document.querySelector('#scanner-video video')
  if (!videoEl) return
  const canvas = document.createElement('canvas')
  canvas.width = videoEl.videoWidth || 640
  canvas.height = videoEl.videoHeight || 480
  const ctx = canvas.getContext('2d')
  ctx.drawImage(videoEl, 0, 0, canvas.width, canvas.height)
  photoUrl.value = canvas.toDataURL('image/jpeg', 0.8)
  if (navigator.vibrate) navigator.vibrate(100)
  // 拍照后自动扫描图片中的条码
  scanPhotoImage(photoUrl.value)
}

async function scanPhotoImage(dataUrl) {
  scanningPhoto.value = true
  photoCodes.value = []
  try {
    const response = await fetch(dataUrl)
    const blob = await response.blob()
    const result = await Html5Qrcode.scanFile(blob, false)
    // result 可能是单个对象或数组
    const results = Array.isArray(result) ? result : [result]
    const codes = results
      .filter(r => r && r.decodedText)
      .map(r => r.decodedText)
      .filter((v, i, a) => a.indexOf(v) === i) // 去重
    if (codes.length > 0) {
      photoCodes.value = codes
      selectedCode.value = codes[0]
      if (navigator.vibrate) navigator.vibrate([100, 50, 100])
    }
  } catch (e) {
    // 未识别到条码，保持 photoUrl 显示
  }
  scanningPhoto.value = false
}

function selectPhotoCode(code) {
  selectedCode.value = code
}

function useSelectedCode() {
  if (selectedCode.value) {
    emit('update:modelValue', selectedCode.value)
    emit('scan', selectedCode.value)
    close()
  }
}

function confirmPhoto() {
  if (photoUrl.value) {
    emit('photo', photoUrl.value)
    close()
  }
}

function retakePhoto() {
  photoUrl.value = ''
  photoCodes.value = []
  selectedCode.value = ''
  scanningPhoto.value = false
}

async function toggleFlash() {
  if (!html5QrCode) return
  try {
    await html5QrCode.applyVideoConstraints({
      advanced: [{ torch: !flashOn.value }],
    })
    flashOn.value = !flashOn.value
  } catch {
    // 不支持闪光灯
  }
}

async function checkFlash() {
  try {
    if (!html5QrCode) return
    const capabilities = html5QrCode.getRunningTrackCapabilities()
    hasFlash.value = capabilities?.torch?.() !== undefined
  } catch {
    hasFlash.value = false
  }
}

function onManual() {
  const v = scanValue.value.trim()
  if (v) {
    emit('update:modelValue', v)
    emit('scan', v)
    close()
  }
}

function onKeyEnter() {
  onManual()
}

function onInput(e) {
  emit('update:modelValue', e)
}

onUnmounted(() => {
  stopScan()
})
</script>

<template>
  <div class="scanner-wrapper">
    <el-input
      :model-value="modelValue"
      :placeholder="placeholder"
      clearable
      @update:model-value="onInput"
      @keyup.enter="$emit('scanEnter')"
    >
      <template #suffix>
        <el-button :icon="Camera" size="small" link @click="open" />
      </template>
    </el-input>

    <el-dialog
      v-model="visible"
      :title="scanMode ? '扫码录入' : '拍照录入'"
      :width="dialogFullscreen ? '100%' : '400px'"
      :fullscreen="dialogFullscreen"
      :close-on-click-modal="false"
      :destroy-on-close="true"
      @closed="close"
      class="scanner-dialog"
    >
      <div class="scanner-body">
        <!-- 摄像头区域 -->
        <div class="scanner-video-wrapper" @click.stop="tapToFocus">
          <div id="scanner-video" class="scanner-video" />
          <div v-if="scanResult && scanMode" class="scan-result-banner">
            <span>识别成功：{{ scanResult }}</span>
          </div>
          <div v-if="photoUrl && !scanMode" class="photo-preview">
            <img :src="photoUrl" alt="拍摄照片" />
            <div v-if="scanningPhoto" class="scanning-overlay">
              <el-icon class="is-loading" :size="32"><Aim /></el-icon>
              <span>正在识别...</span>
            </div>
          </div>
          <div v-if="cameraError" class="camera-error">{{ cameraError }}</div>
        </div>

        <!-- 工具栏 -->
        <div class="scanner-toolbar">
          <el-button-group v-if="!cameraError">
            <el-button
              :type="scanMode ? 'primary' : ''"
              size="small"
              @click="switchToScan"
            >
              <el-icon><Camera /></el-icon>
              扫码
            </el-button>
            <el-button
              :type="!scanMode ? 'primary' : ''"
              size="small"
              @click="switchToPhoto"
            >
              <el-icon><PictureFilled /></el-icon>
              拍照
            </el-button>
          </el-button-group>
          <el-button
            v-if="!cameraError && !photoUrl"
            :type="focusing ? 'primary' : ''"
            size="small"
            :icon="Aim"
            :loading="focusing"
            @click="triggerFocus"
          >
            对焦
          </el-button>
          <el-button
            v-if="!cameraError && hasFlash && !photoUrl"
            :type="flashOn ? 'warning' : ''"
            size="small"
            :icon="Sunny"
            @click="toggleFlash"
          >
            {{ flashOn ? '关灯' : '开灯' }}
          </el-button>
        </div>

        <!-- 拍照模式：拍照按钮 -->
        <div v-if="!scanMode && !photoUrl && !cameraError" class="photo-capture-area">
          <el-button type="primary" size="large" circle class="capture-btn" @click="capturePhoto">
            <el-icon :size="28"><Camera /></el-icon>
          </el-button>
          <p class="capture-hint">将产品对准框内，点击拍照</p>
        </div>

        <!-- 拍照模式：识别到的条码选择 -->
        <div v-if="!scanMode && photoCodes.length > 0" class="photo-codes-section">
          <div class="photo-codes-label">识别到 {{ photoCodes.length }} 个条码，点击选择：</div>
          <div class="photo-codes-list">
            <el-tag
              v-for="code in photoCodes"
              :key="code"
              :type="selectedCode === code ? 'primary' : 'info'"
              size="large"
              class="photo-code-tag"
              @click="selectPhotoCode(code)"
            >
              {{ code }}
            </el-tag>
          </div>
          <div class="photo-code-actions">
            <el-button @click="retakePhoto" :icon="Refresh">重拍</el-button>
            <el-button type="primary" @click="useSelectedCode" :icon="PictureFilled">使用选中</el-button>
          </div>
        </div>

        <!-- 拍照模式：预览（无识别结果） -->
        <div v-if="!scanMode && photoUrl && photoCodes.length === 0 && !scanningPhoto" class="photo-actions">
          <el-button @click="retakePhoto" :icon="Refresh">重拍</el-button>
          <el-button type="primary" @click="confirmPhoto" :icon="PictureFilled">使用照片</el-button>
        </div>

        <!-- 手动输入 -->
        <div class="scanner-input">
          <el-input
            v-model="scanValue"
            :placeholder="scanMode ? '手动输入条码号' : '输入备注说明'"
            clearable
            @keyup.enter="onKeyEnter"
          />
          <el-button type="primary" @click="onManual" style="margin-left:8px;flex-shrink:0">确定</el-button>
        </div>

        <div v-if="scanMode && !cameraError" class="scan-hint">
          将条码/二维码对准框内，自动识别 · 点击画面可对焦
        </div>
      </div>

      <template #footer>
        <el-button @click="close">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.scanner-wrapper {
  display: inline-flex;
  align-items: center;
  width: 100%;
}
.scanner-wrapper :deep(.el-input) {
  width: 100%;
}

.scanner-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.scanner-video-wrapper {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  background: #000;
  min-height: 200px;
  cursor: crosshair;
  -webkit-tap-highlight-color: transparent;
}

.scanner-video {
  width: 100%;
  min-height: 200px;
}

.scanner-video :deep(video) {
  width: 100%;
  min-height: 200px;
  object-fit: cover;
}

.scan-result-banner {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(103, 194, 58, 0.9);
  color: #fff;
  padding: 8px 12px;
  font-size: 14px;
  text-align: center;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.photo-preview {
  position: relative;
}
.photo-preview img {
  width: 100%;
  display: block;
  border-radius: 8px;
}

.scanning-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  gap: 8px;
  font-size: 14px;
  border-radius: 8px;
}

.camera-error {
  color: #f56c6c;
  padding: 12px;
  text-align: center;
  font-size: 14px;
}

.scanner-toolbar {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.photo-capture-area {
  text-align: center;
  padding: 12px 0;
}

.capture-btn {
  width: 64px !important;
  height: 64px !important;
  border: 4px solid #fff;
  box-shadow: 0 0 0 2px #409eff;
  transition: transform 0.2s;
}

.capture-btn:active {
  transform: scale(0.9);
}

.capture-hint {
  margin-top: 8px;
  color: #909399;
  font-size: 13px;
}

.photo-codes-section {
  background: #f0f9eb;
  border-radius: 8px;
  padding: 12px;
}
.photo-codes-label {
  font-size: 13px;
  color: #67c23a;
  margin-bottom: 8px;
  font-weight: 500;
}
.photo-codes-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}
.photo-code-tag {
  cursor: pointer;
  font-size: 14px;
  padding: 6px 14px;
  transition: transform 0.15s;
}
.photo-code-tag:active {
  transform: scale(0.95);
}
.photo-code-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.photo-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.scanner-input {
  display: flex;
  align-items: center;
}

.scanner-input :deep(.el-input) {
  flex: 1;
}

.scan-hint {
  text-align: center;
  color: #909399;
  font-size: 12px;
}

/* 移动端全屏适配 */
@media screen and (max-width: 768px) {
  .scanner-video-wrapper {
    min-height: 260px;
  }
  .scanner-video {
    min-height: 260px;
  }
  .scanner-video :deep(video) {
    min-height: 260px;
  }
}
</style>