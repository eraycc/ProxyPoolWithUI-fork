<template>
  <div class="api-page fade-in">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <ApiOutlined />
        API 接口文档
      </h1>
      <p class="page-description">
        本系统提供的所有 API 接口说明和使用示例
      </p>
    </div>

    <!-- API 统计卡片 -->
    <a-row :gutter="[16, 16]" class="stats-row">
      <a-col :xs="24" :sm="12" :md="6">
        <div class="stat-card gradient-bg-blue">
          <div class="stat-icon">
            <ApiOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-label">总接口数</div>
            <div class="stat-value">{{ totalApis }}</div>
          </div>
        </div>
      </a-col>

      <a-col :xs="24" :sm="12" :md="6">
        <div class="stat-card gradient-bg-green">
          <div class="stat-icon">
            <CheckCircleOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-label">GET 接口</div>
            <div class="stat-value">{{ getApis }}</div>
          </div>
        </div>
      </a-col>

      <a-col :xs="24" :sm="12" :md="6">
        <div class="stat-card gradient-bg-orange">
          <div class="stat-icon">
            <SendOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-label">POST 接口</div>
            <div class="stat-value">{{ postApis }}</div>
          </div>
        </div>
      </a-col>

      <a-col :xs="24" :sm="12" :md="6">
        <div class="stat-card gradient-bg-purple">
          <div class="stat-icon">
            <ThunderboltOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-label">服务状态</div>
            <div class="stat-badge">
              <span class="status-indicator online"></span>
              在线
            </div>
          </div>
        </div>
      </a-col>
    </a-row>

    <!-- API 分类列表 -->
    <a-collapse v-model:activeKey="activeKeys" class="api-collapse" accordion>
      <!-- 代理获取接口 -->
      <a-collapse-panel key="proxy" class="api-panel">
        <template #header>
          <div class="panel-header">
            <DatabaseOutlined class="panel-icon" />
            <span class="panel-title">代理获取接口</span>
            <a-tag color="blue">{{ proxyApis.length }} 个接口</a-tag>
          </div>
        </template>
        
        <div v-for="api in proxyApis" :key="api.path" class="api-item">
          <div class="api-header">
            <a-tag :color="getMethodColor(api.method)">{{ api.method }}</a-tag>
            <code class="api-path">{{ api.path }}</code>
            <a-button 
              type="link" 
              size="small" 
              @click="copyToClipboard(getFullUrl(api.path))"
            >
              <CopyOutlined />
              复制
            </a-button>
          </div>
          <div class="api-desc">{{ api.description }}</div>
          <div v-if="api.params" class="api-params">
            <strong>参数：</strong>
            <span v-for="(param, index) in api.params" :key="index">
              <code>{{ param }}</code>{{ index < api.params.length - 1 ? ', ' : '' }}
            </span>
          </div>
          <div class="api-example">
            <strong>示例：</strong>
            <code class="example-code">{{ api.example }}</code>
            <a-button 
              type="link" 
              size="small"
              @click="testApi(api)"
            >
              <PlayCircleOutlined />
              测试
            </a-button>
          </div>
          <div v-if="api.response" class="api-response">
            <strong>响应示例：</strong>
            <pre class="response-code">{{ api.response }}</pre>
          </div>
        </div>
      </a-collapse-panel>

      <!-- Clash 订阅接口 -->
      <a-collapse-panel key="clash" class="api-panel">
        <template #header>
          <div class="panel-header">
            <CloudOutlined class="panel-icon" />
            <span class="panel-title">Clash 订阅接口</span>
            <a-tag color="purple">{{ clashApis.length }} 个接口</a-tag>
          </div>
        </template>
        
        <div v-for="api in clashApis" :key="api.path" class="api-item">
          <div class="api-header">
            <a-tag :color="getMethodColor(api.method)">{{ api.method }}</a-tag>
            <code class="api-path">{{ api.path }}</code>
            <a-button 
              type="link" 
              size="small" 
              @click="copyToClipboard(getFullUrl(api.path))"
            >
              <CopyOutlined />
              复制
            </a-button>
          </div>
          <div class="api-desc">{{ api.description }}</div>
          <div v-if="api.params" class="api-params">
            <strong>参数：</strong>
            <span v-for="(param, index) in api.params" :key="index">
              <code>{{ param }}</code>{{ index < api.params.length - 1 ? ', ' : '' }}
            </span>
          </div>
          <div v-if="api.note" class="api-note">
            <strong>说明：</strong>
            <span>{{ api.note }}</span>
          </div>
          <div class="api-example">
            <strong>示例：</strong>
            <code class="example-code">{{ api.example }}</code>
            <a-button 
              type="link" 
              size="small"
              @click="testApi(api)"
            >
              <PlayCircleOutlined />
              测试
            </a-button>
          </div>
        </div>
      </a-collapse-panel>

      <!-- 管理接口 -->
      <a-collapse-panel key="management" class="api-panel">
        <template #header>
          <div class="panel-header">
            <SettingOutlined class="panel-icon" />
            <span class="panel-title">管理接口</span>
            <a-tag color="green">{{ managementApis.length }} 个接口</a-tag>
          </div>
        </template>
        
        <div v-for="api in managementApis" :key="api.path" class="api-item">
          <div class="api-header">
            <a-tag :color="getMethodColor(api.method)">{{ api.method }}</a-tag>
            <code class="api-path">{{ api.path }}</code>
            <a-button 
              type="link" 
              size="small" 
              @click="copyToClipboard(getFullUrl(api.path))"
            >
              <CopyOutlined />
              复制
            </a-button>
          </div>
          <div class="api-desc">{{ api.description }}</div>
          <div v-if="api.body" class="api-body">
            <strong>请求体：</strong>
            <pre class="body-code">{{ JSON.stringify(api.body, null, 2) }}</pre>
          </div>
          <div class="api-example">
            <strong>示例：</strong>
            <code class="example-code">{{ api.example }}</code>
          </div>
        </div>
      </a-collapse-panel>
    </a-collapse>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  ApiOutlined,
  CheckCircleOutlined,
  SendOutlined,
  ThunderboltOutlined,
  DatabaseOutlined,
  CloudOutlined,
  SettingOutlined,
  CopyOutlined,
  PlayCircleOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'

