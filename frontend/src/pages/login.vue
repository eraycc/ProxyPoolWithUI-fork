<template>
  <div class="login-container">
    <!-- 动态背景 -->
    <div class="login-background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="particles">
        <div class="particle" v-for="i in 80" :key="i" :style="getParticleStyle(i)"></div>
      </div>
      <div class="grid-overlay"></div>
    </div>
    
    <!-- 登录卡片 -->
    <div class="login-card" :class="{ 'card-shake': loginError }">
      <!-- 装饰性元素 -->
      <div class="card-decoration">
        <div class="decoration-circle circle-1"></div>
        <div class="decoration-circle circle-2"></div>
        <div class="decoration-line"></div>
      </div>
      
      <div class="login-header">
        <div class="logo-section">
          <div class="logo-container">
            <CloudServerOutlined class="logo-icon" />
            <div class="logo-glow"></div>
          </div>
          <h1 class="title">代理池管理系统</h1>
        </div>
        <p class="subtitle">ProxyPool Management System</p>
        <div class="status-indicator">
          <span class="status-text">
            {{ isOnline ? '系统运行正常' : '正在连接服务器...' }}
          </span>
          <span class="status-icon">{{ isOnline ? '✓' : '⏳' }}</span>
        </div>
      </div>
      
      <a-form
        :model="formState"
        name="login"
        @finish="handleLogin"
        class="login-form"
        :rules="rules"
      >
        <a-form-item name="username" class="form-item">
          <a-input
            v-model:value="formState.username"
            size="large"
            placeholder="请输入用户名"
            :prefix="h(UserOutlined, { class: 'input-icon' })"
            autocomplete="username"
            @focus="onInputFocus"
            @blur="onInputBlur"
            class="custom-input"
          >
          </a-input>
        </a-form-item>

        <a-form-item name="password" class="form-item">
          <a-input-password
            v-model:value="formState.password"
            size="large"
            placeholder="请输入密码"
            :prefix="h(LockOutlined, { class: 'input-icon' })"
            autocomplete="current-password"
            @focus="onInputFocus"
            @blur="onInputBlur"
            class="custom-input"
          >
          </a-input-password>
        </a-form-item>

        <a-form-item class="form-item remember-item">
          <a-checkbox v-model:checked="formState.remember" class="custom-checkbox">
            记住我
          </a-checkbox>
          <a class="forgot-password" @click="showForgotPassword">忘记密码？</a>
        </a-form-item>

        <a-form-item class="form-item">
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            :loading="loading"
            class="login-button"
            block
          >
            <template v-if="!loading">
              <LoginOutlined class="button-icon" />
              立即登录
            </template>
            <template v-else>
              <LoadingOutlined class="button-icon" />
              登录中...
            </template>
          </a-button>
        </a-form-item>
      </a-form>

      <div class="login-footer">
        <a-divider class="divider">
          <span class="divider-text">系统特性</span>
        </a-divider>
        <div class="features-grid">
          <div class="feature-item" v-for="feature in features" :key="feature.key">
            <component :is="feature.icon" class="feature-icon" />
            <span class="feature-text">{{ feature.text }}</span>
          </div>
        </div>
        
      </div>
    </div>

    <!-- 底部信息 -->
    <div class="copyright">
      <div class="copyright-content">
        <span>© 2025 ProxyPool Management System</span>
        <div class="social-links">
          <a href="#" class="social-link">GitHub</a>
          <a href="#" class="social-link">文档</a>
          <a href="#" class="social-link">支持</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 禁用默认布局
