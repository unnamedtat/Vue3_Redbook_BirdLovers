<script setup>
import { ref } from 'vue'
import { ElMessage, genFileId } from 'element-plus'
import { useUserStore } from '@/stores/useUserStore'
import {updateUserAvatar, updateUserInfo} from '@/apis/main'

const userStore = useUserStore()
const dialogFormVisible = ref(false)
// 文件上传对象
const upload = ref(null)
// 上传头像成功后修改pinia数据
const fileList = ref([])
const handleExceed = (files) => {
  upload.value.clearFiles()
  const file = files[0]
  file.uid = genFileId()
  upload.value.handleStart(file)
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
// 控制表单信息
const form = ref({
  username: '',
  signature: ''
})
const openDialog = () => {
  form.value.username = userStore.userInfo.username
  form.value.signature = userStore.userInfo.signature
  dialogFormVisible.value = true
}
// 表单验证规则
const rules = {
  username: [{ required: true, message: '用户名不能为空！', trigger: 'blur' }],
  signature: [{ required: true, message: '个性签名不能为空!', trigger: 'blur' }]
}
// 表单对象
const formRef = ref(null)
const doUpdate = async () => {
  const { username, signature } = form.value
  const isModified =
    username !== userStore.userInfo.username || signature !== userStore.userInfo.signature
  const isAvatarUploaded = fileList.value.length === 1

  if (!isModified && !isAvatarUploaded) {
    ElMessage({ type: 'warning', message: '未作任何修改！' })
    return
  }
  else{
    const promises = [];
    if (isModified) {
      promises.push(updateUserInfo({ username, signature })
          .then((response) => {
              userStore.changeInfo({ username, signature })
              ElMessage({ type: 'success', message: '用户信息更新成功' })
      }));
    }
    if (isAvatarUploaded) {
      promises.push(upload.value.submit());
    }
    await Promise.all(promises);
    dialogFormVisible.value = false
    return
  }
}
const handleFileUpload = (option) => {
  const formData = new FormData()
  formData.append('file', fileList.value[0].raw)
  updateUserAvatar({formData})
    .then((response)=>{
      userStore.changeAvatar({ avatar: response.info })
      ElMessage({ type: 'success', message: '头像上传成功' })
      upload.value.clearFiles()
    })
    .catch(async (error) => {
      ElMessage({
        type: 'warning',
        message: '头像上传失败'
      })
    })
}
defineExpose({ openDialog })
</script>

<template>
  <el-dialog v-model="dialogFormVisible" title="更新个人信息" center draggable>
    <div class="fileUpload">
      <el-upload
        v-model:file-list="fileList"
        ref="upload"
        action=""
        :http-request="handleFileUpload"
        :limit="1"
        :on-exceed="handleExceed"
        :auto-upload="false"
        :on-change="handleChange"
        :headers="userStore.headersObj"
      >
        <template #trigger>
          <el-button class="btn" type="primary" round>选择一个文件</el-button>
        </template>
        <template #tip>
          <div class="el-upload__tip" style="color: red; text-align: left">
            仅限一个文件，新文件将会被覆盖
          </div>
        </template>
      </el-upload>
    </div>
    <div class="fileUpload">
      <el-form :model="form" ref="formRef" :rules="rules" label-position="top">
        <el-form-item prop="username" label="昵称" label-width="100px" style="margin: 30px">
          <el-input v-model="form.username" maxlength="6" show-word-limit class="my" />
        </el-form-item>
        <el-form-item prop="signature" label="个性签名" label-width="100px" style="margin: 30px">
          <el-input v-model="form.signature" class="my" />
        </el-form-item>
      </el-form>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false" round>取消</el-button>
        <el-button type="primary" @click="doUpdate" round>确认</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped lang="scss">
.fileUpload {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  button {
    margin-left: 20px;
    margin-bottom: 20px;
  }
}

.el-form {
  width: 80%;
}

.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>
