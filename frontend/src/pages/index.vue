<template>
  <div class="proxy-page fade-in">
    <!-- 统计卡片区域 -->
    <a-row :gutter="[16, 16]" class="stats-row">
      <a-col :xs="24" :sm="12" :md="6">
        <div class="stat-card enhanced-card gradient-bg-blue slide-in-up" style="animation-delay: 0s">
          <div class="stat-icon">
            <DatabaseOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-main">
              <div class="stat-label">全部代理数量</div>
              <div class="stat-value">{{ sumProxiesCnt.toLocaleString() }}</div>
            </div>
                                <a-tooltip title="目前数据库中的代理总数，包含没有通过验证的代理">
              <QuestionCircleOutlined class="stat-help" />
                                </a-tooltip>
          </div>
        </div>
            </a-col>

      <a-col :xs="24" :sm="12" :md="6">
        <div class="stat-card enhanced-card gradient-bg-green slide-in-up" style="animation-delay: 0.1s">
          <div class="stat-icon">
            <CheckCircleOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-main">
              <div class="stat-label">当前可用代理</div>
              <div class="stat-value">{{ validatedProxiesCnt.toLocaleString() }}</div>
            </div>
            <div class="stat-badge" v-if="validatedProxiesCnt > 0">
              <span class="status-indicator online"></span>
              在线
            </div>
          </div>
        </div>
            </a-col>

      <a-col :xs="24" :sm="12" :md="6">
        <div class="stat-card enhanced-card gradient-bg-orange slide-in-up" style="animation-delay: 0.2s">
          <div class="stat-icon">
            <ClockCircleOutlined />
          </div>
          <div class="stat-content">
            <div class="stat-main">
              <div class="stat-label">等待验证</div>
              <div class="stat-value">{{ pendingProxiesCnt.toLocaleString() }}</div>
            </div>
                                <a-tooltip>
                                    <template #title>
                表示这些代理的下次验证时间已经到了，但还没有完成验证
                                    </template>
              <QuestionCircleOutlined class="stat-help" />
                                </a-tooltip>
          </div>
        </div>
            </a-col>

      <a-col :xs="24" :sm="12" :md="6">
        <div class="stat-card enhanced-card control-card slide-in-up" style="animation-delay: 0.3s">
          <div class="control-content">
            <div class="control-item">
              <span class="control-label">自动刷新</span>
              <a-switch v-model:checked="autoupdate" size="small" />
            </div>
            <div class="control-item">
              <span class="control-label">间隔(秒)</span>
              <a-input-number
                v-model:value="refreshInterval"
                :min="5"
                :max="300"
                :step="5"
                size="small"
                style="width: 80px"
                @change="onIntervalChange"
              />
            </div>
            <div class="control-item" style="font-size: 11px">
              <ClockCircleOutlined style="margin-right: 4px" />
              <span class="control-time">{{ lastupdate }}</span>
            </div>
          </div>
        </div>
            </a-col>
        </a-row>

    <!-- 代理列表 -->
    <div class="table-container enhanced-card scale-in">
      <div class="table-header">
        <h2 class="table-title">
          <UnorderedListOutlined />
          可用代理列表
        </h2>
      </div>

      <!-- 搜索筛选区域 -->
      <div class="search-filters-container">
        <a-space :size="10" wrap class="filter-space">
          <!-- 国家下拉框 -->
          <a-select
            v-model:value="searchCountry"
            placeholder="🌍 国家/地区"
            style="width: 140px"
            size="small"
            allow-clear
            show-search
            :filter-option="filterCountryOption"
            class="filter-select"
          >
            <a-select-option value="">全部国家</a-select-option>
            <a-select-option value="中国">🇨🇳 中国</a-select-option>
            <a-select-option value="美国">🇺🇸 美国</a-select-option>
            <a-select-option value="日本">🇯🇵 日本</a-select-option>
            <a-select-option value="韩国">🇰🇷 韩国</a-select-option>
            <a-select-option value="新加坡">🇸🇬 新加坡</a-select-option>
            <a-select-option value="香港">🇭🇰 香港</a-select-option>
            <a-select-option value="台湾">🇹🇼 台湾</a-select-option>
            <a-select-option value="德国">🇩🇪 德国</a-select-option>
            <a-select-option value="英国">🇬🇧 英国</a-select-option>
            <a-select-option value="法国">🇫🇷 法国</a-select-option>
            <a-select-option value="加拿大">🇨🇦 加拿大</a-select-option>
            <a-select-option value="本地">🏠 本地</a-select-option>
            <a-select-option value="未知">🌐 未知</a-select-option>
          </a-select>
          
          <!-- 来源下拉框 -->
          <a-select
            v-model:value="searchSource"
            placeholder="📡 来源"
            style="width: 150px"
            size="small"
            allow-clear
            show-search
            :filter-option="filterSourceOption"
            class="filter-select"
          >
            <a-select-option value="">全部来源</a-select-option>
            <a-select-option 
              v-for="source in sourceOptions" 
              :key="source" 
              :value="source"
            >
              {{ source }}
            </a-select-option>
          </a-select>
          
          <!-- 协议下拉框 -->
          <a-select
            v-model:value="filterProtocol"
            placeholder="🔌 协议类型"
            style="width: 120px"
            size="small"
            allow-clear
            class="filter-select"
          >
            <a-select-option value="">全部协议</a-select-option>
            <a-select-option value="http">HTTP</a-select-option>
            <a-select-option value="https">HTTPS</a-select-option>
            <a-select-option value="socks4">SOCKS4</a-select-option>
            <a-select-option value="socks5">SOCKS5</a-select-option>
          </a-select>
          
          <!-- IP输入框 -->
          <a-input
            v-model:value="searchIP"
            placeholder="🔍 搜索 IP"
            style="width: 140px"
            size="small"
            allow-clear
            class="filter-input"
          />
          
          <!-- 端口输入框 -->
          <a-input
            v-model:value="searchPort"
            placeholder="🔢 端口"
            style="width: 100px"
            size="small"
            allow-clear
            class="filter-input"
          />
          
          <!-- 延迟范围输入框 -->
          <a-input
            v-model:value="searchLatency"
            placeholder="⚡ 延迟 如<1000"
            style="width: 130px"
            size="small"
            allow-clear
            class="filter-input"
          />
          
          <!-- 存活时间输入框 -->
          <a-input
            v-model:value="searchAliveTime"
            placeholder="⏱️ 存活 如>3600"
            style="width: 130px"
            size="small"
            allow-clear
            class="filter-input"
          />
          
          <!-- 新增代理按钮 -->
          <a-button 
            type="primary" 
            size="small"
            @click="showAddModal"
            class="add-btn"
          >
            <PlusOutlined />
            新增代理
          </a-button>
          
          <!-- 复制 Clash 订阅按钮 -->
          <a-button 
            type="default" 
            size="small"
            @click="copyClashSubscription"
            class="clash-btn"
          >
            <CopyOutlined />
            复制 Clash 订阅
          </a-button>
          
          <!-- 清空筛选按钮 -->
          <a-button 
            type="primary" 
            size="small" 
            danger
            @click="clearAllFilters"
            v-if="hasActiveFilters"
            class="clear-btn"
          >
            <ClearOutlined />
            清空
          </a-button>
          
          <!-- 激活筛选标签 -->
          <a-tag color="blue" v-if="hasActiveFilters" class="active-tag">
            {{ activeFiltersCount }} 个筛选
          </a-tag>
        </a-space>
      </div>

      <!-- 新增代理弹窗 -->
      <a-modal
        v-model:open="addModalVisible"
        title="新增代理"
        width="600px"
        @ok="handleAddProxy"
        @cancel="handleCancelAdd"
        :confirmLoading="addLoading"
      >
        <a-form
          :model="addForm"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 18 }"
          class="add-proxy-form"
        >
          <a-form-item label="来源" required>
            <a-input
              v-model:value="addForm.fetcher_name"
              placeholder="请输入来源，如: 手动添加"
              allow-clear
            />
          </a-form-item>

          <a-form-item label="协议" required>
            <a-select
              v-model:value="addForm.protocol"
              placeholder="请选择协议"
              allow-clear
            >
              <a-select-option value="http">HTTP</a-select-option>
              <a-select-option value="https">HTTPS</a-select-option>
              <a-select-option value="socks4">SOCKS4</a-select-option>
              <a-select-option value="socks5">SOCKS5</a-select-option>
            </a-select>
          </a-form-item>

          <a-form-item label="IP地址" required>
            <a-input
              v-model:value="addForm.ip"
              placeholder="请输入IP地址，如: 127.0.0.1"
              allow-clear
            />
          </a-form-item>

          <a-form-item label="端口" required>
            <a-input-number
              v-model:value="addForm.port"
              placeholder="请输入端口"
              :min="1"
              :max="65535"
              style="width: 100%"
            />
          </a-form-item>

          <a-form-item label="账号">
            <a-input
              v-model:value="addForm.username"
              placeholder="如需认证请输入账号"
              allow-clear
            />
          </a-form-item>

          <a-form-item label="密码">
            <a-input-password
              v-model:value="addForm.password"
              placeholder="如需认证请输入密码"
              allow-clear
            />
          </a-form-item>

          <a-form-item label="国家">
            <a-input
              v-model:value="addForm.country"
              placeholder="请输入国家，如: 中国"
              allow-clear
            />
          </a-form-item>

          <a-form-item label="地址">
            <a-input
              v-model:value="addForm.address"
              placeholder="请输入详细地址，如: 北京"
              allow-clear
            />
          </a-form-item>
        </a-form>
      </a-modal>

        <a-table
            :columns="columns"
        :data-source="filteredProxies"
        :row-key="(r: any) => `${r.protocol}://${r.ip}:${r.port}`"
        :bordered="false"
        :loading="false"
        v-model:pagination="pagination"
        @change="handleTableChange"
        :scroll="{ x: 1200 }"
        class="modern-table"
        size="small"
      >
        <template #bodyCell="{ column, record }">
          <!-- 来源列 -->
          <template v-if="column.key === 'fetcher_name'">
            <a-tag color="purple">
              <GlobalOutlined style="margin-right: 4px" />
              {{ record.fetcher_name }}
            </a-tag>
          </template>

          <!-- 协议列 -->
          <template v-else-if="column.key === 'protocol'">
            <a-tag :color="getProtocolColor(record.protocol)">
              {{ record.protocol.toUpperCase() }}
            </a-tag>
          </template>

          <!-- IP列 -->
          <template v-else-if="column.key === 'ip'">
            <code class="ip-code">{{ record.ip }}</code>
          </template>

          <!-- 端口列 -->
          <template v-else-if="column.key === 'port'">
            <a-tag color="default">{{ record.port }}</a-tag>
          </template>
          
          <!-- 国家/地区列 -->
          <template v-else-if="column.key === 'country'">
            <div class="country-info">
              <span class="country-flag">{{ getCountryFlag(record.country || '未知') }}</span>
              <span class="country-name">{{ record.country || '未知' }}</span>
            </div>
          </template>
          
          <!-- 地址列 -->
          <template v-else-if="column.key === 'address'">
            <a-tooltip :title="record.address || '无'">
              <span class="address-text">{{ record.address || '-' }}</span>
            </a-tooltip>
          </template>
          
          <!-- 账号列 -->
          <template v-else-if="column.key === 'username'">
            <code class="auth-code" v-if="record.username">{{ record.username }}</code>
            <span class="unknown-text" v-else>未知</span>
          </template>
          
          <!-- 密码列 -->
          <template v-else-if="column.key === 'password'">
            <code class="auth-code" v-if="record.password">{{ record.password }}</code>
            <span class="unknown-text" v-else>未知</span>
          </template>

          <!-- 延迟列 -->
          <template v-else-if="column.key === 'latency'">
            <a-tag :color="getLatencyColor(record.latency)" class="latency-tag">
              <ThunderboltOutlined v-if="record.latency < 1000" />
              <DashboardOutlined v-else />
              {{ record.latency }}ms
            </a-tag>
          </template>

          <!-- 存活时间列 -->
          <template v-else-if="column.key === 'alive_time'">
            <a-tag color="cyan" class="alive-tag">
              <ClockCircleOutlined />
              {{ formatAliveTime(record.alive_time) }}
            </a-tag>
          </template>

          <!-- 验证时间列 -->
          <template v-else-if="column.key === 'validate_date'">
            <span class="time-text">
              {{ record.validate_date ? moment(record.validate_date).format('MM-DD HH:mm:ss') : '-' }}
            </span>
          </template>

          <template v-else-if="column.key === 'to_validate_date'">
            <span class="time-text">
              {{ record.to_validate_date ? moment(record.to_validate_date).format('MM-DD HH:mm:ss') : '-' }}
            </span>
          </template>
          
          <!-- 操作列 -->
          <template v-else-if="column.key === 'action'">
            <a-space :size="4">
              <a-tooltip title="复制代理地址">
                <a-button 
                  type="link" 
                  size="small" 
                  @click="copyProxy(record)"
                  style="padding: 0 4px"
                >
                  <CopyOutlined />
                  代理
                </a-button>
              </a-tooltip>
              
              <!-- 只对socks协议显示V2Ray按钮 -->
              <a-tooltip title="复制V2Ray节点" v-if="record.protocol === 'socks4' || record.protocol === 'socks5'">
                <a-button 
                  type="link" 
                  size="small" 
                  @click="copyV2Ray(record)"
                  style="padding: 0 4px"
                >
                  <LinkOutlined />
                  V2Ray
                </a-button>
              </a-tooltip>
            </a-space>
          </template>
        </template>

        <!-- 表头自定义 -->
        <template #headerCell="{ column }">
          <template v-if="column.key === 'to_validate_date'">
            <span>
                下次验证时间
                <a-tooltip>
                    <template #title>
                  验证器会不断从数据库中取出满足下次验证时间在当前时间之前的代理进行验证
                    </template>
                <QuestionCircleOutlined style="margin-left: 4px; opacity: 0.6" />
                </a-tooltip>
            </span>
          </template>
        </template>
        </a-table>
    </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch, h } from 'vue'
