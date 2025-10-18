<template>
  <div class="app-layout">
    <a-config-provider :locale="locale">
      <a-layout class="layout-main">
        <!-- 侧边栏 -->
        <a-layout-sider
          v-model:collapsed="collapsed"
          :trigger="null"
          collapsible
          :width="240"
          class="layout-sider"
        >
          <!-- Logo区域 -->
          <div class="logo-container">
            <div class="logo" :class="{ collapsed }">
              <CloudServerOutlined class="logo-icon" />
              <transition name="fade">
                <span v-if="!collapsed" class="logo-text">IP池管理</span>
              </transition>
            </div>
            
            <!-- 版本和状态信息 -->
            <transition name="fade">
              <div v-if="!collapsed" class="logo-info">
                <div class="info-item">
                  <span class="status-indicator online"></span>
                  <span>系统运行中</span>
                </div>
                <div class="info-item version-info">
                  v2.0.0 | Nuxt 3
                </div>
              </div>
            </transition>
          </div>

          <!-- 导航菜单 -->
          <a-menu
            v-model:selectedKeys="urlPath"
            theme="dark"
            mode="inline"
            class="nav-menu"
          >
            <a-menu-item key="/" class="menu-item">
              <NuxtLink to="/" class="menu-link">
                <UnorderedListOutlined class="menu-icon" />
                <span class="menu-text">可用代理</span>
                <span v-if="proxyCount" class="menu-badge">{{ proxyCount }}</span>
              </NuxtLink>
            </a-menu-item>

            <a-menu-item key="/fetchers" class="menu-item">
              <NuxtLink to="/fetchers" class="menu-link">
                <RobotOutlined class="menu-icon" />
                <span class="menu-text">爬取器状态</span>
              </NuxtLink>
            </a-menu-item>

            <a-menu-item key="/api" class="menu-item">
              <NuxtLink to="/api" class="menu-link">
                <ApiOutlined class="menu-icon" />
                <span class="menu-text">API 接口</span>
                <a-badge 
                  :count="16" 
                  :number-style="{ backgroundColor: '#52c41a', fontSize: '10px' }"
                  class="menu-count-badge"
                />
              </NuxtLink>
            </a-menu-item>

            <a-menu-divider />

            <a-menu-item key="github" class="menu-item">
              <a
                href="https://github.com/huppugo1/ProxyPoolWithUI"
                target="_blank"
                class="menu-link"
              >
                <GithubOutlined class="menu-icon" />
                <span class="menu-text">GitHub</span>
                <ExportOutlined class="menu-external" />
              </a>
            </a-menu-item>
          </a-menu>

        </a-layout-sider>

        <!-- 主内容区 -->
        <a-layout>
          <!-- 顶部栏 -->
          <a-layout-header class="layout-header">
            <div class="header-left">
              <MenuUnfoldOutlined
                v-if="collapsed"
                class="trigger"
                @click="collapsed = !collapsed"
              />
              <MenuFoldOutlined
                v-else
                class="trigger"
                @click="collapsed = !collapsed"
              />
              
              <div class="header-breadcrumb">
                <a-breadcrumb>
                  <a-breadcrumb-item>
                    <HomeOutlined />
                  </a-breadcrumb-item>
                  <a-breadcrumb-item>{{ pageTitle }}</a-breadcrumb-item>
                </a-breadcrumb>
              </div>
            </div>

            <div class="header-right">
              <a-space :size="16">
                <a-tooltip title="刷新页面">
                  <a-button type="text" @click="refreshPage">
                    <ReloadOutlined />
                  </a-button>
                </a-tooltip>
                
                <a-tooltip title="全屏">
                  <a-button type="text" @click="toggleFullscreen">
                    <FullscreenOutlined v-if="!isFullscreen" />
                    <FullscreenExitOutlined v-else />
                  </a-button>
                </a-tooltip>
              </a-space>
            </div>
          </a-layout-header>

          <!-- 内容区 -->
          <a-layout-content class="layout-content">
            <div class="content-wrapper">
              <slot />
            </div>
          </a-layout-content>

          <!-- 页脚 -->
          <a-layout-footer class="layout-footer">
            <div class="footer-content">
              <div class="footer-left">
                <span>© 2025 IP池管理系统</span>
                <a-divider type="vertical" />
                <span>基于 Nuxt 3 + Vue 3</span>
              </div>
              <div class="footer-right">
                <a href="https://github.com/huppugo1/ProxyPoolWithUI" target="_blank">
                  <GithubOutlined />
                  开源项目
                </a>
              </div>
            </div>
          </a-layout-footer>
        </a-layout>
      </a-layout>
    </a-config-provider>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import {
  CloudServerOutlined,
  UnorderedListOutlined,
  RobotOutlined,
  ApiOutlined,
  GithubOutlined,
  ExportOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  HomeOutlined,
  ReloadOutlined,
  FullscreenOutlined,
  FullscreenExitOutlined
} from '@ant-design/icons-vue'
import moment from 'moment'

