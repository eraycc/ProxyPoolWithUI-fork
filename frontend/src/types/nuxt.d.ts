// Nuxt 3 Auto-imports type declarations
import type { NuxtApp } from '#app'
import type { RuntimeConfig } from 'nuxt/schema'

declare global {
  const useNuxtApp: () => NuxtApp
  const useRuntimeConfig: () => RuntimeConfig
  const useRoute: typeof import('vue-router')['useRoute']
  const useRouter: typeof import('vue-router')['useRouter']
  const navigateTo: typeof import('#app')['navigateTo']
  const onMounted: typeof import('vue')['onMounted']
  const onUnmounted: typeof import('vue')['onUnmounted']
  const ref: typeof import('vue')['ref']
  const computed: typeof import('vue')['computed']
  const watch: typeof import('vue')['watch']
  const defineNuxtPlugin: typeof import('#app')['defineNuxtPlugin']
  const defineNuxtConfig: typeof import('nuxt/config')['defineNuxtConfig']
}

export {}

