<script setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()
// searchValue
const searchInput = ref('')
// search
const searchThings = () => {
  router.replace(`/?query=${searchInput.value}`)
}
import { Sunny, Moon } from '@element-plus/icons-vue'
import { useDark, useToggle } from '@vueuse/core'
const props = defineProps({
  msg: String
})
const isDark = useDark()
const toggleDark = useToggle(isDark)
</script>

<template>
  <el-row class="header-bar">
    <el-col :span="4">
      <!-- icon  -->
      <RouterLink class="banner-link" to="/">
        <img class="banner" src="/banner.png" alt="" />
      </RouterLink>
    </el-col>
    <el-col :span="18">
      <el-input
        v-model="searchInput"
        placeholder="搜索点什么...."
        @keyup.enter="searchThings"
        :prefix-icon="Search"
        clearable
      />
    </el-col>
    <el-col :span="2" style="text-align: center">
      <el-switch
        v-model="isDark"
        :active-icon="Moon"
        :inactive-icon="Sunny"
        inline-prompt
        @change="toggleDark"
        size="large"
      />
    </el-col>
  </el-row>
</template>

<style scoped lang="scss">
.header-bar {
  flex: 1;
  margin-top: 1rem;
}
.banner-link {
  display: block;
  width: 10rem;
  @media (max-width: 768px) {
    width: 6rem;
  }
  .banner {
    width: 100%;
  }
}
:deep .el-input__wrapper {
  border-radius: 100px !important;
  font-size: 1.2rem;
  height: 3rem;
}
</style>
