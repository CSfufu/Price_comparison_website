// 创建 auth.js 模块，集中管理认证状态，供各个组件使用

// src/store/auth.js
import { reactive } from 'vue';
import axios from '../axios';

const state = reactive({
  username: '',
  accessToken: localStorage.getItem('accessToken') || null,
  refreshToken: localStorage.getItem('refreshToken') || null,
  isAuthenticated: !!localStorage.getItem('accessToken'),
});
const fetchUserInfo = async () => {
  if (state.isAuthenticated && !state.username) {
    try {
      const response = await axios.get('accounts/me');
      state.username = response.data.username;
    } catch (error) {
      logout();
    }
  }
};

const login = (accessToken, refreshToken) => {
  localStorage.setItem('accessToken', accessToken);
  localStorage.setItem('refreshToken', refreshToken);
  state.accessToken = accessToken;
  state.refreshToken = refreshToken;
  state.isAuthenticated = true;
  fetchUserInfo();
};

const logout = async () => {
  try {
    await axios.post('accounts/logout/', {
      refresh: state.refreshToken,
    });
  } catch (error) {
    console.error('登出失败', error);
  } finally {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    state.accessToken = null;
    state.refreshToken = null;
    state.username = '';
    state.isAuthenticated = false;
  }
};

export default {
  state,
  fetchUserInfo,
  login,
  logout,
};
