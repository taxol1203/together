<template>
  <li class="party-list-item">
    <router-link :to="{ name: 'PartyDetail', params: { partyId: party.id } }">
      <div class="party">
        <div class="infos">
          <div class="text">
            <h3>{{ party.provider.name }}</h3>
            <p>{{ party.title }}</p>
          </div>
          <div class="logo-wrapper">
            <img :src="providerLogoUrl" :alt="`${party.provider.name} 로고`" />
          </div>
        </div>
        <div class="members">
          <div
            class="image-wrapper"
            v-for="i in membersCount"
            :key="`member${i}`"
          >
            <img
              src="https://cdn-icons-png.flaticon.com/512/2437/2437148.png"
            />
          </div>
          <div
            class="image-wrapper"
            v-for="i in party.memberLimit - membersCount"
            :key="`empty${i}`"
          >
            <img
              src="https://cdn-icons-png.flaticon.com/512/2437/2437116.png"
            />
          </div>
        </div>
        <div class="details">
          <div>
            <p class="date">{{ party.endDate }}까지 ({{ restDays }}일)</p>
          </div>
          <div class="price-wrapper">
            <p class="original-price">
              {{ toCurrency(party.provider.pricePerDay * restDays) }}
            </p>
            <p class="price">
              {{ toCurrency(party.pricePerDay * restDays) }}
            </p>
          </div>
        </div>
      </div>
    </router-link>
  </li>
</template>

<script lang="ts">
import { getRestDays, toCurrency } from '@/libs/func'
import { Party } from '@/libs/interfaces/party'
import { defineComponent, PropType, ref } from 'vue'

export default defineComponent({
  name: 'PartyListItem',
  props: {
    party: {
      type: Object as PropType<Party>,
      required: true,
    },
  },
  setup(props) {
    const providerLogoUrl = `https://image.tmdb.org/t/p/w200${props.party.provider.logoUrl}`
    const membersCount = ref(props.party.payments.length)

    const restDays: number = getRestDays(props.party.endDate)
    return { toCurrency, providerLogoUrl, restDays, membersCount }
  },
})
</script>

<style lang="scss" scoped>
.party-list-item {
  @apply transition-colors;

  &:hover {
    @apply bg-indigo-50;
  }

  .party {
    @apply grid gap-4 p-4 border rounded-md border-gray-100;

    .infos {
      @apply flex justify-between;

      .text {
        h3 {
          @apply md:text-lg font-bold mb-1;
        }
        p {
          @apply text-xs md:text-sm;
        }
      }

      .logo-wrapper {
        @apply w-8 h-8 md:w-10 md:h-10 rounded overflow-hidden;

        img {
          @apply w-full h-full object-fill;
        }
      }
    }

    .members {
      @apply flex gap-2;

      .image-wrapper {
        @apply w-10 h-10 overflow-hidden;
      }
    }

    .details {
      @apply flex justify-between;

      .date {
        @apply text-xs md:text-sm;
      }

      .price-wrapper {
        @apply text-right;

        .original-price {
          @apply text-red-600 text-sm md:text-base font-bold line-through;
        }

        .price {
          @apply md:text-lg font-bold text-gray-700;
        }
      }
    }
  }
}
</style>
