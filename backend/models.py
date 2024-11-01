from extensions import db,bcrypt
from datetime import datetime, timezone


# 员工表
class Employee(db.Model):
    __tablename__ = 'employee'  # 表名应使用 __tablename__ 而非 _tablename_
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名，必须唯一
    email = db.Column(db.String(120), unique=True, nullable=False)  # 邮箱，必须唯一
    password_hash = db.Column(db.String(128), nullable=False)  # 哈希后的密码
    full_name = db.Column(db.String(255), nullable=True)  # 全名
    gender = db.Column(db.Boolean, nullable=True)  # 性别
    phone = db.Column(db.String(20), nullable=True)  # 电话号码
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # 注册时间
    last_login = db.Column(db.DateTime, nullable=True)  # 最近登录时间
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # 用户是否活跃
    role = db.Column(db.String(50), default='user', nullable=False)  # 角色：例如 'user' 或 'admin'

    # 设置密码
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # 验证密码
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # 更新最近登录时间
    def update_last_login(self):
        self.last_login = datetime.now(timezone.utc)
        db.session.commit()

    def to_dict(self):
        """将用户模型转换为字典格式，便于 JSON 序列化"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'gender': self.gender,
            'phone': self.phone,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            'last_login': self.last_login.strftime("%Y-%m-%d %H:%M:%S") if self.last_login else None,
            'is_active': self.is_active,
            'role': self.role
        }

# 客户表
class User(db.Model):
    __tablename__ = 'users'  # 表名为 users
    __table_args__ = {'extend_existing': True}  # 允许扩展已有的表

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(255), nullable=False)  # 公司名称，不能为空
    company_address = db.Column(db.String(255), nullable=True)  # 公司地址，允许为空
    contact_name = db.Column(db.String(255), nullable=True)  # 联系人姓名，允许为空
    contact_email = db.Column(db.String(255), unique=True, nullable=False)  # 联系人邮箱，必须唯一且不为空
    contact_phone = db.Column(db.String(50), nullable=True)  # 联系人电话，允许为空
    customer_level = db.Column(db.String(50), nullable=False)  # 客户等级，不能为空（如 VIP、普通客户等）
    contract_path = db.Column(db.String(255), nullable=True)  # 合同文件路径，允许为空

