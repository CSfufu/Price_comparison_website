<!-- src/views/PriceHistory.vue -->
<template>
  <div class="price-history-container">
    <!-- 用户已认证时显示的内容 -->
    <div v-if="auth.state.isAuthenticated">
      <!-- 输入商品链接 -->
      <el-card class="input-card">
        <el-form @submit.prevent="handleSubmit">
          <el-form-item>
            <el-input
              v-model="productLink"
              placeholder="请输入商品链接"
              clearable
              @keyup.enter.native="handleSubmit"
            >
              <template #prepend>
                <el-icon><Link /></el-icon>
              </template>
              <template #append>
                <el-button type="primary" @click="handleSubmit">查询</el-button>
              </template>
            </el-input>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <el-spin size="large" tip="正在加载价格历史，请稍候...">
          <div class="content"></div>
        </el-spin>
      </div>

      <!-- 价格历史和商品信息 -->
      <div v-else-if="priceHistory.length > 0" class="content-container">
        <!-- 商品信息卡片 -->
        <el-card class="product-info-card">
          <el-row :gutter="20" align="middle">
            <el-col :span="6">
              <img :src="product.image_url" alt="商品图片" class="product-image" />
            </el-col>
            <el-col :span="18">
              <h2>{{ product.name }}</h2>
              <el-link :href="product.link" target="_blank" class="product-link">查看商品</el-link>
            </el-col>
          </el-row>
        </el-card>

        <!-- 时间范围选择器 -->
        <div class="time-range-selector">
          <el-radio-group v-model="selectedRange" @change="updateChartData">
            <el-radio-button label="7d">7天</el-radio-button>
            <el-radio-button label="1m">1个月</el-radio-button>
            <el-radio-button label="1y">1年</el-radio-button>
            <el-radio-button label="all">全部</el-radio-button>
          </el-radio-group>
        </div>

        <!-- 价格历史图表 -->
        <div class="chart-container">
          <el-card>
            <h3>价格历史</h3>
            <v-chart :option="chartOptions" autoresize style="height: 400px;"></v-chart>
          </el-card>
        </div>
      </div>

      <!-- 无价格历史数据 -->
      <div v-else-if="!loading && hasSearched">
        <el-empty description="未找到价格历史数据">
          <el-button type="primary" @click="reset">重新查询</el-button>
        </el-empty>
      </div>
    </div>

    <!-- 用户未认证时显示的提示 -->
    <div v-else class="login-prompt">
      <el-empty description="请登录之后再查看价格历史">
        <template #image>
          <el-icon size="64"><User /></el-icon>
        </template>
        <template #description>
          您尚未登录，请先 <router-link to="/login">登录</router-link> 以查看价格历史。
        </template>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from '../axios'; // 确保 axios 已正确配置
import { ElMessage, ElIcon } from 'element-plus';
import { User, Link } from '@element-plus/icons-vue'; // 导入 User 和 Link 图标
import auth from '../store/auth'; // 引入 auth 模块

// 导入 Vue ECharts 组件
import ECharts from 'vue-echarts';
import { use } from 'echarts/core';
// 引入 ECharts 组件
import {
  CanvasRenderer
} from 'echarts/renderers';
import {
  LineChart
} from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent
} from 'echarts/components';

// 注册 ECharts 组件
use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent
]);

const router = useRouter();

// 引用 ECharts 组件
const VChart = ECharts;

// 定义响应式变量
const productLink = ref('');
const product = ref({});
const priceHistory = ref([]);
const filteredPriceHistory = ref([]); // 过滤后的价格历史数据
const loading = ref(false);
const hasSearched = ref(false); // 标识是否已进行过查询
const selectedRange = ref('all'); // 用户选择的时间范围

// 定义图表配置
const chartOptions = computed(() => ({
  title: {
    text: '价格历史趋势',
    left: 'center',
  },
  tooltip: {
    trigger: 'axis',
    formatter: '{b}<br/>价格: ￥{c}',
  },
  xAxis: {
    type: 'category',
    data: filteredPriceHistory.value.map(item => item.date),
    boundaryGap: false,
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      formatter: '￥{value}',
    },
  },
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 100,
    },
    {
      start: 0,
      end: 100,
    },
  ],
  series: [
    {
      name: '价格',
      type: 'line',
      data: filteredPriceHistory.value.map(item => item.price),
      smooth: true,
      markPoint: {
        data: [
          { type: 'max', name: '最高价' },
          { type: 'min', name: '最低价' },
        ],
      },
    },
  ],
}));

// 处理表单提交
const handleSubmit = () => {
  if (!productLink.value.trim()) {
    ElMessage.warning('请输入商品链接');
    return;
  }
  fetchPriceHistory();
};

// 异步获取商品价格历史数据
const fetchPriceHistory = async () => {
  loading.value = true;
  hasSearched.value = true;

  try {
    // 调用后端 API 获取价格历史
    const response = await axios.post(
      'products/price_history/',
      {
        item_url: productLink.value.trim(),
      },
      {
        timeout: 20000,
      }
    );

    if (response.status === 200) {
      const data = response.data;
      product.value = {
        name: data.name,
        link: data.link,
        image_url: data.image_url,
      };
      priceHistory.value = data.price_history;

      // 根据选择的时间范围更新过滤后的数据
      updateChartData();
    } else {
      ElMessage.error('无法获取价格历史数据');
      priceHistory.value = [];
      filteredPriceHistory.value = [];
    }
  } catch (error) {
    console.error('获取价格历史数据失败', error);
    ElMessage.error('获取价格历史数据失败，请稍后重试');
    priceHistory.value = [];
    filteredPriceHistory.value = [];
  } finally {
    loading.value = false;
  }
};

// 根据选择的时间范围更新过滤后的数据
const updateChartData = () => {
  if (selectedRange.value === 'all') {
    filteredPriceHistory.value = priceHistory.value;
  } else {
    const now = new Date();
    let startDate;

    if (selectedRange.value === '7d') {
      // 最近7天
      startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    } else if (selectedRange.value === '1m') {
      // 最近1个月
      startDate = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate());
    } else if (selectedRange.value === '1y') {
      // 最近1年
      startDate = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate());
    }

    filteredPriceHistory.value = priceHistory.value.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= startDate && itemDate <= now;
    });
  }
};

// 重置查询
const reset = () => {
  productLink.value = '';
  product.value = {};
  priceHistory.value = [];
  filteredPriceHistory.value = [];
  hasSearched.value = false;
  selectedRange.value = 'all';
};
</script>

<style scoped>
.price-history-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px;
}

.input-card {
  padding: 20px;
  background-color: #f9f9f9;
}

.content-container {
  margin-top: 20px;
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

.time-range-selector {
  margin: 20px 0;
  text-align: center;
}

.chart-container {
  margin-top: 20px;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}

.login-prompt {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
}
</style>
