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
  listStocktakes,
  getStocktake,
  getStocktakeLines,
  createStocktake,
  scanItems,
  updateLineReason,
  completeStocktake,
  cancelStocktake,
} from '@/api/stocktake'

describe('Stocktake API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('listStocktakes', () => {
    it('发送GET请求获取盘点列表', async () => {
      request.get.mockResolvedValue({ code: 0, data: { items: [], total: 0 } })
      const res = await listStocktakes({ page: 1, page_size: 20 })
      expect(request.get).toHaveBeenCalledWith('/api/v1/stocktakes', {
        params: { page: 1, page_size: 20 },
      })
      expect(res.data.total).toBe(0)
    })

    it('支持按状态筛选', async () => {
      request.get.mockResolvedValue({ code: 0, data: { items: [], total: 0 } })
      await listStocktakes({ status: 'IN_PROGRESS' })
      expect(request.get).toHaveBeenCalledWith('/api/v1/stocktakes', {
        params: { status: 'IN_PROGRESS' },
      })
    })
  })

  describe('getStocktake', () => {
    it('发送GET请求获取盘点详情', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: { id: 1, stocktake_no: 'PD20260914001', mode: 'CYCLE', status: 'IN_PROGRESS' },
      })
      const res = await getStocktake(1)
      expect(request.get).toHaveBeenCalledWith('/api/v1/stocktakes/1')
      expect(res.data.stocktake_no).toBe('PD20260914001')
    })
  })

  describe('getStocktakeLines', () => {
    it('发送GET请求获取盘点明细', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: [{ id: 1, item_sn: 'SN001', actual_qty: 1, diff_qty: 0 }],
      })
      const res = await getStocktakeLines(1)
      expect(request.get).toHaveBeenCalledWith('/api/v1/stocktakes/1/lines')
      expect(res.data).toHaveLength(1)
    })
  })

  describe('createStocktake', () => {
    it('发送POST请求创建循环盘点', async () => {
      const data = { mode: 'CYCLE', warehouse: '主仓库', remark: '月度盘点' }
      request.post.mockResolvedValue({ code: 0, data: { id: 1, ...data } })
      const res = await createStocktake(data)
      expect(request.post).toHaveBeenCalledWith('/api/v1/stocktakes', data)
      expect(res.data.mode).toBe('CYCLE')
    })

    it('发送POST请求创建全面盘点', async () => {
      const data = { mode: 'FULL', warehouse: '全部仓库' }
      request.post.mockResolvedValue({ code: 0, data: { id: 2, ...data } })
      const res = await createStocktake(data)
      expect(res.data.mode).toBe('FULL')
    })
  })

  describe('scanItems', () => {
    it('发送POST请求扫码盘点', async () => {
      const items = [{ item_sn: 'SN001', actual_qty: 1 }]
      request.post.mockResolvedValue({ code: 0, data: { id: 1, status: 'IN_PROGRESS' } })
      const res = await scanItems(1, { items })
      expect(request.post).toHaveBeenCalledWith('/api/v1/stocktakes/1/scan', { items })
      expect(res.data.status).toBe('IN_PROGRESS')
    })
  })

  describe('updateLineReason', () => {
    it('发送PUT请求更新差异原因', async () => {
      const data = { diff_reason: '实物缺失' }
      request.put.mockResolvedValue({ code: 0, data: { id: 1, ...data } })
      const res = await updateLineReason(1, data)
      expect(request.put).toHaveBeenCalledWith('/api/v1/stocktakes/lines/1', data)
      expect(res.data.diff_reason).toBe('实物缺失')
    })
  })

  describe('completeStocktake', () => {
    it('发送POST请求完成盘点', async () => {
      request.post.mockResolvedValue({
        code: 0,
        data: { id: 1, status: 'COMPLETED', remark: '盘点完成' },
      })
      const res = await completeStocktake(1, { remark: '盘点完成' })
      expect(request.post).toHaveBeenCalledWith('/api/v1/stocktakes/1/complete', {
        remark: '盘点完成',
      })
      expect(res.data.status).toBe('COMPLETED')
    })
  })

  describe('cancelStocktake', () => {
    it('发送POST请求取消盘点', async () => {
      request.post.mockResolvedValue({
        code: 0,
        data: { id: 1, status: 'CANCELLED' },
      })
      const res = await cancelStocktake(1)
      expect(request.post).toHaveBeenCalledWith('/api/v1/stocktakes/1/cancel')
      expect(res.data.status).toBe('CANCELLED')
    })
  })
})