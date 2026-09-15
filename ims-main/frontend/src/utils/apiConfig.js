const STORAGE_KEY = 'api_base_url'
const DEFAULT_BASE_URL = 'http://192.168.10.77:8000'
let cachedBaseUrl = null

const isCapacitor = () => !!(window.Capacitor?.isNativePlatform?.())

export function getDefaultBaseUrl() {
  return import.meta.env.VITE_API_BASE_URL || DEFAULT_BASE_URL
}

export async function getApiBaseUrl() {
  if (cachedBaseUrl) return cachedBaseUrl

  if (isCapacitor()) {
    try {
      const { Preferences } = await import('@capacitor/preferences')
      const { value } = await Preferences.get({ key: STORAGE_KEY })
      cachedBaseUrl = value || DEFAULT_BASE_URL
    } catch {
      cachedBaseUrl = DEFAULT_BASE_URL
    }
  } else {
    cachedBaseUrl = localStorage.getItem(STORAGE_KEY) || getDefaultBaseUrl()
  }

  return cachedBaseUrl
}

export async function setApiBaseUrl(url) {
  const normalized = url.replace(/\/+$/, '')
  cachedBaseUrl = normalized

  if (isCapacitor()) {
    try {
      const { Preferences } = await import('@capacitor/preferences')
      await Preferences.set({ key: STORAGE_KEY, value: normalized })
    } catch {
      // fallback to localStorage
      localStorage.setItem(STORAGE_KEY, normalized)
    }
  } else {
    localStorage.setItem(STORAGE_KEY, normalized)
  }
}

export function getCachedBaseUrl() {
  return cachedBaseUrl
}

export function resetBaseUrlCache() {
  cachedBaseUrl = null
}

export function clearApiBaseUrl() {
  cachedBaseUrl = null
  localStorage.removeItem(STORAGE_KEY)
  if (isCapacitor()) {
    import('@capacitor/preferences').then(({ Preferences }) => {
      Preferences.remove({ key: STORAGE_KEY })
    })
  }
}