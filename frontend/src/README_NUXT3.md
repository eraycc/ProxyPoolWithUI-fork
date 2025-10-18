# Nuxt 3 前端使用指南

## 🎉 已升级到 Nuxt 3

本项目前端已成功从 Nuxt 2 升级到 Nuxt 3，使用最新的技术栈。

## 📋 技术栈

- **Nuxt 3.19.3** - 现代化的 Vue 框架
- **Vue 3.5.22** - 最新的 Vue.js
- **TypeScript** - 类型安全
- **Ant Design Vue 4.0** - UI 组件库
- **Vite 7.1** - 极速构建工具
- **Composition API** - Vue 3 推荐的 API 风格

## 🚀 快速开始

### 生产模式（推荐）

直接运行已构建好的静态文件：

```bash
# 在项目根目录
python main.py
```

访问：http://localhost:5000/web

### 开发模式

用于开发和调试：

**终端 1 - 后端：**
```bash
python main.py
```

**终端 2 - 前端热重载：**
```bash
cd frontend\src
npm run dev
```

访问：http://localhost:3000

## 📦 常用命令

```bash
# 安装依赖
npm install

# 开发模式（热重载）
npm run dev

# 构建生产版本
npm run generate

# 预览构建结果
npm run preview

# 类型检查
npx nuxi typecheck
```

## 📁 项目结构

```
frontend/src/
├── app.vue              # 应用入口
├── nuxt.config.ts       # Nuxt 配置
├── package.json         # 依赖管理
├── pages/               # 页面
│   ├── index.vue        # 首页（代理列表）
│   └── fetchers.vue     # 爬取器状态
├── layouts/             # 布局
│   └── default.vue      # 默认布局（侧边栏）
├── plugins/             # 插件
│   ├── axios.ts         # HTTP 客户端
│   └── antd.ts          # Ant Design Vue
└── types/               # TypeScript 类型
    ├── nuxt.d.ts        # Nuxt 自动导入类型
    └── app.d.ts         # 应用类型定义
```

## 🔧 开发指南

### 添加新页面

在 `pages/` 目录创建 `.vue` 文件：

```vue
<template>
  <div>
    <h1>新页面</h1>
  </div>
</template>

<script setup lang="ts">
// 使用 Composition API
const message = ref('Hello Nuxt 3')
</script>
```

Nuxt 会自动创建路由：
- `pages/example.vue` → `/web/example`

### 使用 HTTP 客户端

```vue
<script setup lang="ts">
const { $http } = useNuxtApp()

// GET 请求
const fetchData = async () => {
  const data = await $http.get('/api/endpoint')
  console.log(data)
}

// POST 请求
const postData = async () => {
  const result = await $http.post('/api/endpoint', { key: 'value' })
}
</script>
```

### 添加新组件

在 `components/` 目录创建组件：

```vue
<!-- components/MyComponent.vue -->
<template>
  <div>{{ message }}</div>
</template>

<script setup lang="ts">
defineProps<{
  message: string
}>()
</script>
```

使用时无需导入（自动导入）：

```vue
<template>
  <MyComponent message="Hello" />
</template>
```

### TypeScript 类型

定义接口：

```typescript
// types/models.ts
export interface Proxy {
  protocol: string
  ip: string
  port: number
  latency: number
  alive_time: number
  created_date: string
  validated: boolean
}
```

使用：

```vue
<script setup lang="ts">
import type { Proxy } from '~/types/models'

const proxies = ref<Proxy[]>([])
</script>
```

## 🎨 样式

### 全局样式

在 `nuxt.config.ts` 中配置：

```typescript
export default defineNuxtConfig({
  css: [
    'ant-design-vue/dist/reset.css',
    '~/assets/css/global.css'
  ]
})
```

### 组件样式

```vue
<style scoped>
/* scoped 样式只影响当前组件 */
.my-class {
  color: blue;
}
</style>

<style>
/* 全局样式 */
</style>
```

## 🔄 重新构建

修改代码后需要重新构建：

```bash
cd frontend\src
npm run generate
```

构建输出位置：`frontend/deployment/public/`

## ⚙️ 配置

### API 基础 URL

在 `nuxt.config.ts` 中配置：

```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: process.env.NODE_ENV === 'production' 
        ? '/' 
        : 'http://localhost:5000'
    }
  }
})
```

### 环境变量

创建 `.env` 文件：

```bash
# .env
NUXT_PUBLIC_API_BASE=http://localhost:5000
```

## 🐛 常见问题

### TypeScript 错误

**问题**：`Cannot find name 'useNuxtApp'`

**解决**：
1. 确保 `types/nuxt.d.ts` 存在
2. 重启 TypeScript 服务器（VS Code: Ctrl+Shift+P → "TypeScript: Restart TS Server"）
3. 运行 `npm run postinstall` 生成类型

### 构建错误

**问题**：构建失败

**解决**：
1. 删除 `node_modules` 和 `package-lock.json`
2. 重新安装：`npm install`
3. 清除缓存：`rm -rf .nuxt`

### 页面空白

**问题**：访问页面显示空白

**解决**：
1. 清除浏览器缓存（Ctrl+F5）
2. 检查浏览器控制台错误
3. 确认后端正在运行
4. 检查 API 路径配置

## 📚 学习资源

- [Nuxt 3 文档](https://nuxt.com/)
- [Vue 3 文档](https://vuejs.org/)
- [Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [TypeScript 文档](https://www.typescriptlang.org/)
- [Ant Design Vue](https://antdv.com/)

## 🔐 最佳实践

1. **使用 TypeScript**：为所有新代码添加类型
2. **使用 Composition API**：比 Options API 更灵活
3. **使用自动导入**：Nuxt 3 会自动导入组件和 composables
4. **保持组件小而专注**：每个组件只做一件事
5. **使用 ESLint**：保持代码风格一致

## 🆕 新功能

### 存活时间列

首页代理列表新增"存活时间"列，显示代理在数据库中的时长：

```vue
<template>
  <a-table :columns="columns" :data-source="proxies">
    <!-- 存活时间会自动格式化 -->
  </a-table>
</template>

<script setup lang="ts">
const formatAliveTime = (seconds: number) => {
  // 智能格式化：X天X时 / X时X分 / X分X秒
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  
  if (days > 0) return `${days}天${hours}时`
  if (hours > 0) return `${hours}时${minutes}分`
  return `${minutes}分${seconds % 60}秒`
}
</script>
```

## 🎯 性能优化

1. **代码分割**：使用动态导入
   ```typescript
   const MyComponent = defineAsyncComponent(() => 
     import('~/components/MyComponent.vue')
   )
   ```

2. **图片优化**：使用 Nuxt Image
   ```vue
   <NuxtImg src="/image.jpg" width="200" height="200" />
   ```

3. **懒加载**：延迟加载非关键组件
   ```vue
   <LazyMyComponent v-if="show" />
   ```

## 📞 支持

遇到问题？

1. 查看 [Nuxt 3 文档](https://nuxt.com/)
2. 检查 `frontend/src_backup/` 中的原始代码
3. 查看浏览器开发者工具控制台
4. 检查终端错误信息

---

**版本**: 2.0.0  
**更新时间**: 2025-10-18  
**状态**: ✅ 生产就绪

