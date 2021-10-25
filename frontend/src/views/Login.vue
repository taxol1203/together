<template>
  <div class="container">
    <div class="body">
      <div class="logo">
        <!-- temporary element -->
        <img src="@/images/temp_auth_logo.png" alt="OTT_logo" />
      </div>
      <div class="input-container">
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
        <div class="input-container__sub-option">
          <div>
            <input
              class="mr-1 bg-indigo-800"
              type="checkbox"
              id="checkSaveEmail"
              v-model="isSaveEmail"
            />
            <label
              class="relative bottom-0.5 text-xs text-gray-600"
              for="checkSaveEmail"
              >이메일 저장하기</label
            >
          </div>
          <router-link
            class="relative top-1 text-xs text-gray-600 float-right"
            :to="{ name: 'ResetPassword' }"
            >비밀번호 찾기
          </router-link>
        </div>
        <button
          class="input-container__submit-btn"
          :class="{ disabled: !isValidFormData }"
          :disabled="!isValidFormData"
          @click="submit"
        >
          <!-- TODO: 로딩 상태 분기해서 로딩스피너와 교체할 것 -->
          로그인
        </button>
        <router-link
          class="text-sm text-center text-gray-600 font-medium"
          :to="{ name: 'Register' }"
          >이메일로 회원가입하기
        </router-link>
        <!-- Social Login area -->
        <hr class="my-1" />
        <p class="text-center text-gray-600 text-xs font-medium">
          SNS 계정으로 로그인
        </p>
        <div class="input-container__social-btn-group">
          <button
            v-for="(provider, key) in snsProviders"
            :class="provider.name"
            :key="key"
            @click="handleSocialLoginClick(provider.name)"
          >
            <img
              :src="require(`@/assets/images/${provider.name}_login.png`)"
              :alt="provider.name"
            />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue'
import TextInput from '@/components/TextInput.vue'
import { emailValidator } from '@/libs/validator'
import { useStore } from 'vuex'
import { FormDataList, ValidateData, SNSProviders } from '@/libs/interface'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'Login',
  components: {
    TextInput,
  },
  setup() {
    const store = useStore()
    const router = useRouter()

    const snsProviders = ref<SNSProviders>({
      google: {
        name: 'google',
      },
      naver: {
        name: 'naver',
      },
      kakao: {
        name: 'kakao',
      },
    })

    const isSaveEmail = ref<boolean>(
      localStorage.getItem('email') ? true : false
    )

    const isValidFormData = computed(() => {
      const keys = Object.keys(formData.value)
      return keys.every((key) => {
        const errors = Object.keys(formData.value[key].errors)
        return formData.value[key].value !== '' && !errors.length
      })
    })

    const formData = ref<FormDataList>({
      email: {
        label: '이메일',
        type: 'email',
        value: localStorage.getItem('email') || '',
        placeholder: '이메일을 입력하세요.',
        validator: emailValidator,
        errors: {},
      },
      password: {
        label: '비밀번호',
        type: 'password',
        value: '',
        placeholder: '비밀번호를 입력하세요.',
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
      if (isSaveEmail.value) {
        localStorage.setItem('email', formData.value['email'].value)
      }
      if (isValidFormData.value) {
        const email = formData.value['email'].value
        const password = formData.value['password'].value
        // TODO: Add loading spinner
        try {
          await store.dispatch('auth/login', {
            email,
            password,
          })
          router.push({ name: 'ContentList' })
        } catch (error) {
          alert(error)
        }
      }
    }

    const handleSocialLoginClick = async (platform: string) => {
      if (platform === 'google') {
        const REDIRECT_URI = ``
        const CLIENT_ID = ''
        const SCOPE = 'https://www.googleapis.com/auth/userinfo.email'

        const link = `https://accounts.google.com/o/oauth2/v2/auth?scope=${SCOPE}&client_id=${CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}`
        location.href = link
      } else if (platform === 'kakao') {
        const REDIRECT_URI = ``
        const REST_API_KEY = ''

        const link = `https://kauth.kakao.com/oauth/authorize?client_id=${REST_API_KEY}&redirect_uri=${REDIRECT_URI}&response_type=code`
        location.href = link
      }
    }

    return {
      store,
      router,
      snsProviders,
      isSaveEmail,
      isValidFormData,
      formData,
      handleUpdateValidate,
      submit,
      handleSocialLoginClick,
    }
  },
})
</script>

<style lang="scss" scoped>
.body {
  @apply flex flex-col justify-center items-center w-full h-screen sm:-mt-20 -mt-16 -mb-20;

  .logo {
    @apply mb-4;
  }
  .input-container {
    @apply grid gap-2 px-8 w-full sm:w-96;

    &__input-list {
      @apply grid gap-3 w-full;
    }
    &__submit-btn {
      @apply w-full rounded-lg py-3 text-sm text-white font-bold bg-indigo-900;

      &.disabled {
        @apply opacity-50;
      }
    }
    &__sub-option {
      @apply flex flex-row justify-between;
    }
    &__social-btn-group {
      @apply flex justify-around w-full rounded-lg py-3 text-sm text-gray-600 font-bold;
      button {
        @apply rounded-md w-14 h-14;

        &.kakao {
          @apply bg-yellow-400;
        }
        &.google {
          @apply bg-gray-100;
        }
        &.naver {
          @apply bg-green-500;
        }
      }
    }
  }
}
</style>
