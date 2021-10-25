<template>
  <section class="banner-section">
    <div class="container p-0 flex">
      <img
        class="w-full object-cover object-top"
        :src="require(`@/assets/images/ott_party_banner.jpg`)"
        alt=""
      />
    </div>
  </section>
  <div class="container">
    <LoadingSection v-if="loading" />
    <section class="party-section" v-else>
      <header class="section-header">
        <h1>파티에 참여하세요!</h1>
        <router-link :to="{ name: 'PartyCreate' }" v-if="isLogin">
          파티 만들기
        </router-link>
      </header>
      <ul class="party-list">
        <PartyListItem
          v-for="party in parties"
          :key="party.id"
          :party="party"
        />
      </ul>
    </section>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { Party } from '@/libs/interfaces/party'
import PartyListItem from '@/components/PartyListItem.vue'
import LoadingSection from '@/components/Common/LoadingSection.vue'

export default defineComponent({
  name: 'PartyList',
  components: { PartyListItem, LoadingSection },
  setup() {
    const store = useStore()
    const loading = ref(true)
    const isLogin = computed(() => store.getters['auth/isLogin'])
    const parties = ref<Party[]>([])

    onMounted(async () => {
      parties.value = await store.dispatch('party/getParties')
      loading.value = false
    })
    return { loading, isLogin, parties }
  },
})
</script>

<style lang="scss" scoped>
.banner-section {
  @apply flex h-44 md:h-80 bg-indigo-500;
}

.party-section {
  @apply py-6 px-4;

  .section-header {
    @apply mb-4 flex items-center justify-between;

    h1 {
      @apply text-2xl font-bold;
    }

    a {
      @apply inline-block py-2 px-4 text-sm text-white font-bold rounded-full bg-indigo-900;
    }
  }

  .party-list {
    @apply grid gap-4 md:grid-cols-2 xl:grid-cols-3;
  }
}
</style>
