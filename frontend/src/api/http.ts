import router from '@/router'
import store from '@/store'
import axios from 'axios'

const http = axios.create({
  baseURL: 'https://j5d202.p.ssafy.io/api/v1',
})

http.interceptors.request.use(function (config) {
  const accessToken = store.getters['auth/getToken']
  if (accessToken) {
    config.headers['Authorization'] = `Bearer ${accessToken}`
  }
  return config
})

http.interceptors.response.use(
  (value) => {
    return value
  },
  (error) => {
    if (error?.response?.data?.code === 'token_not_valid') {
      store.dispatch('auth/logout')
      router.push({
        name: 'Login',
      })
      alert('로그인이 필요합니다')
    }
    console.dir(error)
  }
)

export default http
