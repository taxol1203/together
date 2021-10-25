<template>
  <div class="container">
    <div class="body">
      <div class="input-container">
        <div class="input-container__info">
          비밀번호를 초기화 합니다.
          <br />
          로그인 할 새 비밀번호를 입력하세요.
        </div>
        <div class="input-container__input-list">
          <TextInput
            v-for="(field, key) in formData"
            v-model="field.value"
            :key="key"
            :name="key"
            :field="field"
            :formData="formData"
            @submit="submit"
            @update:validate="handleUpdateValidate($event)"
          />
        </div>
        <button
          class="input-container__submit-btn"
          :class="{ disabled: !isValidFormData }"
          :disabled="!isValidFormData"
          @click="submit"
        >
          비밀번호 변경
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import TextInput from '@/components/TextInput.vue'
import {
  passwordSecurityValidator,
  passwordConfirmValidator,
} from '@/libs/validator'
import { FormDataList, ValidateData } from '@/libs/interface'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  name: 'ChangePassword',
  components: {
    TextInput,
  },
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const resetPassword = computed(() => store.state.auth.resetPassword)
    const resetEmail = computed(() => store.state.auth.resetEmail)
    const isValidFormData = computed(() => {
      const keys = Object.keys(formData.value)
      return keys.every((key) => {
        const errors = Object.keys(formData.value[key].errors)
        return formData.value[key].value !== '' && !errors.length
      })
    })
    const formData = ref<FormDataList>({
      password: {
        label: '새 비밀번호',
        type: 'password',
        value: '',
        placeholder: '새 비밀번호',
        validator: passwordSecurityValidator,
        errors: {},
      },
      passwordConfirm: {
        label: '새 비밀번호 확인',
        type: 'password',
        value: '',
        placeholder: '새 비밀번호 확인',
        validator: passwordConfirmValidator,
        errors: {},
      },
    })

    const handleUpdateValidate = (data: ValidateData) => {
      const { key, type, status, message } = data
      // message와 같이 undefined로 올 수도 있는 경우, 체크를 잘 해주어야 함
      if (!status && message) {
        formData.value[key].errors[type] = message
      } else {
        delete formData.value[key].errors[type]
      }
    }

    const submit = async () => {
      if (isValidFormData.value) {
        const new_password1 = formData.value['password'].value
        const new_password2 = formData.value['passwordConfirm'].value
        const uid = route.params.uid
        const token = route.params.token
        const response = await store.dispatch('auth/resetPasswordConfirm', {
          uid,
          token,
          new_password1,
          new_password2,
        })
        if (response.status === 200) {
          router.push({ name: 'Login' })
        }
      }
    }

    return {
      store,
      route,
      resetEmail,
      resetPassword,
      formData,
      isValidFormData,
      handleUpdateValidate,
      submit,
    }
  },
})
</script>

<style lang="scss" scoped>
.body {
  @apply flex flex-col justify-center items-center w-full h-screen -mt-20 -mb-20;

  .input-container {
    @apply grid gap-2 px-8 w-full sm:w-96;

    &__input-list {
      @apply grid gap-3 w-full;
    }
    &__info {
      @apply w-full rounded-md text-indigo-900 bg-indigo-50 px-4 py-4 mb-8 font-bold text-base text-center;
    }
    &__submit-btn {
      @apply w-full rounded-lg py-3 text-xs text-white font-bold bg-indigo-900 text-center;

      &.disabled {
        @apply opacity-50;
      }
    }
  }
}
</style>
