<template>
  <Header />
  <router-view />
  <BottomNav v-if="showBottomNav" />
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue'
import Header from '@/components/Common/Header.vue'
import BottomNav from '@/components/Common/BottomNav.vue'
import { useRoute } from 'vue-router'

export default defineComponent({
  components: { Header, BottomNav },
  setup() {
    const route = useRoute()
    const showBottomNav = computed(() => {
      return route.matched.length
        ? route.matched[0].name !== 'AuthLayout'
        : true
    })

    return { route, showBottomNav }
  },
})
</script>

<style lang="scss">
#app {
  @apply min-h-screen;
}
</style>
