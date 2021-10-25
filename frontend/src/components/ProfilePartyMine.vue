<template>
  <div class="profile-party__box" :class="party.provider.name">
    <header>
      <div class="profile-party__box__text--array">
        <p class="font-semibold">{{ party.provider.name }}</p>
        <img
          :src="providerLogoUrl"
          class="profile-party__box__image--size"
          alt="이미지"
        />
      </div>
      <div class="profile-party__box__text--array2">
        <p>{{ party.endDate }} 까지 ({{ restDays }}일)</p>
        <p class="font-bold">10,900원</p>
      </div>
    </header>
    <div class="detail-info" v-if="isExpanded">
      <hr />
      <div class="account-info">
        <h4>계정 정보</h4>
        <div class="info-wrapper">
          <p>아이디</p>
          <p>{{ party.serviceId }}</p>
        </div>
        <div class="info-wrapper">
          <p>비밀번호</p>
          <input
            class="select-none cursor-pointer ml-auto"
            type="password"
            :value="party.servicePassword"
            @mouseenter="handleMouseEnter"
            @mouseleave="handleMouseLeave"
            style="text-align: right"
            readonly
          />
        </div>
      </div>
      <div class="host-info">
        <h4>파티장 정보</h4>
        <div class="info-wrapper">
          <p>이름</p>
          <p>{{ party.host.nickName }}</p>
        </div>
        <div class="info-wrapper">
          <p>휴대폰 번호</p>
          <p>{{ party.host.phoneNumber }}</p>
        </div>
      </div>
    </div>
    <button class="toggle-button" @click="handleToggleClick">
      <span class="material-icons" v-if="isExpanded">expand_less</span>
      <span class="material-icons" v-else>expand_more</span>
    </button>
  </div>
</template>

<script lang="ts">
import { getRestDays } from '@/libs/func'
import { Party } from '@/libs/interfaces/party'
import { defineComponent, onBeforeUnmount, onMounted, PropType, ref } from 'vue'

export default defineComponent({
  name: 'ProfilePartyMine',
  props: {
    party: {
      type: Object as PropType<Party>,
      required: true,
    },
  },
  setup(props) {
    const providerLogoUrl = `https://image.tmdb.org/t/p/w200${props.party.provider.logoUrl}`
    const isExpanded = ref<boolean>(false)
    const restDays = ref<number>(getRestDays(props.party.endDate))

    const setIsExpanded = () => {
      console.log(window.innerWidth)
      isExpanded.value = window.innerWidth >= 768 ? true : false
    }

    const handleMouseEnter = (event: Event) => {
      const target = event.target as HTMLInputElement
      target.type = 'text'
    }

    const handleMouseLeave = (event: Event) => {
      const target = event.target as HTMLInputElement
      target.type = 'password'
    }

    onMounted(() => {
      setIsExpanded()
      window.addEventListener('resize', setIsExpanded)
    })

    onBeforeUnmount(() => {
      window.removeEventListener('resize', setIsExpanded)
    })

    const handleToggleClick = () => {
      isExpanded.value = !isExpanded.value
    }

    return {
      providerLogoUrl,
      isExpanded,
      restDays,
      handleToggleClick,
      handleMouseEnter,
      handleMouseLeave,
    }
  },
})
</script>

<style lang="scss" scoped>
.profile-party__box {
  &.Netflix {
    @apply border-red-500;
  }
  &.Watcha {
    @apply border-pink-500;
  }
  &.wavve {
    @apply border-blue-500;
  }

  .profile-party__box__text--array {
    @apply flex justify-between;

    .profile-party__box__image--size {
      @apply w-12 h-12;
    }
  }

  .profile-party__box__text--array2 {
    @apply flex justify-between;
  }

  .profile-party__box__text--array3 {
    @apply font-semibold mt-4;
  }

  .profile-party__box__text--array4 {
    @apply flex justify-between my-2 mx-0;
  }

  header {
    @apply grid gap-8 mb-6;
  }

  .detail-info {
    @apply grid gap-6;

    .info-wrapper {
      @apply flex items-center justify-between;
    }

    .account-info,
    .host-info {
      @apply grid gap-2;

      h4 {
        @apply font-bold text-gray-600;
      }
    }
  }

  .toggle-button {
    @apply w-full md:hidden hover:bg-gray-100;
  }
}
</style>
