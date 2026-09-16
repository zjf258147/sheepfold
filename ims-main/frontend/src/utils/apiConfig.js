const STORAGE_KEY = 'api_base_url'
let cachedBaseUrl = null

const isCapacitor = () => !!(window.Capacitor?.isNativePlatform?.())

export function getDefaultBaseUrl() {
  return import.meta.env.VITE_API_BASE_URL || ''
}

export async function getApiBaseUrl() {
  if (cachedBaseUrl !== null) return cachedBaseUrl

  if (isCapacitor()) {
    try {
      const { Preferences } = await import('@capacitor/preferences')
      const { value } = await Preferences.get({ key: STORAGE_KEY })
      cachedBaseUrl = value || ''
    } catch {
      cachedBaseUrl = ''
    }
  } else {
    const stored = localStorage.getItem(STORAGE_KEY)
    cachedBaseUrl = stored !== null ? stored : getDefaultBaseUrl()
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

export function getFrontendUrl(backendUrl) {
  const base = backendUrl || getCachedBaseUrl() || getDefaultBaseUrl() || ''
  const frontendPort = import.meta.env.VITE_FRONTEND_PORT || '8080'
  try {
    const url = new URL(base)
    url.port = frontendPort
    return url.origin
  } catch {
    return base.replace(/:8000$/, `:${frontendPort}`)
  }
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