<!-- src/views/Register.vue -->
<template>
  <div>
    <h2>用户注册</h2>
    <form @submit.prevent="register">
      <div>
        <label for="username">用户名：</label>
        <input type="text" v-model="form.username" required />
      </div>
      <div>
        <label for="email">邮箱：</label>
        <input type="email" v-model="form.email" required />
      </div>
      <div>
        <label for="password">密码：</label>
        <input type="password" v-model="form.password" required />
      </div>
      <div>
        <label for="password2">确认密码：</label>
        <input type="password" v-model="form.password2" required />
      </div>
      <button type="submit">注册</button>
    </form>
    <div v-if="error" style="color: red;">
      <p v-for="(msg, key) in error" :key="key">{{ key }}: {{ msg }}</p>
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
        email: '',
        password: '',
        password2: ''
      },
      error: null
    }
  },
  methods: {
    async register() {
      try {
        const response = await apiClient.post('accounts/register/', this.form)
        // 注册成功后自动登录
        const loginResponse = await apiClient.post('accounts/login/', {
          username: this.form.username,
          password: this.form.password
        })
        localStorage.setItem('access_token', loginResponse.data.access)
        localStorage.setItem('refresh_token', loginResponse.data.refresh)
        this.$router.push('/')
        alert('注册成功，已自动登录')
      } catch (err) {
        if (err.response && err.response.data) {
          this.error = err.response.data
        } else {
          this.error = { detail: "发生错误，请稍后再试" }
        }
      }
    }
  }
}
</script>
