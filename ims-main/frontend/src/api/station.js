import request from '@/utils/request'

export function listStations(params) {
  return request.get('/api/v1/stations', { params })
}

export function listAllActiveStations() {
  return request.get('/api/v1/stations/all')
}

export function getStation(id) {
  return request.get(`/api/v1/stations/${id}`)
}

export function createStation(data) {
  return request.post('/api/v1/stations', data)
}

export function updateStation(id, data) {
  return request.put(`/api/v1/stations/${id}`, data)
}

export function deleteStation(id) {
  return request.delete(`/api/v1/stations/${id}`)
}