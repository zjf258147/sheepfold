import { describe, it, expect } from 'vitest'
import { formatDateTime, dateTimeColumnFormatter } from '@/utils/datetime'

describe('formatDateTime', () => {
  it('null or empty returns dash', () => {
    expect(formatDateTime(null)).toBe('-')
    expect(formatDateTime(undefined)).toBe('-')
    expect(formatDateTime('')).toBe('-')
  })

  it('ISO string with T separator', () => {
    expect(formatDateTime('2026-09-10T08:30:00')).toBe('2026-09-10 08:30:00')
  })

  it('ISO string with space separator', () => {
    expect(formatDateTime('2026-09-10 08:30:00')).toBe('2026-09-10 08:30:00')
  })

  it('Date object', () => {
    const d = new Date(2026, 8, 10, 8, 30, 0) // month is 0-indexed
    expect(formatDateTime(d)).toBe('2026-09-10 08:30:00')
  })

  it('returns original string for unparseable input', () => {
    expect(formatDateTime('not-a-date')).toBe('not-a-date')
  })

  it('single digit month and day pad correctly', () => {
    expect(formatDateTime('2026-01-05T03:07:09')).toBe('2026-01-05 03:07:09')
  })

  it('trailing whitespace is trimmed', () => {
    expect(formatDateTime('  2026-09-10T08:30:00  ')).toBe('2026-09-10 08:30:00')
  })
})

describe('dateTimeColumnFormatter', () => {
  it('delegates to formatDateTime', () => {
    expect(dateTimeColumnFormatter(null, null, '2026-09-10T08:30:00')).toBe('2026-09-10 08:30:00')
    expect(dateTimeColumnFormatter(null, null, null)).toBe('-')
  })
})