// @ts-ignore
definePageMeta({
  layout: false
})
import { ref, reactive, h, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { message, Modal } from 'ant-design-vue'
import {
  UserOutlined,
  LockOutlined,
  LoginOutlined,
  CloudServerOutlined,
  SafetyOutlined,
  ClockCircleOutlined,
  InfoCircleOutlined,
  LoadingOutlined,
  ThunderboltOutlined,
  GlobalOutlined,
  RocketOutlined
} from '@ant-design/icons-vue'

const { $http } = useNuxtApp() as any
const router = useRouter()

const formState = reactive({
  username: '',
  password: '',
  remember: true
})

const loading = ref(false)
const loginError = ref(false)
const isOnline = ref(true)
const inputFocused = ref(false)

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

// 系统特性列表
const features = ref([
  { key: 'automation', icon: SafetyOutlined, text: '自动采集' },
  { key: 'validation', icon: ThunderboltOutlined, text: '智能验证' },
  { key: 'management', icon: GlobalOutlined, text: '统一管理' },
  { key: 'monitoring', icon: RocketOutlined, text: '实时监控' }
])

// 粒子动画样式
const getParticleStyle = (index: number) => {
  const random = (min: number, max: number) => Math.random() * (max - min) + min
  return {
    left: `${random(0, 100)}%`,
    top: `${random(0, 100)}%`,
    width: `${random(2, 8)}px`,
    height: `${random(2, 8)}px`,
    animationDuration: `${random(20, 40)}s`,
    animationDelay: `${random(0, 10)}s`,
    opacity: random(0.3, 0.8)
  }
}

// 输入框焦点事件
const onInputFocus = () => {
  inputFocused.value = true
}

const onInputBlur = () => {
  inputFocused.value = false
}

// 忘记密码
const showForgotPassword = () => {
  Modal.info({
    title: '忘记密码',
    content: '请联系系统管理员重置密码，或使用默认账户登录。',
    okText: '知道了'
  })
}

// 检查系统状态
const checkSystemStatus = async () => {
  try {
    const response = await $http.get('/auth/ping')
    isOnline.value = response.success
  } catch (error) {
    isOnline.value = false
  }
}

const handleLogin = async () => {
  loading.value = true
  loginError.value = false
  
  try {
    const response = await $http.post('/auth/login', {
      username: formState.username,
      password: formState.password
    })
    
    if (response.success) {
      // 存储token
      localStorage.setItem('token', response.token)
      
      // 存储用户信息
      localStorage.setItem('user', JSON.stringify(response.user))
      
      // 如果选择记住我，存储到localStorage
      if (formState.remember) {
        localStorage.setItem('remember', 'true')
      } else {
        localStorage.removeItem('remember')
      }
      
      message.success({
        content: '登录成功！正在跳转...',
        duration: 2
      })
      
      // 跳转到首页
      setTimeout(() => {
        router.push('/')
      }, 800)
    }
  } catch (error: any) {
    console.error('登录失败:', error)
    loginError.value = true
    message.error({
      content: error.message || '登录失败，请检查用户名和密码',
      duration: 3
    })
    
    // 重置错误状态
    setTimeout(() => {
      loginError.value = false
    }, 1000)
  } finally {
    loading.value = false
  }
}

// 组件挂载时检查是否已登录
onMounted(() => {
  const token = localStorage.getItem('token')
  if (token) {
    // 已登录，跳转到首页
    router.push('/')
  }
  
  // 检查系统状态
  checkSystemStatus()
  
  // 定期检查系统状态
  setInterval(checkSystemStatus, 30000)
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

/* 渐变球体 */
.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  animation: orbFloat 20s ease-in-out infinite;
}

.orb-1 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.3) 0%, transparent 70%);
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(118, 75, 162, 0.3) 0%, transparent 70%);
  top: 60%;
  right: 15%;
  animation-delay: -7s;
}

.orb-3 {
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(240, 147, 251, 0.3) 0%, transparent 70%);
  bottom: 20%;
  left: 20%;
  animation-delay: -14s;
}

@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}

/* 网格覆盖层 */
.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: float linear infinite;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

@keyframes float {
  0% {
    transform: translateY(100vh) rotate(0deg) scale(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
    transform: translateY(90vh) rotate(36deg) scale(1);
  }
  90% {
    opacity: 1;
    transform: translateY(10vh) rotate(324deg) scale(1);
  }
  100% {
    transform: translateY(-10vh) rotate(360deg) scale(0);
    opacity: 0;
  }
}

.login-card {
  width: 450px;
  padding: 50px 45px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 
    0 25px 80px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 1;
  animation: slideIn 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  transition: all 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 35px 100px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.3);
}

.login-card.card-shake {
  animation: shake 0.5s ease-in-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-80px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

/* 卡片装饰元素 */
.card-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
  border-radius: 24px;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  animation: decorationFloat 8s ease-in-out infinite;
}

.circle-1 {
  width: 80px;
  height: 80px;
  top: -40px;
  right: -40px;
  animation-delay: 0s;
}

.circle-2 {
  width: 60px;
  height: 60px;
  bottom: -30px;
  left: -30px;
  animation-delay: -4s;
}

.decoration-line {
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, rgba(102, 126, 234, 0.3) 50%, transparent 100%);
  animation: lineGlow 3s ease-in-out infinite;
}

@keyframes decorationFloat {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(10px, -10px) rotate(180deg); }
}

@keyframes lineGlow {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.8; }
}

.login-header {
  text-align: center;
  margin-bottom: 45px;
  position: relative;
}

.logo-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 12px;
}

.logo-container {
  position: relative;
  display: inline-block;
}

.logo-icon {
  font-size: 48px;
  color: #667eea;
  animation: logoFloat 3s ease-in-out infinite;
  position: relative;
  z-index: 2;
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 60px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  animation: glowPulse 2s ease-in-out infinite;
}

