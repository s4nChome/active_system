# create_admin.py
from app import db, app
from models import Employee

with app.app_context():
    # 检查是否已经存在 admin 用户
    # if not Employee.query.filter_by(username="admin1").first():
    #     # 创建用户实例
        admin_user = Employee(username="admin", email="admin@example.com",role="admin")
        admin_user.set_password("123456")  # 使用 set_password 方法加密密码

        # 将用户添加到会话并提交
        db.session.add(admin_user)
        db.session.commit()

        print("Admin user created successfully!")
    # else:
    #     print("Admin user already exists!")
