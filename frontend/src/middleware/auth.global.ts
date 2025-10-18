// 全局路由守卫 - 检查登录状态
export default defineNuxtRouteMiddleware((to, from) => {
  // 在客户端运行
  if (process.client) {
    const token = localStorage.getItem('token')
    const isLoginPage = to.path === '/login'
    
    // 如果没有token且不是登录页，跳转到登录页
    if (!token && !isLoginPage) {
      return navigateTo('/login')
    }
    
    // 如果有token且是登录页，跳转到首页
    if (token && isLoginPage) {
      return navigateTo('/')
    }
  }
})

