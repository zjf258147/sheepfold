import request from '@/utils/request'

export function getIncomingReceiptPrintData(id) {
  return request.get(`/api/v1/print/incoming_receipt/${id}`)
}

export function getIncomingReceiptBatchPrintData(ids) {
  return Promise.all(ids.map(id => request.get(`/api/v1/print/incoming_receipt/${id}`)))
}

export function getShipmentPrintData(id) {
  return request.get(`/api/v1/print/shipment/${id}`)
}

export function getShipmentBatchPrintData(ids) {
  return Promise.all(ids.map(id => request.get(`/api/v1/print/shipment/${id}`)))
}

export function getIncomingInspectionPrintData(id) {
  return request.get(`/api/v1/print/incoming_inspection/${id}`)
}

export function getIncomingInspectionBatchPrintData(ids) {
  return Promise.all(ids.map(id => request.get(`/api/v1/print/incoming_inspection/${id}`)))
}

export function getIncomingReturnPrintData(id) {
  return request.get(`/api/v1/print/incoming_return/${id}`)
}

export function getIncomingReturnBatchPrintData(ids) {
  return Promise.all(ids.map(id => request.get(`/api/v1/print/incoming_return/${id}`)))
}

export function getRmaRepairPrintData(id) {
  return request.get(`/api/v1/print/rma_repair/${id}`)
}

export function getRmaRepairBatchPrintData(ids) {
  return Promise.all(ids.map(id => request.get(`/api/v1/print/rma_repair/${id}`)))
}

export function getBomPrintData(id) {
  return request.get(`/api/v1/print/bom/${id}`)
}

export function getBomBatchPrintData(ids) {
  return Promise.all(ids.map(id => request.get(`/api/v1/print/bom/${id}`)))
}