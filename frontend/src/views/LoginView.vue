<!-- 登录 -->

<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="login-title">欢迎登录</h2>
      <el-form :model="form" :rules="rules" ref="loginForm" label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            type="password"
            v-model="form.password"
            show-password
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm" class="login-button">登录</el-button>
        </el-form-item>
      </el-form>
      <p v-if="error" class="error">{{ error }}</p>
    </el-card>
  </div>
</template>

<script>
import request from '@/request';

export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      error: '',
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    };
  },
methods: {
  async submitForm() {
    this.$refs.loginForm.validate(async (valid) => {
      if (valid) {
        try {
          const response = await request.post('/login', {
            username: this.form.username,
            password: this.form.password
          });

          // 假设后端返回的 JWT 存储在 localStorage 中
          localStorage.setItem('token', response.access_token);
          this.$notify({
            title: '成功',
            message: '登录成功',
            type: 'success'
          });
          this.$router.push('/'); // 跳转到 Dashboard 或其他受保护页面
        } catch (error) {
          // 检查错误响应并根据状态码设置错误消息
          if (error.response) {
            if (error.response.status === 403) {
              this.error = '账号已被停用，请联系管理员';
            } else if (error.response.status === 401) {
              this.error = '用户名或密码错误';
            } else {
              this.error = '登录失败，请稍后再试';
            }
          } else {
            // 如果请求失败或未收到响应
            this.error = '无法连接服务器，请检查网络连接';
          }
        }
      }
    });
  }
}

};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  width: 400px;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
}

.error {
  color: red;
  text-align: center;
  font-size: 14px;
  margin-top: 15px;
}
</style>