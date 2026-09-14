import request from '@/utils/request'

export function listRmaReturns(params) {
  return request.get('/api/v1/rma/returns', { params })
}

export function getRmaReturn(id) {
  return request.get(`/api/v1/rma/returns/${id}`)
}

export function createRmaReturn(data) {
  return request.post('/api/v1/rma/returns', data)
}

export function assignRmaReturn(id, data) {
  return request.post(`/api/v1/rma/returns/${id}/assign`, data)
}

export function transferRmaReturn(id, data) {
  return request.post(`/api/v1/rma/returns/${id}/transfer`, data)
}

export function getRmaDiagnoses(returnId) {
  return request.get(`/api/v1/rma/returns/${returnId}/diagnoses`)
}

export function createRmaDiagnosis(data) {
  return request.post('/api/v1/rma/diagnoses', data)
}

export function getRmaRepairs(returnId) {
  return request.get(`/api/v1/rma/returns/${returnId}/repairs`)
}

export function createRmaRepair(data) {
  return request.post('/api/v1/rma/repairs', data)
}

export function getRmaScraps(returnId) {
  return request.get(`/api/v1/rma/returns/${returnId}/scraps`)
}

export function createRmaScrap(data) {
  return request.post('/api/v1/rma/scraps', data)
}

export function approveRmaScrap(id, data) {
  return request.post(`/api/v1/rma/scraps/${id}/approve`, data)
}

export function exportRmaReturns(params) {
  return request.get('/api/v1/rma/export', { params, responseType: 'blob' })
}

export function getRmaReships(returnId) {
  return request.get(`/api/v1/rma/returns/${returnId}/reships`)
}

export function createRmaReship(data) {
  return request.post('/api/v1/rma/reships', data)
}

export function getRmaQualityChecks(returnId) {
  return request.get(`/api/v1/rma/returns/${returnId}/quality-checks`)
}

export function createRmaQualityCheck(data) {
  return request.post('/api/v1/rma/quality-checks', data)
}

export function getRmaWarehouseIns(returnId) {
  return request.get(`/api/v1/rma/returns/${returnId}/warehouse-ins`)
}

export function createRmaWarehouseIn(data) {
  return request.post('/api/v1/rma/warehouse-ins', data)
}