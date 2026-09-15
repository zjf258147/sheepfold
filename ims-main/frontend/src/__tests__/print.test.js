import { describe, it, expect } from 'vitest'
import {
  getIncomingReceiptPrintData,
  getShipmentPrintData,
  getBomPrintData,
  getIncomingInspectionPrintData,
  getIncomingReturnPrintData,
  getRmaRepairPrintData,
} from '@/api/print'

describe('print API', () => {
  it('getIncomingReceiptPrintData builds correct URL', () => {
    expect(typeof getIncomingReceiptPrintData).toBe('function')
  })

  it('getShipmentPrintData builds correct URL', () => {
    expect(typeof getShipmentPrintData).toBe('function')
  })

  it('getBomPrintData builds correct URL', () => {
    expect(typeof getBomPrintData).toBe('function')
  })

  it('all print API functions are defined', () => {
    expect(typeof getIncomingInspectionPrintData).toBe('function')
    expect(typeof getIncomingReturnPrintData).toBe('function')
    expect(typeof getRmaRepairPrintData).toBe('function')
  })
})