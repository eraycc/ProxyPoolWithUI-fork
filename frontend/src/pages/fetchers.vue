<template>
  <div class="fetchers-page fade-in">
    <!-- 控制区域 -->
    <a-row :gutter="[16, 16]" class="control-row">
      <a-col :xs="24" :sm="12" :md="8">
        <div class="control-card enhanced-card slide-in-up">
          <div class="control-header">
            <SyncOutlined :spin="autoupdate" />
            <span>自动刷新</span>
          </div>
          <a-switch v-model:checked="autoupdate" size="large" />
          <div class="control-info">
            <ClockCircleOutlined />
            <span>{{ lastupdate }}</span>
          </div>
        </div>
            </a-col>

      <a-col :xs="24" :sm="12" :md="8">
        <div class="control-card enhanced-card slide-in-up" style="animation-delay: 0.1s">
          <div class="control-header">
            <ClearOutlined />
            <span>数据管理</span>
          </div>
          <a-button type="primary" danger @click="clearStatus" :loading="clearing" size="large">
            <DeleteOutlined />
                            清空统计信息
                        </a-button>
          <a-tooltip title="清空'总共爬取代理数量'等，已经爬取到的代理不会删除">
            <QuestionCircleOutlined class="help-icon" />
                        </a-tooltip>
                    </div>
      </a-col>

      <a-col :xs="24" :sm="24" :md="8">
        <div class="stats-card enhanced-card slide-in-up" style="animation-delay: 0.2s">
          <div class="stats-item">
            <span class="stats-label">爬取器总数</span>
            <span class="stats-value">{{ fetchers.length }}</span>
          </div>
          <div class="stats-item">
            <span class="stats-label">已启用</span>
            <span class="stats-value success">{{ enabledCount }}</span>
          </div>
          <div class="stats-item">
            <span class="stats-label">已禁用</span>
            <span class="stats-value disabled">{{ disabledCount }}</span>
          </div>
        </div>
            </a-col>
        </a-row>

    <!-- 爬取器卡片网格 -->
    <div class="fetchers-grid">
      <div
        v-for="(fetcher, index) in fetchers"
        :key="fetcher.name"
        class="fetcher-card enhanced-card scale-in hover-lift"
        :style="{ animationDelay: `${index * 0.05}s` }"
      >
        <!-- 状态指示器 -->
        <div class="fetcher-status" :class="{ active: fetcher.enable }">
          <span class="status-dot"></span>
          <span class="status-text">{{ fetcher.enable ? '启用中' : '已禁用' }}</span>
        </div>

        <!-- 爬取器名称 -->
        <div class="fetcher-header">
          <h3 class="fetcher-name">
            <GlobalOutlined />
            {{ fetcher.name }}
          </h3>
          <a-switch
            :checked="fetcher.enable"
            @change="enableChange(fetcher)"
            :loading="fetcher.loading"
          />
        </div>

        <!-- 统计数据 - 紧凑布局 -->
        <div class="fetcher-stats">
          <div class="stat-row">
            <div class="stat-item compact">
              <CheckCircleOutlined class="stat-icon success" />
              <span class="stat-label">可用</span>
              <span class="stat-number">{{ fetcher.validated_cnt || 0 }}</span>
            </div>
            <div class="stat-item compact">
              <DatabaseOutlined class="stat-icon info" />
              <span class="stat-label">库存</span>
              <span class="stat-number">{{ fetcher.in_db_cnt || 0 }}</span>
            </div>
          </div>
          <div class="stat-row">
            <div class="stat-item compact">
              <LineChartOutlined class="stat-icon primary" />
              <span class="stat-label">总数</span>
              <span class="stat-number">{{ fetcher.sum_proxies_cnt || 0 }}</span>
            </div>
            <div class="stat-item compact">
              <RiseOutlined class="stat-icon warning" />
              <span class="stat-label">本次</span>
              <span class="stat-number">{{ fetcher.last_proxies_cnt || 0 }}</span>
            </div>
          </div>
        </div>

        <!-- 时间信息 -->
        <div class="fetcher-footer">
          <div class="footer-item">
            <ClockCircleOutlined />
            <span v-if="fetcher.last_fetch_date">
              {{ moment(fetcher.last_fetch_date).fromNow() }}
                        </span>
            <span v-else class="no-data">暂无数据</span>
          </div>
          <div class="footer-time" v-if="fetcher.last_fetch_date">
            {{ moment(fetcher.last_fetch_date).format('YYYY-MM-DD HH:mm') }}
          </div>
        </div>

        <!-- 进度条（可选） -->
        <div class="fetcher-progress" v-if="fetcher.sum_proxies_cnt > 0">
          <a-progress
            :percent="Math.min(100, (fetcher.validated_cnt / fetcher.sum_proxies_cnt) * 100)"
            :show-info="false"
            :stroke-color="{
              '0%': '#108ee9',
              '100%': '#87d068'
            }"
            size="small"
          />
        </div>
      </div>
    </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import {
  QuestionCircleOutlined,
  SyncOutlined,
  ClockCircleOutlined,
  ClearOutlined,
  DeleteOutlined,
  GlobalOutlined,
  CheckCircleOutlined,
  DatabaseOutlined,
  LineChartOutlined,
  RiseOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import moment from 'moment'

// Nuxt auto-imports
const { $http } = useNuxtApp() as any

const fetchers = ref<any[]>([])
const autoupdate = ref(true)
const lastupdate = ref('')
const clearing = ref(false)
let handle: NodeJS.Timeout | null = null

// 计算启用/禁用数量
const enabledCount = computed(() => fetchers.value.filter(f => f.enable).length)
const disabledCount = computed(() => fetchers.value.filter(f => !f.enable).length)

const update = async () => {
  try {
    const data = await $http.get('/fetchers_status')
    fetchers.value = data.fetchers.map((f: any) => ({ ...f, loading: false }))
    lastupdate.value = moment().format('HH:mm:ss')
  } catch (error) {
    console.error('更新数据失败:', error)
    message.error('更新数据失败')
  }
}

const clearStatus = async () => {
  clearing.value = true
  try {
    await $http.get('/clear_fetchers_status')
    message.success('清空成功')
    await update()
  } catch (error) {
    message.error('清空失败')
  } finally {
    clearing.value = false
  }
}

const enableChange = async (fetcher: any) => {
  fetcher.loading = true
  try {
    const enable = fetcher.enable ? '0' : '1'
    await $http.get('/fetcher_enable', { name: fetcher.name, enable })
    message.success(`${fetcher.name} ${fetcher.enable ? '已禁用' : '已启用'}`)
    await update()
  } catch (error) {
    message.error('修改失败')
    fetcher.loading = false
  }
}

onMounted(() => {
  handle = setInterval(() => {
    if (autoupdate.value) {
      update()
    }
  }, 2000)
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
.fetchers-page {
  padding: 0;
}

/* 控制区域 */
.control-row {
  margin-bottom: 24px;
}

.control-card {
  padding: 20px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 130px;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.control-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
}

.control-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.help-icon {
  margin-top: 8px;
  opacity: 0.6;
  cursor: help;
}

/* 统计卡片 */
.stats-card {
  padding: 20px;
  border-radius: 12px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 130px;
}

.stats-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.stats-label {
  font-size: 13px;
  color: rgba(0, 0, 0, 0.65);
}

.stats-value {
  font-size: 28px;
  font-weight: bold;
  color: #1890ff;
}

.stats-value.success {
  color: #52c41a;
}

.stats-value.disabled {
  color: rgba(0, 0, 0, 0.25);
}

/* 爬取器卡片网格 */
.fetchers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.fetcher-card {
  padding: 16px;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.fetcher-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #1890ff, #52c41a);
  transform: scaleX(0);
  transition: transform 0.3s;
}

.fetcher-card:hover::before {
  transform: scaleX(1);
}

/* 状态指示器 */
.fetcher-status {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.04);
  font-size: 12px;
}

.fetcher-status.active {
  background: rgba(82, 196, 26, 0.1);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.25);
  animation: pulse 2s ease-in-out infinite;
}

.fetcher-status.active .status-dot {
  background: #52c41a;
}

.status-text {
  color: rgba(0, 0, 0, 0.65);
  font-weight: 500;
}

.fetcher-status.active .status-text {
  color: #52c41a;
}

/* 爬取器头部 */
.fetcher-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-right: 80px;
}

