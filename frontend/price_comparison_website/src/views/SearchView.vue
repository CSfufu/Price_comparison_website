<!-- src/views/SearchView.vue -->
<template>
  <div class="search-container">
    <!-- 搜索输入框 -->
    <el-input
      v-model="keyword"
      placeholder="请输入商品关键词"
      class="search-input"
      @keyup.enter="handleSearch"
    >
      <template #append>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </template>
    </el-input>

    <!-- Cookie 输入框（折叠面板） -->
    <el-collapse v-model="activeCollapse">
      <el-collapse-item title="高级选项（输入您的 Cookie）" name="1">
        <el-form :model="cookies" label-width="120px">
          <el-form-item label="京东 Cookie">
            <el-input v-model="cookies.cookie_jd" placeholder="请输入您的京东 Cookie"></el-input>
          </el-form-item>
          <el-form-item label="淘宝 Cookie">
            <el-input v-model="cookies.cookie_tb" placeholder="请输入您的淘宝 Cookie"></el-input>
          </el-form-item>
        </el-form>
        <p class="cookie-warning">
          注意：输入您的 Cookie 存在安全风险，请确保您信任此网站。Cookie 中包含您的登录信息，泄露可能导致账户安全问题。
        </p>
      </el-collapse-item>
    </el-collapse>

    <!-- 排序选项（仅在搜索成功后显示） -->
    <div v-if="searched" class="sort-options">
      <el-select v-model="sortOrder" placeholder="选择排序方式" @change="handleSortChange">
        <el-option label="默认" value="default"></el-option>
        <el-option label="价格升序" value="asc"></el-option>
        <el-option label="价格降序" value="desc"></el-option>
      </el-select>
    </div>

    <!-- 显示搜索结果 -->
    <div v-if="loading" class="loading">
      <el-icon :size="48"><Loading /></el-icon>
      <span>正在搜索，请稍候...</span>
    </div>

    <div v-else-if="searchResults.length > 0" class="results">
      <el-table :data="sortedSearchResults" style="width: 100%">
        <el-table-column prop="platform" label="平台" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.platform === '京东' ? 'success' : 'warning'">
              {{ scope.row.platform }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="商品名称">
          <template #default="scope">
            <el-link :href="scope.row.link" target="_blank">{{ getTruncatedText(scope.row.name, 60) }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" width="100">
          <template #default="scope">
            ￥{{ scope.row.price }}
          </template>
        </el-table-column>
        <el-table-column prop="store_name" label="店铺名称" width="150">
          <template #default="scope">
            <el-link :href="scope.row.store_link" target="_blank">{{ getTruncatedText(scope.row.store_name, 30) }}</el-link>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewDetails(scope.row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

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

    <div v-else-if="!loading && searchResults.length === 0 && searched">
      <el-empty description="未找到相关商品" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import axios from '../axios'; // 确保 axios 已正确配置
import { useRouter } from 'vue-router';
import { ElMessage, ElIcon } from 'element-plus';
import { Loading } from '@element-plus/icons-vue'; // 导入 Loading 图标

const keyword = ref('');
const loading = ref(false);
const searchResults = ref([]);
const totalResults = ref(0);
const pageSize = 60; // 根据后端设置
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

// 处理排序变化（如果希望后端处理排序，可以在此重新发送请求）
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
    const response = await axios.post('products/search/', {
      keyword: keyword.value,
      cookie_jd: cookies.value.cookie_jd, // 传递用户输入的京东 Cookie
      cookie_tb: cookies.value.cookie_tb, // 传递用户输入的淘宝 Cookie
      offset: (currentPage.value - 1) * pageSize,
      limit: pageSize,
    }, {
      timeout: 20000,
    });

    // 处理搜索结果
    const { jd, tb } = response.data;

    // 合并结果
    const combinedResults = [
      ...(jd ? jd.results : []),
      ...(tb ? tb.results : [])
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

// 监听排序方式变化（如果希望后端处理排序）
watch(sortOrder, () => {
  // 如果后端支持排序参数，可以在此重新发送请求
  // fetchSearchResults();
});
</script>

<style scoped>
.search-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.search-input {
  margin-bottom: 20px;
}

.sort-options {
  margin-bottom: 20px;
}

.loading {
  text-align: center;
  margin-top: 50px;
}

.results {
  margin-top: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.cookie-warning {
  color: red;
  margin-top: 10px;
}
</style>
