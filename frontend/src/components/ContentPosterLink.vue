<template>
  <router-link
    class="card"
    :to="{
      name: 'ContentDetail',
      params: { contentId: content.id, contentType },
    }"
  >
    <div class="wrap">
      <div class="front">
        <img :src="posterPath" :alt="`${content.originalTitle}의 포스터`" />
      </div>
      <div class="back">
        <h3 class="title">{{ content.title }}</h3>
      </div>
    </div>
  </router-link>
</template>

<script lang="ts">
import { Content } from '@/libs/interfaces/content'
import { defineComponent, PropType } from 'vue'

export default defineComponent({
  name: 'ContentPosterLink',
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
    const posterPath = `https://image.tmdb.org/t/p/w200${props.content.posterPath}`
    return { posterPath }
  },
})
</script>

<style lang="scss" scoped>
.card,
.wrap {
  perspective: 500px;
}

.card {
  @apply cursor-pointer;

  .wrap {
    transform-style: preserve-3d;
    @apply transition-all duration-500;
  }

  &:hover .wrap {
    transform: rotateY(180deg);
  }

  .front,
  .back {
    backface-visibility: hidden;
    transform-style: preserve-3d;
    @apply overflow-hidden rounded-md;
  }

  .front {
    padding-top: 142.1686747%;
    @apply relative flex;

    img {
      @apply absolute inset-0 w-full;
    }
  }

  .back {
    transform: rotateY(180deg);
    @apply absolute inset-0 p-4 bg-indigo-800 text-white flex items-center justify-center;

    .title {
      @apply text-lg text-indigo-100 font-medium text-center;
    }
  }
}
</style>