import {
  QuestionCircleOutlined,
  DatabaseOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  ReloadOutlined,
  UnorderedListOutlined,
  SearchOutlined,
  GlobalOutlined,
  ThunderboltOutlined,
  DashboardOutlined,
  EnvironmentOutlined,
  CopyOutlined,
  LinkOutlined,
  ClearOutlined,
  ApiOutlined,
  PlusOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import moment from 'moment'

// Nuxt auto-imports
const { $http } = useNuxtApp() as any

const proxies = ref<any[]>([])
const sumProxiesCnt = ref(0)
const validatedProxiesCnt = ref(0)
const pendingProxiesCnt = ref(0)
const autoupdate = ref(true)
const lastupdate = ref('')
const loading = ref(false)
const filterProtocol = ref('')
const searchIP = ref('')
const searchPort = ref('')
const searchSource = ref('')
const searchCountry = ref('')
const searchLatency = ref('') // 延迟筛选
const searchAliveTime = ref('') // 存活时间筛选
const refreshInterval = ref(10) // 默认10秒
const sourceOptions = ref<string[]>([]) // 来源选项列表

// 新增代理相关
const addModalVisible = ref(false)
const addLoading = ref(false)
const addForm = ref({
  fetcher_name: '手动添加',
  protocol: '',
  ip: '',
  port: null as number | null,
  username: '',
  password: '',
  country: '',
  address: ''
})

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  pageSizeOptions: ['10', '20', '50', '100'],
  showTotal: (total: number) => `共 ${total} 条`,
  size: 'small' as const,
  onChange: (page: number, pageSize: number) => {
    pagination.value.current = page
    pagination.value.pageSize = pageSize
  },
  onShowSizeChange: (current: number, size: number) => {
    pagination.value.current = 1
    pagination.value.pageSize = size
  }
})
let handle: ReturnType<typeof setTimeout> | null = null

