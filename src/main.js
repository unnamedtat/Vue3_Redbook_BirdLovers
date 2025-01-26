import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import '@/assets/font/iconfont.css'
import '@/styles/common.scss'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import '@/styles/element/dark.scss'
import { componentPlugin } from '@/components'
import { lazyPlugin } from '@/directives'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia).use(router).use(componentPlugin).use(lazyPlugin).mount('#app')
