<template>
  <el-tooltip :content="tooltipContent" placement="right">
    <component
      :is="to ? RouterLink : 'div'"
      :to="to"
      class="menu-option"
      :style="!to ? { cursor: 'pointer' } : null"
      @click="!to && $emit('click')"
    >
      <el-icon size="x-large">
        <component :is="icon" />
      </el-icon>
      <p class="menuText" :class="{ open: isMenuOpen }">{{ text }}</p>
    </component>
  </el-tooltip>
</template>

<script setup>
import { defineProps } from 'vue'
import { RouterLink } from 'vue-router'

defineProps({
  to: {
    type: String,
    default: ''
  },
  icon: {
    type: Object,
    required: true
  },
  text: {
    type: String,
    required: true
  },
  tooltipContent: {
    type: String,
    required: true
  },
  isMenuOpen: {
    type: Boolean,
    default: false
  }
})
defineEmits(['click'])
</script>

<style scoped lang="scss">
.menu-option {
  color: var(--el-text-color-primary);
  position: relative;
  border: none;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  border-radius: 0.2rem;
  transition: 0.3s ease;
  &:hover {
    background-color: var(--el-color-primary-light-9);
    .el-icon {
      color: var(--el-color-primary);
    }
  }
  .el-icon {
    text-align: center;
    width: $aside-icon-size;
    font-size: $aside-icon-font-size;
  }
  p {
    width: calc(100% - $aside-icon-size);
  }
}

.menuText {
  transform: translateX(-250px);
  opacity: 0;
  transition: transform 0.3s ease 0.1s;
}
.open {
  opacity: 1;
  transform: translateX(0);
  text-align: center;
}
</style>