// 格式化存活时间
const formatAliveTime = (seconds: number) => {
  if (!seconds && seconds !== 0) return '-'
  
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (days > 0) {
    return `${days}天${hours}时`
  } else if (hours > 0) {
    return `${hours}时${minutes}分`
  } else if (minutes > 0) {
    return `${minutes}分${secs}秒`
  } else {
    return `${secs}秒`
  }
}

// 获取协议颜色
const getProtocolColor = (protocol: string) => {
  const colorMap: any = {
    http: 'blue',
    https: 'green',
    socks4: 'orange',
    socks5: 'purple'
  }
  return colorMap[protocol] || 'default'
}

// 获取延迟颜色
const getLatencyColor = (latency: number) => {
  if (latency < 1000) return 'success'
  if (latency < 2000) return 'processing'
  if (latency < 4000) return 'warning'
  return 'error'
}

// 搜索过滤
const filteredProxies = computed(() => {
  let result = proxies.value
  
  // 协议筛选
  if (filterProtocol.value) {
    result = result.filter(proxy => 
      proxy.protocol.toLowerCase() === filterProtocol.value.toLowerCase()
    )
  }
  
  // IP 搜索
  if (searchIP.value) {
    const search = searchIP.value.toLowerCase()
    result = result.filter(proxy => 
      proxy.ip.toLowerCase().includes(search)
    )
  }
  
  // 端口搜索
  if (searchPort.value) {
    const search = searchPort.value
    result = result.filter(proxy => 
      proxy.port.toString().includes(search)
    )
  }
  
  // 来源搜索
  if (searchSource.value) {
    const search = searchSource.value.toLowerCase()
    result = result.filter(proxy => 
      proxy.fetcher_name.toLowerCase().includes(search)
    )
  }
  
  // 国家搜索
  if (searchCountry.value) {
    result = result.filter(proxy => {
      return proxy.country === searchCountry.value
    })
  }
  
  // 延迟筛选（支持小于某个值，如 <1000 表示小于1000ms）
  if (searchLatency.value) {
    const latencyStr = searchLatency.value.trim()
    if (latencyStr.startsWith('<')) {
      const maxLatency = parseInt(latencyStr.substring(1))
      if (!isNaN(maxLatency)) {
        result = result.filter(proxy => proxy.latency < maxLatency)
      }
    } else if (latencyStr.startsWith('>')) {
      const minLatency = parseInt(latencyStr.substring(1))
      if (!isNaN(minLatency)) {
        result = result.filter(proxy => proxy.latency > minLatency)
      }
    } else {
      const latency = parseInt(latencyStr)
      if (!isNaN(latency)) {
        result = result.filter(proxy => proxy.latency <= latency)
      }
    }
  }
  
  // 存活时间筛选（支持大于某个值，如 >3600 表示大于3600秒）
  if (searchAliveTime.value) {
    const aliveTimeStr = searchAliveTime.value.trim()
    if (aliveTimeStr.startsWith('>')) {
      const minTime = parseInt(aliveTimeStr.substring(1))
      if (!isNaN(minTime)) {
        result = result.filter(proxy => proxy.alive_time > minTime)
      }
    } else if (aliveTimeStr.startsWith('<')) {
      const maxTime = parseInt(aliveTimeStr.substring(1))
      if (!isNaN(maxTime)) {
        result = result.filter(proxy => proxy.alive_time < maxTime)
      }
    } else {
      const time = parseInt(aliveTimeStr)
      if (!isNaN(time)) {
        result = result.filter(proxy => proxy.alive_time >= time)
      }
    }
  }
  
  // 更新分页总数
  pagination.value.total = result.length
  
  return result
})