@keyframes logoFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-8px) rotate(5deg); }
}

@keyframes glowPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.3; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.6; }
}

.title {
  margin: 0;
  font-size: 32px;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  animation: titleGlow 4s ease-in-out infinite;
}

@keyframes titleGlow {
  0%, 100% { filter: brightness(1); }
  50% { filter: brightness(1.1); }
}

.subtitle {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.6);
  font-weight: 500;
  letter-spacing: 1.2px;
  text-transform: uppercase;
}

/* 状态指示器 */
.status-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 12px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  font-size: 12px;
}

.status-indicator:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.status-text {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.7);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

.status-icon {
  font-size: 12px;
  font-weight: bold;
  color: #52c41a;
  animation: statusIconBounce 2s ease-in-out infinite;
}

.status-dot:not(.online) + .status-text .status-icon {
  color: #ff4d4f;
  animation: statusIconSpin 1s linear infinite;
}

@keyframes statusIconBounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes statusIconSpin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.login-form {
  margin-top: 35px;
}

.form-item {
  margin-bottom: 28px;
}

.custom-input :deep(.ant-input-affix-wrapper),
.custom-input :deep(.ant-input) {
  border-radius: 12px;
  padding: 14px 18px;
  font-size: 15px;
  border: 2px solid #e8e8e8;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
}

.custom-input :deep(.ant-input-affix-wrapper:focus),
.custom-input :deep(.ant-input-affix-wrapper-focused),
.custom-input :deep(.ant-input:focus) {
  border-color: #667eea;
  box-shadow: 
    0 0 0 4px rgba(102, 126, 234, 0.1),
    0 4px 20px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.custom-input :deep(.ant-input-affix-wrapper:hover),
.custom-input :deep(.ant-input:hover) {
  border-color: #667eea;
  transform: translateY(-1px);
}

.input-icon {
  color: #667eea;
  font-size: 18px;
  transition: all 0.3s;
}

.custom-input:focus-within .input-icon {
  color: #764ba2;
  transform: scale(1.1);
}

.remember-item {
  margin-bottom: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.custom-checkbox :deep(.ant-checkbox-wrapper) {
  color: rgba(0, 0, 0, 0.65);
  font-size: 14px;
  font-weight: 500;
}

.custom-checkbox :deep(.ant-checkbox-checked .ant-checkbox-inner) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
}

.forgot-password {
  color: #667eea;
  font-size: 13px;
  text-decoration: none;
  transition: all 0.3s;
  font-weight: 500;
}

.forgot-password:hover {
  color: #764ba2;
  text-decoration: underline;
}

.login-button {
  height: 52px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  background-size: 200% 200%;
  border: none;
  box-shadow: 
    0 6px 20px rgba(102, 126, 234, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2);
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  overflow: hidden;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.login-button:hover {
  transform: translateY(-3px);
  box-shadow: 
    0 10px 30px rgba(102, 126, 234, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.3);
  background-position: 100% 0;
}

.login-button:hover::before {
  left: 100%;
}

.login-button:active {
  transform: translateY(-1px);
}

.button-icon {
  font-size: 18px;
  margin-right: 8px;
  transition: all 0.3s;
}

.login-button:hover .button-icon {
  transform: scale(1.1);
}

.login-footer {
  margin-top: 40px;
}

.divider {
  margin: 28px 0 24px 0;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.5);
}

.divider-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 600;
  padding: 0 16px;
}

.features-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 12px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.7);
  transition: all 0.3s;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.feature-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.2);
}

.feature-icon {
  font-size: 18px;
  color: #667eea;
  transition: all 0.3s;
}

.feature-item:hover .feature-icon {
  transform: scale(1.1);
  color: #764ba2;
}

.feature-text {
  font-weight: 500;
}


.copyright {
  position: absolute;
  bottom: 24px;
  left: 0;
  right: 0;
  z-index: 1;
}

.copyright-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
}

.social-links {
  display: flex;
  gap: 20px;
}

.social-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s;
  padding: 4px 8px;
  border-radius: 6px;
}

.social-link:hover {
  color: rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-card {
    width: 90%;
    max-width: 400px;
    padding: 40px 32px;
    margin: 20px;
  }

  .title {
    font-size: 28px;
  }

  .subtitle {
    font-size: 13px;
  }

  .logo-icon {
    font-size: 42px;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .copyright-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }

  .social-links {
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .login-card {
    width: 95%;
    padding: 32px 24px;
  }

  .title {
    font-size: 24px;
  }

  .logo-icon {
    font-size: 36px;
  }

  .form-item {
    margin-bottom: 24px;
  }

  .remember-item {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>

