import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/tailwind.css'

if (localStorage.getItem('accessToken') && localStorage.getItem('user')) {
  const accessToken = localStorage.getItem('accessToken')
  const refreshToken = localStorage.getItem('refreshToken')

  store.commit('auth/SET_TOKEN', { accessToken, refreshToken })
  // 임시
  store.commit('auth/SET_USER', JSON.parse(localStorage.getItem('user') || ''))
  // 임시
}

createApp(App).use(store).use(router).mount('#app')
