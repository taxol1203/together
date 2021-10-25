<template>
  <ProfileHeader />
  <router-view />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ProfileHeader from '@/components/ProfileHeader.vue'

export default defineComponent({
  name: 'ProfileLayout',
  components: {
    ProfileHeader,
  },
  setup() {
    return {}
  },
})
</script>

<style lang="scss" scoped>
.profile-main__navbar__button {
  @apply flex justify-center items-center h-14 border border-gray-300;

  a {
    @apply font-semibold text-gray-300;
  }

  .router-link-exact-active {
    @apply text-indigo-900;
  }
}

.profile-main__navbar__button--space {
  @apply ml-6;
}
</style>
