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

    <!-- 新增员工对话框 -->
    <el-dialog
      title="新增员工"
      :visible.sync="addDialogVisible"
      width="25%"
      @before-close="handleAddDialogClose"
    >
      <el-form
        ref="addUserForm"
        :model="addForm"
        :rules="addRules"
        label-width="80px"
        class="demo-ruleForm"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="addForm.username"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            type="password"
            v-model="addForm.password"
            show-password
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            type="password"
            v-model="addForm.confirmPassword"
            show-password
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input
            v-model="addForm.full_name"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="addForm.gender">
            <el-radio :label="true">男</el-radio>
            <el-radio :label="false">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="addForm.email"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="addForm.phone"
            autocomplete="off"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button
          plain
          type="danger"
          @click="resetAddForm"
        >清空</el-button>
        <el-button
          plain
          type="success"
          @click="submitAddForm"
        >添加</el-button>
      </div>
    </el-dialog>

    <!-- 修改员工对话框 -->
    <el-dialog
      :title="editDialogTitle"
      :visible.sync="editDialogVisible"
      width="25%"
      @before-close="handleEditDialogClose"
    >
      <el-form
        ref="editUserForm"
        :model="editForm"
        :rules="editRules"
        label-width="80px"
        class="demo-ruleForm"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="editForm.username"
            autocomplete="off"
            :disabled="true"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            type="password"
            v-model="editForm.password"
            show-password
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            type="password"
            v-model="editForm.confirmPassword"
            show-password
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input
            v-model="editForm.full_name"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="editForm.gender">
            <el-radio :label="true">男</el-radio>
            <el-radio :label="false">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="editForm.email"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="editForm.phone"
            autocomplete="off"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button
          plain
          type="danger"
          @click="resetEditForm"
        >重置</el-button>
        <el-button
          plain
          type="success"
          @click="submitEditForm"
        >保存</el-button>
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
      // 新增员工对话框
      addDialogVisible: false,
      addForm: {
        username: '',
        password: '',
        confirmPassword: '',
        full_name: '',
        gender: null,
        email: '',
        phone: '',
      },
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
              if (value !== this.addForm.password) {
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
      // 修改员工对话框
      editDialogVisible: false,
      editDialogTitle: '修改员工信息',
      editForm: {
        id: null,
        username: '',
        password: '',
        confirmPassword: '',
        full_name: '',
        gender: null,
        email: '',
        phone: '',
      },
      editRules: {
        password: [
          { min: 6, message: '密码至少需要6个字符', trigger: 'blur' },
        ],
        confirmPassword: [
          {
            validator: (rule, value, callback) => {
              if (value) {
                if (value !== this.editForm.password) {
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
    // 打开新增员工对话框
    openAddDialog() {
      this.addDialogVisible = true;
      this.resetAddForm();
      this.$nextTick(() => {
        if (this.$refs.addUserForm) {
          this.$refs.addUserForm.clearValidate();
        }
      });
    },
    // 提交新增员工表单
    async submitAddForm() {
      this.$refs.addUserForm.validate(async (valid) => {
        if (valid) {
          try {
            await this.addEmployee();
            this.addDialogVisible = false;
            this.fetchTableData();
            this.$notify.success({
              title: '成功',
              message: '员工添加成功！',
            });
          } catch (error) {
            this.handleAddError(error);
          }
        }
      });
    },
    // 添加员工
    async addEmployee() {
      await request.post('/employees', this.addForm);
      this.resetAddForm();
    },
    // 重置新增员工表单
    resetAddForm() {
      this.addForm = {
        username: '',
        password: '',
        confirmPassword: '',
        full_name: '',
        gender: null,
        email: '',
        phone: '',
      };
      if (this.$refs.addUserForm) {
        this.$refs.addUserForm.resetFields();
      }
    },
    // 处理新增员工错误
    handleAddError(error) {
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
          message: '添加员工失败',
        });
      }
    },
    // 关闭新增员工对话框时的处理
    handleAddDialogClose(done) {
      this.resetAddForm();
      done();
    },
    // 打开修改员工对话框
    openEditDialog(row) {
      this.editDialogVisible = true;
      this.editForm = {
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
        if (this.$refs.editUserForm) {
          this.$refs.editUserForm.clearValidate();
        }
      });
    },
    // 提交修改员工表单
    async submitEditForm() {
      this.$refs.editUserForm.validate(async (valid) => {
        if (valid) {
          try {
            await this.updateEmployee();
            this.editDialogVisible = false;
            this.fetchTableData();
            this.$notify.success({
              title: '成功',
              message: '员工信息更新成功！',
            });
          } catch (error) {
            this.handleEditError(error);
          }
        }
      });
    },
    // 更新员工
    async updateEmployee() {
      const updateData = {};
      Object.keys(this.editForm).forEach((key) => {
        if (
          this.editForm[key] !== '' &&
          this.editForm[key] !== null &&
          key !== 'id' &&
          key !== 'username' // 用户名不允许修改
        ) {
          updateData[key] = this.editForm[key];
        }
      });
      await request.put(`/employees/${this.editForm.id}`, updateData);
      this.resetEditForm();
    },
    // 重置修改员工表单
    resetEditForm() {
      this.editForm = {
        id: null,
        username: '',
        password: '',
        confirmPassword: '',
        full_name: '',
        gender: null,
        email: '',
        phone: '',
      };
      if (this.$refs.editUserForm) {
        this.$refs.editUserForm.resetFields();
      }
    },
    // 处理修改员工错误
    handleEditError(error) {
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
          message: '更新员工失败',
        });
      }
    },
    // 关闭修改员工对话框时的处理
    handleEditDialogClose(done) {
      this.resetEditForm();
      done();
    },
    // 获取员工表格数据
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
    // 处理分页大小变化
    handleSizeChange(newSize) {
      this.pageSize = newSize;
      this.fetchTableData();
    },
    // 切换员工账号状态
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
    // 格式化性别显示
    formatGender(value) {
      return value ? '男' : '女';
    },
  },
};
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
