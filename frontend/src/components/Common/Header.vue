<template>
  <header>
    <router-link class="logo" :to="{ name: 'ContentList' }">
      <div class="logo-wrapper">
        <img src="@/assets/images/logo.png" alt="로고" />
      </div>
    </router-link>
    <nav>
      <router-link :to="{ name: 'ContentList' }">OTT 추천</router-link>
      <router-link :to="{ name: 'PartyList' }">OTT 파티</router-link>
    </nav>
    <div>
      <router-link class="btn login" v-if="!isLogin" :to="{ name: 'Login' }">
        로그인
      </router-link>
      <div class="flex gap-2" v-else>
        <router-link
          class="btn"
          :to="{ name: 'ProfileMain', params: { userId: user.id } }"
        >
          {{ user.username }}
        </router-link>
        <button class="btn logout" @click="handleClickLogoutBtn">
          로그아웃
        </button>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default defineComponent({
  setup() {
    const store = useStore()
    const route = useRouter()
    const isLogin = computed(() => store.getters['auth/isLogin'])
    const user = computed(() => store.state.auth.user)

    const handleClickLogoutBtn = () => {
      store.dispatch('auth/logout')
      route.push({ name: 'ContentList' })
    }

    return { user, isLogin, handleClickLogoutBtn }
  },
})
</script>

<style lang="scss" scoped>
header {
  @apply flex justify-between items-center w-full h-16 border-b px-4;

  .logo-wrapper {
    @apply overflow-hidden w-20 h-10;

    img {
      @apply object-contain object-center;
    }
  }

  nav {
    @apply hidden md:flex mx-auto gap-20;

    a {
      @apply text-lg font-bold text-gray-300;
    }

    .router-link-active {
      @apply text-indigo-900;
    }
  }

  .btn {
    @apply text-sm text-white font-bold py-2 px-4 rounded-full bg-indigo-900;

    &.logout {
      @apply bg-white text-gray-700 rounded;

      &:hover {
        @apply bg-gray-100;
      }
    }
  }
}
</style>
