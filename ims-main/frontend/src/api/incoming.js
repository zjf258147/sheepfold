import request from '@/utils/request'

export function listIncomingReceipts(params) {
  return request.get('/api/v1/incoming/receipts', { params })
}

export function getIncomingReceipt(id) {
  return request.get(`/api/v1/incoming/receipts/${id}`)
}

export function createIncomingReceipt(data) {
  return request.post('/api/v1/incoming/receipts', data)
}

export function updateIncomingReceipt(id, data) {
  return request.put(`/api/v1/incoming/receipts/${id}`, data)
}

export function listIncomingInspections(receiptId) {
  return request.get(`/api/v1/incoming/receipts/${receiptId}/inspections`)
}

export function createIncomingInspection(data) {
  return request.post('/api/v1/incoming/inspections', data)
}

export function createIncomingReturn(data) {
  return request.post('/api/v1/incoming/returns', data)
}

export function exportIncomingReceipts(params) {
  return request.get('/api/v1/incoming/receipts/export', { params, responseType: 'blob' })
}