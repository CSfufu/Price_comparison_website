<!-- src/views/ProductList.vue -->
<template>
  <div class="product-list-container">
    <!-- 用户已认证时显示的内容 -->
    <div v-if="auth.state.isAuthenticated">
      <el-card class="product-list-card">
        <el-row justify="space-between" align="middle">
          <el-col>
            <h2>商品列表</h2>
          </el-col>
        </el-row>

        <!-- 显示 products.length -->
        <div class="debug-info">
          <p>共有 {{ totalResults }} 件商品</p>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading">
          <el-spin size="large" tip="正在加载商品..."></el-spin>
        </div>

        <!-- 商品列表 -->
        <div v-else-if="products.length > 0" class="results">
          <el-row :gutter="20">
            <el-col v-for="product in products" :key="product.id" :span="8">
              <el-card class="product-card" shadow="hover">
                <img :src="product.image_url" alt="商品图片" class="product-image" />
                <div class="product-info">
                  <el-link :href="product.link" target="_blank" class="product-name">
                    {{ getTruncatedText(product.name, 60) }}
                  </el-link>
                  <div class="product-details">
                    <span class="price">￥{{ product.price }}</span>
                    <el-link :href="product.store_link" target="_blank" class="store-name">
                      {{ getTruncatedText(product.store_name, 30) }}
                    </el-link>
                  </div>
                  <el-button type="primary" size="small" @click="viewDetails(product)" class="details-button">
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

    <!-- 用户未认证时显示的提示 -->
    <div v-else class="login-prompt">
      <el-empty description="请登录之后再使用">
        <template #image>
          <el-icon size="64"><User /></el-icon>
        </template>
        <template #description>
          您尚未登录，请先 <router-link to="/login">登录</router-link> 以查看商品列表。
        </template>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '../axios'; // 确保 axios 已正确配置
import { ElMessage, ElIcon } from 'element-plus';
import { User } from '@element-plus/icons-vue'; // 导入 User 图标
import { useRouter } from 'vue-router';
import auth from '../store/auth'; // 引入 auth 模块

const products = ref([]);
const loading = ref(false);
const totalResults = ref(0);
const pageSize = 12; // 每页显示的商品数
const currentPage = ref(1);
const router = useRouter();

// 获取商品列表
const fetchProducts = async () => {
  loading.value = true;

  try {
    const response = await axios.get('products/products_history', {
      params: {
        page: currentPage.value, // 请求的页码
        page_size: pageSize, // 每页显示的数据量
      },
    });
    console.log('API Response:', response.data); // 查看 API 响应结构
    // 处理分页数据
    products.value = response.data.results || [];
    totalResults.value = response.data.count || 0;
    console.log('Products Length:', products.value.length); // 打印 products.length
  } catch (error) {
    console.error('获取商品失败', error);
    ElMessage.error('获取商品失败，请稍后重试。');
    products.value = [];
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
  fetchProducts(); // 请求特定页的数据
};

// 跳转到搜索页面
const goToSearch = () => {
  router.push({ name: 'Search' });
};

// 获取用户信息并初始化
const initialize = async () => {
  await auth.fetchUserInfo(); // 获取用户信息，更新 auth.state.isAuthenticated
  if (auth.state.isAuthenticated) {
    fetchProducts(); // 仅在认证后加载商品
  }
};

// 在组件挂载时获取用户信息
onMounted(() => {
  initialize();
});
</script>

<style scoped>
.debug-info {
  margin-bottom: 20px;
  color: #409EFF;
}

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

/* 新增样式：登录提示 */
.login-prompt {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}
</style>
