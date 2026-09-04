import request from '@/utils/request'

export function listRmaReturns(params) {
  return request.get('/rma/returns', { params })
}

export function getRmaReturn(id) {
  return request.get(`/rma/returns/${id}`)
}

export function createRmaReturn(data) {
  return request.post('/rma/returns', data)
}

export function assignRmaReturn(id, data) {
  return request.post(`/rma/returns/${id}/assign`, data)
}

export function transferRmaReturn(id, data) {
  return request.post(`/rma/returns/${id}/transfer`, data)
}

export function getRmaDiagnoses(returnId) {
  return request.get(`/rma/returns/${returnId}/diagnoses`)
}

export function createRmaDiagnosis(data) {
  return request.post('/rma/diagnoses', data)
}

export function getRmaRepairs(returnId) {
  return request.get(`/rma/returns/${returnId}/repairs`)
}

export function createRmaRepair(data) {
  return request.post('/rma/repairs', data)
}

export function getRmaScraps(returnId) {
  return request.get(`/rma/returns/${returnId}/scraps`)
}

export function createRmaScrap(data) {
  return request.post('/rma/scraps', data)
}

export function approveRmaScrap(id, data) {
  return request.post(`/rma/scraps/${id}/approve`, data)
}

export function getRmaReships(returnId) {
  return request.get(`/rma/returns/${returnId}/reships`)
}

export function createRmaReship(data) {
  return request.post('/rma/reships', data)
}