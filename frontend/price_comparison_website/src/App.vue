<!-- src/App.vue -->
<template>
  <div id="app">
    <el-header>
      <el-row type="flex" justify="space-between" align="middle">
        <el-col>
          <router-link to="/">
            <el-button type="text">首页</el-button>
          </router-link>
        </el-col>
        <el-col>
          <span v-if="!isAuthenticated">
            <router-link to="/login">
              <el-button type="text">登录</el-button>
            </router-link>
            <router-link to="/register">
              <el-button type="text">注册</el-button>
            </router-link>
          </span>
          <span v-else>
            <el-dropdown>
              <span class="el-dropdown-link">
                欢迎，{{ username }}！<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="handleLogout">登出</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </span>
        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </div>
</template>

<script>
import axios from './axios';

export default {
  name: 'App',
  data() {
    return {
      username: '',
      token: localStorage.getItem('token'),
    };
  },
  computed: {
    isAuthenticated() {
      return !!this.token;
    },
  },
  methods: {
    handleLogout() {
      localStorage.removeItem('token');
      this.token = null;
      this.username = '';
      this.$router.push({ name: 'home' });
    },
    async fetchUserInfo() {
      try {
        const response = await axios.get('user/');
        this.username = response.data.username;
      } catch (error) {
        localStorage.removeItem('token');
        this.token = null;
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
/* 全局样式可以在此处调整 */
body {
  margin: 0;
  font-family: 'Helvetica Neue', Arial, sans-serif;
}
</style>
