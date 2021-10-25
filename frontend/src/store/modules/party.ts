import { Module } from 'vuex'
import { RootState } from '@/store/index'
import { SubmitFormData } from '@/libs/interface'
import partyAxios from '@/api/party'
import { Party } from '@/libs/interfaces/party'

interface PartyModule {
  data: string
}

export const party: Module<PartyModule, RootState> = {
  namespaced: true,
  state: {
    data: '',
  },
  mutations: {},
  actions: {
    getParties: async (): Promise<Party[]> => {
      try {
        return await partyAxios.getParties()
      } catch (error: any) {
        console.log(error)
        // Code에 따라 에러 핸들링
        throw new Error(error)
      }
    },
    getParty: async (_, partyId: number | string): Promise<Party> => {
      try {
        return await partyAxios.getParty(+partyId)
      } catch (error: any) {
        console.log(error)
        throw new Error(error)
      }
    },
    async postParty(_, data: SubmitFormData): Promise<Party> {
      try {
        console.log(data)
        return await partyAxios.postParty(data)
      } catch (error: any) {
        console.log(error)
        throw new Error(error)
      }
    },
    async getProviders() {
      try {
        return await partyAxios.getProviders()
      } catch (error) {
        console.log(error)
      }
    },
    async postJoinParty(_, partyId: number) {
      try {
        await partyAxios.postJoinParty(partyId)
      } catch (error) {
        alert(error)
        throw new Error()
      }
    },
  },
  getters: {},
}
