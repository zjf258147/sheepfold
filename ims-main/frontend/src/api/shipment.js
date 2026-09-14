import request from '@/utils/request'

const BASE = '/shipment'

export function listShipments(params) {
  return request.get(`${BASE}/list`, { params })
}

export function getShipment(id) {
  return request.get(`${BASE}/${id}`)
}

export function createShipment(data) {
  return request.post(`${BASE}/`, data)
}

export function updateShipment(id, data) {
  return request.put(`${BASE}/${id}`, data)
}

export function deleteShipment(id) {
  return request.delete(`${BASE}/${id}`)
}