import { onMounted, onUnmounted, ref, watch } from 'vue'
import { defaultDateRange } from '@/utils/datetime'

const STORE_PREFIX = 'ims_filter_'
const CACHE_TTL = 7 * 24 * 60 * 60 * 1000

export function useFilterPersist(key, query, opts = {}) {
  const { defaultMonths = 1, defaultDays = 0 } = opts
  const storageKey = STORE_PREFIX + key
  const ready = ref(false)
  let watchStop = null
  let saveTimer = null

  function readBool(val) {
    return val === true || String(val).toLowerCase() === 'true'
  }

  function load() {
    try {
      const raw = localStorage.getItem(storageKey)
      if (!raw) return false
      const saved = JSON.parse(raw)
      const ago = Date.now() - saved._ts
      if (ago > CACHE_TTL) {
        localStorage.removeItem(storageKey)
        return false
      }
      const keys = Object.keys(saved).filter(k => !k.startsWith('_'))
      for (const k of keys) {
        const v = saved[k]
        if (Array.isArray(v)) {
          if (k === 'dateRange' && readBool(saved._shortcut)) {
            query.value.dateRange = defaultDateRange(
              saved._shortcutDays
                ? { days: saved._shortcutDays }
                : { months: saved._shortcutMonths || defaultMonths }
            )
          } else {
            query.value[k] = v
          }
        } else {
          query.value[k] = v
        }
      }
      return true
    } catch {
      return false
    }
  }

  function save() {
    const data = { ...query.value, _ts: Date.now() }
    const keys = Object.keys(data).filter(k => !k.startsWith('_'))
    if (keys.length === 0) return
    localStorage.setItem(storageKey, JSON.stringify(data))
  }

  function debouncedSave() {
    clearTimeout(saveTimer)
    saveTimer = setTimeout(save, 400)
  }

  function clear() {
    localStorage.removeItem(storageKey)
  }

  function init() {
    const restored = load()
    if (!restored) {
      if (defaultDays > 0) {
        query.value.dateRange = defaultDateRange({ days: defaultDays })
      } else {
        query.value.dateRange = defaultDateRange({ months: defaultMonths })
      }
    }
    ready.value = true
    watchStop = watch(
      () => query.value,
      () => { if (ready.value) debouncedSave() },
      { deep: true }
    )
  }

  onMounted(init)

  onUnmounted(() => {
    clearTimeout(saveTimer)
    if (watchStop) watchStop()
  })

  return { clearStorage: clear }
}