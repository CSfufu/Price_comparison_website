<!-- src/views/Services.vue -->
<template>
  <div class="services-container">
    <!-- 顶部横幅 -->
    <div class="banner">
      <img src="../assets/logo.jpg" alt="Our Services" class="banner-image" />
      <div class="banner-text">
        <h1>我们的服务</h1>
        <p>探索我们为您提供的专业服务</p>
      </div>
    </div>

    <!-- 服务列表 -->
    <div class="services-section">
      <el-row :gutter="20">
        <el-col :span="8" v-for="service in services" :key="service.title">
          <el-card :body-style="{ padding: '20px' }">
            <el-image
              :src="service.icon"
              alt="Service Icon"
              style="width: 64px; height: 64px; margin-bottom: 10px;"
              fit="contain"
            ></el-image>
            <h3>{{ service.title }}</h3>
            <p>{{ service.description }}</p>
            <el-button type="primary" @click="learnMore(service.link)">了解更多</el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 客户评价 -->
    <div class="testimonial-section">
      <h2>客户评价</h2>
      <el-carousel height="200px" :interval="5000" type="card">
        <el-carousel-item v-for="testimonial in testimonials" :key="testimonial.id">
          <div class="testimonial">
            <p>"{{ testimonial.content }}"</p>
            <p class="author">- {{ testimonial.author }}</p>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// 导入服务图标
import service1Icon from '../assets/media/images/banner1.jpeg';
import service2Icon from '../assets/media/images/banner2.jpeg';
import service3Icon from '../assets/media/images/banner3.jpeg';

// 路由实例
const router = useRouter();

// 服务数据
const services = ref([
  {
    icon: service1Icon,
    title: '实时比价',
    description: '实时获取各大电商平台的商品价格，帮您找到最低价。',
    link: '/search',
  },
  {
    icon: service2Icon,
    title: '搜索历史',
    description: '为您推荐最新的优惠信息和折扣券，购物更省钱。',
    link: '/history',
  },
  {
    icon: service3Icon,
    title: '历史价格查询',
    description: '您可以查询目标商品的历史价格，最低的时候购入。',
    link: '/price_history',
  },
]);

// 客户评价数据
const testimonials = ref([
  {
    id: 1,
    content: '这个网站帮我省了很多钱，我再也不用到处找优惠了！',
    author: 'fufu酱',
  },
  {
    id: 2,
    content: '历史价格查询功能非常实用，我可以等到价格最低时购买。',
    author: 'cs',
  },
  {
    id: 3,
    content: '实时比价让我在不同平台间轻松比较，节省了时间。',
    author: 'csfufu',
  },
]);

// 方法
const learnMore = (link) => {
  router.push(link);
};
</script>

<style>
.services-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.banner {
  position: relative;
  text-align: center;
  color: white;
}

.banner-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.banner-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.services-section {
  margin-top: 60px;
}

.services-section .el-card {
  text-align: center;
}

.services-section h3 {
  margin-top: 10px;
  font-size: 24px;
}

.services-section p {
  color: #666;
  margin-top: 10px;
}

.services-section .el-button {
  margin-top: 20px;
}

.testimonial-section {
  margin-top: 80px;
  text-align: center;
}

.testimonial-section h2 {
  font-size: 32px;
  margin-bottom: 20px;
}

.testimonial {
  font-size: 18px;
  color: #666;
  padding: 0 40px;
}

.testimonial .author {
  margin-top: 10px;
  color: #999;
}
</style>
