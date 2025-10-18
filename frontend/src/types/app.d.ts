// App-specific type declarations

// Extend NuxtApp with custom $http plugin
declare module '#app' {
  interface NuxtApp {
    $http: {
      get: (url: string, params?: any) => Promise<any>
      post: (url: string, data?: any, params?: any) => Promise<any>
    }
  }
}

declare module 'vue' {
  interface ComponentCustomProperties {
    $http: {
      get: (url: string, params?: any) => Promise<any>
      post: (url: string, data?: any, params?: any) => Promise<any>
    }
  }
}

export {}

