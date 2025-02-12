<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <el-header style="background-color: #fff; padding: 0 50px;">
      <el-row type="flex" justify="space-between" align="middle">
        <!-- 左侧：Logo -->
        <el-col :span="4">
          <router-link to="/" class="logo">
            <img src="./assets/logo.jpg" alt="Logo" height="40" />
          </router-link>
        </el-col>
        <!-- 中间：导航菜单 -->
        <el-col :span="16">
          <el-menu mode="horizontal" :default-active="$route.path" class="el-menu-demo" background-color="transparent">
            <el-menu-item index="/">
              <router-link to="/">首页</router-link>
            </el-menu-item>
            <el-menu-item index="/about">
              <router-link to="/about">关于我</router-link>
            </el-menu-item>
            <el-menu-item index="/services">
              <router-link to="/services">提供服务</router-link>
            </el-menu-item>
            <el-menu-item index="/search">
              <router-link to="/search">搜索</router-link>
            </el-menu-item>
            <el-menu-item index="/history">
              <router-link to="/history">搜索历史</router-link>
            </el-menu-item>
            <el-menu-item index="/price_history">
              <router-link to="/price_history">历史价格查询</router-link>
            </el-menu-item>
            <el-menu-item index="/alert">
              <router-link to="/alert">降价提醒</router-link>
            </el-menu-item>
          </el-menu>
        </el-col>
        <!-- 右侧：用户操作 -->
        <el-col :span="4" class="nav-buttons">
          <span v-if="!isAuthenticated">
            <router-link to="/login">
              <el-button type="primary" round>登录</el-button>
            </router-link>
            <router-link to="/register">
              <el-button type="success" round>注册</el-button>
            </router-link>
          </span>
          <span v-else>
            <el-dropdown>
              <span class="el-dropdown-link">
                <el-avatar icon="el-icon-user" size="small"></el-avatar>
                {{ username }} <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>
                    <router-link to="/profile">个人中心</router-link>
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">登出</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </span>
        </el-col>
      </el-row>
    </el-header>

    <!-- 主体内容区域 -->
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="220px" v-if="!isMobile" class="custom-aside">
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical-demo"
          background-color="#001529"
          text-color="#fff"
          active-text-color="#ffd04b"
          router
        >
          <el-submenu index="1">
            <template #title>
              <i class="el-icon-s-operation"></i>
              <span>功能菜单</span>
            </template>
            <el-menu-item index="/search">
              <i class="el-icon-s-data"></i>
              <span>实时比价</span>
            </el-menu-item>
            <el-menu-item index="/history">
              <i class="el-icon-s-promotion"></i>
              <span>搜索历史</span>
            </el-menu-item>
            <el-menu-item index="/price_history">
              <i class="el-icon-s-order"></i>
              <span>历史价格查询</span>
            </el-menu-item>
            <el-menu-item index="/alert">
              <i class="el-icon-s-order"></i>
              <span>降价提醒</span>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>

      <!-- 内容区 -->
      <el-main>
        <router-view />
      </el-main>
    </el-container>

    <!-- 页脚 -->
    <el-footer style="text-align: center; padding: 20px;">
      © 2024 fufu酱のWebsite. All rights reserved.
    </el-footer>
  </div>
</template>

<script>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import auth from './store/auth';

export default {
  name: 'App',
  setup() {
    // 获取用户状态
    const router = useRouter();
    const {state, fetchUserInfo, logout} = auth;

    // 判断是否为移动端
    const isMobile = ref(false);

    // 检查当前窗口宽度是否小于1024px
    const checkMobile = () => {
      isMobile.value = window.innerWidth < 1024;
    };

    // 监听窗口尺寸变化
    onMounted(() => {
      checkMobile();
      window.addEventListener('resize', checkMobile);
    });

    // 清理事件监听
    onBeforeUnmount(() => {
      window.removeEventListener('resize', checkMobile);
    });

    // 用户登出
    const handleLogout = () => {
      logout();
      router.push({name: 'home'});
    };

    // 获取用户名和是否认证的计算属性
    const username = computed(() => state.username);
    const isAuthenticated = computed(() => state.isAuthenticated);

    // 初始化用户信息
    onMounted(() => {
      if (state.isAuthenticated && !state.username) {
        fetchUserInfo();
      }
    });

    return {
      username,
      isAuthenticated,
      handleLogout,
      isMobile
    };
  },
};
</script>

<style>
body {
  margin: 0;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  background-color: #f0f2f5;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #ebeef5;
}

.logo img {
  vertical-align: middle;
}

.el-menu-demo {
  border-bottom: none;
}

.nav-buttons .el-button {
  margin-left: 15px;
}

.el-dropdown-link {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.el-avatar {
  margin-right: 5px;
}

.el-aside {
  background-color: #fff;
  border-right: 1px solid #ebeef5;
}

.el-main {
  padding: 20px;
  background-color: #fff;
}

.el-footer {
  background-color: #fff;
  border-top: 1px solid #ebeef5;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 100%;
}

.el-menu-vertical-demo .el-menu-item {
  padding-left: 20px !important;
}

.custom-aside {
  background-color: #001529;
}

.custom-aside .el-menu-vertical-demo {
  background-color: #001529;
  border-right: none;
}

.custom-aside .el-menu-vertical-demo .el-menu-item,
.custom-aside .el-menu-vertical-demo .el-submenu__title {
  color: #fff;
}

.custom-aside .el-menu-vertical-demo .el-menu-item:hover,
.custom-aside .el-menu-vertical-demo .el-submenu__title:hover {
  background-color: #0a1d38;
}

.custom-aside .el-menu-vertical-demo .el-menu-item.is-active,
.custom-aside .el-menu-vertical-demo .el-submenu.is-active .el-submenu__title {
  background-color: #1890ff;
  color: #fff;
}

.custom-aside .el-menu-vertical-demo .el-menu-item i,
.custom-aside .el-menu-vertical-demo .el-submenu__title i {
  color: #fff;
}
</style>
