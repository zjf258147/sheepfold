import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { public: true },
  },
  {
    path: '/',
    component: () => import('@/layout/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/Dashboard.vue'), meta: { title: '首页' } },
      {
        path: 'inventory',
        component: () => import('@/views/Inventory.vue'),
        children: [
          { path: '', name: 'Inventory', component: () => import('@/views/inventory/InventoryDetail.vue'), meta: { title: '实时库存' } },
          { path: 'sku', name: 'InventorySku', component: () => import('@/views/inventory/InventorySkuSummary.vue'), meta: { title: '按SKU统计库存' } },
          { path: 'partner', name: 'InventoryPartner', component: () => import('@/views/inventory/InventoryPartnerSummary.vue'), meta: { title: '按关联单位出库统计' } },
        ],
      },
      { path: 'inbound', name: 'Inbound', component: () => import('@/views/Inbound.vue'), meta: { title: '入库', roles: ['ADMIN', 'WAREHOUSE'] } },
      { path: 'inbound/:id', name: 'InboundDetail', component: () => import('@/views/InboundDetail.vue'), meta: { title: '入库单详情', roles: ['ADMIN', 'WAREHOUSE'] } },
      { path: 'incoming', name: 'IncomingReceipt', component: () => import('@/views/IncomingReceipt.vue'), meta: { title: '来料管理', roles: ['ADMIN', 'WAREHOUSE', 'QUALITY'] } },
      { path: 'rma', name: 'RmaReturn', component: () => import('@/views/RmaReturn.vue'), meta: { title: '返厂维修', roles: ['ADMIN', 'WAREHOUSE', 'QUALITY', 'TEST_ENGINEER', 'PRODUCTION'] } },
      { path: 'shipment', name: 'Shipment', component: () => import('@/views/Shipment.vue'), meta: { title: '出货管理', roles: ['ADMIN', 'WAREHOUSE', 'QUALITY', 'PRODUCTION'] } },
      { path: 'bom', name: 'BOM', component: () => import('@/views/BOM.vue'), meta: { title: 'BOM管理', roles: ['ADMIN', 'WAREHOUSE', 'PRODUCTION'] } },
      { path: 'production-task', name: 'ProductionTask', component: () => import('@/views/ProductionTask.vue'), meta: { title: '生产任务', roles: ['ADMIN', 'WAREHOUSE', 'PRODUCTION'] } },
      { path: 'outbound', name: 'Outbound', component: () => import('@/views/Outbound.vue'), meta: { title: '出库', roles: ['ADMIN', 'WAREHOUSE'] } },
      { path: 'outbound/:id', name: 'OutboundDetail', component: () => import('@/views/OutboundDetail.vue'), meta: { title: '出库单详情', roles: ['ADMIN', 'WAREHOUSE'] } },
      {
        path: 'snapshot',
        component: () => import('@/views/Snapshot.vue'),
        children: [
          { path: '', name: 'SnapshotLedger', component: () => import('@/views/snapshot/SnapshotLedger.vue'), meta: { title: '库存流水' } },
          { path: 'ledger', redirect: { name: 'SnapshotLedger' } },
          { path: 'statistics', name: 'SnapshotStatistics', component: () => import('@/views/snapshot/SnapshotStatistics.vue'), meta: { title: '库存快照汇总' } },
          { path: 'details', name: 'SnapshotDetails', component: () => import('@/views/snapshot/SnapshotDetails.vue'), meta: { title: '快照明细' } },
        ],
      },
      { path: 'products', name: 'Products', component: () => import('@/views/Products.vue'), meta: { title: '商品SKU' } },
      { path: 'partners', name: 'Partners', component: () => import('@/views/Partners.vue'), meta: { title: '往来单位' } },
      { path: 'station', name: 'Station', component: () => import('@/views/Station.vue'), meta: { title: '场站管理', roles: ['ADMIN', 'WAREHOUSE'] } },
      { path: 'device-ledger', name: 'DeviceLedger', component: () => import('@/views/DeviceLedger.vue'), meta: { title: '设备台账', roles: ['ADMIN', 'WAREHOUSE'] } },
      { path: 'stocktake', name: 'Stocktake', component: () => import('@/views/Stocktake.vue'), meta: { title: '盘点管理', roles: ['ADMIN', 'WAREHOUSE'] } },
      { path: 'adjustment', name: 'InventoryAdjustment', component: () => import('@/views/InventoryAdjustment.vue'), meta: { title: '库存调整', roles: ['ADMIN', 'WAREHOUSE'] } },
      { path: 'customers', name: 'Customers', component: () => import('@/views/Customer.vue'), meta: { title: '客户管理' } },
      { path: 'workflow', name: 'Workflow', component: () => import('@/views/WorkflowDiagram.vue'), meta: { title: '业务流程' } },
      { path: 'settings', name: 'Settings', component: () => import('@/views/Settings.vue'), meta: { title: '系统设置', admin: true } },
      { path: 'about', name: 'About', component: () => import('@/views/About.vue'), meta: { title: '关于' } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const token = localStorage.getItem('token')
  if (!to.meta.public && !token) {
    return '/login'
  }
  if (to.path === '/login' && token) {
    return '/dashboard'
  }
  if (to.meta.admin || to.meta.roles) {
    const auth = useAuthStore()
    if (!auth.user) await auth.fetchUser()
    if (to.meta.admin && !auth.isAdmin) return '/dashboard'
    if (to.meta.roles && !to.meta.roles.includes(auth.role) && !auth.isAdmin) return '/dashboard'
  }
})

export default router