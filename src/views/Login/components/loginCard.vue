<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'
import { User, Lock, ChatLineSquare } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/useUserStore'
import { useRouter } from 'vue-router'

// 定义路由
const emit = defineEmits(['changeShow'])
const router = useRouter()
// 账户加密码校验
// 准备表单对象
const formLogin = ref({
  email: '',
  password: '',
  agree: false
})
const formRegister = ref({
  email: '',
  username: '',
  password: '',
  retryPwd: '',
  agree: false
})

// 准备规则对象
const rulesRegister = {
  email: [
    { required: true, message: '邮箱不能为空', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        var emailRegExp = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/
        var emailRegExp1 = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/
        if (
          (!emailRegExp.test(value) && value !== '') ||
          (!emailRegExp1.test(value) && value !== '')
        ) {
          callback(new Error('请输入有效邮箱格式！'))
        } else {
          callback()
        }
      }
    }
  ],
  username: [{ required: true, message: '用户名不能为空！', trigger: 'blur' }],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 14, message: '密码不符合要求', trigger: 'blur' }
  ],
  retryPwd: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 14, message: '密码不符合要求', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== formRegister.value.password) {
          callback(new Error('两次密码不一致！'))
        } else {
          callback()
        }
      }
    }
  ],
  agree: [
    {
      validator: (rule, value, callback) => {
        // 自定义校验逻辑
        if (value) {
          callback()
        } else {
          callback(new Error('请勾选协议'))
        }
      }
    }
  ]
}
const rulesLogin = {
  email: [
    { required: true, message: '邮箱不能为空', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        var emailRegExp = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/
        var emailRegExp1 = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/
        if (
          (!emailRegExp.test(value) && value !== '') ||
          (!emailRegExp1.test(value) && value !== '')
        ) {
          callback(new Error('请输入有效邮箱格式！'))
        } else {
          callback()
        }
      }
    }
  ],
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 14, message: '密码不符合要求', trigger: 'blur' }
  ],
  agree: [
    {
      validator: (rule, value, callback) => {
        // 自定义校验逻辑
        if (value) {
          callback()
        } else {
          callback(new Error('请勾选协议'))
        }
      }
    }
  ]
}

// 获取form实例校验
const formLoginRef = ref(null)
const formRegisterRef = ref(null)

// 准备用户
const userStore = useUserStore()
const doLogin = () => {
  const { email, password } = formLogin.value
  formLoginRef.value.validate(async (valid) => {
    if (valid) {
      // 提示用户
      await userStore.getUserInfo({ email, password })
      emit('changeShow')
      await router.replace(`/user/index/${userStore.userInfo.id}`)
      ElMessage({ type: 'success', message: '登陆成功' })
    }
  })
}
const doRegister = () => {
  const { email, username, password } = formRegister.value
  formRegisterRef.value.validate(async (valid) => {
    if (valid) {
      await userStore.userRegister({ email, username, password })
      ElMessage({ type: 'success', message: '注册成功' })
      toggleForm()
    }
  })
}
const showWhich = ref(true)
const toggleForm = () => {
  showWhich.value = !showWhich.value
}
</script>

<template>
  <div class="box">
    <div class="left-area">
      <div class="web-title">Bird Lovers</div>
      <div class="web-subtitle">传递爱和希望</div>
      <img src="/icon.png" class="image" alt="" />
    </div>
    <div class="right-area" v-if="showWhich">
      <div class="title">登录</div>
      <el-form
        ref="formLoginRef"
        :model="formLogin"
        :rules="rulesLogin"
        label-position="right"
        label-width="0"
        status-icon
      >
        <el-form-item prop="email" class="inputArea">
          <el-input
            class="my"
            v-model="formLogin.email"
            placeholder="请输入邮箱号"
            :prefix-icon="User"
          />
        </el-form-item>
        <el-form-item prop="password" class="inputArea">
          <el-input
            class="my"
            v-model="formLogin.password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        <el-form-item prop="agree" class="inputArea">
          <el-checkbox size="large" v-model="formLogin.agree">
            我已同意隐私条款和服务条款
          </el-checkbox>
        </el-form-item>
        <el-button type="primary" class="sub-btn" @click="doLogin">点击登录</el-button>
      </el-form>
      <el-divider content-position="center">或</el-divider>
      <el-button type="primary" class="sub-btn" @click="toggleForm()">新用户注册</el-button>
    </div>
    <div class="right-area" v-if="!showWhich">
      <div class="title" style="text-align: center">注册</div>
      <el-form
        ref="formRegisterRef"
        :model="formRegister"
        :rules="rulesRegister"
        label-position="right"
        label-width="0"
        status-icon
      >
        <el-form-item prop="email" class="inputArea">
          <el-input
            class="my"
            v-model="formRegister.email"
            placeholder="请输入注册邮箱"
            :prefix-icon="ChatLineSquare"
          />
        </el-form-item>
        <el-form-item prop="username" class="inputArea">
          <el-input
            class="my"
            v-model="formRegister.username"
            placeholder="请输入用户名"
            :prefix-icon="User"
            maxlength="6"
            show-word-limit
          />
        </el-form-item>
        <el-form-item prop="password" class="inputArea">
          <el-input
            class="my"
            v-model="formRegister.password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        <el-form-item prop="retryPwd" class="inputArea">
          <el-input
            class="my"
            v-model="formRegister.retryPwd"
            placeholder="请确认输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        <el-form-item prop="agree" class="inputArea">
          <el-checkbox size="large" v-model="formRegister.agree">
            我已同意隐私条款和服务条款
          </el-checkbox>
        </el-form-item>
        <el-button type="primary" class="sub-btn" @click="doRegister">点击注册</el-button>
      </el-form>
      <el-divider content-position="center">或</el-divider>
      <el-button class="sub-btn" type="primary" @click="toggleForm()">立即登录</el-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.box {
  position: relative;
  background-color: var(--el-bg-color);
  box-shadow: 32px 18px 21px -3px rgba(0, 0, 0, 0.1);
  width: 700px;
  height: 500px;
  border-radius: 2rem;
  display: flex;
  flex-direction: row;
  overflow: hidden;
  .left-area {
    width: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .image {
      width: 50%;
    }
    .web-title {
      font-size: 2rem;
      font-weight: bold;
      margin-bottom: 20px;
    }
    .web-subtitle {
      font-size: 1.5rem;
      color: var(--el-text-color-secondary);
      margin-bottom: 20px;
    }
  }
  .right-area {
    border-left: var(--el-border-color-light) 1px dashed;
    padding-top: 48px;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    .title {
      margin-bottom: 1rem;
      font-size: 1.3rem;
      font-weight: bold;
    }
    .el-form {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 80%;
    }
    .sub-btn {
      width: 10rem;
      height: 3rem;
      border-radius: 999px;
      font-weight: bold;
    }
    .inputArea {
      width: 80%;
    }
  }
  @media screen and (max-width: 768px) {
    width: 80vw;
    .left-area {
      display: none;
    }
  }
}
</style>
