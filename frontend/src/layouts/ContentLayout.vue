<template>
  <router-view :key="$route.fullPath" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ContentLayout',
  setup() {
    return {}
  },
})
</script>

<style lang="scss" scoped></style>
