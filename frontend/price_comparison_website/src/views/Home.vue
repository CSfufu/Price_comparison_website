<!-- src/views/Home.vue -->
<template>
  <div>
    <h2>欢迎来到商品价格比较网站</h2>
    <p v-if="user">你好，{{ user.username }}！</p>
    <p v-else>请登录或注册以获取更多功能。</p>
  </div>
</template>

<script>
import apiClient from '../axios'

export default {
  data() {
    return {
      user: null
    }
  },
  async created() {
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        // 假设有一个获取当前用户信息的 API
        const response = await apiClient.get('accounts/me/')  // 需要在后端实现
        this.user = response.data
      } catch (err) {
        // 令牌可能已过期或无效，清除
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
    }
  }
}
</script>
