<!-- src/views/ProductDetail.vue -->
<!-- src/views/ProductDetail.vue -->
<template>
  <div class="product-detail-container">

    <!-- 商品详情卡片 -->
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
          <!-- 添加“查看历史价格”按钮 -->
          <el-button type="success" @click="fetchPriceHistory" class="history-button">
            查看历史价格
          </el-button>
          <el-button type="warning" @click="openAlertModal" class="alert-button">
            设置降价提醒
          </el-button>
        </el-col>
      </el-row>
    </el-card>


    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <el-spin size="large" tip="正在加载价格历史，请稍候...">
        <div class="content"></div>
      </el-spin>
    </div>

    <!-- 价格历史图表 -->
    <div v-if="priceHistory.length > 0" class="chart-container">
      <!-- 时间范围选择器 -->
      <div class="time-range-selector">
        <el-radio-group v-model="selectedRange" @change="updateChartData">
          <el-radio-button label="7d">7天</el-radio-button>
          <el-radio-button label="1m">1个月</el-radio-button>
          <el-radio-button label="1y">1年</el-radio-button>
          <el-radio-button label="all">全部</el-radio-button>
        </el-radio-group>
      </div>

      <el-card>
        <h3>价格历史趋势</h3>
        <v-chart :option="chartOptions" autoresize style="height: 400px;"></v-chart>
      </el-card>
    </div>

    <!-- 无价格历史数据 -->
    <div v-else-if="priceHistory.length === 0 && hasSearched && !loading">
      <el-empty description="未找到价格历史数据" />
    </div>

    <SetPriceAlertModal
        v-if="product"
      :visible="alertModalVisible"
      :product="product"
      @update:visible="alertModalVisible = $event"
    />

  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '../axios';
import { ElMessage, ElButton, ElIcon, ElRadioGroup, ElRadioButton } from 'element-plus';
import { ArrowLeft } from '@element-plus/icons-vue';
import SetPriceAlertModal from '../components/SetPriceAlertModal.vue';


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

const route = useRoute();
const router = useRouter();
const product = ref(null);
const loading = ref(false);

// 价格历史相关变量
const priceHistory = ref([]);
const filteredPriceHistory = ref([]);
const hasSearched = ref(false);
const selectedRange = ref('all');

// 引用 ECharts 组件
const VChart = ECharts;

const alertModalVisible = ref(false);
const emit = defineEmits(['update:visible']);

const openAlertModal = () => {
  console.log('设置降价提醒按钮被点击');
  alertModalVisible.value = true;
};

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

// 跳转到购买链接
const goToBuy = (link) => {
  if (link && (link.startsWith('http://') || link.startsWith('https://'))) {
    window.open(link, '_blank');
  } else {
    ElMessage.warning('无效的购买链接');
  }
};

// 获取商品详情
const getProductDetail = async () => {
  const productId = route.params.id;
  if (!productId) {
    ElMessage.error('无效的商品 ID');
    return;
  }

  try {
    const response = await axios.get(`products/${productId}/`);
    product.value = response.data;
  } catch (error) {
    console.error('获取商品详情失败', error);
    ElMessage.error('获取商品详情失败，请稍后重试');
  }
};

// 处理价格历史查询
const fetchPriceHistory = async () => {
  if (!product.value || !product.value.link) {
    ElMessage.error('无法获取商品链接');
    return;
  }

  loading.value = true;
  hasSearched.value = true;

  try {
    // 调用后端 API 获取价格历史
    const response = await axios.post(
      'products/price_history/',
      {
        item_url: product.value.link.trim(),
      },
      {
        timeout: 20000,
      }
    );

    if (response.status === 200) {
      const data = response.data;
      // 更新价格历史数据
      priceHistory.value = data.price_history;
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

// 在组件挂载时获取商品详情
onMounted(() => {
  getProductDetail();
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

.history-button {
  margin-left: 10px;
}

.chart-container {
  margin-top: 40px;
}

.time-range-selector {
  margin: 20px 0;
  text-align: center;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
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

