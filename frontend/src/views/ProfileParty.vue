<template>
  <div class="container grid max-w-3xl px-4 pt-6">
    <p class="profile-party__text--array">내 파티</p>
    <div
      class="profile-party__box--array"
      v-if="user.payments && user.payments.length"
    >
      <ProfilePartyMine
        v-for="party in user.payments"
        :key="party.id"
        :party="party"
      />
    </div>
    <section class="no-content-section" v-else>
      <div class="no-content-info-container">
        <p>아직 참가중인 파티가 없어요</p>
        <p>다른 사람들과 함께 즐겨볼까요?</p>
      </div>
      <router-link :to="{ name: 'PartyList' }"> Together! </router-link>
    </section>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue'
import ProfilePartyMine from '@/components/ProfilePartyMine.vue'
import { useStore } from 'vuex'
import { OutputUser } from '@/libs/interfaces/auth'

export default defineComponent({
  name: 'ProfileParty',
  components: {
    ProfilePartyMine,
  },
  setup() {
    const store = useStore()
    const user = computed<OutputUser[]>(() => store.state.auth.user)

    onMounted(async () => {
      // TODO: 내가 속한 파티 가져오기
      // try {
      //   const res = await axios.get(`http://localhost:3000/myparty`)
      //   parties.value = res.data
      // } catch (error) {
      //   console.log(error)
      // }
    })
    return {
      user,
    }
  },
})
</script>

<style lang="scss" scoped>
.profile-party__box--array {
  @apply grid gap-2;

  .profile-party__box {
    @apply px-4 py-4 border rounded-md;

    .profile-party__box__image--size {
      @apply w-12 h-12;
    }
  }
}

.profile-party__text--array {
  @apply text-2xl font-bold mb-4;
}

.no-content-section {
  @apply grid max-w-sm w-full mx-auto;

  .no-content-info-container {
    @apply p-4 bg-indigo-500 text-center font-medium text-white rounded-md mb-4;
  }

  a {
    @apply w-full inline-block py-4 text-center font-bold bg-teal-400 rounded transition-colors;

    &:hover {
      @apply bg-teal-300;
    }
  }
}

@media (min-width: 768px) {
  .profile-party__box--array {
    @apply grid grid-cols-2;
  }
  .profile-party__box {
    @apply p-4 border rounded-md;
  }
  .profile-party__text--array {
    @apply text-2xl font-bold;
  }
}
</style>
