<template>
  <div class="container">
    <div class="body">
      <div class="input-container">
        <div class="input-container__input-label primary">
          이메일 / 비밀번호
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
        <div class="input-container__input-label default">내 정보</div>
        <div class="input-container__input-list">
          <TextInput
            v-for="(field, key) in infoData"
            v-model="field.value"
            :key="key"
            :name="key"
            :field="field"
            :formData="infoData"
            @submit="submit"
            @update:validate="handleUpdateValidate($event)"
          />
        </div>
        <button
          class="input-container__submit-btn"
          :class="{
            disabled: !isValidFormData || !isValidInfoData,
          }"
          :disabled="!isValidFormData || !isValidInfoData"
          @click="submit"
        >
          <!-- TODO: 로딩 상태 분기해서 로딩스피너와 교체할 것 -->
          회원가입
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue'
import TextInput from '@/components/TextInput.vue'
import {
  emailValidator,
  passwordSecurityValidator,
  passwordConfirmValidator,
} from '@/libs/validator'
import { FormDataList, ValidateData } from '@/libs/interface'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'Register',
  components: { TextInput },
  setup() {
    const store = useStore()
    const router = useRouter()
    const formData = ref<FormDataList>({
      email: {
        label: '이메일',
        type: 'email',
        value: '',
        placeholder: '이메일',
        validator: emailValidator,
        errors: {},
      },
      password: {
        label: '비밀번호',
        type: 'password',
        value: '',
        placeholder: '비밀번호',
        validator: passwordSecurityValidator,
        errors: {},
      },
      passwordConfirm: {
        label: '비밀번호 확인',
        type: 'password',
        value: '',
        placeholder: '비밀번호 확인',
        validator: passwordConfirmValidator,
        errors: {},
      },
    })

    const infoData = ref<FormDataList>({
      nickName: {
        label: '닉네임',
        type: 'text',
        value: '',
        placeholder: '닉네임',
        errors: {},
      },
      name: {
        label: '이름',
        type: 'text',
        value: '',
        placeholder: '이름',
        errors: {},
      },
      phoneNumber: {
        label: '휴대폰 번호',
        type: 'text',
        value: '',
        placeholder: '휴대폰 번호',
        errors: {},
      },
    })

    const isValidFormData = computed(() => {
      const keys = Object.keys(formData.value)
      return keys.every((key) => {
        const errors = Object.keys(formData.value[key].errors)
        return formData.value[key].value !== '' && !errors.length
      })
    })

    const isValidInfoData = computed(() => {
      const keys = Object.keys(infoData.value)
      return keys.every((key) => {
        return infoData.value[key].value !== ''
      })
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
      if (isValidFormData.value && isValidInfoData.value) {
        const email = formData.value['email'].value
        const password1 = formData.value['password'].value
        const password2 = formData.value['passwordConfirm'].value
        const nick_name = infoData.value['nickName'].value
        const username = infoData.value['name'].value
        const phone_number = infoData.value['phoneNumber'].value
        // TODO: Add loading spinner
        try {
          await store.dispatch('auth/register', {
            email,
            password1,
            password2,
            nick_name,
            username,
            phone_number,
          })
          router.push({ name: 'ContentList' })
        } catch (error) {
          alert(error)
        }
      }
    }
    return {
      store,
      router,
      isValidFormData,
      formData,
      isValidInfoData,
      infoData,
      handleUpdateValidate,
      submit,
    }
  },
})
</script>

<style lang="scss" scoped>
.body {
  @apply flex flex-col justify-center items-center w-full h-screen -mt-16 -mb-20;

  .input-container {
    @apply grid gap-4 px-8 w-full sm:w-96;

    &__input-label {
      @apply text-lg font-bold mb-1;

      &.primary {
        @apply text-indigo-900;
      }

      &.default {
        @apply text-gray-400;
      }
    }

    &__input-list {
      @apply grid gap-3 w-full;
    }
    &__submit-btn {
      @apply w-full rounded-lg py-3 text-sm text-white font-bold bg-indigo-900;

      &.disabled {
        @apply opacity-50;
      }
    }
  }
}
</style>