// 定义 API 类型
interface ApiItem {
  method: string
  path: string
  description: string
  example: string
  response?: string
  params?: string[]
  note?: string
  body?: Record<string, any>
}

const activeKeys = ref<string[]>(['proxy'])

// API 数据
const proxyApis: ApiItem[] = [
  {
    method: 'GET',
    path: '/ping',
    description: '测试 API 状态',
    example: 'curl http://localhost:5000/ping',
    response: 'API OK'
  },
  {
    method: 'GET',
    path: '/fetch_random',
    description: '随机获取一个可用代理',
    example: 'curl http://localhost:5000/fetch_random',
    response: 'http://127.0.0.1:8080'
  },
  {
    method: 'GET',
    path: '/fetch_all',
    description: '获取所有可用代理（逗号分隔）',
    example: 'curl http://localhost:5000/fetch_all',
    response: 'http://127.0.0.1:8080,http://127.0.0.1:8081,...'
  },
  {
    method: 'GET',
    path: '/fetch_http',
    description: '获取一个 HTTP 代理',
    example: 'curl http://localhost:5000/fetch_http',
    response: 'http://127.0.0.1:8080'
  },
  {
    method: 'GET',
    path: '/fetch_http_all',
    description: '获取所有 HTTP 代理',
    example: 'curl http://localhost:5000/fetch_http_all',
    response: 'http://127.0.0.1:8080,http://127.0.0.1:8081'
  },
  {
    method: 'GET',
    path: '/fetch_https',
    description: '获取一个 HTTPS 代理',
    example: 'curl http://localhost:5000/fetch_https',
    response: 'https://127.0.0.1:8443'
  },
  {
    method: 'GET',
    path: '/fetch_https_all',
    description: '获取所有 HTTPS 代理',
    example: 'curl http://localhost:5000/fetch_https_all',
    response: 'https://127.0.0.1:8443,https://127.0.0.1:8444'
  },
  {
    method: 'GET',
    path: '/fetch_socks4',
    description: '获取一个 SOCKS4 代理',
    example: 'curl http://localhost:5000/fetch_socks4',
    response: 'socks4://127.0.0.1:1080'
  },
  {
    method: 'GET',
    path: '/fetch_socks4_all',
    description: '获取所有 SOCKS4 代理',
    example: 'curl http://localhost:5000/fetch_socks4_all',
    response: 'socks4://127.0.0.1:1080,socks4://127.0.0.1:1081'
  },
  {
    method: 'GET',
    path: '/fetch_socks5',
    description: '获取一个 SOCKS5 代理',
    example: 'curl http://localhost:5000/fetch_socks5',
    response: 'socks5://127.0.0.1:1080'
  },
  {
    method: 'GET',
    path: '/fetch_socks5_all',
    description: '获取所有 SOCKS5 代理',
    example: 'curl http://localhost:5000/fetch_socks5_all',
    response: 'socks5://127.0.0.1:1080,socks5://127.0.0.1:1081'
  }
]

