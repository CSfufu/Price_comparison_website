<!-- src/App.vue -->
<template>
  <div id="app">
    <nav>
      <router-link to="/">首页</router-link>
      <span v-if="!isAuthenticated">
        <router-link to="/login">登录</router-link>
        <router-link to="/register">注册</router-link>
      </span>
      <span v-else>
        欢迎，{{ username }}！
        <a href="#" @click.prevent="handleLogout">登出</a>
      </span>
    </nav>
    <hr />
    <router-view />
  </div>
</template>

<script>
import axios from './axios';

export default {
  name: 'App',
  data() {
    return {
      username: '',
    };
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token');
    },
  },
  methods: {
    handleLogout() {
      localStorage.removeItem('token');
      this.username = '';
      this.$router.push({ name: 'home' });
    },
    async fetchUserInfo() {
      try {
        const response = await axios.get('user/');
        this.username = response.data.username;
      } catch (error) {
        // 如果获取用户信息失败，可能是 token 无效
        localStorage.removeItem('token');
      }
    },
  },
  created() {
    if (this.isAuthenticated) {
      this.fetchUserInfo();
    }
  },
};
</script>

<style>
/* 添加一些简单的样式 */
nav {
  margin-bottom: 10px;
}

nav a {
  margin-right: 10px;
}
</style>
