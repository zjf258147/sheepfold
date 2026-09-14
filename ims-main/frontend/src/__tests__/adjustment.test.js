import { describe, it, expect, beforeEach, vi } from 'vitest'

vi.mock('@/utils/request', () => {
  const mockRequest = {
    post: vi.fn(),
    get: vi.fn(),
  }
  return { default: mockRequest }
})

import request from '@/utils/request'
import {
  listAdjustments,
  getAdjustment,
  createAdjustment,
  confirmAdjustments,
} from '@/api/adjustment'

describe('InventoryAdjustment API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('listAdjustments', () => {
    it('发送GET请求获取调整列表', async () => {
      request.get.mockResolvedValue({ code: 0, data: { items: [], total: 0 } })
      const res = await listAdjustments({ page: 1, page_size: 20 })
      expect(request.get).toHaveBeenCalledWith('/api/v1/adjustments', {
        params: { page: 1, page_size: 20 },
      })
      expect(res.data.total).toBe(0)
    })

    it('支持按盘点任务筛选', async () => {
      request.get.mockResolvedValue({ code: 0, data: { items: [], total: 0 } })
      await listAdjustments({ stocktake_id: 1 })
      expect(request.get).toHaveBeenCalledWith('/api/v1/adjustments', {
        params: { stocktake_id: 1 },
      })
    })

    it('支持按调整类型筛选', async () => {
      request.get.mockResolvedValue({ code: 0, data: { items: [], total: 0 } })
      await listAdjustments({ adjustment_type: 'SURPLUS' })
      expect(request.get).toHaveBeenCalledWith('/api/v1/adjustments', {
        params: { adjustment_type: 'SURPLUS' },
      })
    })
  })

  describe('getAdjustment', () => {
    it('发送GET请求获取调整详情', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: { id: 1, adjustment_no: 'TZ20260914001', adjustment_type: 'SURPLUS' },
      })
      const res = await getAdjustment(1)
      expect(request.get).toHaveBeenCalledWith('/api/v1/adjustments/1')
      expect(res.data.adjustment_type).toBe('SURPLUS')
    })
  })

  describe('createAdjustment', () => {
    it('发送POST请求创建盘盈调整', async () => {
      const data = {
        stocktake_id: 1,
        stocktake_line_id: 1,
        adjustment_type: 'SURPLUS',
        reason: '多出一台',
      }
      request.post.mockResolvedValue({ code: 0, data: { id: 1, ...data } })
      const res = await createAdjustment(data)
      expect(request.post).toHaveBeenCalledWith('/api/v1/adjustments', data)
      expect(res.data.adjustment_type).toBe('SURPLUS')
    })

    it('发送POST请求创建盘亏调整', async () => {
      const data = {
        stocktake_id: 1,
        stocktake_line_id: 2,
        adjustment_type: 'SHORTAGE',
        reason: '丢失一台',
      }
      request.post.mockResolvedValue({ code: 0, data: { id: 2, ...data } })
      const res = await createAdjustment(data)
      expect(res.data.adjustment_type).toBe('SHORTAGE')
    })
  })

  describe('confirmAdjustments', () => {
    it('发送POST请求批量确认调整', async () => {
      const data = { adjustment_ids: [1, 2] }
      request.post.mockResolvedValue({
        code: 0,
        data: [
          { id: 1, adjustment_type: 'SURPLUS' },
          { id: 2, adjustment_type: 'SHORTAGE' },
        ],
      })
      const res = await confirmAdjustments(data)
      expect(request.post).toHaveBeenCalledWith('/api/v1/adjustments/confirm', data)
      expect(res.data).toHaveLength(2)
    })
  })
})