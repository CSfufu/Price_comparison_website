<!-- src/components/SetPriceAlertModal.vue -->
<template>
  <el-dialog
    v-model="dialogVisible"
    title="设置降价提醒"
    width="500px"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <el-form
      ref="formRef"
      :model="alertForm"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="商品名称">
        <span>{{ product.name }}</span>
      </el-form-item>

      <el-form-item label="当前价格">
        <span class="price">￥{{ product.price }}</span>
      </el-form-item>

      <el-form-item
        label="目标价格"
        prop="target_price"
      >
        <el-input-number
          v-model="alertForm.target_price"
          :min="0"
          :max="product.price"
          :precision="2"
          :step="0.01"
          style="width: 100%"
          placeholder="请输入目标价格"
        />
        <div class="price-tip">目标价格必须低于当前价格</div>
      </el-form-item>

      <el-form-item label="通知方式">
        <div v-if="userEmail" class="notification-info">
          <el-tag size="small" type="info">
            降价时将通过邮箱 {{ userEmail }} 通知您
          </el-tag>
        </div>
        <div v-else class="notification-warning">
          <el-alert
            type="warning"
            show-icon
            :closable="false"
            title="未获取到邮箱信息，请刷新页面重试"
          />
        </div>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button
        type="primary"
        :loading="loading"
        :disabled="!userEmail"
        @click="submitForm"
      >
        确定
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from '@/axios'
import auth from '@/store/auth'

const props = defineProps({
  visible: {
    type: Boolean,
    required: true
  },
  product: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:visible', 'success'])

// 表单ref
const formRef = ref(null)

// 对话框可见性
const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

// 用户邮箱
const userEmail = computed(() => auth.state.email)

// 表单数据
const alertForm = reactive({
  product: null,
  target_price: null
})

// 表单验证规则
const rules = {
  target_price: [
    { required: true, message: '请输入目标价格', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (!value) {
          callback(new Error('请输入目标价格'))
        } else if (value >= props.product.price) {
          callback(new Error('目标价格必须低于当前价格'))
        } else if (value <= 0) {
          callback(new Error('目标价格必须大于0'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
}

// 加载状态
const loading = ref(false)

// 监听product变化
watch(() => props.product, (newProduct) => {
  if (newProduct?.id) {
    alertForm.product = newProduct.id
  }
}, { immediate: true })

// 组件挂载时确保用户信息已加载
onMounted(async () => {
  if (auth.state.isAuthenticated && !auth.state.username) {
    try {
      await auth.fetchUserInfo()
    } catch (error) {
      ElMessage.error('用户信息加载失败，请重新登录')
    }
  } else if (!auth.state.isAuthenticated) {
    ElMessage.warning('请先登录以设置降价提醒')
    emit('update:visible', false) // Close dialog if not authenticated
  }
})

const handleClose = () => {
  emit('update:visible', false)
}

const submitForm = async () => {
  if (alertForm.target_price >= props.product.price || !alertForm.target_price) {
    ElMessage.error('目标价格无效')
    return
  }

  loading.value = true
  try {
    console.log("Sending data:", {
      product_id: props.product.product_id,
      target_price: alertForm.target_price,
      email: userEmail.value,
      active: true
    });
    // Assuming you need to send a request to save the alert
    const response = await axios.post('alerts/create/', {
      product_id: props.product.product_id, // 确保使用正确的字段名
      target_price: alertForm.target_price,
      email: userEmail.value,
      active: true
    });


    ElMessage.success('降价提醒已设置')
    emit('success')
    handleClose()
  } catch (error) {
  if (error.response) {
    console.error('Server Error:', error.response);
    ElMessage.error(`错误: ${error.response.data.detail || '请求失败'}`);
  } else if (error.request) {
    console.error('Network Error:', error.request);
    ElMessage.error('网络错误，请稍后重试');
  } else {
    console.error('Error:', error.message);
    ElMessage.error('发生未知错误');
  }
} finally {
    loading.value = false
  }
}
</script>


<style scoped>
.price {
  color: #ff4d4f;
  font-weight: 500;
  font-size: 16px;
}

.price-tip {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.notification-info {
  margin: 8px 0;
}

.notification-warning {
  margin: 8px 0;
}
</style>