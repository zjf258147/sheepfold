import request from '@/utils/request'

const BASE = '/bom'

export function listBoms(params) {
  return request.get(`${BASE}/list`, { params })
}

export function getBom(id) {
  return request.get(`${BASE}/${id}`)
}

export function createBom(data) {
  return request.post(`${BASE}/`, data)
}

export function updateBom(id, data) {
  return request.put(`${BASE}/${id}`, data)
}

export function deleteBom(id) {
  return request.delete(`${BASE}/${id}`)
}

export function checkAvailability(bomId) {
  return request.get(`${BASE}/${bomId}/availability`)
}

const TASK_BASE = '/api/v1/production-task'

export function listTasks(params) {
  return request.get(`${TASK_BASE}/list`, { params })
}

export function createTask(data) {
  return request.post(`${TASK_BASE}/`, data)
}

export function updateTask(id, data) {
  return request.put(`${TASK_BASE}/${id}`, data)
}

export function deleteTask(id) {
  return request.delete(`${TASK_BASE}/${id}`)
}

export function exportBoms(params) {
  return request.get(`${BASE}/export`, { params, responseType: 'blob' })
}

export function exportTasks(params) {
  return request.get(`${TASK_BASE}/export`, { params, responseType: 'blob' })
}