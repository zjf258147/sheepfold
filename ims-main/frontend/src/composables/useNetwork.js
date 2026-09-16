import { ref, onMounted, onUnmounted } from 'vue'

const isOnline = ref(true)
const networkType = ref('unknown')

let listeners = []
let isNative = false
let initialized = false
let lastOnline = true

function showOfflineToast() {
  if (lastOnline === false) return
  ElMessage.closeAll()
  ElMessage({
    message: '网络已断开，请检查设备网络连接',
    type: 'warning',
    duration: 0,
    showClose: true,
    customClass: 'offline-toast',
  })
}

function showOnlineToast() {
  ElMessage.closeAll()
  ElMessage({
    message: '网络已恢复',
    type: 'success',
    duration: 3000,
    showClose: true,
  })
}

function init() {
  if (initialized) return
  initialized = true

  isNative = !!(window.Capacitor?.isNativePlatform?.())

  if (isNative) {
    setupNative()
  } else {
    setupBrowser()
  }
}

export function useNetwork() {
  onMounted(() => {
    init()
  })

  onUnmounted(() => {
    // keep global listeners alive across component unmounts
  })

  return {
    isOnline,
    networkType,
  }
}

async function setupNative() {
  try {
    const { Network } = await import('@capacitor/network')
    const status = await Network.getStatus()
    isOnline.value = status.connected
    networkType.value = status.connectionType || 'unknown'
    lastOnline = isOnline.value

    const handler = await Network.addListener('networkStatusChange', (status) => {
      const prev = isOnline.value
      isOnline.value = status.connected
      networkType.value = status.connectionType || 'unknown'

      if (prev && !status.connected) {
        showOfflineToast()
      } else if (!prev && status.connected) {
        showOnlineToast()
      }
      lastOnline = isOnline.value
    })
    listeners.push(handler)
  } catch {
    setupBrowser()
  }
}

function cleanupNative() {
  listeners.forEach((h) => {
    try { h.remove() } catch {}
  })
  listeners = []
}

function setupBrowser() {
  isOnline.value = navigator.onLine
  lastOnline = isOnline.value
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
}

function cleanupBrowser() {
  window.removeEventListener('online', handleOnline)
  window.removeEventListener('offline', handleOffline)
}

function handleOnline() {
  const prev = isOnline.value
  isOnline.value = true
  networkType.value = 'wifi'
  if (!prev) {
    showOnlineToast()
  }
  lastOnline = true
}

function handleOffline() {
  const prev = isOnline.value
  isOnline.value = false
  networkType.value = 'none'
  if (prev) {
    showOfflineToast()
  }
  lastOnline = false
}

// auto-init at module level so network state is tracked immediately
init()

export { isOnline, networkType }