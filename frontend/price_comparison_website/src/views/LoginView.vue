<!-- src/views/LoginView.vue -->
<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="login-title">用户登录</h2>
      <el-form :model="form" :rules="rules" ref="loginForm" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" autocomplete="off" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="form.password" autocomplete="off" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin">登录</el-button>
        </el-form-item>
      </el-form>
      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        show-icon
        class="error-alert"
      ></el-alert>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from '../axios';
import { useRouter } from 'vue-router';
import auth from '../store/auth';

export default {
  name: 'LoginView',
  setup() {
    const form = ref({
      username: '',
      password: '',
    });
    const errorMessage = ref('');
    const router = useRouter();
    const loginForm = ref(null);
    const { login } = auth;

    const rules = {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
    };

    const handleLogin = () => {
      loginForm.value.validate(async (valid) => {
        if (valid) {
          try {
            const response = await axios.post('accounts/login/', form.value);
            const { access, refresh } = response.data;
            login(access, refresh); // 传递 access 和 refresh token
            router.push({ name: 'home' });
          } catch (error) {
            if (error.response && error.response.data) {
              const data = error.response.data;
              let errors = [];
              for (let key in data) {
                if (Array.isArray(data[key])) {
                  errors = errors.concat(data[key]);
                } else if (typeof data[key] === 'string') {
                  errors.push(data[key]);
                }
              }
              errorMessage.value = errors.join('；');
            } else {
              errorMessage.value = '网络错误';
            }
          }
        } else {
          console.log('表单验证失败');
        }
      });
    };

    return {
      form,
      errorMessage,
      handleLogin,
      rules,
      loginForm,
    };
  },
};
</script>

<style>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f5f5f5;
}

.login-card {
  width: 400px;
  padding: 20px;
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
}

.error-alert {
  margin-top: 20px;
}
</style>
