import request from '@/utils/request'

export function listAdjustments(params) {
  return request.get('/api/v1/adjustments', { params })
}

export function getAdjustment(id) {
  return request.get(`/api/v1/adjustments/${id}`)
}

export function createAdjustment(data) {
  return request.post('/api/v1/adjustments', data)
}

export function confirmAdjustments(data) {
  return request.post('/api/v1/adjustments/confirm', data)
}