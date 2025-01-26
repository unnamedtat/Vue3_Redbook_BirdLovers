<script setup lang="ts">
import LoginCard from '@/views/Login/components/loginCard.vue'
</script>
<template>
  <div class="login">
    <login-card></login-card>
  </div>
</template>

<style scoped lang="scss">
.login {
  background-color: var(--el-bg-color);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
}
</style>
