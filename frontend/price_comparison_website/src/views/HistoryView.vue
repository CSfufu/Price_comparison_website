<!-- src/views/HistoryView.vue -->
<template>
  <div class="history-container">
    <!-- 搜索历史区域 -->
    <el-card class="history-card">
      <el-row justify="space-between" align="middle">
        <el-col>
          <h2>搜索历史</h2>
        </el-col>
      </el-row>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <el-spin size="large" tip="正在加载搜索历史..."></el-spin>
      </div>

      <!-- 搜索历史表格 -->
      <div v-else-if="searchHistories.length > 0" class="results">
        <el-row :gutter="20">
          <el-col v-for="history in searchHistories" :key="history.id" :span="8">
            <el-card class="product-card" shadow="hover">
              <img :src="history.product.image_url" alt="商品图片" class="product-image" />
              <div class="product-info">
                <el-link :href="history.product.link" target="_blank" class="product-name">
                  {{ getTruncatedText(history.product.name, 60) }}
                </el-link>
                <div class="product-details">
                  <span class="price">￥{{ history.product.price }}</span>
                  <el-link :href="history.product.store_link" target="_blank" class="store-name">
                    {{ getTruncatedText(history.product.store_name, 30) }}
                  </el-link>
                </div>
                <el-button type="primary" size="small" @click="viewDetails(history.product)" class="details-button">
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

      <!-- 无搜索历史 -->
      <div v-else-if="!loading && searchHistories.length === 0">
        <el-empty description="您还没有搜索过任何商品。">
          <el-button type="primary" @click="goToSearch">立即搜索</el-button>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from '../axios'; // 确保 axios 已正确配置
import { ElMessage, ElEmpty, ElTable, ElTag, ElButton, ElLink, ElPagination, ElCard, ElRow, ElCol } from 'element-plus';
import { useRouter } from 'vue-router';
import auth from '../store/auth'; // 引入 auth 模块

// 状态变量
const searchHistories = ref([]);
const loading = ref(false);
const totalResults = ref(0);
const pageSize = 12; // 每页显示的搜索记录数
const currentPage = ref(1);
const router = useRouter();

// 计算属性，分页后的结果
const paginatedResults = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return searchHistories.value.slice(start, end);
});

// 获取搜索历史
const fetchSearchHistory = async () => {
  if (!auth.state.isAuthenticated) {
    ElMessage.warning('您需要登录才能查看搜索历史。');
    return;
  }

  loading.value = true;

  try {
    const response = await axios.get('products/search-history/', {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${auth.state.token}`, // 使用 JWT 令牌
      },
      params: {
        page: currentPage.value,
        page_size: pageSize,
      },
    });

    searchHistories.value = response.data.results;
    totalResults.value = response.data.count;
  } catch (error) {
    console.error('获取搜索历史失败', error);
    ElMessage.error('获取搜索历史失败，请稍后重试。');
  } finally {
    loading.value = false;
  }
};

// 查看商品详情
const viewDetails = (product) => {
  router.push({ name: 'ProductDetail', params: { product_id: product.product_id } });
};

// 截断文本函数
const getTruncatedText = (text, maxLength) => {
  if (!text) return '';
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page;
  fetchSearchHistory();
};

// 跳转到搜索页面
const goToSearch = () => {
  router.push({ name: 'Search' });
};

// 在组件挂载时获取搜索历史
onMounted(() => {
  fetchSearchHistory();
});
</script>

<style scoped>
.history-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.history-card {
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
  .history-container {
    padding: 0 10px;
  }

  .el-table-column {
    text-align: center;
  }
}
</style>
