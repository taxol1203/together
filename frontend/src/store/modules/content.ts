import { Content, Review } from '@/libs/interfaces/content'
import { Genre } from '@/libs/interface'
import axios from 'axios'
import { Module } from 'vuex'
import { RootState } from '@/store/index'
import contentAxios from '@/api/content'

interface ProfileState {
  movies?: Content[]
  programs?: Content[]
}

export const content: Module<ProfileState, RootState> = {
  namespaced: true,
  state: {},
  mutations: {
    SET_MOVIES(state, movies) {
      state.movies = movies
    },
    REMOVE_MOVIES(state) {
      delete state.movies
    },
    SET_PROGRAMS(state, programs) {
      state.programs = programs
    },
    REMOVE_PROGRAMS(state) {
      delete state.programs
    },
  },
  actions: {
    getMovieList: async ({ getters, commit }): Promise<Content[]> => {
      if (!getters.getMovies) {
        try {
          const movies = await contentAxios.getMovieList()
          commit('SET_MOVIES', movies)
        } catch (error) {
          if (axios.isAxiosError(error)) {
            // Access to config, request, and response
            throw new Error(`${error.code}: ${error.message}`)
          } else {
            // Just a stock error
            throw new Error('알 수 없는 에러 발생')
          }
        }
      }
      return getters.getMovies
    },
    getMovie: async (_, contentId: number | string): Promise<Content> => {
      try {
        return await contentAxios.getMovie(+contentId)
      } catch (error) {
        if (axios.isAxiosError(error)) {
          // Access to config, request, and response
          throw new Error(`${error.code}: ${error.message}`)
        } else {
          // Just a stock error
          throw new Error('알 수 없는 에러 발생')
        }
      }
    },
    getMovieGenreList: async (): Promise<Genre[]> => {
      try {
        return contentAxios.getMovieGenreList()
      } catch (error: any) {
        throw new Error(error.response)
      }
    },
    getProgramList: async ({ getters, commit }): Promise<Content[]> => {
      if (!getters.getPrograms) {
        try {
          const programs = await contentAxios.getProgramList()
          commit('SET_PROGRAMS', programs)
        } catch (error) {
          if (axios.isAxiosError(error)) {
            // Access to config, request, and response
            throw new Error(`${error.code}: ${error.message}`)
          } else {
            // Just a stock error
            throw new Error('알 수 없는 에러 발생')
          }
        }
      }
      return getters.getPrograms
    },
    getProgram: async (_, contentId: number | string): Promise<Content> => {
      try {
        return await contentAxios.getProgram(+contentId)
      } catch (error) {
        if (axios.isAxiosError(error)) {
          // Access to config, request, and response
          throw new Error(`${error.code}: ${error.message}`)
        } else {
          // Just a stock error
          throw new Error('알 수 없는 에러 발생')
        }
      }
    },
    getProgramGenreList: async (): Promise<Genre[]> => {
      try {
        return await contentAxios.getProgramGenreList()
      } catch (error: any) {
        throw new Error(error.response)
      }
    },
    postReview: async (_, { submitData, contentType }): Promise<Review> => {
      try {
        return await contentAxios.postReview(submitData, contentType)
      } catch (error: any) {
        throw new Error(error)
      }
    },
  },
  getters: {
    getMovies(state) {
      return state.movies
    },
    getPrograms(state) {
      return state.programs
    },
  },
}
