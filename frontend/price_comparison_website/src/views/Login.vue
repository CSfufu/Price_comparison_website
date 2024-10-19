<!-- src/views/Login.vue -->
<template>
  <div>
    <h2>用户登录</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">用户名：</label>
        <input type="text" v-model="form.username" required />
      </div>
      <div>
        <label for="password">密码：</label>
        <input type="password" v-model="form.password" required />
      </div>
      <button type="submit">登录</button>
    </form>
    <div v-if="error" style="color: red;">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script>
import apiClient from '../axios'

export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      error: null
    }
  },
  methods: {
    async login() {
      try {
        const response = await apiClient.post('accounts/login/', this.form)
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        this.$router.push('/')
        alert('登录成功')
      } catch (err) {
        if (err.response && err.response.data) {
          this.error = err.response.data.detail || "登录失败"
        } else {
          this.error = "发生错误，请稍后再试"
        }
      }
    }
  }
}
</script>
