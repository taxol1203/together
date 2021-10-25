<template>
  <div class="container grid">
    <section class="noti-section">
      <div class="noti-box">
        <p>파티를 만들고,</p>
        <p>다른 사람들과 함께 하세요 🎉</p>
      </div>
    </section>
    <LoadingSection v-if="loading" />
    <template v-else>
      <section class="confirm-section">
        <h3>파티 참가 정보</h3>
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
          <div class="info">
            <span class="label">수수료</span>
            <span class="value">
              {{ toCurrency(fee) }}
            </span>
          </div>
          <div class="total-cost">
            <span class="label">결제 금액</span>
            <span class="value">
              {{ toCurrency(cost + fee) }}
            </span>
          </div>
        </div>
      </section>
      <button class="confirm-button" @click="handleClick">확인</button>
    </template>
  </div>
</template>

<script lang="ts">
import { getRestDays, toCurrency } from '@/libs/func'
import { Party } from '@/libs/interfaces/party'
import { defineComponent, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import LoadingSection from '@/components/Common/LoadingSection.vue'

export default defineComponent({
  name: 'PartyJoinConfirm',
  components: { LoadingSection },
  props: {
    partyId: {
      type: [Number, String],
      required: true,
    },
  },
  setup(props) {
    const store = useStore()
    const router = useRouter()
    const loading = ref<boolean>(true)
    const party = ref<Party>()
    const restDays = ref<number>()
    const cost = ref<number>()
    const fee = ref<number>()

    const handleClick = () => {
      router.push({ name: 'PartyDetail', params: { partyId: props.partyId } })
    }

    const checkIamMember = (
      partyPayments: {
        id: number
        nickName: string
      }[]
    ) => {
      const userId = store.getters['auth/getUserPK']
      const paymentIds = partyPayments.map((p) => p.id)
      if (!paymentIds.includes(userId)) {
        alert('잘못 접근한 페이지입니다')
        router.push({
          name: 'PartyList',
        })
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
        cost.value = _party.pricePerDay * restDays.value
        fee.value = Math.floor(cost.value * 0.1)
        checkIamMember(_party.payments)
      } catch (error) {
        console.log(error)
      }
      loading.value = false
    })

    return {
      loading,
      party,
      restDays,
      cost,
      fee,
      toCurrency,
      handleClick,
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

.confirm-section {
  @apply py-6 px-4 grid gap-4;

  h3 {
    @apply text-xl font-bold;
  }

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

.confirm-button {
  @apply py-4 rounded-xl bg-indigo-900 text-white font-bold w-full max-w-xs mx-auto;
}
</style>
