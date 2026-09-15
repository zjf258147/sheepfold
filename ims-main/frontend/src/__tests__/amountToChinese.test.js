import { describe, it, expect } from 'vitest'
import { amountToChinese, formatAmount, paginateItems } from '@/print/print-utils'

describe('amountToChinese', () => {
  it('零元', () => {
    expect(amountToChinese(0)).toBe('零元整')
  })

  it('零元（浮点数）', () => {
    expect(amountToChinese(0.00)).toBe('零元整')
  })

  it('整百元', () => {
    expect(amountToChinese(100)).toBe('壹佰元整')
  })

  it('整百元（浮点数）', () => {
    expect(amountToChinese(100.00)).toBe('壹佰元整')
  })

  it('只有角', () => {
    expect(amountToChinese(0.50)).toBe('伍角整')
  })

  it('元角分组合', () => {
    expect(amountToChinese(1234.56)).toBe('壹仟贰佰叁拾肆元伍角陆分')
  })

  it('万元', () => {
    expect(amountToChinese(10000)).toBe('壹万元整')
  })

  it('亿元', () => {
    expect(amountToChinese(100000000)).toBe('壹亿元整')
  })

  it('最大值（千万级）', () => {
    expect(amountToChinese(99999999.99)).toBe('玖仟玖佰玖拾玖万玖仟玖佰玖拾玖元玖角玖分')
  })

  it('负数应抛出异常', () => {
    expect(() => amountToChinese(-100)).toThrow('金额不能为负数')
  })

  it('壹元整', () => {
    expect(amountToChinese(1)).toBe('壹元整')
  })

  it('拾元整', () => {
    expect(amountToChinese(10)).toBe('壹拾元整')
  })

  it('零角零分', () => {
    expect(amountToChinese(0.01)).toBe('壹分')
  })

  it('壹角', () => {
    expect(amountToChinese(0.10)).toBe('壹角整')
  })

  it('壹角零分', () => {
    expect(amountToChinese(0.11)).toBe('壹角壹分')
  })

  it('浮点精度验证（0.99）', () => {
    expect(amountToChinese(0.99)).toBe('玖角玖分')
  })

  it('最大值不含undefined', () => {
    const result = amountToChinese(99999999.99)
    expect(result).not.toContain('undefined')
  })
})

describe('formatAmount', () => {
  it('整数金额', () => {
    expect(formatAmount(100)).toBe('¥100.00')
  })

  it('小数金额', () => {
    expect(formatAmount(1234.56)).toBe('¥1,234.56')
  })

  it('零元', () => {
    expect(formatAmount(0)).toBe('¥0.00')
  })

  it('大金额千分位', () => {
    expect(formatAmount(1000000)).toBe('¥1,000,000.00')
  })

  it('浮点精度（0.1+0.2）', () => {
    expect(formatAmount(0.1 + 0.2)).toBe('¥0.30')
  })

  it('小数四舍五入', () => {
    expect(formatAmount(0.995)).toBe('¥1.00')
  })
})

describe('paginateItems', () => {
  it('25行分2页', () => {
    const items = Array.from({ length: 25 }, (_, i) => ({ row_no: i + 1 }))
    const pages = paginateItems(items)
    expect(pages.length).toBe(2)
    expect(pages[0].length).toBe(20)
    expect(pages[1].length).toBe(5)
  })

  it('空数组返回空页', () => {
    const pages = paginateItems([])
    expect(pages.length).toBe(1)
    expect(pages[0].length).toBe(0)
  })

  it('单页', () => {
    const items = Array.from({ length: 10 }, (_, i) => ({ row_no: i + 1 }))
    const pages = paginateItems(items)
    expect(pages.length).toBe(1)
    expect(pages[0].length).toBe(10)
  })

  it('正好一页（20条）', () => {
    const items = Array.from({ length: 20 }, (_, i) => ({ row_no: i + 1 }))
    const pages = paginateItems(items)
    expect(pages.length).toBe(1)
    expect(pages[0].length).toBe(20)
  })
})