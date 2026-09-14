import { config } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

config.global.plugins = [ElementPlus]

globalThis.ElMessage = {
  error: () => {},
  success: () => {},
  warning: () => {},
  info: () => {},
}

const localStorageMock = (() => {
  let store = {}
  return {
    getItem: (key) => store[key] ?? null,
    setItem: (key, value) => { store[key] = String(value) },
    removeItem: (key) => { delete store[key] },
    clear: () => { store = {} },
  }
})()

Object.defineProperty(globalThis, 'localStorage', { value: localStorageMock })