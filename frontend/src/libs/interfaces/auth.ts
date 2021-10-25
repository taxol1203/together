import { Party } from '@/libs/interfaces/party'

export interface Token {
  accessToken: string
  refreshToken: string
}

export type InputUser = {
  id: number
  username: string
  nick_name: string
  phone_number: string
  email: string
  fav_movie_genres?: {
    id: number
    name: string
    k_name: string
  }[]
  fav_program_genres?: {
    id: number
    name: string
    k_name: string
  }[]
  payments?: Party[]
}

export type OutputUser = {
  id: number
  username: string
  nickName: string
  phoneNumber: string
  email: string
  favMovieGenres?: {
    id: number
    name: string
    kName: string
  }[]
  favProgramGenres?: {
    id: number
    number: string
    kName: string
  }[]
  payments?: Party[]
}
