<script setup>
import { useRoute } from 'vue-router'
import { computed, onMounted, ref } from 'vue'
import HomeCard from '@/views/Explore/components/homeCard.vue'
import { doFocus, queryUserIndex, queryUserPost } from '@/apis/main'
import { useDetail } from '@/composables/useDetail'
import { onClickOutside, useResizeObserver } from '@vueuse/core'
import { useUserStore } from '@/stores/useUserStore'
import { ElMessage } from 'element-plus'
import { WaterFall } from '@/utils/waterFall'
import throttle from '@/utils/throttle'

const route = useRoute()
const Details = useDetail()
const userStore = useUserStore()

// 加载用户信息 //////////////////////////////////////////////////////////////
const userInfo = ref({})
const userSkeleton = computed(() => Boolean(Object.keys(userInfo.value).length === 0))
const getUserInfo = async () => {
  const id = route.params.id
  const res = await queryUserIndex({ id })
  userInfo.value = res.data
  document.title = res.data.user.username + ' .Bird Lover'
}
const doFocusOn = async (id) => {
  if (userStore.userInfo.id === id) {
    ElMessage({ type: 'warning', message: '不能对自己进行关注操作' })
    return
  }
  const res = await doFocus({ id })
  userStore.extendUserInfo(1, id)
  ElMessage({ type: 'success', message: res.info })
}
// 主页切换标签 //////////////////////////////////////////////////////////////
const radio = ref('post')
const userPost = ref([])
const userCollect = ref([])
const userFavorite = ref([])

const columns = ref(0)
const card_columns = ref({})

const waterFallWrapper = ref(null)
const waterFall = new WaterFall(columns, card_columns, userPost)

useResizeObserver(waterFallWrapper, (entries) => {
  const { width, height } = entries[0].contentRect
  waterFall.calculate(width)
  waterFall.init()
})

const typeMap = {
  post: {
    name: '帖子',
    data: userPost,
    emptyDescription: '现在还没有帖子...',
    firstLoaded: ref(false),
    LoadedFinished: ref(false)
  },
  collect: {
    name: '收藏',
    data: userCollect,
    emptyDescription: '现在还没有收藏...',
    firstLoaded: ref(false),
    LoadedFinished: ref(false)
  },
  like: {
    name: '点赞',
    data: userFavorite,
    emptyDescription: '现在还没有点赞...',
    firstLoaded: ref(false),
    LoadedFinished: ref(false)
  }
}

const FirstLoading = computed(() => !typeMap[radio.value].firstLoaded.value)
const infiniteLoadDisabled = computed(() => typeMap[radio.value].LoadedFinished.value)
// 请求用户投稿数据
const Toggle = async () => {
  // 切换标签页
  const type = radio.value
  waterFall.cards = typeMap[type].data
  waterFall.calculate()
  const user_id = route.params.id
  const offset = 0
  // 仅在第一次加载时请求数据
  if (!typeMap[type].firstLoaded.value) {
    const post = await queryUserPost({ user_id, types: typeMap[type].name, offset })
    typeMap[type].firstLoaded.value = true
    typeMap[type].data.value = post.info
    waterFall.cards = typeMap[type].data
  }
  waterFall.init()
}

// 加载新数据时的节流
const infiniteLoad = throttle(async () => {
  const type = radio.value
  const user_id = userInfo.value.user.id
  const offset = typeMap[type].data.value.length
  const post = await queryUserPost({ user_id, types: typeMap[type].name, offset })
  if (post.info.length === 0) {
    // 没有更多数据，禁用滚动加载
    typeMap[type].LoadedFinished.value = true
  } else {
    typeMap[type].data.value = [...typeMap[type].data.value, ...post.info]
    waterFall.loadMore(post.info)
  }
}, 300)

// 卡片详情页的内容 //////////////////////////////////////////////////////////
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
}
const afterDoComment = (comment) => Details.afterDoComment(comment)
const close = () => {
  overlayShow.value = false
}
onClickOutside(overlay, () => {
  overlayShow.value = false
})
// 卡片详情页的内容结束 //////////////////////////////////////////////////////////
onMounted(async () => {
  await Promise.all([getUserInfo(), Toggle()])
})
</script>

<template>
  <el-skeleton class="userInfo-skeleton" :loading="userSkeleton">
    <template #template>
      <div class="userInfo wrapper">
        <el-skeleton-item variant="circle" />
        <div class="skeleton-text">
          <el-skeleton-item variant="p" style="width: 60%" />
          <el-skeleton-item variant="p" style="width: 80%" />
          <el-skeleton-item variant="p" style="width: 60%" />
        </div>
        <div class="skeleton-text">
          <el-skeleton-item variant="p" style="width: 40%" />
        </div>
      </div>
    </template>
    <template #default>
      <div class="userInfo" v-if="userInfo.user">
        <el-row>
          <el-col :span="9">
            <el-avatar :size="150" :src="userInfo.user.avatar"></el-avatar>
          </el-col>
          <el-col :span="9">
            <h2>{{ userInfo.user.username }}</h2>
            <p>{{ userInfo.user.signature }}</p>
            <div class="tag-area">
              <el-tag type="info" round>{{ userInfo.user.focusOn }} 关注</el-tag>
              <el-tag type="success" round>{{ userInfo.user.fans }} 粉丝</el-tag>
              <el-tag type="primary" round> {{ userInfo.user.postsCount }} 笔记数 </el-tag>
            </div>
          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="doFocusOn(userInfo.user.id)"> 关注 </el-button>
          </el-col>
        </el-row>
      </div>
    </template>
  </el-skeleton>
  <div class="check-box" @change="Toggle">
    <el-radio-group v-model="radio" size="large">
      <el-radio-button
        v-for="(type, index) in Object.keys(typeMap)"
        :key="index"
        :label="typeMap[type].name"
        :value="type"
      />
    </el-radio-group>
  </div>
  <div ref="waterFallWrapper">
    <BLCardSkeleton :loading="FirstLoading" :columns="columns" :rows="2" class="user-home-card">
      <template #default>
        <div v-if="typeMap[radio].data.length === 0">
          <el-empty :description="typeMap[radio].emptyDescription" />
        </div>
        <div
          class="infinite-container"
          v-infinite-scroll="infiniteLoad"
          :infinite-scroll-disabled="infiniteLoadDisabled"
          :infinite-scroll-delay="200"
          :infinite-scroll-distance="100"
          v-else
        >
          <home-card :card_columns="card_columns" @show-detail="showMessage"></home-card>
        </div>
      </template>
    </BLCardSkeleton>
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
          <BLCardDetail :detail="detail" @afterDoComment="afterDoComment" ref="overlay" />
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/components/cardCommon';
.userInfo-skeleton {
  --el-skeleton-circle-size: 150px;
  .skeleton-text {
    width: 150px;
    height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    margin-left: 20px;
  }
}
.userInfo {
  display: flex;
  align-items: center;
  justify-content: center;
  .el-col {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
  }
}
.check-box {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}
.user-home-card {
  margin-top: 30px;
}
.tag-area {
  width: 400px;
}
</style>
