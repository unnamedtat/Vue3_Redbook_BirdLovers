<script setup>
const props = defineProps({
  detail: {
    type: Object,
    required: true
  },
  afterDoComment: {
    type: Function,
    required: true
  }
})
</script>

<template>
  <BLCardDetail :detail="detail" @afterDoComment="afterDoComment" ref="overlay" />
</template>

<style scoped lang="scss"></style>