// 根据IP获取国家（简化版本，实际应该调用IP地理位置API）
const getCountryFromIP = (ip: string): string => {
  // 这里是简化版本，实际应该调用真实的IP地理位置API
  // 可以使用 ip-api.com, ipapi.co 等服务
  if (ip.startsWith('192.168') || ip.startsWith('10.') || ip.startsWith('172.')) {
    return '本地'
  }
  // 这里可以添加更多的IP段判断
  // 实际使用时应该调用后端API或第三方服务
  return '未知'
}

// 根据国家代码获取国旗 Emoji
const getCountryFlag = (country: string): string => {
  const countryFlags: Record<string, string> = {
    '中国': '🇨🇳',
    '美国': '🇺🇸',
    '日本': '🇯🇵',
    '韩国': '🇰🇷',
    '新加坡': '🇸🇬',
    '香港': '🇭🇰',
    '台湾': '🇹🇼',
    '德国': '🇩🇪',
    '英国': '🇬🇧',
    '法国': '🇫🇷',
    '加拿大': '🇨🇦',
    '澳大利亚': '🇦🇺',
    '俄罗斯': '🇷🇺',
    '印度': '🇮🇳',
    '巴西': '🇧🇷',
    '本地': '🏠',
    '未知': '🌍'
  }
  return countryFlags[country] || '🌍'
}

