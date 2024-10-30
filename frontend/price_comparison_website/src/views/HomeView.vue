<!-- src/views/HomeView.vue -->
<template>
  <div class="home-container">
    <!-- 轮播图 -->
    <el-carousel height="500px" :interval="4000" arrow="always">
      <el-carousel-item v-for="item in carouselItems" :key="item.id">
        <img :src="item.image" alt="Carousel Image" class="carousel-image" />
      </el-carousel-item>
    </el-carousel>

    <!-- 主体内容 -->
    <div class="home-content">
      <!-- 登录状态下的欢迎信息 -->
      <el-card v-if="isAuthenticated" class="user-info-card">
        <h3>欢迎  {{ username }}！</h3>
        <p>来到了全世界最好的商品购物比价网站</p>
      </el-card>

      <!-- 未登录状态下的提示信息 -->
      <el-card v-else class="guest-info-card">
        <h3>欢迎来到商品价格比较网站</h3>
        <p>请先登录以获取个性化体验。</p>
        <el-button type="primary" @click="goToLogin">登录</el-button>
        <el-button @click="goToRegister">注册</el-button>
      </el-card>

      <!-- 公共内容（无论是否登录都显示） -->
      <el-row :gutter="20">
        <el-col :span="24">
          <h2 class="home-title">欢迎来到商品价格比较网站</h2>
          <p class="home-description">
            我们为您提供各大电商平台的商品价格比较，帮助您以最优惠的价格购买心仪的商品。
          </p>
        </el-col>
      </el-row>
      <el-row :gutter="20" class="feature-section">
        <el-col :span="8" v-for="feature in features" :key="feature.title">
          <el-card :body-style="{ padding: '20px' }">
            <el-image
              :src="feature.icon"
              alt="Feature Icon"
              style="width: 64px; height: 64px; margin-bottom: 10px;"
              fit="contain"
            ></el-image>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
            <el-button
              v-if = "feature.link"
              type="primary"
              size="small"
              @click.stop="navigateTo(feature.link)"
            >
              查看详情
            </el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue';
import { useRouter } from 'vue-router';
import auth from '../store/auth';

// 导入轮播图图片
import banner1 from '../assets/media/images/banner1.jpeg';
import banner2 from '../assets/media/images/banner4.jpeg';
import banner3 from '../assets/media/images/banner5.jpeg';

// 导入功能图标

const { state, fetchUserInfo } = auth;
const router = useRouter();

const isAuthenticated = computed(() => state.isAuthenticated);
const username = computed(() => state.username);

const goToLogin = () => {
  router.push({ name: 'login' });
};

const goToRegister = () => {
  router.push({ name: 'register' });
};

onMounted(() => {
  if (state.isAuthenticated && !state.username) {
    fetchUserInfo();
  }
});

const navigateTo = (link) => {
  router.push(link);
};


const carouselItems = ref([
  { id: 1, image: banner1 },
  { id: 2, image: banner2 },
  { id: 3, image: banner3 },
]);

const features = ref([
  {
    icon: banner1,
    title: '实时比价',
    description: '实时获取各大电商平台的商品价格，帮您找到最低价。',
    link: '/search'
  },
  {
    icon: banner2,
    title: '搜索历史',
    description: '为您推荐最新的优惠信息和折扣券，购物更省钱。',
    link: '/history'
  },
  {
    icon: banner3,
    title: '历史价格查询',
    description: '您可以查询想要的目标商品历史价格，最低的时候购入。',
    link: '/price_history'
  },
]);
</script>

<style>
.home-container {
  background-color: #f5f5f5;
}

.carousel-image {
  width: 100%;
  height: 500px;
  object-fit: cover;
}

.home-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.home-title {
  text-align: center;
  font-size: 32px;
  margin-bottom: 20px;
}

.home-description {
  text-align: center;
  font-size: 18px;
  color: #666;
}

.feature-section {
  margin-top: 40px;
}

.feature-section .el-col {
  display: flex;
  justify-content: center;
}

.el-card {
  text-align: center;
}

.el-card h3 {
  margin-top: 10px;
  font-size: 24px;
}

.el-card p {
  color: #666;
  margin-top: 10px;
}

.feature-card {
  text-align: center;
  transition: box-shadow 0.3s;
}

.feature-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}


.user-info-card,
.guest-info-card {
  max-width: 600px;
  margin: 40px auto;
  text-align: center;
}

.user-info-card h3,
.guest-info-card h3 {
  font-size: 28px;
  margin-bottom: 20px;
}
</style>