.fetcher-name {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  gap: 6px;
}

/* 统计数据 */
.fetcher-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.stat-row {
  display: flex;
  gap: 8px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 6px;
  transition: all 0.3s;
  flex: 1;
}

.stat-item.compact {
  justify-content: flex-start;
}

.stat-item:hover {
  background: rgba(0, 0, 0, 0.04);
}

.stat-icon {
  font-size: 14px;
  flex-shrink: 0;
}

.stat-icon.success {
  color: #52c41a;
}

.stat-icon.info {
  color: #1890ff;
}

.stat-icon.primary {
  color: #667eea;
}

.stat-icon.warning {
  color: #faad14;
}

.stat-label {
  font-size: 11px;
  color: rgba(0, 0, 0, 0.45);
  white-space: nowrap;
}

.stat-number {
  font-size: 14px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
  margin-left: auto;
}

/* 底部信息 */
.fetcher-footer {
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.footer-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.65);
}

.footer-time {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
  font-family: 'Courier New', monospace;
}

.no-data {
  color: rgba(0, 0, 0, 0.25);
}

/* 进度条 */
.fetcher-progress {
  margin-top: 12px;
}

/* 响应式 */
@media (max-width: 768px) {
  .fetchers-grid {
    grid-template-columns: 1fr;
  }

  .control-card {
    height: auto;
    min-height: 110px;
    padding: 16px;
  }

  .stats-card {
    height: auto;
    flex-direction: column;
    gap: 12px;
    padding: 16px;
  }

  .fetcher-stats .stat-row {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .fetcher-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding-right: 0;
  }

  .fetcher-status {
    position: static;
    margin-bottom: 12px;
  }
}
</style>
