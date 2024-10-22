<!-- src/views/HomeView.vue -->
<template>
  <div class="home-container">
    <el-carousel height="300px" :interval="4000" arrow="always">
      <el-carousel-item v-for="item in carouselItems" :key="item.id">
        <img :src="item.image" alt="Carousel Image" class="carousel-image" />
      </el-carousel-item>
    </el-carousel>
    <div class="home-content">
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
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      carouselItems: [
      { id: 1, image: '../media/images/banner1.jpeg' },
      { id: 2, image: '../media/images/banner2.jpeg' },
      { id: 3, image: '../media/images/banner3.jpeg' },
    ],
    features: [
      {
        icon: '/icons/compare.svg',
        title: '价格比较',
        description: '一键比较多家电商平台价格，省时省力。',
      },
      {
        icon: '/icons/discount.svg',
        title: '优惠促销',
        description: '汇总各大平台优惠信息，不错过任何折扣。',
      },
      {
        icon: '/icons/security.svg',
        title: '安全保障',
        description: '严格的数据审核机制，确保信息真实可靠。',
      },
    ],
    };
  },
};
</script>

<style>
.home-container {
  background-color: #f5f5f5;
}

.carousel-image {
  width: 100%;
  height: 300px;
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
</style>
