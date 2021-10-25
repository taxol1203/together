export type Provider = '넷플릭스' | '왓챠' | '웨이브' | ''

export interface Party {
  id: number
  payments: {
    id: number
    nickName: string
  }[]
  host: {
    id: number
    nickName: string
    username: string
    phoneNumber: string
  }
  title: string
  desc: string
  memberLimit: number
  serviceId: string
  servicePassword: string
  endDate: string
  pricePerDay: number
  provider: {
    id: number
    name: string
    pricePerDay: number
    logoUrl: string
  }
}

export interface PartyProvider {
  id: number
  name: 'Netflix' | 'wavve' | 'Watcha'
  pricePerDay: number
  logoUrl: number
}
