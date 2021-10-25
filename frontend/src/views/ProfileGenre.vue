<template>
  <div class="container grid gap-4 max-w-xl">
    <section class="noti-section">
      <div class="noti-box">
        <p>좋아하는 장르를 선택하면,</p>
        <p>콘텐츠를 추천해 드릴게요 🎉</p>
      </div>
    </section>
    <LoadingSection v-if="loading" />
    <template v-else>
      <section class="genre-section">
        <header>
          <h3>영화 장르 선택</h3>
        </header>
        <div class="genre-wrapper">
          <transition-group name="genres">
            <button
              class="genre-button active"
              v-for="genre in favMovieGenreList"
              :key="genre.id"
              @click="handleRemoveFromFavMovieGenreList(genre)"
            >
              {{ genre.kName }}
            </button>
            <button
              class="genre-button"
              v-for="genre in movieGenreList"
              :key="genre.id"
              @click="handleAddToFavMovieGenreList(genre)"
            >
              {{ genre.kName }}
            </button>
          </transition-group>
        </div>
      </section>
      <section class="genre-section">
        <header>
          <h3>TV 프로그램 장르 선택</h3>
        </header>
        <div class="genre-wrapper">
          <transition-group name="genres">
            <button
              class="genre-button active"
              v-for="genre in favProgramGenreList"
              :key="genre.id"
              @click="handleRemoveFromFavProgramGenreList(genre)"
            >
              {{ genre.kName }}
            </button>
            <button
              class="genre-button"
              v-for="genre in ProgramGenreList"
              :key="genre.id"
              @click="handleAddToFavProgramGenreList(genre)"
            >
              {{ genre.kName }}
            </button>
          </transition-group>
        </div>
      </section>
      <SubmitButton label="저장하기" @click="handleClick" />
    </template>
  </div>
</template>

<script lang="ts">
import { Genre } from '@/libs/interface'
import { defineComponent, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import LoadingSection from '@/components/Common/LoadingSection.vue'
import SubmitButton from '@/components/Common/SubmitButton.vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'ProfileGenre',
  components: { LoadingSection, SubmitButton },
  setup() {
    const store = useStore()
    const router = useRouter()
    const loading = ref<boolean>(true)
    const movieGenreList = ref<Genre[]>([])
    const favMovieGenreList = ref<Genre[]>([])
    const ProgramGenreList = ref<Genre[]>([])
    const favProgramGenreList = ref<Genre[]>([])

    const handleAddToFavMovieGenreList = (selectedGenre: Genre) => {
      movieGenreList.value = movieGenreList.value.filter(
        (genre) => genre.id !== selectedGenre.id
      )
      favMovieGenreList.value.push(selectedGenre)
    }

    const handleRemoveFromFavMovieGenreList = (selectedGenre: Genre) => {
      favMovieGenreList.value = favMovieGenreList.value.filter(
        (genre) => genre.id !== selectedGenre.id
      )
      movieGenreList.value.push(selectedGenre)
    }

    // TODO: 콘텐츠가 한 테이블 안에 있었으면 다루기 쉬울 것 같다.
    const handleAddToFavProgramGenreList = (selectedGenre: Genre) => {
      ProgramGenreList.value = ProgramGenreList.value.filter(
        (genre) => genre.id !== selectedGenre.id
      )
      favProgramGenreList.value.push(selectedGenre)
    }

    const handleRemoveFromFavProgramGenreList = (selectedGenre: Genre) => {
      favProgramGenreList.value = favProgramGenreList.value.filter(
        (genre) => genre.id !== selectedGenre.id
      )
      ProgramGenreList.value.push(selectedGenre)
    }

    const handleClick = async () => {
      if (confirm('선호 장르를 저장하시겠습니까?')) {
        console.log(favMovieGenreList.value)
        console.log(favProgramGenreList.value)
        try {
          await store.dispatch('auth/updateFavGenres', {
            fav_movie_genres: favMovieGenreList.value,
            fav_program_genres: favProgramGenreList.value,
          })
        } catch (error) {
          alert(error)
        }
        router.push({
          name: 'ProfileMain',
          params: { userId: store.getters['auth/getUserPK'] },
        })
      }
    }

    onMounted(async () => {
      try {
        const movieGenres: Genre[] = await store.dispatch(
          'content/getMovieGenreList'
        )
        const favMovieGenreIds: number[] =
          store.getters['auth/getUserFavMovieGenreIds']
        movieGenres.forEach((genre) => {
          if (favMovieGenreIds.includes(genre.id)) {
            favMovieGenreList.value.push(genre)
          } else {
            movieGenreList.value.push(genre)
          }
        })

        const programGenres: Genre[] = await store.dispatch(
          'content/getProgramGenreList'
        )
        const favProgramGenreIds: number[] =
          store.getters['auth/getUserFavProgramGenreIds']
        programGenres.forEach((genre) => {
          if (favProgramGenreIds.includes(genre.id)) {
            favProgramGenreList.value.push(genre)
          } else {
            ProgramGenreList.value.push(genre)
          }
        })
      } catch (error) {
        alert(error)
        router.push({
          name: 'ProfileMain',
          params: { userId: store.getters['auth/getUserPK'] },
        })
      }

      loading.value = false
    })
    return {
      loading,
      favMovieGenreList,
      movieGenreList,
      ProgramGenreList,
      favProgramGenreList,
      handleClick,
      handleAddToFavMovieGenreList,
      handleRemoveFromFavMovieGenreList,
      handleAddToFavProgramGenreList,
      handleRemoveFromFavProgramGenreList,
    }
  },
})
</script>

<style lang="scss" scoped>
.noti-section {
  @apply py-6 px-4;

  .noti-box {
    @apply w-full py-4 text-center bg-indigo-50 rounded-lg;

    p {
      @apply text-lg font-bold text-indigo-500;
    }
  }
}

.genre-section {
  @apply p-4;

  header {
    @apply mb-6;

    h3 {
      @apply text-2xl font-bold;
    }
  }

  .genre-wrapper {
    @apply flex flex-wrap gap-4;

    .genre-button {
      @apply py-2 px-4 bg-gray-100 text-gray-600 font-bold rounded-md;

      &.active {
        @apply bg-indigo-50 text-indigo-900;
      }
    }
  }
}

.genres-move {
  @apply transition-all;
}
</style>
