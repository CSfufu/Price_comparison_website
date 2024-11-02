<!-- src/views/Alerts.vue -->
<template>
  <div class="alerts-container">
    <!-- 用户已认证时显示的内容 -->
    <div v-if="auth.state.isAuthenticated">
      <el-card class="alerts-card">
        <h2>我的降价提醒</h2>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading">
          <el-spin size="large" tip="正在加载提醒..."></el-spin>
        </div>

        <!-- 提醒列表 -->
        <div v-else-if="alerts.length > 0" class="content-container">
          <el-table :data="alerts" style="width: 100%" border>
            <!-- 商品名称列 -->
            <el-table-column prop="product_name" label="商品名称" width="300">
              <template #default="{ row }">
                <el-link :href="row.product_link" target="_blank">
                  {{ row.product_name }}
                </el-link>
              </template>
            </el-table-column>

            <!-- 当前价格列 -->
            <el-table-column prop="current_price" label="当前价格" width="150">
              <template #default="{ row }">
                ￥{{ row.current_price }}
              </template>
            </el-table-column>

            <!-- 目标价格列 -->
            <el-table-column prop="target_price" label="目标价格" width="150">
              <template #default="{ row }">
                ￥{{ row.target_price }}
              </template>
            </el-table-column>

            <!-- 操作列 -->
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="danger" size="mini" @click="deleteAlert(row.id)">删除</el-button>
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

        <!-- 无提醒数据 -->
        <div v-else class="no-alerts">
          <el-empty description="您还没有设置任何降价提醒。">
            <el-button type="primary" @click="goToSearch">立即设置</el-button>
          </el-empty>
        </div>
      </el-card>
    </div>

    <!-- 用户未认证时显示的提示 -->
    <div v-else class="login-prompt">
      <el-empty description="请登录之后再查看降价提醒">
        <template #image>
          <el-icon size="64"><User /></el-icon>
        </template>
        <template #description>
          您尚未登录，请先 <router-link to="/login">登录</router-link> 以查看和管理您的降价提醒。
        </template>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '../axios'; // 确保 axios 实例已正确配置
import { ElMessage, ElEmpty, ElButton, ElCard, ElTable, ElTableColumn, ElPagination, ElLink, ElIcon } from 'element-plus';
import { User } from '@element-plus/icons-vue'; // 导入 User 图标
import { useRouter } from 'vue-router';
import auth from '../store/auth'; // 引入 auth 模块

// 定义响应式变量
const alerts = ref([]);
const loading = ref(false);
const totalResults = ref(0);
const pageSize = 10;
const currentPage = ref(1);
const router = useRouter();

// 获取降价提醒列表
const fetchAlerts = async () => {
  loading.value = true;
  try {
    const response = await axios.get('alerts/', {
      params: {
        page: currentPage.value,
        page_size: pageSize,
      },
    });
    alerts.value = response.data.results || [];
    totalResults.value = response.data.count || 0;
  } catch (error) {
    console.error('获取降价提醒失败', error);
    ElMessage.error('获取降价提醒失败，请稍后重试。');
  } finally {
    loading.value = false;
  }
};

// 删除降价提醒
const deleteAlert = async (alertId) => {
  try {
    await axios.delete(`/alerts/${alertId}/`);
    ElMessage.success('降价提醒已删除');
    fetchAlerts();
  } catch (error) {
    console.error('删除降价提醒失败', error);
    ElMessage.error('删除降价提醒失败，请稍后重试。');
  }
};

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page;
  fetchAlerts();
};

// 跳转到设置提醒的搜索页面
const goToSearch = () => {
  router.push({ name: '/history' }); // 根据实际路由名称修改
};

// 初始化组件
const initialize = async () => {
  await auth.fetchUserInfo();
  if (auth.state.isAuthenticated) {
    fetchAlerts();
  } else {
    // 如果用户未登录，不做重定向，显示登录提示
    // router.push({ name: 'login' }); // 如果需要自动跳转，可以取消注释
  }
};

onMounted(() => {
  initialize();
});
</script>

<style scoped>
.alerts-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.alerts-card {
  padding: 20px;
  background-color: #f9f9f9;
}

.alerts-card h2 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.content-container {
  margin-top: 20px;
}

.no-alerts {
  margin-top: 20px;
  text-align: center;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.login-prompt {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  padding: 20px;
}

.product-info-card {
  padding: 20px;
  background-color: #f9f9f9;
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.product-info-card h2 {
  margin-bottom: 10px;
}

.product-link {
  display: block;
  margin-top: 10px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .alerts-container {
    padding: 10px;
  }

  .alerts-card {
    padding: 10px;
  }

  .alerts-card h2 {
    font-size: 20px;
  }

  .product-info-card h2 {
    font-size: 20px;
  }

  .el-row {
    flex-direction: column;
  }

  .el-col {
    span: 24 !important;
  }
}
</style>
