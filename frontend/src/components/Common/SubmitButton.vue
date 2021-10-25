<template>
  <button>{{ label }}</button>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'SubmitButton',
  props: {
    label: {
      type: String,
      required: true,
    },
  },
  setup() {
    return {}
  },
})
</script>

<style lang="scss" scoped>
button {
  @apply py-4 rounded-xl bg-indigo-900 text-white font-bold w-full max-w-xs mx-auto;
}
</style>