const clashApis: ApiItem[] = [
  {
    method: 'GET',
    path: '/clash',
    description: '获取 Clash 完整订阅配置（YAML 格式）',
    params: [
      'c (可选) - 按国家筛选，多个用逗号分隔，如 c=CN,US',
      'nc (可选) - 排除指定国家，如 nc=CN',
      'protocol (可选) - 筛选协议类型：http/https/socks5',
      'limit (可选) - 限制返回数量，默认全部'
    ],
    note: '返回完整的 Clash 配置，包含代理节点、代理组和规则。节点名称格式：🇨🇳 中国+IP 或 IP+端口（无国家信息时）',
    example: 'curl http://localhost:5000/clash?c=CN,US&limit=50'
  },
  {
    method: 'GET',
    path: '/clash/proxies',
    description: '获取 Clash 代理节点列表（YAML 格式）',
    params: [
      'c (可选) - 按国家筛选，多个用逗号分隔',
      'nc (可选) - 排除指定国家',
      'protocol (可选) - 筛选协议类型',
      'limit (可选) - 限制返回数量'
    ],
    note: '仅返回代理节点列表，不包含完整配置。适合用于自定义 Clash 配置文件',
    example: 'curl http://localhost:5000/clash/proxies?nc=CN&limit=100'
  }
]

const managementApis: ApiItem[] = [
  {
    method: 'GET',
    path: '/proxies_status',
    description: '获取代理状态和列表',
    params: ['limit (可选) - 限制返回数量，默认 1000'],
    example: 'curl http://localhost:5000/proxies_status?limit=500'
  },
  {
    method: 'GET',
    path: '/fetchers_status',
    description: '获取爬取器状态和统计信息',
    example: 'curl http://localhost:5000/fetchers_status'
  },
  {
    method: 'POST',
    path: '/add_proxy',
    description: '手动添加代理到数据库',
    body: {
      fetcher_name: '手动添加',
      protocol: 'http',
      ip: '127.0.0.1',
      port: 8080,
      username: '可选',
      password: '可选',
      country: '可选',
      address: '可选'
    },
    example: 'curl -X POST http://localhost:5000/add_proxy -H "Content-Type: application/json" -d \'{"fetcher_name":"手动添加","protocol":"http","ip":"127.0.0.1","port":8080}\''
  },
  {
    method: 'GET',
    path: '/fetcher_enable',
    description: '启用或禁用指定爬取器',
    params: ['name (必填) - 爬取器名称', 'enable (必填) - 0=禁用, 1=启用'],
    example: 'curl "http://localhost:5000/fetcher_enable?name=KuaidailiFetcher&enable=1"'
  },
  {
    method: 'GET',
    path: '/clear_fetchers_status',
    description: '清空所有爬取器的统计信息',
    example: 'curl http://localhost:5000/clear_fetchers_status'
  }
]

