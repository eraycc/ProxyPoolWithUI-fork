import axios from 'axios'
import type { AxiosInstance } from 'axios'

// @ts-ignore - Nuxt 3 auto-import
export default defineNuxtPlugin((nuxtApp) => {
  // @ts-ignore - Nuxt 3 auto-import
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string

  const axiosInstance: AxiosInstance = axios.create({
    baseURL,
    timeout: 30000, // 增加到 30 秒，避免某些操作超時
    withCredentials: true
  })

  // 请求拦截器
  axiosInstance.interceptors.response.use(
    (response) => {
      return response
    },
    async (error) => {
      console.error('网络错误:', error.message)
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
          console.error('API 错误:', data.message)
          throw new Error(data.message || 'API 返回错误')
        }
        
        return data
      } catch (error: any) {
        console.error('请求失败:', error.message)
        throw error
      }
    }

    async post(url: string, data?: any, params?: any) {
      try {
        const response = await axiosInstance.post(url, data, { params })
        const resData = response.data
        
        if (!resData.success) {
          console.error('API 错误:', resData.message)
          throw new Error(resData.message || 'API 返回错误')
        }
        
        return resData
      } catch (error: any) {
        console.error('请求失败:', error.message)
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

