import { describe, it, expect, beforeEach, vi } from 'vitest'

vi.mock('@/utils/request', () => {
  const mockRequest = {
    post: vi.fn(),
    get: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  }
  return { default: mockRequest }
})

import request from '@/utils/request'
import {
  listStations,
  listAllActiveStations,
  getStation,
  createStation,
  updateStation,
  deleteStation,
} from '@/api/station'

describe('Station API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('listStations', () => {
    it('发送GET请求，带上分页参数', async () => {
      request.get.mockResolvedValue({ code: 0, data: { items: [], total: 0 } })
      const res = await listStations({ page: 1, page_size: 20 })
      expect(request.get).toHaveBeenCalledWith('/api/v1/stations', {
        params: { page: 1, page_size: 20 },
      })
      expect(res.data.total).toBe(0)
    })

    it('发送GET请求，带上筛选参数', async () => {
      request.get.mockResolvedValue({ code: 0, data: { items: [], total: 0 } })
      await listStations({ keyword: '西安', status: 'ACTIVE' })
      expect(request.get).toHaveBeenCalledWith('/api/v1/stations', {
        params: { keyword: '西安', status: 'ACTIVE' },
      })
    })
  })

  describe('listAllActiveStations', () => {
    it('发送GET请求获取全部启用的场站', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: [{ id: 1, name: '测试场站', status: 'ACTIVE' }],
      })
      const res = await listAllActiveStations()
      expect(request.get).toHaveBeenCalledWith('/api/v1/stations/all')
      expect(res.data).toHaveLength(1)
    })
  })

  describe('getStation', () => {
    it('发送GET请求获取单个场站', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: { id: 1, name: '测试场站' },
      })
      const res = await getStation(1)
      expect(request.get).toHaveBeenCalledWith('/api/v1/stations/1')
      expect(res.data.name).toBe('测试场站')
    })
  })

  describe('createStation', () => {
    it('发送POST请求创建场站', async () => {
      const data = { name: '新场站', customer_id: 1 }
      request.post.mockResolvedValue({ code: 0, data: { id: 2, ...data } })
      const res = await createStation(data)
      expect(request.post).toHaveBeenCalledWith('/api/v1/stations', data)
      expect(res.data.id).toBe(2)
    })
  })

  describe('updateStation', () => {
    it('发送PUT请求更新场站', async () => {
      const data = { name: '更新场站' }
      request.put.mockResolvedValue({ code: 0, data: { id: 1, ...data } })
      const res = await updateStation(1, data)
      expect(request.put).toHaveBeenCalledWith('/api/v1/stations/1', data)
      expect(res.data.name).toBe('更新场站')
    })
  })

  describe('deleteStation', () => {
    it('发送DELETE请求删除场站', async () => {
      request.delete.mockResolvedValue({ code: 0, msg: '删除成功' })
      const res = await deleteStation(1)
      expect(request.delete).toHaveBeenCalledWith('/api/v1/stations/1')
      expect(res.msg).toBe('删除成功')
    })
  })
})