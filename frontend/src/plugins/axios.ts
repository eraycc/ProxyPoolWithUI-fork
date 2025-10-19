import axios from 'axios'
import type { AxiosInstance } from 'axios'
import { message } from 'ant-design-vue'

// @ts-ignore - Nuxt 3 auto-import
export default defineNuxtPlugin((nuxtApp) => {
  // @ts-ignore - Nuxt 3 auto-import
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string
  // @ts-ignore - Nuxt 3 auto-import
  const router = useRouter()

  const axiosInstance: AxiosInstance = axios.create({
    baseURL,
    timeout: 30000, // 增加到 30 秒，避免某些操作超時
    withCredentials: true
  })

  // 请求拦截器 - 添加 token
  axiosInstance.interceptors.request.use(
    (config) => {
      // 从 localStorage 获取 token
      const token = localStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  // 响应拦截器 - 处理错误和未授权
  axiosInstance.interceptors.response.use(
    (response) => {
      return response
    },
    async (error) => {
      if (error.response) {
        const status = error.response.status
        const data = error.response.data
        
        // 401 未授权 - token无效或已过期
        if (status === 401) {
          // 清除本地存储
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          
          // 如果不是在登录页面，显示提示并跳转
          if (router.currentRoute.value.path !== '/login') {
            message.error('登录已过期，请重新登录')
            // 跳转到登录页
            setTimeout(() => {
              router.push('/login')
            }, 1000)
          }
        } 
        // 403 禁止访问
        else if (status === 403) {
          message.error('没有权限访问')
        }
        // 其他错误
        else {
          console.error('API错误:', data.message || error.message)
        }
      } else if (error.code === 'ECONNABORTED') {
        // 超时错误，不打印到控制台，让调用者处理
        console.warn('请求超时:', error.config?.url)
      } else if (error.code === 'ERR_NETWORK') {
        // 网络错误
        console.error('网络连接失败，请检查后端服务是否启动')
      } else {
        console.error('请求错误:', error.message)
      }
      
      return Promise.reject(error)
    }
  )

  class Http {
    baseURL: string

    constructor() {
      this.baseURL = baseURL
    }

    async get(url: string, params?: any) {
      try {
        const response = await axiosInstance.get(url, { params })
        const data = response.data
        
        if (!data.success) {
          throw new Error(data.message || 'API 返回错误')
        }
        
        return data
      } catch (error: any) {
        // 不在这里重复打印，由拦截器处理
        throw error
      }
    }

    async post(url: string, data?: any, params?: any) {
      try {
        const response = await axiosInstance.post(url, data, { params })
        const resData = response.data
        
        if (!resData.success) {
          throw new Error(resData.message || 'API 返回错误')
        }
        
        return resData
      } catch (error: any) {
        // 不在这里重复打印，由拦截器处理
        throw error
      }
    }
  }

  const $http = new Http()

  return {
    provide: {
      http: $http
    }
  }
})

