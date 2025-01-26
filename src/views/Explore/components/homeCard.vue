<script setup>
defineProps({
  card_columns: {
    default: () => {}
  }
})
const emit = defineEmits(['show-detail'])
const details = (id, event) => {
  const left = event.x
  const top = event.y
  emit('show-detail', id, left, top)
}
</script>

<template>
  <div class="card-cols">
    <div v-for="col in card_columns" :key="col.id">
      <section v-for="card in col" :key="card.id">
        <div class="card">
          <a
            class="image-container"
            :href="`/explore/${card.id}`"
            :style="{
              height: card.img_info.height / (card.img_info.width / 250) + 'px'
            }"
            @click.prevent="details(card.id, $event)"
          >
            <img class="card-image" v-img-lazy="card.img" />
          </a>
          <div class="article-title">
            <span @click="details(card.id)">
              {{ card.title }}
            </span>
          </div>
          <div class="userInfo">
            <RouterLink :to="`/user/index/${card.user.id}`">
              <img class="avatar" v-img-lazy="card.user.avatar" />
              <span class="username">{{ card.user.username }}</span>
            </RouterLink>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped lang="scss">
.card-cols {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

section {
  break-inside: avoid; // 防止卡片被分割在两列中
  margin: 20px;
}

.image-container {
  display: flex;
  overflow: hidden;
  border-radius: $card-border-radius;
  width: $card-image-width;
  border: var(--el-border-color-light) 0.5px solid;
  transition: all 0.3s ease;
  &:hover {
    background-color: rgba(0, 0, 0, 0.1);
    opacity: 0.7;
  }
  .card-image {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.article-title {
  margin: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.userInfo {
  margin-left: 10px;
  .username {
    margin-left: 10px;
    line-height: 20px;
    color: var(--el-text-color-secondary);
  }
  .avatar {
    vertical-align: middle;
    width: 20px;
    height: 20px;
    border-radius: 20px;
  }
  .avatar,
  .image-container {
    position: relative;
    &::after {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      height: 100%;
      width: 100%;
      background-color: transparent;
    }
  }
}
</style>
