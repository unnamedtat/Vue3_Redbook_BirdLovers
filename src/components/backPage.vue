<script setup>
import { Back } from '@element-plus/icons-vue'
</script>
<template>
  <el-button class="backPage" type="info" :icon="Back"></el-button>
</template>

<style scoped lang="scss">
.backPage {
  position: fixed;
  top: 5%;
  left: 3%;
  justify-content: center;
  align-items: center;
  width: 2.9rem;
  height: 2.9rem;
  border-radius: 50%;
  transition: all 0.3s;
  z-index: 4;
}
</style>
