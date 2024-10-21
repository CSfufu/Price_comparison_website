<!-- src/views/RegisterView.vue -->
<template>
  <div>
    <h2>用户注册</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="username">用户名：</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="email">邮箱：</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">密码：</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div>
        <label for="password2">确认密码：</label>
        <input type="password" id="password2" v-model="password2" required />
      </div>
      <button type="submit">注册</button>
    </form>
    <div v-if="errorMessage" style="color: red;">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'RegisterView',
  data() {
    return {
      "username": '',
      "email": '',
      "password": '',
      "password2": '',
      "errorMessage": '',
    };
  },
  methods: {
    async handleRegister() {
      if (this.password !== this.password2) {
        this.errorMessage = '密码不匹配';
        return;
      }

      try {
        const response = await axios.post('accounts/register/', {
          "username": this.username,
          "email": this.email,
          "password": this.password,
          "password2": this.password2,
        });
        // 假设后端返回用户信息和 token
        const { token } = response.data;
        localStorage.setItem('token', token);
        this.$router.push({ name: 'home' });
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.detail || '注册失败';
          console.log(error)
        } else {
          this.errorMessage = '网络错误';
        }
      }
    },
  },
};
</script>
