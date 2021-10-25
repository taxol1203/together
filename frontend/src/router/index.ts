import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import store from '@/store'

import AuthLayout from '@/layouts/AuthLayout.vue'
import ContentLayout from '@/layouts/ContentLayout.vue'
import PartyLayout from '@/layouts/PartyLayout.vue'
import ProfileLayout from '@/layouts/ProfileLayout.vue'
import ProfileMain from '@/views/ProfileMain.vue'
import ProfileEdit from '@/views/ProfileEdit.vue'
import ProfileChangePassword from '@/views/ProfileChangePassword.vue'
import ProfileParty from '@/views/ProfileParty.vue'
import ProfileGenre from '@/views/ProfileGenre.vue'
import ContentList from '@/views/ContentList.vue'
import ContentDetail from '@/views/ContentDetail.vue'
import PartyList from '@/views/PartyList.vue'
import PartyDetail from '@/views/PartyDetail.vue'
import PartyJoin from '@/views/PartyJoin.vue'
import PartyJoinConfirm from '@/views/PartyJoinConfirm.vue'
import PartyCreate from '@/views/PartyCreate.vue'

import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import ResetPassword from '@/views/ResetPassword.vue'
import ResetPasswordConfirm from '@/views/ResetPasswordConfirm.vue'

import OauthCallback from '@/views/OauthCallback.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'ContentLayout',
    component: ContentLayout,
    children: [
      {
        path: '',
        name: 'ContentList',
        component: ContentList,
      },
      {
        path: ':contentType/:contentId',
        name: 'ContentDetail',
        component: ContentDetail,
        props: true,
      },
    ],
  },
  {
    path: '/party',
    name: 'PartyLayout',
    component: PartyLayout,
    children: [
      {
        path: '',
        name: 'PartyList',
        component: PartyList,
      },
      {
        path: ':partyId',
        name: 'PartyDetail',
        component: PartyDetail,
        props: true,
      },
      {
        path: 'create',
        name: 'PartyCreate',
        component: PartyCreate,
        meta: { requiresAuth: true },
      },
      {
        path: ':partyId/join',
        name: 'PartyJoin',
        component: PartyJoin,
        props: true,
        meta: { requiresAuth: true },
      },
      {
        path: ':partyId/join/confirm',
        name: 'PartyJoinConfirm',
        component: PartyJoinConfirm,
        props: true,
        meta: { requiresAuth: true },
      },
    ],
  },
  {
    path: '/auth',
    name: 'AuthLayout',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        name: 'Login',
        component: Login,
        meta: { requiresNoAuth: true },
      },
      {
        path: 'reset-password',
        name: 'ResetPassword',
        component: ResetPassword,
        meta: { requiresNoAuth: true },
      },
      {
        path: 'reset-password-confirm/:uid/token/:token/',
        name: 'ResetPasswordConfirm',
        component: ResetPasswordConfirm,
        meta: { requiresNoAuth: true },
      },
      {
        path: 'register',
        name: 'Register',
        component: Register,
        meta: { requiresNoAuth: true },
      },
      {
        path: ':platform/callback',
        name: 'OauthCallback',
        component: OauthCallback,
        props: true,
        meta: { requiresNoAuth: true },
      },
      {
        path: 'social-login-success',
        name: 'SocialLoginSuccess',
        redirect: { name: 'ContentList' },
        meta: { requiresNoAuth: true },
      },
    ],
  },
  {
    path: '/profile',
    name: 'ProfileLayout',
    component: ProfileLayout,
    children: [
      {
        path: ':userId',
        name: 'ProfileMain',
        component: ProfileMain,
        props: true,
      },
      {
        path: 'edit',
        name: 'ProfileEdit',
        component: ProfileEdit,
        meta: { requiresAuth: true },
      },
      {
        path: 'changepassword',
        name: 'ProfileChangePassword',
        component: ProfileChangePassword,
        meta: { requiresAuth: true },
      },
      {
        path: ':userId/party',
        name: 'ProfileParty',
        component: ProfileParty,
      },
      {
        path: ':userId/genre',
        name: 'ProfileGenre',
        component: ProfileGenre,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.getters['auth/isLogin']) {
    alert('로그인 해야 들어올 수 있음')
    router.push({ name: 'Login' })
  }
  if (to.meta.requiresNoAuth && store.getters['auth/isLogin']) {
    alert('로그인 상태에서는 들어올 수 없음')
    router.push({ name: 'ContentList' })
  }
  next()
})

export default router
