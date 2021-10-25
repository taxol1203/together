import http from '@/api/http'
import { keysToCamel } from '@/libs/func'
import { Genre } from '@/libs/interface'
import { Content, Review } from '@/libs/interfaces/content'

const getMovieList = async (): Promise<Content[]> => {
  try {
    const res = await http.get(`/movies/`)
    return keysToCamel(res.data)
  } catch (error: any) {
    throw new Error(error)
  }
}

const getMovie = async (contentId: number): Promise<Content> => {
  try {
    const res = await http.get(`/movies/${contentId}/`)
    return keysToCamel(res.data)
  } catch (error: any) {
    throw new Error(error)
  }
}

const getMovieGenreList = async (): Promise<Genre[]> => {
  try {
    const res = await http.get(`/movies/genre/`)
    return keysToCamel(res.data)
  } catch (error: any) {
    throw new Error(error)
  }
}

const getProgramList = async (): Promise<Content[]> => {
  try {
    const res = await http.get(`/programs/`)
    return keysToCamel(res.data)
  } catch (error: any) {
    throw new Error(error)
  }
}

const getProgram = async (contentId: number): Promise<Content> => {
  try {
    const res = await http.get(`/programs/${contentId}/`)
    return keysToCamel(res.data)
  } catch (error: any) {
    throw new Error(error)
  }
}

const getProgramGenreList = async (): Promise<Genre[]> => {
  try {
    const res = await http.get(`/programs/genre/`)
    return keysToCamel(res.data)
  } catch (error: any) {
    throw new Error(error)
  }
}

const postReview = async (
  submitData: {
    [key: string]: string | number
  },
  contentType: 'movies' | 'programs'
): Promise<Review> => {
  try {
    const res = await http.post(`/${contentType}/review/`, submitData)
    console.log(res)
    return keysToCamel(res.data)
  } catch (error: any) {
    throw new Error(error)
  }
}

export default {
  getMovieList,
  getMovie,
  getMovieGenreList,
  getProgramList,
  getProgram,
  getProgramGenreList,
  postReview,
}
