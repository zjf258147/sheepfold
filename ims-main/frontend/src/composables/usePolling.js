import { ref, computed, onUnmounted, watch } from 'vue'
import { getPollStatus } from '@/api/dashboard'

const DEFAULT_INTERVAL = 30_000

let pollTimer = null
let isActive = false
let intervalMs = DEFAULT_INTERVAL

const pollData = ref({
  inbound_pending: 0,
  outbound_pending: 0,
  device_fault: 0,
  stocktake_in_progress: 0,
  pending_adjustments: 0,
  warranty_expiring_soon: 0,
})

const isOnline = ref(true)
const isPolling = ref(false)

export function usePolling(interval = DEFAULT_INTERVAL) {
  intervalMs = interval

  async function fetchStatus() {
    if (!isActive) return
    isPolling.value = true
    try {
      const res = await getPollStatus()
      if (res.code === 0) {
        pollData.value = res.data
        isOnline.value = true
      }
    } catch {
      isOnline.value = false
    } finally {
      isPolling.value = false
    }
  }

  function start() {
    if (isActive) return
    isActive = true
    fetchStatus()
    pollTimer = setInterval(fetchStatus, intervalMs)
  }

  function stop() {
    isActive = false
    if (pollTimer) {
      clearInterval(pollTimer)
      pollTimer = null
    }
  }

  function setIntervalMs(ms) {
    intervalMs = ms
    if (isActive) {
      stop()
      start()
    }
  }

  onUnmounted(() => {
    stop()
  })

  watch(
    () => intervalMs,
    () => {},
    { immediate: false }
  )

  const totalBadge = computed(() => {
    const d = pollData.value
    return d.inbound_pending + d.outbound_pending + d.device_fault + d.stocktake_in_progress + d.pending_adjustments
  })

  return {
    pollData,
    isOnline,
    isPolling,
    totalBadge,
    start,
    stop,
    setIntervalMs,
    fetchStatus,
  }
}