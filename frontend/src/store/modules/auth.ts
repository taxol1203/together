import * as authApi from '@/api/auth'
import { Module } from 'vuex'
import { RootState } from '@/store/index'
import { InputUser, OutputUser } from '@/libs/interfaces/auth'
import { Token } from '@/libs/interfaces/auth'
import { Genre } from '@/libs/interfaces/content'

interface authModule {
  accessToken: string
  refreshToken: string
  user?: OutputUser
}

export const auth: Module<authModule, RootState> = {
  namespaced: true,
  state: {
    accessToken: '',
    refreshToken: '',
  },
  mutations: {
    SET_TOKEN(state: authModule, { accessToken, refreshToken }: Token) {
      state.accessToken = accessToken
      state.refreshToken = refreshToken
      localStorage.setItem('accessToken', accessToken)
      localStorage.setItem('refreshToken', refreshToken)
    },
    REMOVE_TOKEN(state: authModule) {
      state.accessToken = ''
      state.refreshToken = ''
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    },
    SET_USER(state: authModule, user: OutputUser) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    REMOVE_USER(state: authModule) {
      delete state.user
      localStorage.removeItem('user')
    },
  },
  actions: {
    async login({ commit }, params) {
      const data = await authApi.login(params.email, params.password)
      alert('안녕하세요!')
      commit('SET_TOKEN', {
        accessToken: data.accessToken,
        refreshToken: data.refreshToken,
      })
      commit('SET_USER', data.user)
    },
    logout({ commit }) {
      commit('REMOVE_TOKEN')
      commit('REMOVE_USER')
    },
    async register({ commit }, submitData) {
      try {
        const data = await authApi.register(submitData)
        alert('auth modules: register success')
        // 바로 로그인
        commit('SET_TOKEN', {
          accessToken: data.accessToken,
          refreshToken: data.refreshToken,
        })
        commit('SET_USER', data.user)
        localStorage.setItem('accessToken', data.accessToken)
        localStorage.setItem('refreshToken', data.refreshToken)
        // 임시
        localStorage.setItem('user', JSON.stringify(data.user))
        // 임시
      } catch (error: any) {
        const errorKeys = Object.keys(error.response.data)
        // 에러가 여러 개일 경우, 맨 앞의 에러 하나만 띄우도록 한다.
        throw new Error(error.response.data[errorKeys[0]])
      }
    },
    async resetPassword(context, params) {
      try {
        const response = await authApi.resetPassword(params.email)
        if (response.status === 200) {
          alert(response.data.detail)
        }
        return response
      } catch (error: any) {
        alert(error.response.data)
      }
    },
    async resetPasswordConfirm(context, submitData) {
      try {
        const response = await authApi.resetPasswordConfirm(submitData)
        if (response.status === 200) {
          alert(response.data.detail)
        }
        return response
      } catch (error: any) {
        alert(error.response.data)
      }
    },
    // TODO: 임시
    async getUserData() {
      try {
        const user = await authApi.getUserData()
        return user
      } catch (error) {
        throw new Error('유저 데이터를 가져오던 중 문제가 생겼습니다')
      }
    },
    async updateUserData(
      { commit },
      payload: {
        submitData: InputUser
        userId: number
      }
    ) {
      try {
        const user: OutputUser = await authApi.putUserData(payload)
        commit('SET_USER', user)
      } catch (error: any) {
        throw new Error(error)
      }
    },
    async updateFavGenres(
      { commit },
      submitData: {
        fav_movie_genres: Genre[]
        fav_program_genres: Genre[]
      }
    ) {
      try {
        const user: OutputUser = await authApi.putUserFavGenres(submitData)
        commit('SET_USER', user)
      } catch (error: any) {
        throw new Error(error)
      }
    },
    async oauthLogin({ commit }, params) {
      try {
        const data = await authApi.oauthLogin(params.platform, params.code)
        alert(`auth modules: ${params.platform} login success`)
        commit('SET_TOKEN', {
          accessToken: data.accessToken,
          refreshToken: data.refreshToken,
        })
        commit('SET_USER', data.user)
        localStorage.setItem('accessToken', data.accessToken)
        localStorage.setItem('refreshToken', data.refreshToken)
        // 임시
        localStorage.setItem('user', JSON.stringify(data.user))
      } catch (error: any) {
        alert(error.response.data)
      }
    },
  },
  getters: {
    isLogin(state) {
      return state.accessToken !== ''
    },
    getUserPK(state) {
      return state.user?.id
    },
    getToken(state) {
      return state.accessToken
    },
    getUserNickName(state) {
      return state.user?.nickName
    },
    getUserFavMovieGenres(state) {
      return state.user?.favMovieGenres
    },
    getUserFavMovieGenreIds(state) {
      return (
        state.user?.favMovieGenres &&
        state.user.favMovieGenres.map((genre) => genre.id)
      )
    },
    getUserFavProgramGenres(state) {
      return state.user?.favProgramGenres
    },
    getUserFavProgramGenreIds(state) {
      return (
        state.user?.favProgramGenres &&
        state.user.favProgramGenres.map((genre) => genre.id)
      )
    },
  },
}
