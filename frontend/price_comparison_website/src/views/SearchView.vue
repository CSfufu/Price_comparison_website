<!-- src/views/SearchView.vue -->
<template>
  <div class="search-container">
    <!-- 用户已认证时显示的内容 -->
    <div v-if="auth.state.isAuthenticated">
      <!-- 搜索区域 -->
      <el-card class="search-card">
        <el-row :gutter="20" align="middle">
          <el-col :span="18">
            <el-input
              v-model="keyword"
              placeholder="请输入商品关键词"
              class="search-input"
              @keyup.enter="handleSearch"
              clearable
            >
              <template #prepend>
                <el-icon><Search /></el-icon>
              </template>
              <template #append>
                <el-button type="primary" @click="handleSearch">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="6" class="cookie-collapse">
            <el-collapse v-model="activeCollapse">
              <el-collapse-item title="高级选项（输入您的 Cookie）" name="1">
                <el-form :model="cookies" label-width="100px">
                  <el-form-item label="京东 Cookie">
                    <el-input v-model="cookies.cookie_jd" placeholder="请输入您的京东 Cookie" clearable></el-input>
                  </el-form-item>
                  <el-form-item label="淘宝 Cookie">
                    <el-input v-model="cookies.cookie_tb" placeholder="请输入您的淘宝 Cookie" clearable></el-input>
                  </el-form-item>
                </el-form>
                <p class="cookie-warning">
                  注意：输入您的 Cookie 存在安全风险，请确保您信任此网站。Cookie 中包含您的登录信息，泄露可能导致账户安全问题。
                </p>
              </el-collapse-item>
            </el-collapse>
          </el-col>
        </el-row>
      </el-card>

      <!-- 排序选项 -->
      <el-row v-if="searched" class="sort-row" align="middle">
        <el-col :span="4">
          <span>排序方式：</span>
        </el-col>
        <el-col :span="6">
          <el-select v-model="sortOrder" placeholder="选择排序方式" @change="handleSortChange" clearable>
            <el-option label="默认" value="default"></el-option>
            <el-option label="价格升序" value="asc"></el-option>
            <el-option label="价格降序" value="desc"></el-option>
          </el-select>
        </el-col>
      </el-row>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <el-spin size="large" tip="正在搜索，请稍候...">
          <div class="content"></div>
        </el-spin>
      </div>

      <!-- 搜索结果 -->
      <div v-else-if="searchResults.length > 0" class="results">
        <el-row :gutter="20">
          <el-col v-for="product in paginatedResults" :key="product.product_id" :span="8">
            <el-card class="product-card" shadow="hover">
              <img :src="product.image_url" alt="商品图片" class="product-image" />
              <div class="product-info">
                <el-tag :type="product.platform === '京东' ? 'success' : 'warning'">{{ product.platform }}</el-tag>
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

      <!-- 无搜索结果 -->
      <div v-else-if="!loading && searchResults.length === 0 && searched">
        <el-empty description="未找到相关商品">
          <el-button type="primary" @click="handleSearch">重新搜索</el-button>
        </el-empty>
      </div>
    </div>

    <!-- 用户未认证时显示的提示 -->
    <div v-else class="login-prompt">
      <el-empty description="请登录之后再使用">
        <template #image>
          <el-icon size="64"><User /></el-icon>
        </template>
        <template #description>
          您尚未登录，请先 <router-link to="/login">登录</router-link> 以使用搜索功能。
        </template>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from '../axios'; // 确保 axios 已正确配置
import { useRouter } from 'vue-router';
import { ElMessage, ElIcon } from 'element-plus';
import { Loading, User, Search } from '@element-plus/icons-vue'; // 导入 Loading、User 和 Search 图标
import auth from '../store/auth'; // 引入 auth 模块

