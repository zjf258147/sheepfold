/**
 * 将 ISO 等时间字符串格式化为 YYYY-MM-DD HH:mm:ss。
 */
export function formatDateTime(value) {
  if (value == null || value === '') return '-'

  const str = String(value).trim()
  const match = str.match(/^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})/)
  if (match) return `${match[1]} ${match[2]}`

  const date = new Date(str)
  if (Number.isNaN(date.getTime())) return str

  const pad = (n) => String(n).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
}

/** el-table-column formatter 用法。 */
export function dateTimeColumnFormatter(_row, _column, cellValue) {
  return formatDateTime(cellValue)
}

const pad = (n) => String(n).padStart(2, '0')

/** 计算默认日期范围 [start, end]，end=今天。 */
export function defaultDateRange({ months = 1, days = 0 } = {}) {
  const end = new Date()
  const start = new Date()
  if (days > 0) start.setDate(end.getDate() - days)
  else start.setMonth(end.getMonth() - months)
  const fmt = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
  return [fmt(start), fmt(end)]
}

/** el-date-picker daterange/datetimerange 快捷选项（end=今天）。 */
export const dateRangeShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 7 * 24 * 60 * 60 * 1000)
      return [start, end]
    },
  },
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setMonth(start.getMonth() - 1)
      return [start, end]
    },
  },
  {
    text: '最近半年',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setMonth(start.getMonth() - 6)
      return [start, end]
    },
  },
  {
    text: '最近一年',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setFullYear(start.getFullYear() - 1)
      return [start, end]
    },
  },
  {
    text: '最近两年',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setFullYear(start.getFullYear() - 2)
      return [start, end]
    },
  },
]