<script setup>
import { onMounted, ref } from 'vue'
import HomeCard from '@/views/Explore/components/homeCard.vue'
import { queryPost } from '@/apis/main'
import { onBeforeRouteUpdate, useRoute, useRouter } from 'vue-router'
import { useDetail } from '@/composables/useDetail'
import { onClickOutside } from '@vueuse/core'
import { WaterFall } from '@/utils/waterFall'
import { useResizeObserver } from '@vueuse/core'
import throttle from '@/utils/throttle'

const route = useRoute()
const router = useRouter()
const query = route.query.query
const Details = useDetail()

////////////////////////主页卡片 ////////////////////////////////////////////////////
const cards = ref([])
const disabled = ref(false)

const columns = ref(0)
const card_columns = ref({})

const waterFallWrapper = ref(null)
const waterFall = new WaterFall(columns, card_columns, cards)

useResizeObserver(waterFallWrapper, (entries) => {
  const { width, height } = entries[0].contentRect
  waterFall.calculate(width)
  waterFall.init()
})

// 主页获取帖子
const doQuery = async (offset) => {
  const res = await queryPost({ offset, query })
  cards.value = res.info
}
// 无限滚动
const load = throttle(async () => {
  const offset = cards.value.length
  const res = await queryPost({ offset, query })
  const more = res.info
  if (more.length === 0) {
    disabled.value = true // 没有更多数据，禁用滚动加载
  } else {
    cards.value = [...cards.value, ...more]
    waterFall.loadMore(more)
  }
}, 300)

/////////////////////////////卡片详情 ///////////////////////////////////////////////
const detail = Details.detail
const overlayShow = ref(false)
const overlayX = ref(0) // 覆盖层的水平位置
const overlayY = ref(0) // 覆盖层的垂直位置
const overlay = ref(null)

const getDetails = async (id) => Details.getDetail(id)
const showMessage = async (id, left, top) => {
  overlayX.value = left
  overlayY.value = top
  await getDetails(id)
  overlayShow.value = true
  await router.push('/explore/' + id)
}
const afterDoComment = (comment) => Details.afterDoComment(comment)
const close = () => {
  overlayShow.value = false
  router.replace('/')
}
onClickOutside(overlay, close)

// /////////////////////////初始化页面布局/////////////////////////////////////////

const singleCard = ref(false)
const cardLoading = ref(true)

async function initializeHomePage() {
  await doQuery(0)
  cardLoading.value = false
}

//  仅在本路由挂载后，则用户是点击进入详情页，弹出详情页
onMounted(async () => {
  if (route.params.id) {
    await getDetails(route.params.id)
    singleCard.value = true
  } else {
    await initializeHomePage()
  }
})
// 从详情页子路由返回时，刷新主页
onBeforeRouteUpdate(async (to, from, next) => {
  if (!to.params.id && singleCard.value) {
    singleCard.value = false
    await initializeHomePage()
  }
  next()
})
</script>

<template>
  <router-view
    class="single-card"
    v-if="singleCard"
    :detail="detail"
    :afterDoComment="afterDoComment"
  ></router-view>
  <div v-else ref="waterFallWrapper">
    <BLCardSkeleton :loading="cardLoading" :columns="columns" :rows="3">
      <template #default>
        <div class="empty" v-if="cards.length === 0">
          <el-empty description="没有帖子..."></el-empty>
        </div>
        <div v-else>
          <div
            class="infinite-container"
            v-infinite-scroll="load"
            :infinite-scroll-disabled="disabled"
            :infinite-scroll-distance="200"
          >
            <home-card
              :card_columns="card_columns"
              @show-detail="showMessage"
              ref="homeCardRef"
            ></home-card>
          </div>
          <div>
            <div v-show="overlayShow" class="overlay-background"></div>
            <BLBackPage v-show="overlayShow" @click="close"></BLBackPage>
            <transition
              name="pop-transition"
              :style="{
                '--overlay-x': `${overlayX}px`,
                '--overlay-y': `${overlayY}px`
              }"
            >
              <div class="overlay" v-if="overlayShow">
                <router-view
                  :detail="detail"
                  :afterDoComment="afterDoComment"
                  ref="overlay"
                ></router-view>
              </div>
            </transition>
          </div>
        </div>
      </template>
    </BLCardSkeleton>
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/components/cardCommon';
.single-card {
  margin: 0 auto;
}
.empty {
  margin-top: 10%;
}
</style>