// 来源筛选
const filterSourceOption = (input: string, option: any) => {
  return option.value.toLowerCase().includes(input.toLowerCase())
}

// 国家筛选
const filterCountryOption = (input: string, option: any) => {
  return option.value.toLowerCase().includes(input.toLowerCase())
}

// 复制到剪贴板
const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (err) {
    // 降级方案
    const textarea = document.createElement('textarea')
    textarea.value = text
    textarea.style.position = 'fixed'
    textarea.style.opacity = '0'
    document.body.appendChild(textarea)
    textarea.select()
    try {
      document.execCommand('copy')
      document.body.removeChild(textarea)
      return true
    } catch (e) {
      document.body.removeChild(textarea)
      return false
    }
  }
}

// 复制代理地址
const copyProxy = async (record: any) => {
  // 格式: protocol://username:password@ip:port
  // 如果没有用户名密码，则不添加认证信息
  let proxyUrl = ''
  if (record.username && record.password) {
    proxyUrl = `${record.protocol}://${record.username}:${record.password}@${record.ip}:${record.port}`
  } else {
    proxyUrl = `${record.protocol}://${record.ip}:${record.port}`
  }
  
  const success = await copyToClipboard(proxyUrl)
  if (success) {
    message.success('代理地址已复制到剪贴板')
  } else {
    message.error('复制失败，请手动复制')
  }
}

// 复制V2Ray节点
const copyV2Ray = async (record: any) => {
  // 格式: socks://[认证信息]@[服务器地址]:[端口]#[备注]
  let v2rayUrl = ''
  
  const country = record.country || '未知'
  const remark = `${country}_${record.ip}`
  const remarkEncoded = encodeURIComponent(remark)
  
  if (record.username && record.password) {
    // 有认证信息，需要Base64编码
    const authInfo = `${record.username}:${record.password}`
    const authBase64 = btoa(authInfo)
    
    v2rayUrl = `socks://${authBase64}@${record.ip}:${record.port}#${remarkEncoded}`
  } else {
    // 无认证信息，不需要 @ 符号
    v2rayUrl = `socks://${record.ip}:${record.port}#${remarkEncoded}`
  }
  
  const success = await copyToClipboard(v2rayUrl)
  if (success) {
    message.success('V2Ray节点已复制到剪贴板')
  } else {
    message.error('复制失败，请手动复制')
  }
}

// 是否有激活的筛选条件
const hasActiveFilters = computed(() => {
  return !!(filterProtocol.value || searchIP.value || searchPort.value || searchSource.value || searchCountry.value || searchLatency.value || searchAliveTime.value)
})

// 激活的筛选条件数量
const activeFiltersCount = computed(() => {
  let count = 0
  if (filterProtocol.value) count++
  if (searchIP.value) count++
  if (searchPort.value) count++
  if (searchSource.value) count++
  if (searchCountry.value) count++
  if (searchLatency.value) count++
  if (searchAliveTime.value) count++
  return count
})

// 清空所有筛选
const clearAllFilters = () => {
  filterProtocol.value = ''
  searchIP.value = ''
  searchPort.value = ''
  searchSource.value = ''
  searchCountry.value = ''
  searchLatency.value = ''
  searchAliveTime.value = ''
  pagination.value.current = 1
}

// 显示新增弹窗
const showAddModal = () => {
  addModalVisible.value = true
}

// 取消新增
const handleCancelAdd = () => {
  addModalVisible.value = false
  // 重置表单
  addForm.value = {
    fetcher_name: '手动添加',
    protocol: '',
    ip: '',
    port: null,
    username: '',
    password: '',
    country: '',
    address: ''
  }
}

