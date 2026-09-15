const CN_NUMS = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
const CN_UNITS = ['', '拾', '佰', '仟']
const CN_BIG_UNITS = ['', '万', '亿']

function integerToChinese(num: number): string {
  if (num === 0) return '零'
  let result = ''
  let unitIndex = 0
  while (num > 0) {
    const segment = num % 10000
    if (segment > 0) {
      let segStr = ''
      let temp = segment
      for (let i = 0; i < 4 && temp > 0; i++) {
        const digit = temp % 10
        if (digit > 0) {
          segStr = CN_NUMS[digit] + CN_UNITS[i] + segStr
        } else if (segStr && !segStr.startsWith('零')) {
          segStr = '零' + segStr
        }
        temp = Math.floor(temp / 10)
      }
      if (segStr.endsWith('零')) segStr = segStr.slice(0, -1)
      result = segStr + CN_BIG_UNITS[unitIndex] + result
    } else if (result) {
      result = '零' + result
    }
    num = Math.floor(num / 10000)
    unitIndex++
  }
  if (result.endsWith('零')) result = result.slice(0, -1)
  return result
}

export function amountToChinese(amount: number): string {
  if (amount < 0) throw new Error('金额不能为负数')
  if (amount === 0) return '零元整'
  const totalFen = Math.round(amount * 100)
  const yuan = Math.floor(totalFen / 100)
  const jiao = Math.floor((totalFen % 100) / 10)
  const fen = totalFen % 10

  let result = ''
  if (yuan > 0) {
    result += integerToChinese(yuan) + '元'
  }
  if (jiao > 0) {
    result += CN_NUMS[jiao] + '角'
  }
  if (fen > 0) {
    result += CN_NUMS[fen] + '分'
  }
  if (jiao === 0 && fen === 0 && yuan > 0) {
    result += '整'
  }
  if (yuan === 0 && jiao > 0 && fen === 0) {
    result += '整'
  }
  return result
}

export function formatAmount(amount: number): string {
  return '¥' + amount.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

export const COMPANY_INFO = {
  fullName: '西安敦临计量检测有限公司',
  shortName: '敦临计量',
}

export const PAGE_SIZE = 20

export function paginateItems<T>(items: T[], pageSize: number = PAGE_SIZE): T[][] {
  const pages: T[][] = []
  for (let i = 0; i < items.length; i += pageSize) {
    pages.push(items.slice(i, i + pageSize))
  }
  return pages.length > 0 ? pages : [[]]
}

export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return ''
  return dateStr.slice(0, 10)
}

export function formatDateTime(dateStr: string | null | undefined): string {
  if (!dateStr) return ''
  return dateStr.replace('T', ' ')
}