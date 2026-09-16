import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './style.css'
import { formatDateTime } from './utils/datetime'
import { useBrandStore } from './stores/brand'

const app = createApp(App)

app.config.globalProperties.$formatDateTime = formatDateTime

const pinia = createPinia()
app.use(pinia)
app.use(router)

const initRemoteDetection = async () => {
  const isApp = !!(window.Capacitor?.isNativePlatform?.())
  if (!isApp) return

  try {
    const urlParams = new URLSearchParams(window.location.search)
    const tokenFromUrl = urlParams.get('token')
    if (tokenFromUrl) {
      localStorage.setItem('token', tokenFromUrl)
      window.history.replaceState({}, '', window.location.pathname)
    }

    const { Preferences } = await import('@capacitor/preferences')
    const { value } = await Preferences.get({ key: 'use_online' })
    if (value !== 'true') return

    const apiBase = localStorage.getItem('api_base_url')
    const baseUrl = apiBase || ''
    if (!baseUrl) return

    const controller = new AbortController()
    setTimeout(() => controller.abort(), 3000)
    const res = await fetch(`${baseUrl}/health`, { signal: controller.signal })

    if (res.ok) {
      const token = localStorage.getItem('token') || ''
      await Preferences.set({ key: 'jump_token', value: token })
      const { getFrontendUrl } = await import('@/utils/apiConfig')
      const frontendUrl = getFrontendUrl(baseUrl)
      window.location.href = `${frontendUrl}/login?token=${encodeURIComponent(token)}`
    }
  } catch {
    /* 静默留在本地 */
  }
}

const brand = useBrandStore(pinia)
brand.fetchBranding().finally(async () => {
  await initRemoteDetection()
  app.mount('#app')
})