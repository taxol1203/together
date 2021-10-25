export const getRestDays = (endDate: string): number => {
  return Math.floor(
    (new Date(endDate).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)
  )
}

export const toCurrency = (price: number): string => {
  return `${String(price).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}원`
}

type InnerObj = {
  [key: string]: string | number
}

type Obj = {
  [key: string]: string | number | InnerObj
}

const isArray = (a: any) => Array.isArray(a)
const isObject = (o: any) =>
  o === Object(o) && !Array.isArray(o) && typeof o !== 'function'

const toCamel = (s: string) => {
  return s.replace(/([-_][a-z])/gi, ($1) => {
    return $1.toUpperCase().replace('-', '').replace('_', '')
  })
}

const to_snake = (s: string) => {
  return s.replace(/([A-Z])/g, ($1) => {
    return `_${$1.toUpperCase()}`
  })
}

export const keysToCamel = (o: any) => {
  if (isObject(o)) {
    const n: Obj = {}

    Object.keys(o).forEach((k) => {
      n[toCamel(k)] = keysToCamel(o[k])
    })

    return n
  } else if (isArray(o)) {
    return o.map((i: any) => {
      return keysToCamel(i)
    })
  }

  return o
}

export const keys_to_snake = (o: any) => {
  if (isObject(o)) {
    const n: Obj = {}

    Object.keys(o).forEach((k) => {
      n[to_snake(k)] = keys_to_snake(o[k])
    })

    return n
  } else if (isArray(o)) {
    return o.map((i: any) => {
      return keys_to_snake(i)
    })
  }

  return o
}
