<template>
  <div>
    <!-- 新增员工按钮 -->
    <el-button
      plain
      type="primary"
      @click="openAddDialog"
      style="margin-bottom: 20px;"
    >新增员工</el-button>

    <!-- 员工表格 -->
    <el-table
      :data="tableData"
      stripe
      style="width: 100%"
      v-loading="loading"
    >
      <el-table-column prop="username" label="用户名" width="180" />
      <el-table-column prop="full_name" label="姓名" />
      <el-table-column label="性别">
        <template #default="scope">
          {{ formatGender(scope.row.gender) }}
        </template>
      </el-table-column>
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="phone" label="电话" />
      <el-table-column prop="created_at" label="创建时间" />
      <el-table-column prop="last_login" label="最近登录" />
      <el-table-column label="账号状态">
        <template #default="scope">
          <el-switch
            v-model="scope.row.is_active"
            active-color="#13ce66"
            inactive-color="#ff4949"
            @change="confirmStatusChange(scope.row)"
          />
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button
            plain
            type="success"
            @click="openEditDialog(scope.row)"
            size="small"
          >修改</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <div style="text-align: center; margin-top: 20px;">
      <el-pagination
        background
        layout="prev, pager, next, sizes, total"
        :total="total"
        :page-size="pageSize"
        :current-page.sync="currentPage"
        @current-change="fetchTableData"
        @size-change="handleSizeChange"
      />
    </div>

    <!-- 新增/修改员工对话框 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="25%"
      @before-close="handleDialogClose"
    >
      <el-form
        ref="userForm"
        :model="currentForm"
        :rules="rules"
        label-width="80px"
        class="demo-ruleForm"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="currentForm.username"
            autocomplete="off"
            :disabled="isEdit"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            type="password"
            v-model="currentForm.password"
            show-password
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            type="password"
            v-model="currentForm.confirmPassword"
            show-password
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input
            v-model="currentForm.full_name"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="currentForm.gender">
            <el-radio :label="true">男</el-radio>
            <el-radio :label="false">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="currentForm.email"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="currentForm.phone"
            autocomplete="off"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button
          v-if="!isEdit"
          plain
          type="danger"
          @click="resetForm"
        >清空</el-button>
        <el-button
          plain
          type="success"
          @click="submitForm"
        >{{ isEdit ? '保存' : '添加' }}</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import request from '@/request';

