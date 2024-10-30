<!-- src/views/AboutView.vue -->
<template>
  <div class="about-container">
    <!-- 顶部横幅 -->
    <div class="banner">
      <img src="../assets/media/images/banner2.jpeg" alt="About Us" class="banner-image" />
      <div class="banner-text">
        <h1>关于我们</h1>
        <p>了解我们的使命和团队</p>
      </div>
    </div>

    <!-- 使命宣言 -->
    <div class="mission-section">
      <h2>我们的使命</h2>
      <p>
        我们致力于为消费者提供最全面、最准确的商品价格比较服务，<br>帮助您以最优惠的价格购买心仪的商品。
      </p>
    </div>

    <!-- 团队介绍 -->
    <div class="team-section">
      <h2>我们的团队</h2>
      <el-row :gutter="20">
        <el-col :span="8" v-for="member in teamMembers" :key="member.name">
          <el-card :body-style="{ padding: '20px' }">
            <el-avatar :src="member.photo" size="large"></el-avatar>
            <h3>{{ member.name }}</h3>
            <p class="position">{{ member.position }}</p>
            <p>{{ member.description }}</p>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 联系方式 -->
    <div class="contact-section">
      <h2>联系我</h2>
      <p>如果您有任何问题或建议，欢迎通过以下方式联系我们：</p>
      <ul>
        <li><i class="el-icon-home"></i> 个人主页：<a href="https://csfufu.life" target="_blank">fufu酱のNotebook</a></li>
        <li><i class="el-icon-message"></i> 邮箱：chenshuang@zju.edu.cn</li>
        <li><i class="el-icon-phone"></i> 电话：+86 183 8100 2338</li>
        <li><i class="el-icon-position"></i> 地址：浙江省杭州市西湖区浙江大学玉泉校区</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 导入团队成员照片
import member1Photo from '../assets/media/images/banner1.jpeg';
import member2Photo from '../assets/media/images/banner2.jpeg';
import member3Photo from '../assets/media/images/banner3.jpeg';

// 团队成员数据
const teamMembers = ref([
  {
    name: 'fufu酱',
    position: '首席执行官',
    photo: member1Photo,
    description: '负责公司的整体战略和运营。',
  },
  {
    name: 'cs',
    position: '技术总监',
    photo: member2Photo,
    description: '负责技术团队的管理和产品研发。',
  },
  {
    name: 'csfufu',
    position: '美工',
    photo: member3Photo,
    description: '负责网站美化和升级。',
  },
]);
</script>

<style>
.about-container {
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

.mission-section,
.team-section,
.contact-section {
  margin-top: 60px;
}

.mission-section h2,
.team-section h2,
.contact-section h2 {
  font-size: 32px;
  margin-bottom: 20px;
  text-align: center;
}

.mission-section p,
.contact-section p {
  font-size: 18px;
  color: #666;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.team-section .el-card {
  text-align: center;
}

.team-section h3 {
  margin-top: 10px;
  font-size: 24px;
}

.team-section .position {
  color: #999;
  margin-bottom: 10px;
}

.team-section p {
  color: #666;
  margin-top: 10px;
}

.contact-section ul {
  list-style: none;
  padding: 0;
  font-size: 18px;
  color: #666;
  max-width: 800px;
  margin: 0 auto;
}

.contact-section li {
  margin-top: 10px;
}

.contact-section i {
  margin-right: 10px;
  color: #1890ff;
}
</style>
