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
import { login, getMe } from '@/api/auth'

describe('API封装测试', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Auth API', () => {
    it('login发送POST请求', async () => {
      request.post.mockResolvedValue({
        code: 0,
        data: { access_token: 'mock-jwt' },
      })

      const res = await login({ username: 'admin', password: '123456' })
      expect(request.post).toHaveBeenCalledWith('/api/v1/auth/login', {
        username: 'admin',
        password: '123456',
      })
      expect(res.data.access_token).toBe('mock-jwt')
    })

    it('login处理错误响应', async () => {
      request.post.mockRejectedValue(new Error('用户名或密码错误'))

      try {
        await login({ username: 'wrong', password: 'wrong' })
        expect.unreachable()
      } catch (err) {
        expect(err.message).toBe('用户名或密码错误')
      }
    })

    it('getMe发送GET请求', async () => {
      request.get.mockResolvedValue({
        code: 0,
        data: { username: 'admin', nickname: '管理员', role: 'ADMIN' },
      })

      const res = await getMe()
      expect(request.get).toHaveBeenCalledWith('/api/v1/auth/me')
      expect(res.data.username).toBe('admin')
      expect(res.data.role).toBe('ADMIN')
    })

    it('getMe处理网络错误', async () => {
      request.get.mockRejectedValue(new Error('Network Error'))

      try {
        await getMe()
        expect.unreachable()
      } catch (err) {
        expect(err.message).toBe('Network Error')
      }
    })
  })
})