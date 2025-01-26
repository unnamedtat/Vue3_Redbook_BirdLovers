<script setup>
import { ref } from 'vue'
import { Promotion, Expand, Tools, House, Document, User } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/useUserStore'
import { ElMessage } from 'element-plus'
import LoginCard from '@/views/Login/components/loginCard.vue'
import { onClickOutside } from '@vueuse/core'
import AsideButton from '@/views/Home/components/asideButton.vue'
import UserInfoDialog from '@/views/Home/components/userInfoDialog.vue'

const userStore = useUserStore()
// 控制菜单样式
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}
// 登出
const confirm = async () => {
  const res = await userStore.userLogout()
  ElMessage({ type: 'success', message: res.info })
}
// 显示登录界面
const show = ref(false)
const changeShow = () => {
  show.value = !show.value
}
const userInfoDialog = ref(null)
const openDialog = () => {
  userInfoDialog.value.openDialog()
}
const overlay = ref(null)

onClickOutside(overlay, () => {
  show.value = false
})
</script>

<template>
  <nav style="user-select: none" class="menu" :class="{ open: isMenuOpen }">
    <el-tooltip effect="dark" content="切换菜单样式" placement="right">
      <div class="actions-bar">
        <div>
          <el-button id="menuBtn" @click="toggleMenu">
            <el-icon><Expand /></el-icon>
          </el-button>
          <p
            class="menu-text"
            :class="{ 'text-open': isMenuOpen }"
            v-show="userStore.userInfo.username"
          >
            你好，{{ userStore.userInfo.username }}！
          </p>
        </div>
      </div>
    </el-tooltip>
    <ul class="options-bar">
      <li class="menu-item">
        <aside-button
          to="/"
          tooltipContent="主页，发现新事物"
          text="主页"
          :isMenuOpen="isMenuOpen"
          :icon="House"
        />
      </li>
      <li class="menuBreak">
        <hr />
      </li>
      <li class="menu-item">
        <aside-button
          to="/user/uploads"
          tooltipContent="发布观鸟"
          text="发布"
          :isMenuOpen="isMenuOpen"
          :icon="Promotion"
        />
      </li>
      <li class="menu-item" v-if="userStore.userInfo.id">
        <aside-button
          :icon="Tools"
          text="更新个人信息"
          tooltip-content="更新个人信息"
          :is-menu-open="isMenuOpen"
          :show-if="userStore.userInfo.id"
          @click="openDialog"
        />
      </li>
      <li class="menu-item" v-if="userStore.userInfo.id">
        <aside-button
          to="/user/control"
          tooltipContent="个人帖子管理"
          text="个人帖子管理"
          :isMenuOpen="isMenuOpen"
          :icon="Document"
        />
      </li>
    </ul>
    <div class="userInfo-bar">
      <div v-if="userStore.userInfo.id">
        <div class="menuUser">
          <RouterLink :to="`/user/index/${userStore.userInfo.id}`">
            <img :src="userStore.userInfo.avatar" alt="avatar" />
            <p class="username menu-text" :class="{ 'text-open': isMenuOpen }" v-show="isMenuOpen">
              {{ userStore.userInfo.username }}
            </p>
            <p class="menu-text arrow" :class="{ 'text-open': isMenuOpen }">
              <i class="iconfont icon-youjiantou"></i>
            </p>
          </RouterLink>
        </div>
        <div class="exit-button">
          <el-tooltip effect="dark" content="退出登录" placement="right">
            <div>
              <el-popconfirm
                @confirm="confirm"
                title="确认退出吗?"
                confirm-button-text="确认"
                cancel-button-text="取消"
              >
                <template #reference>
                  <button type="button" @click="">
                    <i class="iconfont icon-tuichu"></i>
                  </button>
                </template>
              </el-popconfirm>
            </div>
          </el-tooltip>
        </div>
      </div>
      <div v-else>
        <el-tooltip content="登录" placement="right">
          <div class="exit-button">
            <div>
              <button title="登录" type="button" @click="changeShow">
                <el-icon size="x-large">
                  <User />
                </el-icon>
              </button>
            </div>
          </div>
        </el-tooltip>
      </div>
    </div>
  </nav>
  <div class="overlay" v-if="show">
    <login-card @changeShow="changeShow" ref="overlay" />
  </div>
  <user-info-dialog ref="userInfoDialog"></user-info-dialog>
</template>

<style scoped lang="scss">
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
}

.iconfont {
  font-size: $aside-icon-font-size;
}

.menu {
  width: $aside-bar-width;
  &.open {
    width: $aside-bar-open-width;
    #menuBtn {
      transform: rotate(180deg);
    }
  }
  height: 100%;
  transition: 0.3s ease 0.15s;
  display: flex;
  flex-direction: column;
  .actions-bar {
    flex: 1;
    padding: 0.5rem;
    overflow: hidden;
    div {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      transition: 0.3s ease;
      p {
        width: calc(100% - 45px);
        text-align: center;
      }
      #menuBtn {
        border-radius: 0.2rem;
        font-size: $aside-icon-font-size;
        border: none;
        width: $aside-icon-size;
        height: $aside-icon-size;
      }
    }
  }
  .options-bar {
    overflow: hidden;
    flex: 6;
    display: flex;
    padding: 0 0.5rem;
    align-items: center;
    flex-direction: column;
    .menu-item {
      width: 100%;
      height: 45px;
      margin: 0.3rem;
    }
  }
  .userInfo-bar {
    flex: 3;
    display: flex;
    flex-direction: column-reverse;
    .menuUser {
      padding-left: 0.5rem;
      flex: 0 0 25%;
      a {
        overflow: hidden;
        display: block;
        position: relative;
        &:hover p {
          animation: animArrow 0.3s ease 2;
        }
        p {
          position: absolute;
          top: calc((100% - $aside-icon-font-size) / 2);
          left: calc(90% - $aside-icon-font-size);
        }
        .username {
          font-size: 1rem;
          left: 40%;
        }
        img {
          //margin-left: ;
          width: $aside-icon-size;
          height: $aside-icon-size;
          object-fit: cover;
          border-radius: 0.5rem;
        }
      }
    }
    .exit-button {
      overflow: hidden;
      flex: 0 0 25%;
      width: 100%;
      //height: $aside-icon-font-size;
      padding: 1rem;
      div {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: space-around;
        border-radius: 0.5rem;
        transition: 0.3s ease;
        button {
          background-color: transparent;
          outline: none;
          border: none;
          border-radius: 0.5rem;
          //color: #000;
          width: 100%;
          height: 45px;
          transition: 0.3s ease;
          font-size: 1rem;
          &:hover {
            color: var(--el-color-error);
          }
        }
      }
    }
  }
  .menu-text {
    transform: translateX(-17.8rem);
    opacity: 0;
    transition: transform 0.3s ease 0.1s;
    &.text-open {
      color: var(--el-text-color-primary);
      opacity: 1;
      transform: translateX(0);
    }
  }
  .menuBreak {
    width: 100%;
    height: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    hr {
      width: 90%;
      height: 2px;
      background-color: var(--el-text-color-primary);
      border: none;
      border-radius: 5px;
    }
  }
}

@keyframes animArrow {
  0% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(0.5rem);
  }
  100% {
    transform: translateX(0);
  }
}
</style>
