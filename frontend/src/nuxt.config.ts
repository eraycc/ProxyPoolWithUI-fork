// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  
  app: {
    baseURL: '/web/',
    head: {
      title: '私人IP池管理界面',
      htmlAttrs: {
        lang: 'zh-CN'
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'IP池管理系统' }
      ]
    }
  },

  css: [
    'ant-design-vue/dist/reset.css',
    '~/assets/css/global.css'
  ],

  modules: [],

  runtimeConfig: {
    public: {
      apiBase: process.env.NODE_ENV === 'production' ? '/' : 'http://localhost:5000'
    }
  },

  ssr: false,
  
  nitro: {
    output: {
      dir: '../deployment'
    }
  },

  vite: {
    ssr: {
      noExternal: ['moment', 'ant-design-vue']
    }
  }
})