moment.locale('zh-cn')

const locale = zhCN
const route = useRoute()
const router = useRouter()
const collapsed = ref(false)
const urlPath = ref<string[]>([])
const isFullscreen = ref(false)
const proxyCount = ref(0)

// 页面标题
const pageTitle = computed(() => {
  const titleMap: Record<string, string> = {
    '/': '可用代理列表',
    '/fetchers': '爬取器状态监控',
    '/api': 'API 接口文档'
  }
  return titleMap[route.path] || '代理池管理'
})

// 更新导航
const updateNav = () => {
  const data = /^\/[^/]*/.exec(route.path || '')
  if (data) {
    urlPath.value = [data[0]]
  } else {
    urlPath.value = []
  }
}

// 刷新页面
const refreshPage = () => {
  router.go(0)
}

// 切换全屏
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } else {
    document.exitFullscreen()
    isFullscreen.value = false
  }
}

// 监听全屏变化
if (process.client) {
  document.addEventListener('fullscreenchange', () => {
    isFullscreen.value = !!document.fullscreenElement
  })
}

watch(() => route.path, updateNav)

onMounted(() => {
  updateNav()
})
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.layout-main {
  min-height: 100vh;
}

/* 侧边栏样式 */
.layout-sider {
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
  position: relative;
  z-index: 10;
}

.layout-sider :deep(.ant-layout-sider-children) {
  display: flex;
  flex-direction: column;
}

/* Logo区域 */
.logo-container {
  padding: 16px;
  margin-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.3s;
}

.logo.collapsed {
  justify-content: center;
}

.logo-icon {
  font-size: 24px;
  color: #1890ff;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  white-space: nowrap;
}

/* Logo下方信息 */
.logo-info {
  margin-top: 12px;
  padding: 8px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 6px;
}

.logo-info .info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.75);
}

.logo-info .version-info {
  color: rgba(255, 255, 255, 0.55);
  font-family: 'Courier New', monospace;
  font-weight: 500;
  padding-left: 18px;
}

/* 导航菜单 */
.nav-menu {
  flex: 1;
  border-right: none;
}

.nav-menu :deep(.ant-menu-item) {
  margin: 4px 8px;
  border-radius: 6px;
  height: 44px;
  line-height: 44px;
}

.menu-link {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  position: relative;
}

.menu-icon {
  font-size: 18px;
}

.menu-text {
  flex: 1;
}

.menu-badge {
  background: #1890ff;
  color: #fff;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 500;
}

.menu-count-badge {
  margin-left: auto;
}

.menu-count-badge :deep(.ant-badge-count) {
  box-shadow: none;
}

.menu-external {
  font-size: 12px;
  opacity: 0.6;
}

/* 顶部栏 */
.layout-header {
  background: #fff;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 9;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.trigger {
  font-size: 18px;
  cursor: pointer;
  transition: color 0.3s;
  padding: 8px;
}

.trigger:hover {
  color: #1890ff;
}

.header-breadcrumb :deep(.ant-breadcrumb) {
  font-size: 14px;
}

.header-right :deep(.ant-btn) {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 内容区 */
.layout-content {
  margin: 24px;
  min-height: calc(100vh - 184px);
}

.content-wrapper {
  min-height: 100%;
}

/* 页脚 */
.layout-footer {
  background: #fff;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.footer-left,
.footer-right {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.65);
}

.footer-right a {
  display: flex;
  align-items: center;
  gap: 4px;
  color: rgba(0, 0, 0, 0.65);
  text-decoration: none;
  transition: color 0.3s;
}

.footer-right a:hover {
  color: #1890ff;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .layout-header {
    padding: 0 16px;
  }

  .layout-content {
    margin: 16px;
  }

  .header-breadcrumb {
    display: none;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
  }
}
</style>
