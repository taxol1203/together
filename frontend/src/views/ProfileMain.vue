<template>
  <div class="container max-w-screen-md">
    <section class="profile-main__info__section">
      <div class="profile-main__info__top--array">
        <h2 class="text-2xl font-bold">프로필</h2>
      </div>
      <div class="info-container">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-bold">개인 정보</h3>
          <router-link :to="{ name: 'ProfileEdit' }">수정</router-link>
        </div>
        <div class="grid gap-3">
          <div class="profile-main__info--array">
            <p class="label">닉네임</p>
            <p class="value">{{ user.nickName }}</p>
          </div>
          <div class="profile-main__info--array">
            <p class="label">이름</p>
            <p class="value">{{ user.username }}</p>
          </div>
          <div class="profile-main__info--array">
            <p class="label">휴대폰 번호</p>
            <p class="value">{{ user.phoneNumber }}</p>
          </div>
          <div class="profile-main__info--array">
            <p class="label">이메일</p>
            <p class="value">{{ user.email }}</p>
          </div>
        </div>
      </div>
      <div class="grid gap-4">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-bold">선호 장르</h3>
          <router-link :to="{ name: 'ProfileGenre', params: { userId } }">
            수정
          </router-link>
        </div>
        <div class="grid gap-3">
          <h4 class="text-lg font-medium">영화</h4>
          <div class="genre-container flex flex-wrap gap-2">
            <div
              class="genre py-2 px-4 bg-indigo-50 rounded"
              v-for="genre in user.favMovieGenres"
              :key="genre.id"
            >
              {{ genre.kName }}
            </div>
          </div>
        </div>
        <div class="grid gap-3">
          <h4 class="text-lg font-medium">TV 프로그램</h4>
          <div class="genre-container flex flex-wrap gap-2">
            <div
              class="genre py-2 px-4 bg-indigo-50 rounded"
              v-for="genre in user.favProgramGenres"
              :key="genre.id"
            >
              {{ genre.kName }}
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="profile-main__seen__section" v-if="false">
      <header>
        <h3>내가 본 컨텐츠</h3>
        <router-link class="flex" to="/">
          <span class="material-icons">chevron_right</span>
        </router-link>
      </header>
      <ul class="contents-list">
        <li
          class="contents-list-item"
          v-for="content in contents"
          :key="content.id"
        >
          <ContentPosterLink :content="content" />
        </li>
      </ul>
    </section>
    <section class="profile-main__rating__section" v-if="false">
      <header>
        <h3>내가 평가한 콘텐츠</h3>
        <router-link class="flex" to="/">
          <span class="material-icons">chevron_right</span>
        </router-link>
      </header>
      <ul class="contents-list">
        <li
          class="contents-list-item"
          v-for="content in contents"
          :key="content.id"
        >
          <ContentPosterLink :content="content" />
        </li>
      </ul>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import ContentPosterLink from '@/components/ContentPosterLink.vue'
import { useStore } from 'vuex'
import { Content } from '@/libs/interfaces/content'

export default defineComponent({
  name: 'ProfileMain',
  components: {
    ContentPosterLink,
  },
  props: {
    userId: {
      type: [String, Number],
    },
  },
  setup() {
    const store = useStore()
    const loading = ref<boolean>(true)
    const user = computed(() => store.state.auth.user)
    const contents = ref<Content[]>([])
    return {
      loading,
      user,
      contents,
    }
  },
})
</script>

<style lang="scss" scoped>
.profile-main__info__section {
  @apply py-6 px-4 grid gap-10;

  .profile-main__info__top--array {
    @apply flex justify-between items-center;
  }

  .info-container {
    @apply grid gap-4;

    .profile-main__info--array {
      @apply flex justify-between items-center;

      .label {
        @apply font-medium text-gray-700;
      }
    }
  }
}

.profile-main__seen__section,
.profile-main__rating__section {
  @apply py-6 px-4 grid gap-4;

  header {
    @apply flex items-center justify-between;

    h3 {
      @apply text-xl font-bold;
    }
  }

  .contents-list {
    @apply grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-2;
  }
}
</style>