// 复制 Clash 订阅链接
const copyClashSubscription = async () => {
  try {
    // @ts-ignore - Nuxt 3 auto-import
    const config = useRuntimeConfig()
    const baseURL = config.public.apiBase as string
    const clashUrl = `${baseURL}/clash`
    
    // 使用 Clipboard API 复制
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(clashUrl)
      message.success('Clash 订阅链接已复制到剪贴板！')
    } else {
      // 降级方案：使用传统的复制方法
      const textArea = document.createElement('textarea')
      textArea.value = clashUrl
      textArea.style.position = 'fixed'
      textArea.style.left = '-999999px'
      document.body.appendChild(textArea)
      textArea.select()
      try {
        document.execCommand('copy')
        message.success('Clash 订阅链接已复制到剪贴板！')
      } catch (err) {
        message.error('复制失败，请手动复制：' + clashUrl)
        console.error('复制失败:', err)
      }
      document.body.removeChild(textArea)
    }
  } catch (error) {
    console.error('复制 Clash 订阅链接失败:', error)
    message.error('复制失败，请稍后重试')
  }
}

// 新增代理
const handleAddProxy = async () => {
  // 验证必填项
  if (!addForm.value.fetcher_name) {
    message.error('请输入来源')
    return
  }
  if (!addForm.value.protocol) {
    message.error('请选择协议')
    return
  }
  if (!addForm.value.ip) {
    message.error('请输入IP地址')
    return
  }
  if (!addForm.value.port) {
    message.error('请输入端口')
    return
  }

  // 验证IP格式
  const ipRegex = /^(\d{1,3}\.){3}\d{1,3}$/
  if (!ipRegex.test(addForm.value.ip)) {
    message.error('IP地址格式不正确')
    return
  }

  addLoading.value = true
  try {
    // 构建请求参数
    const params: any = {
      fetcher_name: addForm.value.fetcher_name,
      protocol: addForm.value.protocol,
      ip: addForm.value.ip,
      port: addForm.value.port
    }

    // 添加可选字段
    if (addForm.value.username) {
      params.username = addForm.value.username
    }
    if (addForm.value.password) {
      params.password = addForm.value.password
    }
    if (addForm.value.country) {
      params.country = addForm.value.country
    }
    if (addForm.value.address) {
      params.address = addForm.value.address
    }

    // 调用API（这里需要后端提供对应的接口）
    await $http.post('/add_proxy', params)
    
    message.success('代理添加成功')
    addModalVisible.value = false
    handleCancelAdd()
    
    // 刷新列表
    await update()
  } catch (error: any) {
    console.error('添加代理失败:', error)
    message.error(error.message || '添加代理失败')
  } finally {
    addLoading.value = false
  }
}

const columns = [
    {
    title: '来源',
    dataIndex: 'fetcher_name',
    key: 'fetcher_name',
    width: 140
  },
  {
    title: '协议',
    dataIndex: 'protocol',
    key: 'protocol',
    width: 80
  },
  {
    title: 'IP地址',
    dataIndex: 'ip',
    key: 'ip',
    width: 130
    },
    {
        title: '端口',
    dataIndex: 'port',
    key: 'port',
    width: 70
    },
    {
        title: '国家',
        dataIndex: 'country',
    key: 'country',
    width: 110
    },
    {
        title: '地址',
        dataIndex: 'address',
    key: 'address',
    width: 180
    },
    {
        title: '账号',
        dataIndex: 'username',
    key: 'username',
    width: 90
    },
    {
        title: '密码',
        dataIndex: 'password',
    key: 'password',
    width: 90
    },
    {
        title: '延迟',
        dataIndex: 'latency',
    key: 'latency',
    width: 90,
    sorter: (a: any, b: any) => a.latency - b.latency
  },
  {
    title: '存活',
    dataIndex: 'alive_time',
    key: 'alive_time',
    width: 100,
    sorter: (a: any, b: any) => a.alive_time - b.alive_time
  },
  {
    title: '上次验证',
        dataIndex: 'validate_date',
    key: 'validate_date',
    width: 120
    },
    {
        dataIndex: 'to_validate_date',
    key: 'to_validate_date',
    width: 120
    },
    {
        title: '操作',
        key: 'action',
    width: 160,
    fixed: 'right'
  }
]

