import { describe, it, expect, beforeEach, vi } from 'vitest'

vi.mock('@/utils/request', () => {
  const mockRequest = {
    post: vi.fn(),
    get: vi.fn(),
    put: vi.fn(),
  }
  return { default: mockRequest }
})

import request from '@/utils/request'
import {
  listDevices,
  getDevice,
  createDevice,
  updateDevice,
  removeDevice,
  checkWarranty,
} from '@/api/deviceLedger'

describe('DeviceLedger API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('listDevices', () => {
    it('发送GET请求获取设备台账列表', async () => {
      request.get.mockResolvedValue({ code: 0, data: { items: [], total: 0 } })
      const res = await listDevices({ page: 1, page_size: 20 })
      expect(request.get).toHaveBeenCalledWith('/api/v1/device-ledger', {
        params: { page: 1, page_size: 20 },
      })
      expect(res.data.total).toBe(0)
    })

    it('支持按场站筛选', async () => {
      request.get.mockResolvedValue({ code: 0, data: { items: [], total: 0 } })
      await listDevices({ station_id: 1 })
      expect(request.get).toHaveBeenCalledWith('/api/v1/device-ledger', {
        params: { station_id: 1 },
      })
    })

    it('支持按状态筛选', async () => {
      request.get.mockResolvedValue({ code: 0, data: { items: [], total: 0 } })
      await listDevices({ status: 'RUNNING' })
      expect(request.get).toHaveBeenCalledWith('/api/v1/device-ledger', {
        params: { status: 'RUNNING' },
      })
    })
  })

  describe('getDevice', () => {
    it('发送GET请求获取单个设备台账', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: { id: 1, item_sn: 'SN001', station_name: '西安场站' },
      })
      const res = await getDevice(1)
      expect(request.get).toHaveBeenCalledWith('/api/v1/device-ledger/1')
      expect(res.data.station_name).toBe('西安场站')
    })
  })

  describe('createDevice', () => {
    it('发送POST请求登记设备到场站', async () => {
      const data = { item_sn: 'SN002', station_id: 1, installed_date: '2026-09-14' }
      request.post.mockResolvedValue({ code: 0, data: { id: 2, ...data } })
      const res = await createDevice(data)
      expect(request.post).toHaveBeenCalledWith('/api/v1/device-ledger', data)
      expect(res.data.id).toBe(2)
    })
  })

  describe('updateDevice', () => {
    it('发送PUT请求更新设备台账', async () => {
      const data = { software_version: 'v2.0', status: 'FAULT' }
      request.put.mockResolvedValue({ code: 0, data: { id: 1, ...data } })
      const res = await updateDevice(1, data)
      expect(request.put).toHaveBeenCalledWith('/api/v1/device-ledger/1', data)
      expect(res.data.status).toBe('FAULT')
    })
  })

  describe('removeDevice', () => {
    it('发送POST请求回收设备', async () => {
      const data = { removed_date: '2026-09-14' }
      request.post.mockResolvedValue({
        code: 0,
        data: { id: 1, status: 'RECOVERED', removed_date: '2026-09-14' },
      })
      const res = await removeDevice(1, data)
      expect(request.post).toHaveBeenCalledWith('/api/v1/device-ledger/1/remove', data)
      expect(res.data.status).toBe('RECOVERED')
    })
  })

  describe('checkWarranty', () => {
    it('发送GET请求检查质保', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: { item_sn: 'SN001', in_warranty: true, days_remaining: 365 },
      })
      const res = await checkWarranty('SN001')
      expect(request.get).toHaveBeenCalledWith('/api/v1/device-ledger/warranty/SN001')
      expect(res.data.in_warranty).toBe(true)
    })

    it('质保已过期的设备返回 in_warranty=false', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: { item_sn: 'SN002', in_warranty: false, days_remaining: -30 },
      })
      const res = await checkWarranty('SN002')
      expect(res.data.in_warranty).toBe(false)
      expect(res.data.days_remaining).toBe(-30)
    })

    it('未找到设备时处理', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: { item_sn: 'NONEXIST', in_warranty: false, warranty_start: null, warranty_end: null },
      })
      const res = await checkWarranty('NONEXIST')
      expect(res.data.in_warranty).toBe(false)
      expect(res.data.warranty_start).toBeNull()
    })
  })
})