<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore.js'
import { computed, onBeforeMount, ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import {uploadPost, uploadPostInfo} from '@/apis/main'
import { getCurrentTime } from '@/utils/getTime'
import throttle from "@/utils/throttle";

const router = useRouter()
const userStore = useUserStore()
const checkLogin = () => {
  if (!userStore.userInfo.id) {
    router.replace('/login')
  }
}

onBeforeMount(() => checkLogin())

const fileList = ref([])
const fileListUrl = computed(() => fileList.value.map((item) => item.url))
const title = ref('')
const content = ref('')
const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const Post = ref({})
const PostId = ref(0)
const currentTime = getCurrentTime()

const handlePictureCardPreview = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url
  dialogVisible.value = true
  return true
}

const handleChange = (uploadFile, uploadFiles) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'] // 可接受的图片类型
  const maxSize = 2 // 最大文件大小，单位：MB
  if (!allowedTypes.includes(uploadFile.raw.type)) {
    ElMessage.error('请上传正确的图片文件!')
    upload.value.handleRemove(uploadFile)
    return false
  } else if (uploadFile.raw.size / 1024 / 1024 > maxSize) {
    ElMessage.error(`文件大小最多${maxSize}MB!`)
    upload.value.handleRemove(uploadFile)
    return false
  }

  return true
}
const upload = ref(null)
const doUploads = async () => {
  if (fileListUrl.value.length === 0) {
    ElMessage.warning('请至少上传一张图片!')
    return
  }
  if (title.value === '') {
    ElMessage.warning('请输入标题')
    return
  }
  const data = {
    title: title.value,
    content: content.value,
    user_id: userStore.userInfo.id
  }
  const res = await uploadPostInfo(data)
  PostId.value = res.info
  await upload.value.submit()
  ElMessage({ type: 'success', message: '发布成功，5秒后跳转到主页' })
  setTimeout(() => {
    router.replace('/')
  }, 5000)
}
const handleExceed = () => {
  ElMessage.warning('最多可以添加9张图片哦!')
}

const handleUploadPost =throttle( (option) => {
  const formData = new FormData()
  fileList.value.forEach((file, index) => {
    formData.append('files[]', file.raw);
  });
  formData.append('id',PostId.value)
  uploadPost({formData}).then((res)=>console.log(res))
},5000)
</script>

<template>
  <div class="content-container">
    <div class="content">
      <el-row>
        <div class="img-editor">
          <h2>上传图片</h2>
          <div class="img-container">
            <el-upload
              v-model:file-list="fileList"
              action=""
              :http-request="handleUploadPost"
              class="preview-upload"
              ref="upload"
              list-type="picture-card"
              multiple
              :limit="9"
              :on-preview="handlePictureCardPreview"
              :on-change="handleChange"
              :auto-upload="false"
              :on-exceed="handleExceed"
            >
              <el-icon>
                <Plus />
              </el-icon>
            </el-upload>
          </div>
        </div>
      </el-row>
      <el-row>
        <div class="content-edit">
          <h2>内容区</h2>
          <div>
            <el-input
              v-model="title"
              maxlength="20"
              placeholder="请输入标题"
              show-word-limit
              type="text"
            />
            <el-input
              v-model="content"
              maxlength="3000"
              placeholder="请输入内容"
              show-word-limit
              type="textarea"
              :rows="15"
            />
          </div>
        </div>
      </el-row>
      <el-row>
        <el-button type="primary" size="large" @click="doUploads">发布推文</el-button>
      </el-row>
    </div>
    <div class="preview-content">
      <div class="preview-user-info">
        <el-avatar :src="userStore.userInfo.avatar" size="small" />
        <span>{{ userStore.userInfo.username }}</span>
      </div>
      <el-carousel style="background-color: black">
        <el-carousel-item v-for="item in fileListUrl" :key="item" height="120px">
          <img :src="item" style="height: 100%; width: 100%; object-fit: contain" alt="" />
        </el-carousel-item>
      </el-carousel>
      <div class="preview-text-title">{{ title ? title : '标题' }}</div>
      <div class="preview-text-content">{{ content ? content : '内容' }}</div>
      <time class="time">{{ currentTime }}</time>
      <hr />
      <el-empty description="现在还没有评论"></el-empty>
    </div>
  </div>
  <el-dialog v-model="dialogVisible">
    <img :src="dialogImageUrl" alt="Preview Image" />
  </el-dialog>
</template>

<style scoped lang="scss">
.img-editor {
  :deep(.el-upload--picture-card),
  :deep(.el-upload-list--picture-card .el-upload-list__item) {
    width: 6rem;
    height: 6rem;
  }
  .preview-upload {
    margin: 1.6rem;
  }
}
.content-edit {
  width: 100%;
  .el-input {
    width: 30%;
    margin: 1rem 0 1rem 1.5rem;
  }
  .el-textarea {
    width: 90%;
    margin: 0 0 1rem 1.5rem;
  }
}
.el-row {
  h2 {
    font-size: 1.2rem;
    margin-left: 1.5rem;
  }
  .el-button {
    margin-left: 1.5rem;
  }
}
.content-container {
  display: flex;
  .preview-content {
    margin: 1rem;
    width: 18rem;
    height: 100%;
    .preview-user-info {
      display: flex;
      align-items: center;
    }
    .preview-text-title {
      font-weight: bold;
    }
    .preview-text-content {
      overflow-x: scroll;
      font-size: 0.8rem;
      white-space: nowrap;
      //white-space: pre-wrap;
      //overflow-wrap: break-word;
    }
    .time {
      font-size: 0.8rem;
      color: var(--el-text-color-secondary);
    }
  }
  .content {
    border-right: var(--el-text-color-secondary) 2px dashed;
    flex: 1;
  }
}
.el-dialog {
  img {
    width: 100%;
    height: 100%;
  }
}
@media screen and (max-width: 768px) {
  .preview-content {
    display: none;
  }
  .content-container .content {
    border-right: none;
  }
}
</style>
