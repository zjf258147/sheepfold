import request from '@/utils/request'

export function listDevices(params) {
  return request.get('/api/v1/device-ledger', { params })
}

export function getDevice(id) {
  return request.get(`/api/v1/device-ledger/${id}`)
}

export function createDevice(data) {
  return request.post('/api/v1/device-ledger', data)
}

export function updateDevice(id, data) {
  return request.put(`/api/v1/device-ledger/${id}`, data)
}

export function removeDevice(id, data) {
  return request.post(`/api/v1/device-ledger/${id}/remove`, data)
}

export function checkWarranty(itemSn) {
  return request.get(`/api/v1/device-ledger/warranty/${itemSn}`)
}