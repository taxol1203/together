<template>
  <div class="home"></div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'OauthCallback',
  components: {},
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()

    onMounted(async () => {
      const platform = route.params.platform
      const urlSearchParams = new URLSearchParams(window.location.search)
      const params = Object.fromEntries(urlSearchParams.entries())
      const code = params.code
      try {
        // Loading spinner
        await store.dispatch('auth/oauthLogin', {
          platform,
          code,
        })
        router.push({ name: 'ContentList' })
      } catch (error) {
        alert(error)
      }
    })
    return {
      store,
      route,
      router,
    }
  },
})
</script>

<style lang="scss" scoped></style>
