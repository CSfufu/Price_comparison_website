<!-- src/views/RegisterView.vue -->
<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2 class="register-title">用户注册</h2>
      <el-form :model="form" :rules="rules" ref="registerForm" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" autocomplete="off" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" autocomplete="off" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="form.password" autocomplete="off" />
        </el-form-item>
        <el-form-item label="确认密码" prop="password2">
          <el-input type="password" v-model="form.password2" autocomplete="off" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister">注册</el-button>
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

export default {
  name: 'RegisterView',
  setup() {
    const form = ref({
      username: '',
      email: '',
      password: '',
      password2: '',
    });
    const errorMessage = ref('');
    const router = useRouter();
    const registerForm = ref(null);

    const rules = {
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] },
      ],
      password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
      password2: [
        { required: true, message: '请再次输入密码', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (value !== form.value.password) {
              callback(new Error('两次输入的密码不一致'));
            } else {
              callback();
            }
          },
          trigger: 'blur',
        },
      ],
    };

    const handleRegister = () => {
      registerForm.value.validate(async (valid) => {
        if (valid) {
          try {
            await axios.post('accounts/register/', form.value);
            // 注册成功后，跳转到登录页面
            router.push({ name: 'login' });
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
      handleRegister,
      rules,
      registerForm,
    };
  },
};
</script>

<style>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f5f5f5;
}

.register-card {
  width: 400px;
  padding: 20px;
}

.register-title {
  text-align: center;
  margin-bottom: 20px;
}

.error-alert {
  margin-top: 20px;
}
</style>
