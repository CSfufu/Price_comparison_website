<!-- src/components/SetPriceAlertModal.vue -->
<template>
  <el-dialog
    v-model="dialogVisible"
    title="设置降价提醒"
    width="500px"
    :teleport="'body'"
    :modal="true"
    :lock-scroll="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <!-- 表单内容 -->
    <el-form :model="alertForm" label-width="100px">
      <!-- 商品名称显示 -->
      <el-form-item label="商品名称">
        <span>{{ product.name }}</span>
      </el-form-item>

      <!-- 当前价格显示 -->
      <el-form-item label="当前价格">
        <span>￥{{ product.price }}</span>
      </el-form-item>

      <!-- 目标价格输入 -->
      <el-form-item label="目标价格">
        <el-input-number
          v-model="alertForm.target_price"
          :min="0"
          :step="0.01"
          placeholder="请输入目标价格"
          style="width: 100%;"
        ></el-input-number>
      </el-form-item>

      <!-- 通知方式选择 -->
      <el-form-item label="通知方式">
        <el-checkbox-group v-model="alertForm.notification_methods">
          <el-checkbox label="email">邮件</el-checkbox>
          <!-- 可以根据需要添加其他通知方式 -->
        </el-checkbox-group>
      </el-form-item>
    </el-form>

    <!-- 弹窗底部按钮 -->
    <template #footer>
      <el-button @click="closeDialog">取消</el-button>
      <el-button type="primary" @click="submitAlert" :loading="loading">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, reactive } from 'vue';
import axios from '@/axios.js'; // 确保 axios 实例配置正确
import { ElMessage } from 'element-plus';

// 定义组件接收的 props
const props = defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
  product: {
    type: Object,
    required: true,
  },
});

// 定义组件发出的事件
const emit = defineEmits(['update:visible']);

// 创建一个本地的可变状态 `dialogVisible`，并与 `props.visible` 同步
const dialogVisible = ref(props.visible);

// 监听 `props.visible` 的变化，同步到 `dialogVisible`
watch(
  () => props.visible,
  (newVal) => {
    dialogVisible.value = newVal;
  }
);

// 监听 `dialogVisible` 的变化，向父组件同步
watch(
  dialogVisible,
  (newVal) => {
    emit('update:visible', newVal);
  }
);

// 定义表单数据
const alertForm = reactive({
  product: null, // 商品 ID
  target_price: null, // 目标价格
  notification_methods: [], // 通知方式数组
});

// 监听 `props.product` 的变化，更新 `alertForm.product`
watch(
  () => props.product,
  (newProduct) => {
    if (newProduct && newProduct.id) {
      alertForm.product = newProduct.id;
    }
  },
  { immediate: true }
);

// 定义 loading 状态
const loading = ref(false);

// 关闭弹窗的方法
const closeDialog = () => {
  dialogVisible.value = false;
  resetForm();
};

// 重置表单数据的方法
const resetForm = () => {
  alertForm.target_price = null;
  alertForm.notification_methods = [];
};

// 提交表单的方法
const submitAlert = async () => {
  // 表单验证
  if (alertForm.target_price === null || alertForm.target_price === undefined) {
    ElMessage.warning('请设置目标价格');
    return;
  }

  if (alertForm.notification_methods.length === 0) {
    ElMessage.warning('请选择至少一种通知方式');
    return;
  }

  loading.value = true;

  try {
    // 发送 POST 请求到后端创建降价提醒
    await axios.post('alerts/', {
      product: alertForm.product,
      target_price: alertForm.target_price,
      notification_methods: alertForm.notification_methods,
    });

    ElMessage.success('降价提醒设置成功');
    closeDialog();
  } catch (error) {
    console.error('设置降价提醒失败', error);
    if (error.response && error.response.data) {
      // 后端返回的错误信息
      const errorMsg = Object.values(error.response.data).flat().join(' ');
      ElMessage.error(`设置降价提醒失败: ${errorMsg}`);
    } else {
      ElMessage.error('设置降价提醒失败，请稍后重试');
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.el-dialog__body {
  padding: 20px 20px 0 20px;
}

.el-form-item {
  margin-bottom: 20px;
}
</style>
