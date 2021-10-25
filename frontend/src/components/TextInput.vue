<template>
  <div class="grid gap-1">
    <div class="input-container">
      <input
        autocomplete="off"
        :type="field.type"
        :value="modelValue"
        :class="{ active: labelActive, isError: isError }"
        :id="name"
        @blur="handleBlur"
        @focus="handleFocus"
        @input="handleInput"
        @keydown.enter="$emit('submit')"
      />
      <label
        class="input-container__placeholder"
        :class="{ active: labelActive, isError: isError }"
        :for="name"
      >
        <p v-if="labelActive">{{ field.label }}</p>
        <p v-else>{{ field.placeholder }}</p>
      </label>
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
import { computed, defineComponent, PropType, ref, watch } from 'vue'
import {
  FormDataList,
  FormDataListItem,
  ValidateParam,
  ValidateData,
  InputEvent,
} from '@/libs/interface'

export default defineComponent({
  name: 'TextInput',
  props: {
    field: {
      type: Object as PropType<FormDataListItem>,
      required: true,
    },
    modelValue: {
      type: String,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    formData: {
      type: Object as PropType<FormDataList>,
      required: true,
    },
  },
  emits: ['update:modelValue', 'update:validate'],
  setup(props, { emit }) {
    const modelValue = computed(() => props.modelValue)
    const labelActive = ref<boolean>(Boolean(props.modelValue))
    const isError = computed(() =>
      Object.keys(props.field.errors).length === 0 ? false : true
    )

    const validate = (text: string) => {
      const name = props.name
      const validator = props.field.validator
      const formData = props.formData
      if (validator && name && formData) {
        const validateParam: ValidateParam = {
          key: name,
          value: text,
          form: props.field,
        }
        if (formData['password']) {
          const res: ValidateData = validator(
            validateParam,
            formData['password'].value
          )
          emit('update:validate', res)
        } else {
          const res: ValidateData = validator(validateParam)
          emit('update:validate', res)
        }
      }
    }

    const handleBlur = (event: InputEvent<HTMLInputElement>) => {
      if (event.target.value !== '') {
        validate(event.target.value)
      }
      labelActive.value = props.modelValue ? true : false
    }

    const handleFocus = () => {
      labelActive.value = true
    }

    const handleInput = (event: InputEvent<HTMLInputElement>) => {
      // modelValue를 먼저 업데이트 해 줘야 validate가 정상적인 로직으로 진행된다.
      emit('update:modelValue', event.target.value)
      if (props.field.errors) {
        validate(event.target.value)
      }
    }

    watch(modelValue, (value) => {
      // 입력값이 변할 때마다 에러 체크
      labelActive.value = Boolean(value)
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
  @apply relative w-full;

  input {
    @apply relative mb-1 text-sm outline-none px-4 py-3 rounded-md bg-transparent border border-gray-300 w-full py-2;

    &.active {
      @apply border-indigo-900;
    }
    &.isError {
      @apply border-red-500;
    }
  }
  &__placeholder {
    @apply absolute top-2 left-4 p-1 text-sm text-gray-300 transition-all cursor-text bg-white rounded-md;
    transform: translateY(0);

    &.active {
      @apply text-xs text-indigo-900;
      transform: translateY(-85%);
    }
    &.isError {
      @apply text-red-500;
    }
  }
  .error-list {
    &__item {
      @apply text-xs text-red-500;
    }
  }
}
</style>
