<!-- src/views/ProductDetail.vue -->
<template>
  <div class="product-detail-container">
    <!-- 回退按钮 -->
    <el-button type="default" @click="goBack" class="back-button">
      <el-icon><ArrowLeft /></el-icon> 返回
    </el-button>

    <el-card v-if="product">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-image
            :src="product.image_url"
            fit="contain"
            style="width: 100%; height: 400px;"
            :preview-src-list="[product.image_url]"
          />
        </el-col>
        <el-col :span="16">
          <h2>{{ product.name }}</h2>
          <p><strong>价格：</strong>￥{{ product.price }}</p>
          <p><strong>店铺：</strong>{{ product.store_name }}</p>
          <el-button type="primary" @click="goToBuy(product.link)">
            前往购买
          </el-button>
        </el-col>
      </el-row>
    </el-card>
    <el-empty v-else description="商品详情未找到" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '../axios';
import { ElMessage, ElButton, ElIcon } from 'element-plus';
import { ArrowLeft } from '@element-plus/icons-vue'; // 导入箭头图标

const route = useRoute();
const router = useRouter();
const product = ref(null);

// 跳转到购买链接
const goToBuy = (link) => {
  if (link && (link.startsWith('http://') || link.startsWith('https://'))) {
    window.open(link, '_blank');
  } else {
    ElMessage.warning('无效的购买链接');
  }
};

// 回退到上一页
const goBack = () => {
  router.back();
};

// 异步获取商品详情
onMounted(async () => {
  const productId = route.params.id; // 使用 'id' 作为 'product_id'
  if (!productId) {
    ElMessage.error('无效的商品 ID');
    return;
  }

  try {
    const response = await axios.get(`products/${productId}/`); // 确保后端接口支持以 product_id 获取详情
    product.value = response.data;
  } catch (error) {
    console.error('获取商品详情失败', error);
    ElMessage.error('获取商品详情失败，请稍后重试');
  }
});
</script>

<style scoped>
.product-detail-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.back-button {
  margin-bottom: 20px;
}

/* 优化样式，移除调试用的红色边框 */
.product-detail-container h2,
.product-detail-container p {
  margin: 10px 0;
}

.product-detail-container h2 {
  font-size: 24px;
  font-weight: bold;
}

.product-detail-container p {
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .product-detail-container {
    padding: 10px;
  }

  .el-row {
    flex-direction: column;
  }

  .el-col {
    span: 24 !important;
  }

  .back-button {
    width: 100%;
    justify-content: center;
  }
}
</style>
