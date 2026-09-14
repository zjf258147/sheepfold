import { describe, it, expect, beforeEach, vi } from 'vitest'

vi.mock('@/utils/request', () => {
  const mockRequest = {
    get: vi.fn(),
  }
  return { default: mockRequest }
})

import request from '@/utils/request'
import { getPhase2Stats } from '@/api/dashboard'

describe('Dashboard Phase2 API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getPhase2Stats', () => {
    it('发送GET请求获取二期看板统计数据', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: {
          total_stations: 5,
          active_stations: 4,
          devices_in_field: 42,
          devices_fault: 3,
          pending_stocktakes: 1,
          adjustments_today: 0,
        },
      })
      const res = await getPhase2Stats()
      expect(request.get).toHaveBeenCalledWith('/api/v1/dashboard/phase2-stats')
      expect(res.data.total_stations).toBe(5)
      expect(res.data.active_stations).toBe(4)
    })

    it('处理全部为0的返回', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: {
          total_stations: 0,
          active_stations: 0,
          devices_in_field: 0,
          devices_fault: 0,
          pending_stocktakes: 0,
          adjustments_today: 0,
        },
      })
      const res = await getPhase2Stats()
      expect(res.data.total_stations).toBe(0)
    })

    it('处理网络错误', async () => {
      request.get.mockRejectedValue(new Error('Network Error'))
      try {
        await getPhase2Stats()
        expect.unreachable()
      } catch (err) {
        expect(err.message).toBe('Network Error')
      }
    })
  })
})