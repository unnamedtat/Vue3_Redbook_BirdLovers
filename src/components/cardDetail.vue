<script setup>
import { ChatRound, Edit } from '@element-plus/icons-vue'
import { onMounted, ref, computed } from 'vue'
import {
  doComment,
  doFocus,
  unFollow,
  controlUserCollectOrLike,
  getComment,
  loadReplies
} from '@/apis/main'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/useUserStore'
import { getCurrentTime } from '@/utils/getTime'
import { useRouter } from 'vue-router'

const props = defineProps({
  detail: {
    type: Object,
    required: true
  }
})
const user_id = ref(props.detail.user.id)
const comments = ref([])
// 子传父
const emit = defineEmits(['afterDoComment'])
const userStore = useUserStore()

const router = useRouter()
// 更改用户对帖子的状态 /////////////////////////////////////////////////
const isLogin = computed(() => {
  return userStore.userInfo && Object.keys(userStore.userInfo).length > 0
})
const handleLoginRedirect = () => {
  ElMessage({ type: 'warning', message: `请先登录!` })
  setTimeout(() => {
    router.push('/login')
  }, 3)
}
const doFocusOn = async () => {
  if (userStore.userInfo.id === user_id.value) {
    ElMessage({ type: 'warning', message: '不能对自己进行关注操作' })
    return
  }
  const res = await doFocus({ id: user_id.value })
  userStore.extendUserInfo(1, user_id.value)
  ElMessage({ type: 'success', message: res.info })
}
const cancelFocusOn = async () => {
  const res = await unFollow({ id: user_id.value })
  userStore.removeFocus(1, user_id.value)
  ElMessage({ type: 'success', message: res.info })
}

const checkFollow = computed(() => {
  return userStore.userFocus.includes(user_id.value)
})
const checkCollect = (id) => {
  return userStore.userCollect.includes(id)
}
const checkFavorite = (id) => {
  return userStore.userFavorite.includes(id)
}
//更改帖子的点赞收藏状态
const doCommentState = async (type, detail) => {
  const post_id = detail.id
  if (type === 'like') {
    const operator = checkFavorite(post_id)
    const res = await controlUserCollectOrLike({ post_id, operator, type })
    if (operator) {
      userStore.removeFocus(2, post_id)
      detail.likeCount--
      ElMessage({ type: 'success', message: res.info })
    } else {
      userStore.extendUserInfo(2, post_id)
      detail.likeCount++
      ElMessage({ type: 'success', message: res.info })
    }
  } else if (type === 'collect') {
    const operator = checkCollect(post_id)
    const res = await controlUserCollectOrLike({ post_id, operator, type })
    if (operator) {
      detail.collectCount--
      userStore.removeFocus(3, post_id)
      ElMessage({ type: 'success', message: res.info })
    } else {
      detail.collectCount++
      userStore.extendUserInfo(3, post_id)
      ElMessage({ type: 'success', message: res.info })
    }
  }
}
//////////////////////////////////////////////////////////////////

// 评论内容////////////////////////////////////////////////////////
const content = ref('')
const to = ref(0)
const commentInput = ref(null)
const sendComment = async (post, to) => {
  const info = ref([
    {
      id: 0,
      user: userStore.userInfo,
      content: content.value,
      createTime: getCurrentTime(),
      replyCount: 0,
      replies: []
    }
  ])
  if (to === 0 || to === '0') {
    const data = {
      post_id: post.id,
      content: content.value
    }
    const res = await doComment({ data })
    ElMessage({ type: 'success', message: res.info })
    info.value[0].id = res.id
    console.log(res.id, info.value)
    comments.value = [...comments.value, ...info.value]
  } else {
    const data = {
      post_id: post.id,
      content: content.value,
      parent_comment_id: to
    }
    const res = await doComment({ data })
    ElMessage({ type: 'success', message: res.info })
    const comment = comments.value.find((item) => item.id === to)
    comment.replies = [...comment.replies, ...info.value]
    clearReply()
  }
  emit('afterDoComment')
  content.value = ''
}
const commentMain = (item) => {
  to.value = item.id
  const toPeople = item.user.username
  commentInput.value.input.placeholder = `回复${toPeople}: `
}
const loadReply = async (item) => {
  const offset = item.replies.length
  const id = item.id
  const res = await loadReplies({ id, offset })
  item.replies = [...item.replies, ...res.info]
  item.replyCount -= res.count
}
const clearReply = () => {
  content.value = ''
  to.value = 0
}
/////////////////////////////////////////////////////////////////

// 无限加载评论 //////////////////////////////////////////////////
const disabled = ref(true)
const load = async () => {
  disabled.value = true
  const offset = comments.value.length
  const id = props.detail.id
  const res1 = await getComment({ id, offset })
  const data = res1.info
  if (data.length !== 0) {
    disabled.value = false
    comments.value = [...comments.value, ...data]
  } else {
    disabled.value = true
  }
}
//////////////////////////////////////////////////////////////

