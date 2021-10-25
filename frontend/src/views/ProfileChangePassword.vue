<template>
  <div class="container max-w-sm">
    <section class="form-section">
      <header>
        <h3>비밀번호 변경</h3>
      </header>
      <form @submit="handleSubmit">
        <div class="fields">
          <TextInput
            v-for="(field, key) in formData"
            :key="key"
            :field="field"
            :formData="formData"
            :name="key"
            v-model="field.value"
            @update:validate="handleUpdateValidate"
          />
        </div>
        <div class="buttons">
          <button :class="{ valid: formIsValid }" :disabled="!formIsValid">
            확인
          </button>
          <router-link to="/">돌아가기</router-link>
        </div>
      </form>
    </section>
  </div>
</template>

<script lang="ts">
import { FormData, ValidateData } from '@/libs/interface'
import { requiredValidator } from '@/libs/validator'
import { computed, defineComponent, ref } from 'vue'
import TextInput from '@/components/Common/TextInput.vue'

export default defineComponent({
  components: { TextInput },
  setup() {
    const formData = ref<FormData>({
      currentPassword: {
        label: '현재 비밀번호',
        type: 'password',
        value: '',
        placeholder: '현재 비밀번호를 입력하세요',
        errors: {},
        validators: [requiredValidator],
      },
      newPassword: {
        label: '새 비밀번호',
        type: 'password',
        value: '',
        placeholder: '새 비밀번호를 입력하세요',
        errors: {},
        validators: [requiredValidator],
      },
      confirmNewPassword: {
        label: '새 비밀번호 확인',
        type: 'password',
        value: '',
        placeholder: '새 비밀번호를 입력하세요',
        errors: {},
        validators: [requiredValidator],
      },
    })

    const newPasswordCheck = computed(() => {
      return (
        formData.value.newPassword.value ===
        formData.value.confirmNewPassword.value
      )
    })

    const formErrorCheck = computed(() => {
      return Object.keys(formData.value).every((key) => {
        return (
          Object.keys(formData.value[key].errors).length === 0 &&
          formData.value[key].value
        )
      })
    })

    const formIsValid = computed(() => {
      return newPasswordCheck.value && formErrorCheck.value
    })

    const handleSubmit = async (event: Event) => {
      event.preventDefault()
      // try {
      //   const res = await axios.put(``)
      // } catch (error) {
      //   console.log(error)
      // }
    }

    const handleUpdateValidate = (validateRes: ValidateData) => {
      const { key, type, status } = validateRes

      if (status) {
        delete formData.value[key].errors[type]
      } else if (validateRes.message) {
        formData.value[key].errors[type] = validateRes.message
      } else {
        throw new Error('망했어요')
      }
    }

    return {
      formData,
      formIsValid,
      handleSubmit,
      handleUpdateValidate,
    }
  },
})
</script>

<style lang="scss" scoped>
.form-section {
  @apply py-6 px-4 grid gap-6;

  header h3 {
    @apply text-xl font-bold;
  }

  form {
    @apply grid gap-10;

    .fields {
      @apply grid gap-4;
    }

    .buttons {
      @apply grid gap-2;

      button {
        @apply mx-auto w-full max-w-sm py-4 bg-gray-100 text-gray-400 font-bold rounded-xl;

        &.valid {
          @apply bg-indigo-900 text-white;
        }
      }

      a {
        @apply mx-auto;
      }
    }
  }
}
</style>
