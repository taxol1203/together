import { createStore } from 'vuex'
import { content } from '@/store/modules/content'
import { party } from '@/store/modules/party'
import { auth } from '@/store/modules/auth'

export interface RootState {
  data: string
}

export default createStore<RootState>({
  modules: { content, party, auth },
})