export default {
  data() {
    return {
      loading: false,
      dialogVisible: false,
      isEdit: false,
      dialogTitle: '新增员工',
      currentForm: {
        id: null,
        username: '',
        password: '',
        confirmPassword: '',
        full_name: '',
        gender: null,
        email: '',
        phone: '',
      },
      rules: {}, // 动态设置验证规则
      addRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, message: '用户名至少需要3个字符', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码至少需要6个字符', trigger: 'blur' },
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value !== this.currentForm.password) {
                callback(new Error('两次输入的密码不一致'));
              } else {
                callback();
              }
            },
            trigger: 'blur',
          },
        ],
        full_name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' },
        ],
        email: [
          { required: true, message: '请输入有效的邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' },
        ],
        phone: [
          { required: true, message: '请输入有效的手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' },
        ],
      },
      editRules: {
        password: [
          { min: 6, message: '密码至少需要6个字符', trigger: 'blur' },
        ],
        confirmPassword: [
          {
            validator: (rule, value, callback) => {
              if (value) {
                if (value !== this.currentForm.password) {
                  callback(new Error('两次输入的密码不一致'));
                } else {
                  callback();
                }
              } else {
                callback();
              }
            },
            trigger: 'blur',
          },
        ],
        full_name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' },
        ],
        email: [
          {
            validator: (rule, value, callback) => {
              if (value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(value)) {
                  callback(new Error('请输入正确的邮箱格式'));
                } else {
                  callback();
                }
              } else {
                callback();
              }
            },
            trigger: 'blur',
          },
        ],
        phone: [
          {
            validator: (rule, value, callback) => {
              if (value) {
                const phoneRegex = /^1[3-9]\d{9}$/;
                if (!phoneRegex.test(value)) {
                  callback(new Error('手机号格式不正确'));
                } else {
                  callback();
                }
              } else {
                callback();
              }
            },
            trigger: 'blur',
          },
        ],
      },
      tableData: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
    };
  },
  created() {
    this.fetchTableData();
  },
  methods: {
    openAddDialog() {
      this.isEdit = false;
      this.dialogTitle = '新增员工';
      this.dialogVisible = true;
      this.rules = this.addRules; // 使用新增规则
      this.currentForm = {
        id: null,
        username: '',
        password: '',
        confirmPassword: '',
        full_name: '',
        gender: null,
        email: '',
        phone: '',
      };
      this.$nextTick(() => {
        this.resetForm();
      });
    },
    openEditDialog(row) {
      this.isEdit = true;
      this.dialogTitle = '修改员工信息';
      this.dialogVisible = true;
      this.rules = this.editRules; // 使用修改规则
      this.currentForm = {
        id: row.id,
        username: row.username,
        password: '',
        confirmPassword: '',
        full_name: row.full_name,
        gender: row.gender,
        email: row.email,
        phone: row.phone,
      };
      this.$nextTick(() => {
        if (this.$refs.userForm) {
          this.$refs.userForm.clearValidate();
        }
      });
    },
    async fetchTableData() {
      this.loading = true;
      try {
        const response = await request.get('/employees', {
          params: { page: this.currentPage, limit: this.pageSize },
        });
        this.tableData = response.data || [];
        this.total = response.total || 0;
      } catch (error) {
        this.$notify.error({
          title: '加载失败',
          message: '无法获取员工数据',
        });
      } finally {
        this.loading = false;
      }
    },
    handleSizeChange(newSize) {
      this.pageSize = newSize;
      this.fetchTableData();
    },
    async submitForm() {
      this.$refs.userForm.validate(async (valid) => {
        if (valid) {
          try {
            if (this.isEdit) {
              await this.updateEmployee();
            } else {
              await this.addEmployee();
            }
            this.dialogVisible = false;
            this.fetchTableData();
            this.$notify.success({
              title: '成功',
              message: `员工${this.isEdit ? '更新' : '添加'}成功！`,
            });
          } catch (error) {
            // 错误处理逻辑
            if (error.response && error.response.status === 409) {
              const errorMsg = error.response.data.msg;
              if (errorMsg === 'Username already exists') {
                this.$notify.error({
                  title: '错误',
                  message: '用户名已存在，请更换用户名',
                });
              } else if (errorMsg === 'Email already exists') {
                this.$notify.error({
                  title: '错误',
                  message: '邮箱已存在，请更换邮箱',
                });
              } else {
                this.$notify.error({
                  title: '错误',
                  message: errorMsg || '操作失败',
                });
              }
            } else {
              this.$notify.error({
                title: '错误',
                message: `${this.isEdit ? '更新' : '添加'}员工失败`,
              });
            }
          }
        }
      });
    },
    async addEmployee() {
      await request.post('/employees', this.currentForm);
      this.resetForm();
    },
    async updateEmployee() {
      const updateData = {};
      Object.keys(this.currentForm).forEach((key) => {
        if (
          this.currentForm[key] !== '' &&
          this.currentForm[key] !== null &&
          key !== 'id' &&
          key !== 'username' // 用户名不允许修改
        ) {
          updateData[key] = this.currentForm[key];
        }
      });
      await request.put(`/employees/${this.currentForm.id}`, updateData);
    },
    resetForm() {
      if (this.$refs.userForm) {
        this.$refs.userForm.resetFields();
      }
    },
    async confirmStatusChange(row) {
      const newStatus = row.is_active;
      try {
        await request.put(`/employees/${row.id}/status`, {
          is_active: newStatus,
        });
        this.$notify.success({
          title: '成功',
          message: `员工 ${row.username} 的状态已更新`,
        });
      } catch (error) {
        row.is_active = !newStatus; // 回滚状态
        this.$notify.error({
          title: '错误',
          message: '状态更新失败',
        });
      }
    },
    formatGender(value) {
      return value ? '男' : '女';
    },
    handleDialogClose(done) {
      this.resetForm(); // 重置表单
      this.dialogVisible = false; // 关闭对话框
      done(); // 完成关闭操作
    },
  },
};
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
