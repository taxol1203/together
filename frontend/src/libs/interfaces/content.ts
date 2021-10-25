// export interface Content {
//   id: number
//   title: string
//   posterPath: string
//   simRate: number
//   providers: string[]
//   firstAirYear: number
//   rated: string
//   seasons: number
//   overview: string
// }

export interface Youtube {
  id: {
    kind: string
    videoId: string
  }
  snippet: {
    title: string
    thumbnails: {
      medium?: {
        url: string
      }
      high?: {
        url: string
      }
    }
  }
}

export interface Comment {
  id: number
  user: {
    nickName: string
    profileImg: string
  }
  comment: string
  like: number
  rating: number
}

export interface Genre {
  id: number
  name: string
  kName: string
  genreId: number
}

export type ProviderNameEn =
  | 'Netflix'
  | 'Watcha'
  | 'Naver Store'
  | 'wavve'
  | 'Amazon Prime Video'
  | 'Disney Plus'
  | 'Google Play Movies'

interface Provider {
  id: number
  logoUrl: string
  name: ProviderNameEn
  pricePerDay: number
}

export interface Content {
  id: number
  movieId: number
  originalTitle: string
  title: string
  overview: string
  posterPath: string
  releaseDate: string
  providers: Provider[]
  recommends: {
    [key: string]: string
  }[]
  genres: Genre[]
  reviews: Review[]
}

export type ProviderFilter = {
  name: ProviderNameEn
  active: boolean
}[]

export interface Review {
  id: number
  userId: string
  rating: number
  content: string
  programId?: number
  movieId?: number
}
