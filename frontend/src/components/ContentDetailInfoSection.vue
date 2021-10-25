<template>
  <section class="info-section">
    <header class="section-header">
      <span class="title">{{ content.title }}</span>
      <div class="sim-rate" v-if="false">{{ content.simRate }}%</div>
    </header>
    <ul class="provider-list">
      <li
        class="provider-item"
        v-for="provider in content.providers"
        :key="provider.id"
      >
        {{ provider.name }}
      </li>
    </ul>
    <div class="details">
      <div>{{ content.releaseDate }}</div>
      <div v-if="content.rated">{{ content.rated }}</div>
      <div v-if="content.seasons">시즌 {{ content.seasons }}개</div>
    </div>
    <div class="overview">
      {{ content.overview }}
    </div>
    <fieldset
      class="rating-wrapper"
      @change="handleClickRatingBtn"
      v-if="isLogin"
    >
      <template v-for="i in 5" :key="i">
        <input
          type="radio"
          v-model="rating"
          :id="`rating${6 - i}`"
          name="rating"
          :value="6 - i"
        />
        <label class="material-icons star" :for="`rating${6 - i}`">star</label>
      </template>
    </fieldset>
  </section>
</template>

<script lang="ts">
import { Content } from '@/libs/interfaces/content'
import { computed, defineComponent, PropType, ref } from 'vue'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'ContentDetailInfoSection',
  props: {
    content: {
      type: Object as PropType<Content>,
      required: true,
    },
    contentType: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const store = useStore()
    const rating = ref<number>(0)
    const isLogin = computed(() => store.getters['auth/isLogin'])

    const handleClickRatingBtn = async () => {
      const score = rating.value * 2
      const submitData: {
        [key: string]: string | number
      } = {
        user_id: store.getters['auth/getUserNickName'],
        rating: score,
      }
      if (props.contentType === 'movies') {
        submitData.movie_id = props.content.id
      } else {
        submitData.program_id = props.content.id
      }
      const ok = confirm(`내가 매긴 점수: ${score}점`)
      if (ok) {
        store.dispatch('content/postReview', {
          submitData,
          contentType: props.contentType,
        })
      } else {
        rating.value = 0
      }
    }

    return {
      rating,
      isLogin,
      handleClickRatingBtn,
    }
  },
})
</script>

<style lang="scss" scoped>
.info-section {
  @apply relative z-10 p-4 grid gap-2 select-none md:text-white;

  .section-header {
    @apply flex justify-between items-center;

    .title {
      @apply text-2xl font-bold;
    }

    .sim-rate {
      @apply text-xs text-yellow-400 bg-gray-900 rounded-md py-0.5 px-2;
    }
  }

  .provider-list {
    @apply flex flex-wrap gap-2;

    .provider-item {
      @apply hover:text-red-400;
    }
  }

  .details {
    @apply flex gap-2 text-sm;
  }

  .overview {
    word-break: keep-all;
    max-height: 80px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: break-spaces;
    @apply text-sm;
  }

  .rating-wrapper {
    @apply p-2 border border-gray-200 rounded mr-auto flex flex-row-reverse gap-1;

    input {
      @apply hidden;
    }
    .star {
      @apply text-gray-200 cursor-pointer;
    }

    input:checked ~ label, /* show gold star when clicked */
    &:not(:checked) > label:hover, /* hover current star */
    &:not(:checked) > label:hover ~ label {
      @apply text-yellow-400;
    }

    input:checked + label:hover, /* hover current star when changing rating */
    input:checked ~ label:hover,
    label:hover ~ input:checked ~ label, /* lighten current selection */
    input:checked ~ label:hover ~ label {
      @apply text-yellow-300;
    }
  }
}
</style>
