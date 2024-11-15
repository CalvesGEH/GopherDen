// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },

  build: {
    transpile: ['vuetify'],
  },

  modules: [
    '@sidebase/nuxt-auth',
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
  ],

  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },

  nitro: {
    devProxy: {
        '/api': {
            target: 'http://localhost:7877/api',
            changeOrigin: true
        }
    }
  },

  app: {
    pageTransition: { name: 'page', mode: 'out-in' }
  },

  auth: {
    sessionRefresh: {
      enableOnWindowFocus: true,
      enablePeriodically: 60000,
    },
    baseURL: '/api/auth/',
    provider: {
      type: 'refresh',
      pages: {
        login: '/login'
      },
      session: { 
        dataType: {
          id: 'string',
          username: 'string',
          email: 'string',
          admin: 'boolean',
        },
      },
      endpoints: {
        signIn: { path: '/token', method: 'post'} ,
        signUp: { path: '/register', method: 'post' },
        signOut: { path: '/logout', method: 'post' },
        getSession: { path: '/get-session', method: 'get' },
        refresh: { path: '/refresh', method: 'post' },
      },
      token: { 
        signInResponseTokenPointer: '/access_token',
        type: 'Bearer',
        cookieName: 'gopherden.access_token',
      },
      refreshToken: {
        signInResponseRefreshTokenPointer: '/access_token',
        refreshRequestTokenPointer: '/access_token',
        cookieName: 'gopherden.access_token',
      },
    },
  },

})
