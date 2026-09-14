import request from '@/utils/request'

export function listCustomers(params) {
  return request.get('/api/v1/customers', { params })
}

export function createCustomer(data) {
  return request.post('/api/v1/customers', data)
}

export function updateCustomer(id, data) {
  return request.put(`/api/v1/customers/${id}`, data)
}