<!-- src/views/LoginView.vue -->
<template>
  <div>
    <h2>用户登录</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">用户名：</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">密码：</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">登录</button>
    </form>
    <div v-if="errorMessage" style="color: red;">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('accounts/login/', {
          "username": this.username,
          "password": this.password,
        });
        // 假设后端返回 token
        const { token } = response.data;
        localStorage.setItem('token', token);
        this.$router.push({ name: 'home' });
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.detail || '登录失败';
          console.log(error)
        } else {
          this.errorMessage = '网络错误';
        }
      }
    },
  },
};
</script>
