<template>
  <div class="grid gap-1">
    <div class="input-container">
      <div class="input-wrapper">
        <input
          :id="name"
          :class="{ active: labelActive, isError: isError }"
          autocomplete="off"
          :type="field.type"
          :value="modelValue"
          @blur="handleBlur"
          @focus="handleFocus"
          @input="handleInput"
          @keydown.enter="$emit('submit')"
        />
        <label
          class="placeholder"
          :class="{ active: labelActive, isError: isError }"
          :for="name"
        >
          <p v-if="labelActive">{{ field.label }}</p>
          <p v-else>{{ field.placeholder }}</p>
        </label>
      </div>
      <div
        class="error-list"
        v-if="field.errors && Object.keys(field.errors).length"
      >
        <p
          v-for="(error, key) in field.errors"
          :key="key"
          class="error-list__item"
        >
          {{ error }}
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref, watchEffect } from 'vue'
import { FormData, FormField, InputEvent } from '@/libs/interface'

export default defineComponent({
  name: 'TextInput',
  props: {
    field: {
      type: Object as PropType<FormField>,
      required: true,
    },
    modelValue: {
      type: [String, Number],
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    formData: {
      type: Object as PropType<FormData>,
      required: true,
    },
  },
  emits: ['update:modelValue', 'update:validate'],
  setup(props, { emit }) {
    const labelActive = ref<boolean>(props.modelValue !== '')
    const isError = computed(() =>
      Object.keys(props.field.errors).length === 0 ? false : true
    )

    const validate = (value: string | number) => {
      const name = props.name
      const validators = props.field?.validators

      // validator가 없다면
      if (!validators || validators.length == 0) return

      // 모든 validator를 순회하며, 유효성 검사 시작
      validators.forEach((validator) => {
        const validateRes = validator(name, value)
        emit('update:validate', validateRes)
      })
    }

    const handleBlur = (event: InputEvent<HTMLInputElement>) => {
      if (event.target.value !== '') {
        validate(event.target.value)
      }
      labelActive.value = props.modelValue !== '' ? true : false
    }

    const handleFocus = () => {
      labelActive.value = true
    }

    const handleInput = (event: InputEvent<HTMLInputElement>) => {
      // modelValue를 먼저 업데이트 해 줘야 validate가 정상적인 로직으로 진행된다.
      const value =
        props.field.type === 'number' ? +event.target.value : event.target.value
      emit('update:modelValue', value)
      if (props.field?.errors) {
        validate(value)
      }
    }

    watchEffect(() => {
      labelActive.value = props.modelValue !== ''
    })

    return {
      labelActive,
      isError,
      handleBlur,
      handleFocus,
      handleInput,
    }
  },
})
</script>

<style lang="scss" scoped>
.input-container {
  @apply relative w-full grid gap-1;

  .input-wrapper {
    @apply relative text-sm w-full;

    input {
      @apply w-full p-4 z-10 outline-none rounded-md bg-transparent border border-gray-300;

      &:focus {
        @apply border-indigo-900;
      }

      &.isError {
        @apply border-red-500;
      }
    }

    .placeholder {
      @apply absolute top-3 left-4 p-1 text-sm font-medium text-gray-300 transition-all cursor-text bg-white rounded-md;
      transform: translateY(0);

      &.active {
        @apply text-sm text-indigo-900;
        transform: translateY(-100%);
      }
      &.isError {
        @apply text-red-500;
      }
    }
  }
  .error-list {
    @apply grid gap-1;

    &__item {
      @apply text-sm text-red-500;
    }
  }
}
</style>
