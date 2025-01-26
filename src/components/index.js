// 插件全局注册
import cardDetail from './cardDetail.vue'
import backPage from './backPage.vue'
import cardSkeleton from '@/components/cardSkeleton.vue'
export const componentPlugin = {
  install(app) {
    app.component('BLCardDetail', cardDetail)
    app.component('BLBackPage', backPage)
    app.component('BLCardSkeleton', cardSkeleton)
  }
}
