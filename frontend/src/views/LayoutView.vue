<template>
  <div>
    <el-container>
      <!-- 头部区域 -->
      <el-header class="app-header">
        <div class="header-left">
          <img src="@/assets/logo.png" alt="Logo" class="app-logo" />
          <span class="app-title">HOGM在线激活系统</span>
        </div>
        <!-- 红色退出登录文本 -->
        <span class="logout-button" @click="logout">退出登录</span>
      </el-header>

      <!-- 侧边栏和主体 -->
      <el-container class="app-container">
        <el-aside class="app-aside" :width="isCollapsed ? '64px' : '200px'">
          <el-scrollbar class="no-scrollbar">
            <el-menu
              :default-active="$route.path"
              router
              class="el-menu-demo"
              :collapse="isCollapsed"
              collapse-transition
            >
              <el-menu-item index="/dashboard">
                <i class="el-icon-s-data"></i>
                <span slot="title" v-if="!isCollapsed">概览</span>
              </el-menu-item>
              <el-menu-item index="/employee">
                <i class="el-icon-s-tools"></i>
                <span slot="title" v-if="!isCollapsed">员工管理</span>
              </el-menu-item>
              <el-menu-item index="/user">
                <i class="el-icon-s-custom"></i>
                <span slot="title" v-if="!isCollapsed">客户管理</span>
              </el-menu-item>
              <el-menu-item index="/key">
                <i class="el-icon-key"></i>
                <span slot="title" v-if="!isCollapsed">授权管理</span>
              </el-menu-item>
              <el-menu-item index="/history">
                <i class="el-icon-s-claim"></i>
                <span slot="title" v-if="!isCollapsed">授权历史</span>
              </el-menu-item>
            </el-menu>
          </el-scrollbar>
        </el-aside>

        <!-- 主体内容 -->
        <el-main class="app-main">
          <router-view /> <!-- 渲染路由内容 -->
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import request from '@/request';

export default {
  name: 'LayoutView',
  data() {
    return {
      isCollapsed: false,
      isMobile: false,
    };
  },
  mounted() {
    window.addEventListener("resize", this.handleResize);
    this.handleResize();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.handleResize);
  },
  methods: {
    handleResize() {
      this.isMobile = window.innerWidth < 768;
      this.isCollapsed = this.isMobile;
    },

    // 退出登录
    async logout() {
      try {
        await this.$confirm('确定退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        });

        // 调用封装的 request 进行 API 请求
        await request.post('/logout');
      } finally {
        // 清除本地 token 并跳转至登录页面
        localStorage.removeItem('token');
        this.$notify({
          title: '成功',
          message: '已退出登录',
          type: 'success',
        });
        this.$router.push('/login');
      }
    }
  },
};
</script>

<style scoped>
/* 样式保持不变 */
.app-header {
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 红色退出登录文本样式 */
.logout-button {
  color: #f56c6c;
  font-weight: bold;
  cursor: pointer;
  padding: 0 10px;
}

.logout-button:hover {
  color: #ff4c4c;
}

.header-left {
  display: flex;
  align-items: center;
}

.app-logo {
  width: 80px;
  margin-right: 10px;
  border-radius: 8px;
}

.app-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.app-container {
  min-height: calc(100vh - 64px);
  display: flex;
  flex-direction: row;
  padding: 6px 4px 6px 4px;
}

.app-aside {
  background-color: #ffffff;
  border-right: 1px solid #ebeef5;
  transition: width 0.5s linear;
  overflow: hidden;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.no-scrollbar >>> .el-scrollbar__wrap {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.no-scrollbar >>> .el-scrollbar__wrap::-webkit-scrollbar {
  display: none;
}

.no-scrollbar >>> .el-scrollbar__bar {
  display: none !important;
}

.app-main {
  background-color: #f5f7fa;
  padding: 20px;
  overflow: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  margin-left: 10px;
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .app-header {
    justify-content: space-between;
    padding: 5px;
  }
  .app-logo {
    width: 50px;
  }
  .app-title {
    font-size: 18px;
  }
}
</style>
