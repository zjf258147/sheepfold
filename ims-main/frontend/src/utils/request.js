import axios from 'axios'
import router from '@/router'
import { getApiBaseUrl } from './apiConfig'

const request = axios.create({
  timeout: 30000,
})

let baseUrlReady = false
let baseUrlPromise = null

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
    return res
  },
  (error) => {
    const status = error.response?.status
    const detail = error.response?.data?.detail
    if (status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
    } else {
      ElMessage.error(detail || error.message || '网络错误')
    }
    return Promise.reject(error)
  }
)

export default request