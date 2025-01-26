<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    required: true
  },
  columns: {
    type: Number,
    required: true
  },
  rows: {
    type: Number,
    required: true
  }
})
</script>

<template>
  <el-skeleton :loading="loading">
    <template #template>
      <section v-for="i in columns">
        <div v-for="j in rows" class="skeleton-div">
          <el-skeleton-item
            variant="rect"
            class="skeleton-img"
            :style="{
              height:
                i % 2 === 1
                  ? j === 1
                    ? '280px'
                    : j === 2
                      ? '240px'
                      : '200px'
                  : j === 1
                    ? '220px'
                    : j === 2
                      ? '260px'
                      : '190px'
            }"
          />
          <div class="skeleton-text">
            <el-skeleton-item variant="p" style="width: 70%" />
            <el-skeleton-item variant="p" style="width: 40%" />
          </div>
        </div>
      </section>
    </template>
    <slot></slot>
  </el-skeleton>
</template>

<style scoped lang="scss">
.el-skeleton {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  .skeleton-div {
    .skeleton-img {
      border-radius: $card-border-radius;
      width: $card-image-width;
    }
    .skeleton-text div {
      padding: 0.5rem;
    }
  }
}
</style>
