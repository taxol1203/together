<template>
  <div class="container">
    <LoadingSection v-if="loading" />
    <div v-else class="py-10 px-4 grid gap-10">
      <section class="partyinfo-section">
        <h3>파티 정보</h3>
        <div class="info-container">
          <div class="info">
            <span class="label">서비스</span>
            <span class="value">{{ party.provider.name }}</span>
          </div>
          <div class="info">
            <span class="label">파티 이름</span>
            <span class="value">{{ party.title }}</span>
          </div>
          <div class="info">
            <span class="label">파티장</span>
            <span class="value">{{ party.host.nickName }}</span>
          </div>
          <div class="info">
            <span class="label">파티 종료일</span>
            <span class="value"> {{ party.endDate }} ({{ restDays }}일) </span>
          </div>
          <div class="info">
            <span class="label">참가비</span>
            <span class="value">
              {{ toCurrency(cost) }}
            </span>
          </div>
        </div>
      </section>
      <section class="payinfo-section">
        <h3>결제 정보</h3>
        <div class="info-container">
          <div class="info">
            <span class="label">이름</span>
            <span class="value">{{ me.nickName }}</span>
          </div>
          <div class="info">
            <span class="label">참가비</span>
            <span class="value">
              {{ toCurrency(cost) }}
            </span>
          </div>
          <div class="info">
            <span class="label">참가 수수료</span>
            <span class="value">
              {{ toCurrency(fee) }}
            </span>
          </div>
          <div class="info">
            <span class="label">결제방법</span>
            <span class="value">신용카드 </span>
          </div>
          <div class="total-cost">
            <span class="label">결제 금액</span>
            <span class="value">{{ toCurrency(cost + fee) }}</span>
          </div>
        </div>
      </section>
      <button class="submit-button" @click="handleClick">결제하기</button>
    </div>
  </div>
</template>

<script lang="ts">
import { getRestDays, toCurrency } from '@/libs/func'
import { OutputUser } from '@/libs/interfaces/auth'
import { Party } from '@/libs/interfaces/party'
import { computed, defineComponent, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import LoadingSection from '@/components/Common/LoadingSection.vue'

export default defineComponent({
  name: 'PartyJoin',
  components: { LoadingSection },
  props: {
    partyId: {
      type: [String, Number],
      required: true,
    },
  },
  setup(props) {
    const store = useStore()
    const router = useRouter()
    const loading = ref(true)
    const party = ref<Party>()
    const restDays = ref<number>(0)
    const cost = computed(
      () => party.value && party.value.pricePerDay * restDays.value
    )
    const fee = computed(
      () =>
        party.value &&
        Math.floor(party.value.pricePerDay * restDays.value * 0.1)
    )
    const me = computed<OutputUser>(() => store.state.auth.user)

    const handleClick = async () => {
      const ok = confirm('결제를 하시겠습니까?')
      if (ok) {
        try {
          await store.dispatch('party/postJoinParty', +props.partyId)
        } catch (error) {
          console.log('gg')
          router.push({
            name: 'PartyDetail',
            params: { partyId: props.partyId },
          })
          return
        }
        router.push({
          name: 'PartyJoinConfirm',
          params: { partyId: props.partyId },
        })
      }
    }

    const checkHost = (hostId: number) => {
      if (hostId === me.value.id) {
        alert('호스트는 자신의 파티에 참가할 수 없습니다')
        router.push({ name: 'PartyDetail', params: { partyId: props.partyId } })
      }
    }

    onMounted(async () => {
      try {
        const _party: Party = await store.dispatch(
          'party/getParty',
          props.partyId
        )
        party.value = _party
        restDays.value = getRestDays(_party.endDate)
      } catch (error) {
        console.log(error)
      }

      if (party.value) {
        checkHost(party.value.host.id)
      }

      loading.value = false
    })

    return { loading, me, cost, fee, party, restDays, toCurrency, handleClick }
  },
})
</script>

<style lang="scss" scoped>
.container {
  @apply max-w-3xl;
}

h3 {
  @apply text-xl font-bold mb-4;
}

.partyinfo-section,
.payinfo-section {
  .info-container {
    @apply p-4 border rounded-md grid gap-4;

    .info,
    .total-cost {
      @apply flex justify-between;

      .label {
        flex-basis: 100px;
        @apply flex-shrink-0;
      }

      .value {
        @apply text-right;
      }
    }

    .total-cost {
      @apply p-4 border border-indigo-900 bg-indigo-100 font-bold;
    }
  }
}

.submit-button {
  @apply py-4 rounded-xl bg-indigo-900 text-white font-bold w-full max-w-xs mx-auto;
}
</style>