// 统计
const totalApis = computed(() => proxyApis.length + clashApis.length + managementApis.length)
const getApis = computed(() => [...proxyApis, ...clashApis, ...managementApis].filter(api => api.method === 'GET').length)
const postApis = computed(() => managementApis.filter(api => api.method === 'POST').length)

// 方法颜色
const getMethodColor = (method: string) => {
  const colors: Record<string, string> = {
    'GET': 'blue',
    'POST': 'green',
    'PUT': 'orange',
    'DELETE': 'red'
  }
  return colors[method] || 'default'
}

// 获取完整 URL
const getFullUrl = (path: string) => {
  return `http://localhost:5000${path}`
}

// 复制到剪贴板
const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    message.success('已复制到剪贴板')
  } catch (err) {
    message.error('复制失败')
  }
}

// 测试 API
const testApi = (api: ApiItem) => {
  const url = getFullUrl(api.path)
  window.open(url, '_blank')
  message.info('已在新标签页打开')
}
</script>

<style scoped>
.api-page {
  max-width: 1400px;
  margin: 0 auto;
}

/* 页面标题 */
.page-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.page-title {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(0, 0, 0, 0.85);
}

.page-description {
  margin: 0;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.45);
}

/* 统计卡片 */
.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  padding: 20px;
  border-radius: 12px;
  color: white;
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 100px;
}

.stat-icon {
  font-size: 32px;
  opacity: 0.9;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  line-height: 1;
}

.stat-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 12px;
}

.gradient-bg-blue {
  background: linear-gradient(135deg, #667eea 0%, #1890ff 100%);
}

.gradient-bg-green {
  background: linear-gradient(135deg, #52c41a 0%, #95de64 100%);
}

.gradient-bg-orange {
  background: linear-gradient(135deg, #faad14 0%, #ffc53d 100%);
}

.gradient-bg-purple {
  background: linear-gradient(135deg, #722ed1 0%, #9254de 100%);
}

/* API 折叠面板 */
.api-collapse {
  background: #fff;
  border-radius: 12px;
  margin-bottom: 24px;
}

.api-collapse :deep(.ant-collapse-item) {
  border-bottom: 1px solid #f0f0f0;
}

.api-collapse :deep(.ant-collapse-item:last-child) {
  border-bottom: none;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  font-size: 16px;
}

.panel-icon {
  font-size: 20px;
  color: #1890ff;
}

.panel-title {
  flex: 1;
}

/* API 项目 */
.api-item {
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  margin-bottom: 16px;
}

.api-item:last-child {
  margin-bottom: 0;
}

.api-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.api-path {
  flex: 1;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  background: #fff;
  padding: 4px 12px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
}

.api-desc {
  margin-bottom: 8px;
  color: rgba(0, 0, 0, 0.65);
}

.api-params,
.api-body,
.api-note {
  margin: 8px 0;
  font-size: 13px;
}

.api-params code,
.api-body code {
  background: #fff;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  color: #d4380d;
}

.api-note {
  padding: 8px 12px;
  background: #e6f7ff;
  border-left: 3px solid #1890ff;
  border-radius: 4px;
  color: rgba(0, 0, 0, 0.65);
}

.api-example {
  margin: 8px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.example-code {
  flex: 1;
  background: #fff;
  padding: 8px 12px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  overflow-x: auto;
  border: 1px solid #d9d9d9;
}

.api-response {
  margin-top: 8px;
}

.response-code {
  background: #fff;
  padding: 12px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  overflow-x: auto;
  margin: 4px 0 0 0;
  border: 1px solid #d9d9d9;
}

.body-code {
  background: #fff;
  padding: 12px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  overflow-x: auto;
  margin: 4px 0 0 0;
  border: 1px solid #d9d9d9;
}

/* 动画 */
.fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 状态指示器 */
.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.status-indicator.online {
  background: #52c41a;
  box-shadow: 0 0 0 2px rgba(82, 196, 26, 0.3);
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
