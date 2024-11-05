<!-- src/views/Alerts.vue -->
<template>
  <div class="alerts-container">
    <transition name="fade" mode="out-in">
      <!-- 已认证用户的内容 -->
      <div v-if="auth.state.isAuthenticated" class="authenticated-content">
        <el-card class="alerts-card" :body-style="{ padding: '0px' }">
          <!-- 头部区域 -->
          <div class="card-header">
            <div class="header-content">
              <div class="title-section">
                <el-icon class="bell-icon"><Bell /></el-icon>
                <h2>我的降价提醒</h2>
              </div>
              <el-button 
                type="primary" 
                class="add-alert-btn"
                @click="gotoHistory"
                :icon="Plus"
              >
                添加提醒
              </el-button>
            </div>
          </div>

          <!-- 加载状态 -->
          <div v-if="loading" class="loading-container">
            <el-skeleton :rows="5" animated />
          </div>

          <!-- 提醒列表 -->
          <div v-else-if="alerts.length > 0" class="alerts-list">
            <TransitionGroup 
              name="list" 
              tag="div"
              class="transition-group"
            >
              <div 
                v-for="alert in alerts" 
                :key="alert.id" 
                class="alert-item"
              >
                <div class="alert-content">
                  <div class="product-info">
                    <el-image 
                      :src="alert.image_url || '/placeholder.png'"
                      class="product-thumbnail"
                      fit="cover"
                    >
                      <template #error>
                        <div class="image-placeholder">
                          <el-icon><Picture /></el-icon>
                        </div>
                      </template>
                    </el-image>
                    <div class="product-details">
                      <el-link 
                        :href="alert.product_link" 
                        target="_blank"
                        class="product-name"
                      >
                        {{ alert.product_name }}
                      </el-link>
                      <div class="price-info">
                        <div class="price-item">
                          <span class="label">当前价格:</span>
                          <span class="price current">¥{{ formatPrice(alert.current_price) }}</span>
                        </div>
                        <div class="price-item">
                          <span class="label">目标价格:</span>
                          <span class="price target">¥{{ formatPrice(alert.target_price) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="actions">
                    <el-popconfirm
                      title="确定要删除这条降价提醒吗？"
                      @confirm="deleteAlert(alert.id)"
                      confirm-button-text="确定"
                      cancel-button-text="取消"
                    >
                      <template #reference>
                        <el-button 
                          type="danger" 
                          :icon="Delete"
                          circle
                          class="delete-btn"
                        />
                      </template>
                    </el-popconfirm>
                  </div>
                </div>
              </div>
            </TransitionGroup>

            <!-- 分页 -->
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="currentPage"
                :page-size="pageSize"
                :total="totalResults"
                layout="prev, pager, next"
                background
                @current-change="handlePageChange"
              />
            </div>
          </div>

          <!-- 无数据状态 -->
          <div v-else class="empty-state">
            <el-empty>
              <template #image>
                <el-icon class="empty-icon"><Bell /></el-icon>
              </template>
              <template #description>
                <div class="empty-text">
                  <p>您还没有设置任何降价提醒</p>
                  <el-button 
                    type="primary" 
                    @click="gotoHistory"
                    class="mt-4"
                  >
                    立即设置
                  </el-button>
                </div>
              </template>
            </el-empty>
          </div>
        </el-card>
      </div>

      <!-- 未认证用户的提示 -->
      <div v-else class="unauthorized-content">
        <el-card class="login-card">
          <template #header>
            <div class="login-card-header">
              <el-icon class="login-icon"><User /></el-icon>
              <h2>请先登录</h2>
            </div>
          </template>
          <div class="login-content">
            <p>登录后即可查看和管理您的降价提醒</p>
            <el-button 
              type="primary" 
              @click="goToLogin"
              class="login-btn"
            >
              立即登录
            </el-button>
          </div>
        </el-card>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Bell, Picture, User, Delete, Plus } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import axios from '../axios';
import auth from '../store/auth';

// 响应式状态
const alerts = ref([]);
const loading = ref(false);
const totalResults = ref(0);
const pageSize = 10;
const currentPage = ref(1);
const router = useRouter();

// 格式化价格
const formatPrice = (price) => {
  return Number(price).toFixed(2);
};

// 获取降价提醒列表
const fetchAlerts = async () => {
  loading.value = true;
  try {
    const response = await axios.get('/alerts/', {
      params: {
        page: currentPage.value,
        page_size: pageSize,
      },
    });
    alerts.value = response.data.results || [];
    totalResults.value = response.data.count || 0;
  } catch (error) {
    console.error('获取降价提醒失败', error);
    ElMessage.error({
      message: '获取降价提醒失败，请稍后重试',
      duration: 3000,
    });
  } finally {
    loading.value = false;
  }
};

// 删除降价提醒
const deleteAlert = async (alertId) => {
  try {
    await axios.delete(`/alerts/${alertId}/`);
    ElMessage.success({
      message: '降价提醒已删除',
      duration: 2000,
    });
    fetchAlerts();
  } catch (error) {
    console.error('删除降价提醒失败', error);
    ElMessage.error({
      message: '删除降价提醒失败，请稍后重试',
      duration: 3000,
    });
  }
};

// 处理分页变化
const handlePageChange = (page) => {
  currentPage.value = page;
  fetchAlerts();
};

// 导航方法
const goToSearch = () => {
  router.push('/search');
};

const gotoHistory = () => {
  router.push('/history');
};

const goToLogin = () => {
  router.push('/login');
};

// 初始化
const initialize = async () => {
  await auth.fetchUserInfo();
  if (auth.state.isAuthenticated) {
    fetchAlerts();
  }
};

onMounted(() => {
  initialize();
});
</script>

<style scoped>
.alerts-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.authenticated-content,
.unauthorized-content {
  animation: fadeIn 0.3s ease-in-out;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--el-border-color-lighter);
  background-color: var(--el-fill-color-blank);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.bell-icon {
  font-size: 1.5rem;
  color: var(--el-color-primary);
}

.title-section h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.loading-container {
  padding: 2rem;
}

.alerts-list {
  min-height: 200px;
}

.alert-item {
  padding: 1rem;
  transition: background-color 0.3s ease;
}

.alert-item:hover {
  background-color: var(--el-fill-color-lighter);
}

.alert-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.product-thumbnail {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--el-fill-color-lighter);
  color: var(--el-text-color-placeholder);
}

