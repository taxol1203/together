<template>
  <section class="banner-section">
    <div class="absolute inset-0 bg-black opacity-60"></div>
    <img
      class="w-full h-full object-cover"
      :src="require(`@/assets/images/ott_banner.jpg`)"
      alt=""
    />
  </section>
  <div class="container">
    <LoadingSection v-if="loading" />
    <template v-else>
      <section class="filter-section">
        <div class="filter-list">
          <button
            class="filter-button"
            :class="{ active: provider.active }"
            v-for="(provider, index) in providers"
            :key="provider.name"
            @click="handleFilterClick(index)"
          >
            {{ provider.name }}
            <!-- <img
              :src="require(`@/assets/images/logo/${provider.name}.png`)"
              :alt="provider.name"
            /> -->
          </button>
        </div>
      </section>
      <section class="contents-section">
        <header class="section-header">추천 컨텐츠 (영화)</header>
        <ul class="contents-list">
          <transition-group name="contents">
            <li
              class="contents-item"
              v-for="content in displayedMovieList"
              :key="content.id"
            >
              <ContentPosterLink :content="content" :contentType="'movies'" />
            </li>
          </transition-group>
        </ul>
      </section>
      <section class="contents-section">
        <header class="section-header">추천 컨텐츠 (TV)</header>
        <ul class="contents-list">
          <transition-group name="contents">
            <li
              class="contents-item"
              v-for="content in displayedProgramList"
              :key="content.id"
            >
              <ContentPosterLink :content="content" :contentType="'programs'" />
            </li>
          </transition-group>
        </ul>
      </section>
    </template>
  </div>
</template>
<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { ProviderFilter, ProviderNameEn } from '@/libs/interfaces/content'
import ContentPosterLink from '@/components/ContentPosterLink.vue'
import LoadingSection from '@/components/Common/LoadingSection.vue'
import { Content } from '@/libs/interfaces/content'

export default defineComponent({
  name: 'ContentList',
  components: { ContentPosterLink, LoadingSection },
  setup() {
    const store = useStore()
    const loading = ref<boolean>(true)
    const movies = ref<Content[]>([])
    const programs = ref<Content[]>([])

    const providers = ref<ProviderFilter>([
      { name: 'Netflix', active: true },
      { name: 'Watcha', active: true },
      { name: 'Naver Store', active: true },
      { name: 'wavve', active: true },
      { name: 'Disney Plus', active: true },
      { name: 'Google Play Movies', active: true },
      { name: 'Amazon Prime Video', active: true },
    ])

    const activeProviders = computed(() => {
      const res: ProviderNameEn[] = []
      providers.value.forEach((p) => {
        if (p.active) {
          res.push(p.name)
        }
      })
      return res
    })

    const displayedMovieList = computed(() => {
      return movies.value.filter((content) => {
        return content.providers.some((p) =>
          activeProviders.value.includes(p.name)
        )
      })
    })

    const displayedProgramList = computed(() => {
      return programs.value.filter((content) => {
        return content.providers.some((p) =>
          activeProviders.value.includes(p.name)
        )
      })
    })

    const handleFilterClick = (index: number) => {
      if (providers.value.every((p) => p.active)) {
        providers.value.forEach((p, i) => {
          p.active = i === index ? true : false
        })
      } else {
        providers.value[index].active = !providers.value[index].active
        if (providers.value.every((p) => p.active === false)) {
          console.log('hh')
          providers.value.forEach((p) => (p.active = true))
        }
      }
    }

    onMounted(async () => {
      // TODO
      // Axios 에러인 상황과 알 수 없는 에러인 상황을 함께 다루려면?
      // 에러를 핸들링하는 부분이 컴포넌트쪽으로 올 필요가 있을까?
      try {
        movies.value = await store.dispatch('content/getMovieList')
        programs.value = await store.dispatch('content/getProgramList')
        loading.value = false
      } catch (error) {
        alert(error)
      }
    })
    return {
      loading,
      displayedMovieList,
      displayedProgramList,
      providers,
      handleFilterClick,
    }
  },
})
</script>

<style lang="scss" scoped>
.banner-section {
  @apply relative flex h-44 md:h-80 bg-gray-200;
}
.filter-section {
  @apply py-6 px-4;

  .filter-list {
    @apply flex flex-wrap gap-2;

    .filter-button {
      @apply py-2 px-4 rounded transition-colors;
      /* @apply w-8 h-8 md:w-10 md:h-10 opacity-30; */

      &:hover {
        @apply bg-indigo-200;
      }

      &.active {
        @apply bg-indigo-100;
        /* @apply opacity-100; */

        &:hover {
          @apply bg-indigo-300;
        }
      }

      img {
        @apply object-contain object-center;
      }
    }
  }
}

.contents-section {
  @apply p-4;

  .section-header {
    @apply text-2xl font-bold mb-4;
  }

  .contents-list {
    @apply grid grid-cols-3 sm:grid-cols-4 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-2;

    .poster-wrapper {
      padding-top: 142.1686747%;
      @apply relative flex overflow-hidden rounded-md;

      img {
        @apply absolute inset-0 w-full;
      }
    }
  }
}

/* Transition */
.contents-move {
  @apply transition-all;
}
</style>
