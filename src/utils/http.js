// axios基础配置
import axios from 'axios'
import { useUserStore } from '@/stores/useUserStore'
import router from '@/router'
import { ElMessage } from 'element-plus'


const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000
})

// axios请求拦截器
http.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.userInfo.token) {
      config.headers.Authorization = `Bearer ${userStore.userInfo.token}`
    }
    return config
  },
  (e) => Promise.reject(e)
)

// axios响应式拦截器
http.interceptors.response.use(
  (res) => res.data,
  (e) => {
    if (e.response.status === 401) {
      const userStore = useUserStore()
      userStore.userLogout()
      router.replace('/')
    }
    if (e.response.status === 404) {
      router.replace('/NotFound')
    }
    if (e.response.status === 403) {
      router.replace('/login')
    }
    ElMessage({
      type: 'warning',
      message: e.message
    })
    return Promise.reject(e)
  }
)

export default http
