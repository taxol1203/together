<template>
  <nav class="profile-main__navbar__button">
    <router-link
      :to="{ name: 'ProfileMain', params: { userId: user.id } }"
      :class="{ active: !partyactive }"
    >
      <span>프로필</span>
    </router-link>
    <router-link
      :to="{ name: 'ProfileParty', params: { userId: user.id } }"
      :class="{ active: partyactive }"
      class="profile-main__navbar__button--space"
    >
      <span>파티 관리</span>
    </router-link>
  </nav>
</template>

<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'

export default defineComponent({
  setup() {
    const route = useRoute()
    const store = useStore()
    // console.log(route.path)

    const partyactive = ref<boolean>(route.path.includes('party'))
    const user = computed(() => store.state.auth.user)

    watch(
      () => route.path,
      (newroute) => {
        // console.log(newroute)
        partyactive.value = newroute.includes('party')
      }
    )
    return { partyactive, user }
  },
})
</script>

<style lang="scss" scoped>
.profile-main__navbar__button {
  @apply flex justify-center items-center gap-6 h-14 border border-gray-300;

  a {
    @apply font-semibold text-gray-300 h-full flex items-center justify-center;

    &:hover:not(.active) {
      @apply text-indigo-500;
    }
  }

  .active {
    @apply text-indigo-900;
  }
}

.profile-main__navbar__button--space {
}
</style>
