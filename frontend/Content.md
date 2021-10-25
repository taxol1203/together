### ContentMainInfo

#### Props에 TypeScript type 적용하기

```typescript
import { defineComponent, PropType } from 'vue'

interface Content {
  id: number
  title: string
  posterPath: string
  simRate: number
  providers: string[]
  firstAirYear: number
  rated: string
  seasons: number
  overview: string
}

export default defineComponent({
  props: {
    content: {
      type: Object as PropType<Content>,
    },
  },
  setup() {
    return {}
  },
})
```



### ContentDetail

#### 화면 크기에 따라 InfoSection의 위치를 변경하기

- 하나의 컴포넌트를 만들고, 두 위치에 삽입

  1. v-if 사용

  2. CSS display:none 사용

     ```vue
     <ContentDetailInfoSection class="hidden" :content="content" />
     // 적용되지 않음
     // Section 내부의 클래스 선택을 통해 부여한 CSS가 우선순위
     ```

     

- addEventListener의 resize 이벤트 타겟이 innerWidth를 갖고 있지 않다는 문제

  [해결 방법](https://stackoverflow.com/questions/51955307/property-innerwidth-does-not-exist-on-type-eventtarget/60800415#60800415?newreg=9915b0ca39c44cfcad75cf415afbc2e5)

  ```typescript
  addEventListener('resize', (e) => {
      innerWidth.value = e.target.innerWidth
      // 에러 발생
  })
  
  // 해결 방법
  // target에 Window타입을 적용한다.
  addEventListener('resize', (e) => {
      const w = e.target as Window
      innerWidth.value = w.innerWidth
  })
  ```



### TailwindCSS

#### .container라는 클래스에 속성 지정하기

[Tailwind `.container` the right way!](https://dev.to/bourhaouta/tailwind-container-the-right-way-5g77)

```javascript
// tailwind.config.js
module.exports = {
  plugins: [
    ({ addComponents }) => {
      addComponents({
        ".container": {
          "@apply px-4 mx-auto": {},
        },
      });
    },
  ],
};
```



### Axios

#### Error Type Handling

[참고링크](https://github.com/axios/axios/issues/3612#issuecomment-770224236)

```typescript
axios()
	.then()
    .catch((err: Error | AxiosError) {
    	if (axios.isAxiosError(error))  {
        	// Access to config, request, and response
        } else {
            // Just a stock error
        }
    })
```



### Vuex

#### Module

```typescript
// index.ts

import { createStore } from 'vuex'
import { content } from '@/store/modules/content'

export interface RootState {
  data: string
}

export default createStore<RootState>({
  modules: { content },
})
```



```typescript
// Module
import axios from 'axios'
import { Module } from 'vuex'
import { RootState } from '@/store/index'

interface ProfileState {
  data: string
}

interface Content {
  id: number
  title: string
  posterPath: string
  simRate: number
  providers: string[]
  firstAirYear: number
  rated: string
  seasons: number
  overview: string
}

const apiAxios = axios.create({
  baseURL: 'http://localhost:3000',
})

export const content: Module<ProfileState, RootState> = {
    namespaced: true,
    state: {},
    mutations: {},
    actions: {},
    getters: {},
}
```