const update = async () => {
  loading.value = true
  try {
    const data = await $http.get('/proxies_status')
    proxies.value = data.proxies
    sumProxiesCnt.value = data.sum_proxies_cnt
    validatedProxiesCnt.value = data.validated_proxies_cnt
    pendingProxiesCnt.value = data.pending_proxies_cnt
    lastupdate.value = moment().format('HH:mm:ss')
    
    // 更新来源选项列表
    const sources = new Set<string>()
    data.proxies.forEach((proxy: any) => {
      if (proxy.fetcher_name) {
        sources.add(proxy.fetcher_name)
      }
    })
    sourceOptions.value = Array.from(sources).sort()
  } catch (error) {
    console.error('更新数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 监听所有筛选条件变化，重置到第一页
watch([filterProtocol, searchIP, searchPort, searchSource, searchCountry, searchLatency, searchAliveTime], () => {
  pagination.value.current = 1
})

// 表格分页、排序、筛选变化时触发
const handleTableChange = (pag: any) => {
  console.log('分页变化:', pag)
}

// 重新启动定时器
const restartTimer = () => {
  if (handle) {
    clearInterval(handle)
    handle = null
  }
  if (autoupdate.value) {
    const intervalMs = refreshInterval.value * 1000
    console.log('启动自动刷新定时器，间隔:', refreshInterval.value, '秒')
    handle = setInterval(() => {
      console.log('自动刷新触发')
      update()
    }, intervalMs)
  }
}

// 间隔改变时重启定时器
const onIntervalChange = (value: number | null) => {
  if (value) {
    console.log('刷新间隔改变为:', value, '秒')
    restartTimer()
  }
}

// 监听自动刷新开关
watch(autoupdate, (newVal) => {
  console.log('自动刷新开关:', newVal)
  if (newVal) {
    restartTimer()
  } else if (handle) {
    clearInterval(handle)
    handle = null
  }
})

// 监听刷新间隔变化
watch(refreshInterval, (newVal) => {
  console.log('检测到间隔变化:', newVal, '秒')
  if (autoupdate.value) {
    restartTimer()
  }
})

onMounted(() => {
  restartTimer()
  update()
})

onUnmounted(() => {
  if (handle) {
    clearInterval(handle)
    handle = null
  }
})
</script>

<style scoped>
.proxy-page {
  padding: 0;
}

/* 统计卡片样式 */
.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  padding: 20px;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  height: 100px;
  color: white;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 16px;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transform: translate(30%, -30%);
}

.stat-icon {
  font-size: 32px;
  opacity: 0.9;
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
}

.stat-content {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.stat-main {
  flex: 1;
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
  margin-bottom: 4px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  line-height: 1;
}

.stat-help {
  font-size: 16px;
  opacity: 0.7;
  cursor: help;
  transition: opacity 0.3s;
  flex-shrink: 0;
}

.stat-help:hover {
  opacity: 1;
}

.stat-badge {
  display: inline-flex;
  align-items: center;
  font-size: 11px;
  opacity: 0.9;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 8px;
  border-radius: 12px;
}

/* 渐变背景 */
.gradient-bg-blue {
  background: linear-gradient(135deg, #667eea 0%, #1890ff 100%);
}

.gradient-bg-green {
  background: linear-gradient(135deg, #52c41a 0%, #95de64 100%);
}

.gradient-bg-orange {
  background: linear-gradient(135deg, #faad14 0%, #ffc53d 100%);
}

/* 控制卡片 */
.control-card {
  padding: 20px;
  background: linear-gradient(135deg, #8c8c8c 0%, #595959 100%);
  border: 1px solid #d9d9d9;
  height: 100px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.control-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  height: 100%;
  justify-content: center;
}

.control-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.control-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  white-space: nowrap;
}

.control-time {
  font-family: 'Courier New', monospace;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.85);
}

.refresh-btn {
  padding: 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.9);
}

.refresh-btn:hover {
  color: #fff;
}

/* 控制卡片中的输入框样式 */
.control-card :deep(.ant-input-number) {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.control-card :deep(.ant-input-number-input) {
  color: #fff;
  font-weight: 500;
}

.control-card :deep(.ant-input-number:hover) {
  border-color: rgba(255, 255, 255, 0.5);
}

.control-card :deep(.ant-input-number:focus),
.control-card :deep(.ant-input-number-focused) {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.control-card :deep(.ant-input-number-handler) {
  border-color: rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.6);
}

.control-card :deep(.ant-input-number-handler:hover) {
  color: #fff;
}

/* 表格容器 */
.table-container {
  padding: 10px;
  border-radius: 12px;
  position: relative;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.table-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(0, 0, 0, 0.85);
}

.proxy-count {
  font-size: 14px;
  font-weight: 500;
  color: #1890ff;
  background: #e6f7ff;
  padding: 2px 10px;
  border-radius: 12px;
  margin-left: 8px;
}

/* 搜索筛选区域 */
.search-filters-container {
  margin-bottom: 20px;
  padding: 16px 18px;
  background: linear-gradient(135deg, #f8f9fb 0%, #f5f7fa 100%);
  border-radius: 10px;
  border: 1px solid #e8eaed;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.filter-space {
  width: 100%;
}

/* 筛选选择框样式 */
.filter-select :deep(.ant-select-selector) {
  border-radius: 6px !important;
  border: 1px solid #d9d9d9 !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  background: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.filter-select :deep(.ant-select-selector:hover) {
  border-color: #40a9ff !important;
  box-shadow: 0 2px 6px rgba(24, 144, 255, 0.15);
  transform: translateY(-1px);
}

.filter-select :deep(.ant-select-focused .ant-select-selector) {
  border-color: #1890ff !important;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.12) !important;
  transform: translateY(-1px);
}

.filter-select :deep(.ant-select-arrow) {
  color: #1890ff;
  transition: transform 0.3s;
}

.filter-select :deep(.ant-select-open .ant-select-arrow) {
  transform: rotate(180deg);
}

/* 筛选输入框样式 */
.filter-input {
  border-radius: 6px !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.filter-input :deep(.ant-input) {
  border-radius: 6px !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}





/* 新增按钮样式 */
.add-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  box-shadow: 0 2px 4px rgba(24, 144, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 500;
  background: linear-gradient(135deg, #1890ff 0%, #40a9ff 100%);
  border: none;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.4);
  background: linear-gradient(135deg, #40a9ff 0%, #1890ff 100%);
}

.add-btn:active {
  transform: translateY(0);
}

/* 清空按钮样式 */
.clear-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  box-shadow: 0 2px 4px rgba(255, 77, 79, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 500;
}

.clear-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 77, 79, 0.35);
}

.clear-btn:active {
  transform: translateY(0);
}

/* 激活筛选标签 */
.active-tag {
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 12px;
  border: none;
  font-weight: 500;
  background: linear-gradient(135deg, #1890ff 0%, #40a9ff 100%);
  color: #fff;
  box-shadow: 0 2px 4px rgba(24, 144, 255, 0.3);
  animation: pulse-tag 2s ease-in-out infinite;
}

@keyframes pulse-tag {
  0%, 100% {
    box-shadow: 0 2px 4px rgba(24, 144, 255, 0.3);
  }
  50% {
    box-shadow: 0 2px 8px rgba(24, 144, 255, 0.5);
  }
}

/* 新增代理表单样式 */
.add-proxy-form {
  margin-top: 20px;
}

.add-proxy-form :deep(.ant-form-item) {
  margin-bottom: 16px;
}

.add-proxy-form :deep(.ant-form-item-label > label) {
  font-weight: 500;
}

.add-proxy-form :deep(.ant-form-item-required::before) {
  color: #ff4d4f;
}

/* 现代化表格 */
.modern-table :deep(.ant-table) {
  font-size: 13px;
}

.modern-table :deep(.ant-table-thead > tr > th) {
  background: #fafafa;
  color: rgba(0, 0, 0, 0.85);
  font-weight: 600;
  border-bottom: 2px solid #f0f0f0;
  padding: 8px 12px;
  height: 40px;
}

.modern-table :deep(.ant-table-tbody > tr) {
  transition: all 0.3s;
}

.modern-table :deep(.ant-table-tbody > tr:hover) {
  background: #fafafa;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.modern-table :deep(.ant-table-tbody > tr > td) {
  padding: 6px 12px;
  border-bottom: 1px solid #f5f5f5;
  height: 45px;
}

.modern-table :deep(.ant-tag) {
  border-radius: 4px;
  padding: 0px 6px;
  font-size: 12px;
  line-height: 20px;
  margin: 0;
}

/* 特殊样式 */
.ip-code {
  font-family: 'Courier New', monospace;
  background: #f5f5f5;
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 12px;
  line-height: 20px;
}

/* 国家信息样式 */
.country-info {
  display: flex;
  align-items: center;
  gap: 6px;
}

.country-flag {
  font-size: 18px;
  line-height: 1;
}

.country-name {
  font-size: 13px;
  color: rgba(0, 0, 0, 0.65);
  font-weight: 500;
}

/* 地址文本样式 */
.address-text {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.65);
  display: inline-block;
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 认证信息样式 */
.auth-code {
  font-family: 'Courier New', monospace;
  background: #e6f7ff;
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 11px;
  color: #0050b3;
  border: 1px solid #91d5ff;
  line-height: 18px;
}

/* 未知文本样式 */
.unknown-text {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.25);
  font-style: italic;
}

.latency-tag {
  font-weight: 500;
  padding: 0px 6px;
  line-height: 20px;
  font-size: 11px;
}

.alive-tag {
  font-weight: 500;
  padding: 0px 6px;
  line-height: 20px;
  font-size: 11px;
}

/* 操作按钮样式 */
.ant-btn-link {
  color: #1890ff;
  transition: all 0.3s;
}

.ant-btn-link:hover {
  color: #40a9ff;
  transform: translateY(-1px);
}

.ant-btn-link:active {
  color: #096dd9;
}

.time-text {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.65);
}

/* 响应式 */
@media (max-width: 768px) {
  .stat-card {
    min-height: auto;
    padding: 16px;
  }

  .stat-value {
    font-size: 24px;
  }

  .stat-icon {
    font-size: 28px;
  }

  .table-container {
    padding: 16px;
  }

  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .search-filters-container {
    padding: 12px;
  }

  .filter-space {
    gap: 8px;
  }

  .filter-select,
  .filter-input {
    width: 100% !important;
    min-width: 100% !important;
  }

  .filter-select :deep(.ant-select) {
    width: 100% !important;
  }

  .filter-input :deep(.ant-input) {
    width: 100% !important;
  }

  .clear-btn {
    width: 100%;
    justify-content: center;
  }

  .active-tag {
    width: 100%;
    text-align: center;
  }
}

/* Clash 订阅按钮样式 */
.clash-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
}

.clash-btn:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.clash-btn:active {
  transform: translateY(0);
}
</style>
