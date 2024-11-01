import Vue from 'vue';
import VueRouter from 'vue-router';
import Layout from '@/views/LayoutView.vue';
import LoginView from '@/views/LoginView.vue';
import EmployeeView from '@/views/EmployeeView.vue';
import DashboardView from '@/views/DashboardView.vue';
import UserView from '@/views/UserView.vue';
import KeyView from '@/views/KeyView.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    children: [
      {
        path: '/dashboard',
        name: 'dashboard',
        component: DashboardView
      },
      {
        path: '/employee',
        name: 'employee',
        component: EmployeeView
      },
      {
        path: '/user',
        name: 'user',
        component: UserView
      },
      {
        path: '/key',
        name: 'key',
        component: KeyView
      }
    ]
  },

];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

// 路由守卫，限制未登录用户访问登录页以外的页面
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token'); // 假设 token 保存在 localStorage 中
  
  if (!isAuthenticated && to.name !== 'login') {
    // 如果没有 token 且访问的不是登录页，则重定向到登录页
    next({ name: 'login' });
  } else if (isAuthenticated && to.name === 'login') {
    // 如果已登录但访问的是登录页，重定向到主页（或其他默认页面）
    next({ name: 'Layout' });
  } else {
    next(); // 放行
  }
});

export default router;
