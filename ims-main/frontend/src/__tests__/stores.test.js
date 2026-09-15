import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { useBrandStore } from '@/stores/brand'

describe('Pinia Store测试', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  describe('Auth Store', () => {
    it('初始状态：token为空', () => {
      const auth = useAuthStore()
      expect(auth.token).toBe('')
    })

    it('初始状态：user为null', () => {
      const auth = useAuthStore()
      expect(auth.user).toBeNull()
    })

    it('初始状态：role为空字符串', () => {
      const auth = useAuthStore()
      expect(auth.role).toBe('')
    })

    it('从localStorage恢复token', () => {
      localStorage.setItem('token', 'test-jwt-token')
      setActivePinia(createPinia())
      const auth = useAuthStore()
      expect(auth.token).toBe('test-jwt-token')
    })

    it('hasRole检查角色', () => {
      const auth = useAuthStore()
      auth.user = { role: 'WAREHOUSE' }
      expect(auth.hasRole('WAREHOUSE')).toBe(true)
      expect(auth.hasRole('ADMIN')).toBe(false)
    })

    it('isAdmin计算属性', () => {
      const auth = useAuthStore()
      auth.user = { role: 'ADMIN' }
      expect(auth.isAdmin).toBe(true)
      auth.user = { role: 'WAREHOUSE' }
      expect(auth.isAdmin).toBe(false)
    })

    it('isWarehouse计算属性', () => {
      const auth = useAuthStore()
      auth.user = { role: 'WAREHOUSE' }
      expect(auth.isWarehouse).toBe(true)
      expect(auth.isQuality).toBe(false)
    })

    it('isQuality计算属性', () => {
      const auth = useAuthStore()
      auth.user = { role: 'QUALITY' }
      expect(auth.isQuality).toBe(true)
    })

    it('isProduction计算属性', () => {
      const auth = useAuthStore()
      auth.user = { role: 'PRODUCTION' }
      expect(auth.isProduction).toBe(true)
    })

    it('isTestEngineer计算属性', () => {
      const auth = useAuthStore()
      auth.user = { role: 'TEST_ENGINEER' }
      expect(auth.isTestEngineer).toBe(true)
    })

    it('isStaff计算属性', () => {
      const auth = useAuthStore()
      auth.user = { role: 'STAFF' }
      expect(auth.isStaff).toBe(true)
    })

    it('logout清除token和user', () => {
      const auth = useAuthStore()
      auth.token = 'test-token'
      auth.user = { role: 'WAREHOUSE' }
      auth.logout()
      expect(auth.token).toBe('')
      expect(auth.user).toBeNull()
      expect(localStorage.getItem('token')).toBeNull()
    })

    it('hasRole中ADMIN可通过所有角色检查', () => {
      const auth = useAuthStore()
      auth.user = { role: 'ADMIN' }
      expect(auth.hasRole('WAREHOUSE')).toBe(true)
      expect(auth.hasRole('QUALITY')).toBe(true)
      expect(auth.hasRole('PRODUCTION')).toBe(true)
    })
  })

  describe('Brand Store', () => {
    it('初始状态：默认应用名', () => {
      const brand = useBrandStore()
      expect(brand.appName).toBe('IMS')
    })

    it('初始状态：默认副标题', () => {
      const brand = useBrandStore()
      expect(brand.appSubtitle).toBe('一物一码库存管理系统')
    })

    it('初始状态：loaded为false', () => {
      const brand = useBrandStore()
      expect(brand.loaded).toBe(false)
    })

    it('apply设置品牌信息', () => {
      const brand = useBrandStore()
      brand.apply({ app_name: 'Jove', app_subtitle: '智能库存', logo_url: '/logo.png' })
      expect(brand.appName).toBe('Jove')
      expect(brand.appSubtitle).toBe('智能库存')
      expect(brand.logoUrl).toBe('/logo.png')
    })

    it('apply空数据不改变默认值', () => {
      const brand = useBrandStore()
      brand.apply(null)
      expect(brand.appName).toBe('IMS')
      expect(brand.appSubtitle).toBe('一物一码库存管理系统')
    })

    it('apply空对象使用默认值', () => {
      const brand = useBrandStore()
      brand.apply({})
      expect(brand.appName).toBe('IMS')
      expect(brand.appSubtitle).toBe('一物一码库存管理系统')
    })

    it('applyDocumentTitle更新页面标题', () => {
      const brand = useBrandStore()
      brand.apply({ app_name: 'TestApp' })
      expect(document.title).toBe('TestApp')
    })
  })
})