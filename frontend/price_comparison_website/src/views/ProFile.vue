<!-- src/views/ProFile.vue -->
<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <div class="card-header">
        <h2>{{ userInfo.username }} の 个人信息</h2>
      </div>
      <div class="card-content">
        <el-form :model="userInfo" label-width="100px">
          <el-form-item label="用户名">
            <el-input v-model="userInfo.username" disabled></el-input>
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="userInfo.email" disabled></el-input>
          </el-form-item>
          <!-- 添加更多用户信息 -->
        </el-form>
      </div>
      <!-- 可选的编辑按钮 -->
      <!--
      <div class="card-actions">
        <el-button type="primary" @click="editProfile">编辑信息</el-button>
      </div>
      -->
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import auth from '../store/auth';

// 路由实例
const router = useRouter();

// 从 store 获取用户信息
const { state, fetchUserInfo } = auth;

const isAuthenticated = computed(() => state.isAuthenticated);

const userInfo = ref({
  username: '',
  email: '',
  // 其他用户信息字段
});

onMounted(async () => {
  if (!isAuthenticated.value) {
    // 未登录，跳转到登录页面
    router.push({ name: 'login' });
  } else {
    if (!state.username) {
      // 如果状态中没有用户信息，获取用户信息
      await fetchUserInfo();
    }
    // 将获取到的用户信息赋值给 userInfo
    userInfo.value = {
      username: state.username,
      email: state.email,
      // 其他用户信息字段
    };
  }
});

// 可选的编辑功能
/*
const editProfile = () => {
  // 跳转到编辑个人信息页面，或者开启编辑模式
};
*/
</script>

<style>
.profile-container {
  max-width: 600px;
  margin: 40px auto;
}

.profile-card {
  padding: 20px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin-top: 10px;
}

.card-content {
  margin-top: 20px;
}

.card-actions {
  text-align: center;
  margin-top: 20px;
}
</style>
