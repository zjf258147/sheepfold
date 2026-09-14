import request from '@/utils/request'

export function listStocktakes(params) {
  return request.get('/api/v1/stocktakes', { params })
}

export function getStocktake(id) {
  return request.get(`/api/v1/stocktakes/${id}`)
}

export function getStocktakeLines(id) {
  return request.get(`/api/v1/stocktakes/${id}/lines`)
}

export function createStocktake(data) {
  return request.post('/api/v1/stocktakes', data)
}

export function scanItems(id, data) {
  return request.post(`/api/v1/stocktakes/${id}/scan`, data)
}

export function updateLineReason(lineId, data) {
  return request.put(`/api/v1/stocktakes/lines/${lineId}`, data)
}

export function completeStocktake(id, data) {
  return request.post(`/api/v1/stocktakes/${id}/complete`, data)
}

export function cancelStocktake(id) {
  return request.post(`/api/v1/stocktakes/${id}/cancel`)
}