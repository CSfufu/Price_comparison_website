// src/axios.js
import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:5173/api/',
  headers: {
    'Content-Type': 'application/json',
  }
})

// 添加请求拦截器以附加 JWT 令牌// src/axios.js

let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })

  failedQueue = []
}

apiClient.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise(function(resolve, reject) {
          failedQueue.push({ resolve, reject })
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token
          return axios(originalRequest)
        }).catch(err => {
          return Promise.reject(err)
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        // 无刷新令牌，跳转到登录
        window.location.href = '/login'
        return Promise.reject(error)
      }

      try {
        const response = await axios.post('http://127.0.0.1:5173/api/accounts/token/refresh/', {
          refresh: refreshToken
        })
        localStorage.setItem('access_token', response.data.access)
        apiClient.defaults.headers['Authorization'] = 'Bearer ' + response.data.access
        originalRequest.headers['Authorization'] = 'Bearer ' + response.data.access
        processQueue(null, response.data.access)
        return apiClient(originalRequest)
      } catch (err) {
        processQueue(err, null)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

export default apiClient
