<!-- src/views/ProductListView.vue -->
<template>
  <div class="product-list-container">
    <el-card class="product-list-card">
      <el-row justify="space-between" align="middle">
        <el-col>
          <h2>商品列表</h2>
        </el-col>
      </el-row>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <el-spin size="large" tip="正在加载商品..."></el-spin>
      </div>

      <!-- 商品列表 -->
      <div v-else-if="products.length > 0" class="results">
        <el-row :gutter="20">
          <el-col
            v-for="product in paginatedProducts"
            :key="product.id"
            :span="8"
          >
            <el-card class="product-card" shadow="hover">
              <img
                :src="product.image_url"
                alt="商品图片"
                class="product-image"
              />
              <div class="product-info">
                <el-link
                  :href="product.link"
                  target="_blank"
                  class="product-name"
                >
                  {{ getTruncatedText(product.name, 60) }}
                </el-link>
                <div class="product-details">
                  <span class="price">￥{{ product.price }}</span>
                  <el-link
                    :href="product.store_link"
                    target="_blank"
                    class="store-name"
                  >
                    {{ getTruncatedText(product.store_name, 30) }}
                  </el-link>
                </div>
                <el-button
                  type="primary"
                  size="small"
                  @click="viewDetails(product)"
                  class="details-button"
                >
                  详情
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            background
            layout="prev, pager, next"
            :total="totalResults"
            :page-size="pageSize"
            :current-page.sync="currentPage"
            @current-change="handlePageChange"
          />
        </div>
      </div>

      <!-- 无商品数据 -->
      <div v-else-if="!loading && products.length === 0">
        <el-empty description="暂无商品数据。">
          <el-button type="primary" @click="goToSearch">立即搜索</el-button>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from '../axios'; // 确保 axios 已正确配置
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';

const products = ref([]);
const loading = ref(false);
const totalResults = ref(0);
const pageSize = 12; // 每页显示的商品数
const currentPage = ref(1);
const router = useRouter();

// 计算属性，分页后的结果
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return products.value.slice(start, end);
});

// 获取商品列表
const fetchProducts = async () => {
  loading.value = true;

  try {
    const response = await axios.get('products/products_history'); // 使用 'products/' 端点
    console.log('API Response:', response.data); // 调试日志
    console.log("products length", products.value.length)
    products.value = response.data || []; // 确保为数组
    totalResults.value = response.data.count || 0;
  } catch (error) {
    console.error('获取商品失败', error);
    ElMessage.error('获取商品失败，请稍后重试。');
    products.value = []; // 确保为空数组
    totalResults.value = 0;
  } finally {
    loading.value = false;
  }
};

// 查看商品详情
const viewDetails = (product) => {
  // 解析路由以获取完整的 URL
  const routeData = router.resolve({
    name: 'ProductDetail',
    params: { id: product.product_id },
  });
  // 在新标签页中打开
  window.open(routeData.href, '_blank');
};

// 截断文本函数
const getTruncatedText = (text, maxLength) => {
  if (!text) return '';
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page;
  // 如果后端支持分页，可以在这里请求特定页的数据
  // 否则，前端已经通过计算属性处理了分页
};

// 跳转到搜索页面
const goToSearch = () => {
  router.push({ name: 'search' });
};

// 在组件挂载时获取商品列表
onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
/* 您的样式保持不变，或根据需要进行调整 */
.product-list-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.product-list-card {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.product-card {
  margin-bottom: 20px;
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.product-info {
  padding: 15px;
}

.product-name {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin: 10px 0;
}

.product-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.price {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
}

.store-name {
  font-size: 14px;
  color: #409EFF;
}

.details-button {
  width: 100%;
}

@media (max-width: 768px) {
  .product-list-container {
    padding: 0 10px;
  }
}
</style>
