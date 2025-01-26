<script setup>
import headNav from '@/views/Home/components/headNav.vue'
import asideNav from '@/views/Home/components/asideNav.vue'
</script>

<template>
  <el-container class="container">
    <el-header>
      <head-nav />
    </el-header>
    <el-container class="content-container">
      <el-aside>
        <aside-nav />
      </el-aside>
      <el-main>
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped lang="scss">
.el-container {
  height: 100vh;
  width: 100vw;
  .el-header {
    height: $header-height;
  }
  .el-main {
    flex: 1;
    overflow-y: scroll;
  }
  .el-aside {
    height: calc(100vh - $header-height);
    width: auto !important;
  }
}
</style>