onMounted(() => load())
</script>

<template>
  <div class="box" v-if="detail.id">
    <!-- 图片区 -->
    <div class="card-img">
      <el-carousel>
        <el-carousel-item v-for="item in detail.imgs" :key="item">
          <img class="image" :src="item" alt="" />
        </el-carousel-item>
      </el-carousel>
    </div>
    <!-- 卡牌详情区 -->
    <div class="card-text-content">
      <!-- 卡片头部 -->
      <el-row class="card-publish-user">
        <router-link :to="`/user/index/${detail.user.id}`">
          <el-avatar :src="detail.user.avatar" size="large" />
        </router-link>
        <div class="username">{{ detail.user.username }}</div>
        <el-button type="info" @click="cancelFocusOn" class="focus-on-btn" v-if="checkFollow">
          已关注
        </el-button>
        <el-button
          type="primary"
          class="focus-on-btn"
          v-else
          @click="isLogin ? doFocusOn : handleLoginRedirect()"
        >
          关注
        </el-button>
      </el-row>
      <!-- 卡片头部结束 -->
      <el-row class="card-main-content">
        <!-- 卡片内容 -->
        <h2 class="card-title">{{ detail.title }}</h2>
        <p class="card-content">{{ detail.content }}</p>
        <time class="time">{{ detail.createTime }}</time>
        <!-- 卡片内容结束 -->
        <hr />
        <!-- 评论区 -->
        <div v-if="comments" v-infinite-scroll="load" :infinite-scroll-disabled="disabled">
          <el-empty description="现在还没有评论" v-if="comments.length === 0" />
          <div v-else class="comments-box">
            <div class="comments-title">共{{ detail.commentCount }}条评论</div>
            <div v-for="item in comments" :key="item.id">
              <el-row :gutter="10">
                <el-col :span="2.5">
                  <a :href="`/user/index/${item.user.id}`">
                    <el-avatar :src="item.user.avatar" :size="30"></el-avatar>
                  </a>
                </el-col>
                <el-col :span="20">
                  <div>{{ item.user.username }}</div>
                  <div class="comment-text">{{ item.content }}</div>
                  <time class="time">{{ item.createTime }}</time>
                  <el-icon style="float: right; font-size: medium" @click="commentMain(item)">
                    <ChatRound />
                  </el-icon>
                </el-col>
                <el-col class="sub-comments">
                  <div v-for="reply in item.replies" :key="reply.id">
                    <!-- 渲染子评论的内容 -->
                    <el-row style="margin-left: 2rem">
                      <el-col :span="2.5">
                        <a :href="`/user/index/${reply.user.id}`">
                          <el-avatar :src="reply.user.avatar" :size="25"></el-avatar>
                        </a>
                      </el-col>
                      <el-col :span="20">
                        <div>{{ reply.user.username }}</div>
                        <div class="comment-text">{{ reply.content }}</div>
                        <time class="time">{{ reply.createTime }}</time>
                      </el-col>
                    </el-row>
                  </div>
                  <div class="more" @click="loadReply(item)" v-if="item.replyCount > 0">
                    展开{{ item.replyCount }}条回复
                  </div>
                </el-col>
              </el-row>
              <el-divider />
            </div>
          </div>
        </div>
      </el-row>
      <!-- 评论区结束 -->
      <el-divider style="margin-top: 0" />
      <el-row class="comment-editor">
        <el-row>
          <el-button link @click="isLogin ? doCommentState('like', detail) : handleLoginRedirect()">
            <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" width="25" height="25">
              <path
                d="M512 901.746939c-13.583673 0-26.122449-4.179592-37.093878-13.061225-8.881633-7.314286-225.697959-175.020408-312.424489-311.379592C133.746939 532.37551 94.040816 471.24898 94.040816 384.522449c0-144.718367 108.146939-262.269388 240.326531-262.269388 67.395918 0 131.657143 30.82449 177.632653 84.636735 45.453061-54.334694 109.191837-84.636735 177.110204-84.636735 132.702041 0 240.326531 117.55102 240.326531 262.269388 0 85.159184-37.093878 143.673469-67.395919 191.216327l-1.044898 1.567346c-86.726531 136.359184-303.542857 304.587755-312.424489 311.379592-10.44898 8.359184-22.987755 13.061224-36.571429 13.061225z"
                :fill="!checkFavorite(detail.id) ? '#cecccc' : '#d81e06'"
                p-id="3346"
              ></path>
            </svg>
            <el-text size="large" type="info">{{ detail.likeCount }}</el-text>
          </el-button>
          <el-button
            link
            @click="isLogin ? doCommentState('collect', detail) : handleLoginRedirect()"
          >
            <svg
              x="1689148085763"
              class="icon"
              viewBox="0 0 1024 1024"
              xmlns="http://www.w3.org/2000/svg"
              p-id="4912"
              width="25"
              height="25"
            >
              <path
                d="M512.009505 25.054894l158.199417 320.580987 353.791078 51.421464L767.995248 646.579761l60.432101 352.365345-316.417844-166.354615-316.436854 166.354615 60.432101-352.365345L0 397.057345l353.791078-51.421464z"
                :fill="!checkCollect(detail.id) ? '#cecccc' : '#f4ea2a'"
                p-id="4913"
              ></path>
            </svg>
            <el-text size="large" type="info">{{ detail.collectCount }}</el-text>
          </el-button>
          <el-button link @click="clearReply">
            <svg
              x="1689148939874"
              class="icon"
              viewBox="0 0 1024 1024"
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              p-id="6375"
              width="25"
              height="25"
            >
              <path
                d="M512 0C226.742857 0 0 197.485714 0 446.171429c0 138.971429 73.142857 270.628571 190.171429 351.085714L190.171429 1024l226.742857-138.971429c29.257143 7.314286 65.828571 7.314286 95.085714 7.314286 285.257143 0 512-197.485714 512-446.171429C1024 197.485714 797.257143 0 512 0zM256 512C219.428571 512 190.171429 482.742857 190.171429 446.171429S219.428571 380.342857 256 380.342857c36.571429 0 65.828571 29.257143 65.828571 65.828571S292.571429 512 256 512zM512 512C475.428571 512 446.171429 482.742857 446.171429 446.171429S475.428571 380.342857 512 380.342857c36.571429 0 65.828571 29.257143 65.828571 65.828571S548.571429 512 512 512zM768 512C731.428571 512 702.171429 482.742857 702.171429 446.171429s29.257143-65.828571 65.828571-65.828571c36.571429 0 65.828571 29.257143 65.828571 65.828571S804.571429 512 768 512z"
                p-id="6376"
                fill="#cecccc"
              ></path>
            </svg>
            <el-text size="large" type="info">{{ detail.commentCount }}</el-text>
          </el-button>
        </el-row>
        <el-input
          v-model="content"
          type="text"
          placeholder="说点什么..."
          ref="commentInput"
          :prefix-icon="Edit"
          @keyup.enter="isLogin ? sendComment(detail, to) : handleLoginRedirect()"
          clearable
        />
      </el-row>
    </div>
    <!-- 卡牌详情区结束 -->
  </div>