.product-details {
  flex: 1;
  min-width: 0;
}

.product-name {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.price-info {
  display: flex;
  gap: 1.5rem;
}

.price-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.label {
  color: var(--el-text-color-secondary);
  font-size: 0.875rem;
}

.price {
  font-weight: 600;
  font-size: 1rem;
}

.price.current {
  color: var(--el-color-danger);
}

.price.target {
  color: var(--el-color-success);
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.delete-btn {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.alert-item:hover .delete-btn {
  opacity: 1;
}

.pagination-container {
  padding: 1rem;
  display: flex;
  justify-content: center;
  border-top: 1px solid var(--el-border-color-lighter);
}

.empty-state {
  padding: 4rem 2rem;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  color: var(--el-text-color-placeholder);
}

.empty-text {
  margin-top: 1rem;
  color: var(--el-text-color-secondary);
}

.login-card {
  max-width: 400px;
  margin: 4rem auto;
}

.login-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.login-icon {
  font-size: 1.5rem;
  color: var(--el-color-primary);
}

.login-content {
  text-align: center;
  padding: 2rem 0;
}

.login-btn {
  margin-top: 1.5rem;
}

/* 动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .alerts-container {
    margin: 1rem auto;
  }

  .card-header {
    padding: 1rem;
  }

  .title-section h2 {
    font-size: 1.125rem;
  }

  .product-thumbnail {
    width: 60px;
    height: 60px;
  }

  .price-info {
    flex-direction: column;
    gap: 0.5rem;
  }

  .add-alert-btn span {
    display: none;
  }
}
</style>