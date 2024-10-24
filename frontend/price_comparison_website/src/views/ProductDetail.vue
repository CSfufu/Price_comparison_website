<!-- src/views/ProductDetail.vue -->
<template>
  <div class="product-detail-container">
    <el-card v-if="product">
      <el-row>
        <el-col :span="8">
          <el-image :src="product.image_url" fit="contain" style="width: 100%; height: 400px;" />
        </el-col>
        <el-col :span="16">
          <h2>{{ getTruncatedText(product.name, 50) }}</h2>
          <p>价格：￥{{ product.price }}</p>
          <p>店铺：{{ getTruncatedText(product.store_name, 30) }}</p>
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
import { useRoute } from 'vue-router';
import axios from '../axios';
import { ElMessage } from 'element-plus';

const route = useRoute();
const product = ref(null);

const goToBuy = (link) => {
  if (link && (link.startsWith('http://') || link.startsWith('https://'))) {
    window.open(link, '_blank');
  } else {
    ElMessage.warning('无效的购买链接');
  }
};

// 截断文本函数
const getTruncatedText = (text, maxLength) => {
  if (!text) return '';
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

onMounted(async () => {
  const id = route.params.id;
  try {
    const response = await axios.get(`products/${id}/`); // 发送 GET 请求到 `/api/products/427/`
    product.value = response.data;
    console.log('接收到的商品数据:', product.value); // 调试日志

    // 打印字段类型和内容
    console.log('产品名称类型:', typeof product.value.name);
    console.log('产品名称内容:', product.value.name);
    console.log('店铺名称类型:', typeof product.value.store_name);
    console.log('店铺名称内容:', product.value.store_name);
  } catch (error) {
    console.error('获取商品详情失败', error);
    ElMessage.error('获取商品详情失败，请稍后重试');
  }
});
</script>

<style>
.product-detail-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-detail-container h2,
.product-detail-container p.truncate {
  margin: 5px 0;
}

.product-detail-container h2 {
  margin-bottom: 20px;
}

/* 调试样式 */
.product-detail-container h2,
.product-detail-container p {
  border: 1px solid red; /* 临时添加边框用于调试 */
  padding: 5px;
  color: #000; /* 确保文字颜色为黑色 */
}
</style>
