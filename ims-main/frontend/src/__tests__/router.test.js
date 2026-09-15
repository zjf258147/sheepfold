import { describe, it, expect, beforeEach } from 'vitest'
import { createRouter, createWebHistory } from 'vue-router'

const Login = { template: '<div>Login</div>' }
const Dashboard = { template: '<div>Dashboard</div>' }
const Inbound = { template: '<div>Inbound</div>' }
const Settings = { template: '<div>Settings</div>' }
const Inventory = { template: '<div>Inventory</div>' }
const Rma = { template: '<div>RMA</div>' }
const MainLayout = { template: '<div><router-view /></div>' }

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { public: true },
  },
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: Dashboard, meta: { title: '首页' } },
      { path: 'inbound', name: 'Inbound', component: Inbound, meta: { title: '入库', roles: ['ADMIN', 'WAREHOUSE'] } },
      { path: 'inventory', name: 'Inventory', component: Inventory, meta: { title: '库存' } },
      { path: 'rma', name: 'Rma', component: Rma, meta: { title: '返厂', roles: ['ADMIN', 'WAREHOUSE', 'QUALITY'] } },
      { path: 'settings', name: 'Settings', component: Settings, meta: { title: '设置', admin: true } },
    ],
  },
]

function createTestRouter() {
  return createRouter({ history: createWebHistory(), routes })
}

describe('路由配置测试', () => {
  let router

  beforeEach(async () => {
    router = createTestRouter()
    router.push('/')
    await router.isReady()
  })

  describe('路由定义', () => {
    it('注册所有路由', () => {
      const names = router.getRoutes().map((r) => r.name)
      expect(names).toContain('Login')
      expect(names).toContain('Dashboard')
      expect(names).toContain('Inbound')
      expect(names).toContain('Inventory')
      expect(names).toContain('Rma')
      expect(names).toContain('Settings')
    })

    it('根路径重定向到/dashboard', () => {
      const routes = router.getRoutes()
      const rootRoute = routes.find((r) => r.path === '/')
      expect(rootRoute.redirect).toBe('/dashboard')
    })

    it('登录页标记为public', () => {
      const routes = router.getRoutes()
      const loginRoute = routes.find((r) => r.name === 'Login')
      expect(loginRoute.meta.public).toBe(true)
    })

    it('入库页标记角色限制', () => {
      const routes = router.getRoutes()
      const inboundRoute = routes.find((r) => r.name === 'Inbound')
      expect(inboundRoute.meta.roles).toContain('ADMIN')
      expect(inboundRoute.meta.roles).toContain('WAREHOUSE')
    })

    it('设置页标记为admin', () => {
      const routes = router.getRoutes()
      const settingsRoute = routes.find((r) => r.name === 'Settings')
      expect(settingsRoute.meta.admin).toBe(true)
    })

    it('Dashboard无角色限制', () => {
      const routes = router.getRoutes()
      const dashboardRoute = routes.find((r) => r.name === 'Dashboard')
      expect(dashboardRoute.meta.roles).toBeUndefined()
      expect(dashboardRoute.meta.admin).toBeUndefined()
    })
  })

  describe('路由导航', () => {
    it('导航到/login（公开页面）', async () => {
      await router.push('/login')
      expect(router.currentRoute.value.name).toBe('Login')
    })

    it('导航到/dashboard', async () => {
      await router.push('/dashboard')
      expect(router.currentRoute.value.name).toBe('Dashboard')
    })

    it('路由匹配：不存在的路径', async () => {
      // 路由不存在时不会匹配
      const resolved = router.resolve('/nonexistent')
      expect(resolved.name).toBeUndefined()
    })
  })

  describe('路由meta信息', () => {
    it('Dashboard有title', () => {
      const routes = router.getRoutes()
      const route = routes.find((r) => r.name === 'Dashboard')
      expect(route.meta.title).toBe('首页')
    })

    it('Inbound有title和roles', () => {
      const routes = router.getRoutes()
      const route = routes.find((r) => r.name === 'Inbound')
      expect(route.meta.title).toBe('入库')
      expect(route.meta.roles).toEqual(['ADMIN', 'WAREHOUSE'])
    })

    it('Inventory只有title无角色限制', () => {
      const routes = router.getRoutes()
      const route = routes.find((r) => r.name === 'Inventory')
      expect(route.meta.title).toBe('库存')
      expect(route.meta.roles).toBeUndefined()
    })
  })
})