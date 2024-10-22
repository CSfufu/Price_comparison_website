// src/axios.js
import axios from 'axios';
import auth from './store/auth';

// 创建 Axios 实例
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/', // 根据您的后端地址修改
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器：附加 JWT 令牌
apiClient.interceptors.request.use(
  (config) => {
    const token = auth.state.accessToken;
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器：处理令牌刷新
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });

  failedQueue = [];
};

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // 检查错误是否是由于认证问题引起的，并且是否应该重试
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      // 标记原始请求已重试
      originalRequest._retry = true;

      // 获取 refresh token
      const refreshToken = auth.state.refreshToken;

      // 如果没有 refresh token，执行登出操作
      if (!refreshToken) {
        auth.logout();
        return Promise.reject(error);
      }

      // 处理令牌刷新的并发请求
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers['Authorization'] = 'Bearer ' + token;
            return apiClient(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      isRefreshing = true;

      try {
        // 尝试刷新令牌
        const response = await axios.post(
          'http://localhost:8000/api/token/refresh/', // 根据后端实际路径修改
          { refresh: refreshToken }
        );

        const newAccessToken = response.data.access;

        // 更新令牌
        auth.state.accessToken = newAccessToken;
        localStorage.setItem('accessToken', newAccessToken);

        // 更新请求头
        apiClient.defaults.headers['Authorization'] = 'Bearer ' + newAccessToken;
        originalRequest.headers['Authorization'] = 'Bearer ' + newAccessToken;

        processQueue(null, newAccessToken);

        // 重试原始请求
        return apiClient(originalRequest);
      } catch (err) {
        processQueue(err, null);
        auth.logout();
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
