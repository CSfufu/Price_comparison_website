import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    // 让 Vite 监听所有网络接口，外部也能访问
    host: '0.0.0.0', // 默认为 localhost, 改为 0.0.0.0 以接受来自外部的连接
    port: 5173, // 默认端口
    strictPort: true, // 强制 Vite 使用指定端口
  }
})
