import axios from 'axios'
import router from '@/router'
import { getApiBaseUrl } from './apiConfig'
import { isOnline } from '@/composables/useNetwork'

const request = axios.create({
  timeout: 30000,
})

let baseUrlReady = false
let baseUrlPromise = null
let offlineErrorShown = false

request.interceptors.request.use(async (config) => {
  if (!baseUrlReady) {
    if (!baseUrlPromise) {
      baseUrlPromise = getApiBaseUrl()
    }
    const url = await baseUrlPromise
    request.defaults.baseURL = url
    baseUrlReady = true
  }

  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code !== undefined && res.code !== 0) {
      ElMessage.error(res.msg || '请求失败')
      return Promise.reject(new Error(res.msg))
    }
    offlineErrorShown = false
    return res
  },
  (error) => {
    const status = error.response?.status
    const detail = error.response?.data?.detail

    if (status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
      return Promise.reject(error)
    }

    const isNetworkError = !error.response && (
      error.message === 'Network Error' ||
      error.code === 'ERR_NETWORK' ||
      error.code === 'ECONNABORTED'
    )

    if (isNetworkError) {
      if (!isOnline.value) {
        return Promise.reject(error)
      }
      if (!offlineErrorShown) {
        offlineErrorShown = true
        ElMessage.error('无法连接到服务器，请检查网络连接')
      }
      return Promise.reject(error)
    }

    ElMessage.error(detail || error.message || '网络错误')
    return Promise.reject(error)
  }
)

export default request