const keyword = ref('');
const loading = ref(false);
const searchResults = ref([]);
const totalResults = ref(0);
const pageSize = 12; // 每页显示的商品数
const currentPage = ref(1);
const searched = ref(false);
const router = useRouter();

// 用于折叠面板的状态
const activeCollapse = ref([]);

// 存储用户输入的 Cookie
const cookies = ref({
  cookie_jd: '',
  cookie_tb: '',
});

// 排序方式，初始为 'default'
const sortOrder = ref('default'); // 默认选项

// 计算属性，根据 sortOrder 排序商品
const sortedSearchResults = computed(() => {
  if (sortOrder.value === 'asc') {
    return [...searchResults.value].sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
  } else if (sortOrder.value === 'desc') {
    return [...searchResults.value].sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
  } else {
    // 默认排序，保持原始顺序
    return searchResults.value;
  }
});

// 计算属性，分页后的结果
const paginatedResults = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return sortedSearchResults.value.slice(start, end);
});

// 处理搜索逻辑
const handleSearch = () => {
  currentPage.value = 1;
  sortOrder.value = 'default';
  fetchSearchResults();
};

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page;
  fetchSearchResults();
};

// 处理排序变化
const handleSortChange = (value) => {
  sortOrder.value = value;
};

// 异步获取搜索结果
const fetchSearchResults = async () => {
  if (!keyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词');
    return;
  }

  if (!cookies.value.cookie_jd && !cookies.value.cookie_tb) {
    ElMessage.warning('请提供有效的京东或淘宝 Cookie');
    return;
  }

  loading.value = true;
  searched.value = true;

  try {
    // 调用后端搜索接口
    const response = await axios.post(
      'products/search/',
      {
        keyword: keyword.value,
        cookie_jd: cookies.value.cookie_jd, // 传递用户输入的京东 Cookie
        cookie_tb: cookies.value.cookie_tb, // 传递用户输入的淘宝 Cookie
        offset: (currentPage.value - 1) * pageSize,
        limit: pageSize,
      },
      {
        timeout: 20000,
      }
    );

    // 处理搜索结果
    const { jd, tb } = response.data;

    // 合并结果
    const combinedResults = [
      ...(jd ? jd.results : []),
      ...(tb ? tb.results : []),
    ];

    // 计算总数，确保为数字
    const total = (jd && typeof jd.total === 'number' ? jd.total : 0) +
                  (tb && typeof tb.total === 'number' ? tb.total : 0);

    searchResults.value = combinedResults;
    totalResults.value = total;

    // 打印调试信息
    console.log('搜索结果:', searchResults.value);
    console.log('totalResults 类型:', typeof totalResults.value); // 应为 'number'
    console.log('totalResults 值:', totalResults.value); // 应为数字

  } catch (error) {
    console.error('搜索失败', error);
    ElMessage.error('搜索失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

// 跳转购买链接
const goToBuy = (link) => {
  if (link) {
    window.open(link, '_blank');
  } else {
    ElMessage.warning('无效的购买链接');
  }
};

// 查看商品详情
const viewDetails = (product) => {
  // 使用 product_id 作为参数传递
  router.push({ name: 'ProductDetail', params: { id: product.product_id } });
};

// 截断文本函数
const getTruncatedText = (text, maxLength) => {
  if (!text) return '';
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

// 获取用户信息
const initialize = async () => {
  await auth.fetchUserInfo();
};

// 在组件挂载时获取用户信息
onMounted(() => {
  initialize();
});
</script>

<style scoped>
.search-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.search-card {
  padding: 20px;
  background-color: #f9f9f9;
}

.search-input {
  width: 100%;
}

.cookie-collapse {
  text-align: right;
}

.cookie-warning {
  color: #f56c6c;
  margin-top: 10px;
  font-size: 12px;
}

.sort-row {
  margin-top: 20px;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.results {
  margin-top: 20px;
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

.pagination {
  margin-top: 20px;
  text-align: center;
}

.login-prompt {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}
</style>
