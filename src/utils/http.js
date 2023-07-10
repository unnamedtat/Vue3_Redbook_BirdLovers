// axios基础配置
import axios from "axios";
import {useUserStore} from "@/stores/user";
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus";

const router = useRouter()

const http = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 5000,
})

// axios请求拦截器
http.interceptors.request.use(config => {
    const userStore = useUserStore();
    if (userStore.userInfo.token) {
        config.headers.Authorization = `Bearer ${userStore.userInfo.token}`
    }
    return config
}, e => Promise.reject(e))


// axios响应式拦截器
http.interceptors.response.use(res => res.data, e => {
    if (e.response.status === 401) {
        ElMessage({
        type: 'warning',
        message: e.response.data.error
    })
        const userStore = useUserStore();
        userStore.userLogout()
        router.replace('/')
    }
    return Promise.reject(e)
})


export default http