// src/request.js
import axios from 'axios';
import { Message } from 'element-ui'; // 引入 Element UI 的消息弹框
import router from '@/router'; // 引入 Vue 路由

const request = axios.create({
  baseURL: 'http://192.168.2.219:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  // 添加 validateStatus 配置
  validateStatus: function (status) {
    return status >= 200 && status < 300 || status === 201; // 将 201 视为成功状态
  },
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const isLoginRoute = router.currentRoute.path === '/login';

    if (error.response) {
      const { status } = error.response;

      // 仅在非登录页面执行以下操作
      if (!isLoginRoute) {
        if (status === 401) {
          Message.error('认证失败，请重新登录');
          localStorage.removeItem('token');
          router.push('/login');
        } else if (status === 403) {
          Message.error('无权访问');
        } else if (status === 404) {
          Message.error('请求的资源未找到');
        } else {
          Message.error(error.response.data.message || '请求失败，请稍后再试');
        }
      }
    } else if (!isLoginRoute) {
      Message.error('网络错误，请检查您的网络连接');
    }

    return Promise.reject(error);
  }
);

export default request;