</template>

<style scoped lang="scss">
$box-height: calc(90vh - $header-height);
$card-user-height: 4rem;
$card-comment-editor-height: 4rem;
@mixin layout--narrow {
  // 父元素尺寸小或适应小尺寸，高度比例固定的布局
  display: block;
  width: 100%;
  height: 100%;
  box-shadow: none;
  border-radius: 0;
  .card-img {
    :deep(.el-carousel__container) {
      height: 40vh;
    }
  }
  .card-text-content {
    height: calc(100% - 40vh - #{$card-comment-editor-height});
  }
}
.box {
  transition:
    width 0.3s,
    height 0.3s;
  display: flex;
  overflow: hidden;
  background-color: var(--el-bg-color);
  border-radius: 0.8rem;
  width: 60vw;
  height: $box-height;
  box-shadow:
    -16px 28px 28px -3px rgba(0, 0, 0, 0.1),
    0px 10px 61px -8px rgba(0, 0, 0, 0.1);
  .card-img {
    flex: 14;
    background-color: var(--el-bg-color-page);
    :deep(.el-carousel__container) {
      height: $box-height;
    }
    .image {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
  }
  .card-text-content {
    flex: 10;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    height: 100%;
    .card-publish-user {
      align-items: center;
      height: $card-user-height;
      .username {
        line-height: $card-user-height;
        text-align: center;
        align-items: center;
        font-size: 1.5rem;
        margin-left: 1rem;
        color: var(--el-text-color-regular);
      }
      .focus-on-btn {
        margin-left: auto;
      }
    }
    .card-main-content {
      display: block;
      flex: 1;
      overflow-y: scroll;
      overflow-x: hidden;
      .card-title {
        font-size: 1.4rem;
        line-height: 2rem;
        color: var(--el-text-color-primary);
      }
      .card-content {
        font-size: 1.2rem;
        line-height: 2rem;
        color: var(--el-text-color-primary);
        white-space: pre-wrap;
        overflow-wrap: break-word;
      }
      .time {
        color: var(--el-text-color-secondary);
      }
      .comments-box {
        color: var(--el-text-color-secondary);
        .comment-text {
          margin: 0.5rem;
        }
        .sub-comments {
          margin-top: 0.5rem;
        }
        .comments-title {
          margin: 0.5rem 0 0.5rem 0;
          line-height: 1.3rem;
        }
        .more {
          margin-left: 2rem;
          margin-top: 1rem;
          cursor: pointer;
        }
      }
    }
  }
  .comment-editor {
    height: $card-comment-editor-height;
  }
  @media screen and (max-width: 1080px) {
    @include layout--narrow;
  }
}
</style>
