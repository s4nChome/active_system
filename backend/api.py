# api.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from extensions import db, bcrypt, jwt  # 从 extensions 中导入 jwt 实例
from models import Employee
from datetime import datetime

api_blueprint = Blueprint('api', __name__)

# 创建一个 blocklist 集合来存储已失效的 token JTI
blocklist = set()

# 注销接口
@api_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # 获取 token 的唯一标识符（JWT ID）
    blocklist.add(jti)      # 将 JTI 添加到 blocklist 中，标记为失效
    return jsonify({"msg": "Logout successful"}), 200

# 使用 jwt.token_in_blocklist_loader 装饰器检查 token 是否失效
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blocklist  # 如果 token 在 blocklist 中，则表示已失效

# 登录接口
@api_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # 查询用户是否存在
    employee = Employee.query.filter_by(username=username).first()
    if employee and bcrypt.check_password_hash(employee.password_hash, password):
        # 如果账号密码正确，检查账号状态
        if employee.is_active == 0:
            return jsonify({"msg": "Account has been deactivated"}), 403

        # 更新 last_login 字段
        employee.last_login = datetime.now()
        db.session.commit()

        # 返回访问令牌
        access_token = create_access_token(identity=employee.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid username or password"}), 401



# 创建新员工的接口，只有经过身份验证的用户才能访问
@api_blueprint.route("/employees", methods=["POST"])
@jwt_required()
def create_employee():
    # 获取请求中的数据
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Invalid request data"}), 400
    
    # 检查必填字段
    required_fields = ["username", "password", "email", "full_name", "gender", "phone"]
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"{field} is required"}), 400

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    full_name = data.get("full_name")
    gender = data.get("gender")  # Expecting boolean: True for male, False for female
    phone = data.get("phone")

    # 检查用户名和邮箱是否已存在
    if Employee.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 409
    if Employee.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 409

    # 创建新的员工实例
    new_employee = Employee(
        username=username,
        email=email,
        full_name=full_name,
        gender=gender,
        phone=phone,
        created_at=datetime.now(),
        is_active=True,  # 默认激活状态
        role='user'  # 默认角色
    )
    
    # 设置密码
    new_employee.set_password(password)

    # 将新员工添加到数据库
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"msg": "Employee created successfully", "employee": new_employee.to_dict()}), 201

# 获取员工列表并支持分页的接口
@api_blueprint.route("/employees", methods=["GET"])
@jwt_required()
def get_employees():
    # 获取分页参数，默认为第一页，每页10条
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    # 计算总员工数
    total = Employee.query.count()

    # 查询指定页的数据
    employees = (
        Employee.query
        .order_by(Employee.created_at.desc())  # 按创建时间倒序排列
        .paginate(page=page, per_page=limit, error_out=False)
        .items
    )

    # 转换为字典格式
    employees_data = [employee.to_dict() for employee in employees]

    # 返回分页数据和总数
    return jsonify({
        "data": employees_data,
        "total": total
    }), 200


# 更新员工状态
@api_blueprint.route("/employees/<int:employee_id>/status", methods=["PUT"])
@jwt_required()
def update_employee_status(employee_id):
    data = request.get_json()
    new_status = data.get("is_active")

    if new_status is None:
        return jsonify({"msg": "Missing 'is_active' field in request"}), 400

    # 查找员工
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"msg": "Employee not found"}), 404

    # 更新员工的状态
    employee.is_active = new_status
    db.session.commit()

    return jsonify({"msg": "Employee status updated successfully", "is_active": employee.is_active}), 200

@api_blueprint.route("/employees/<int:employee_id>", methods=["PUT"])
@jwt_required()
def update_employee(employee_id):
    data = request.get_json()
    employee = Employee.query.get_or_404(employee_id)
    
    # 更新字段
    if 'password' in data and data['password']:
        employee.set_password(data['password'])
    employee.full_name = data.get('full_name', employee.full_name)
    employee.gender = data.get('gender', employee.gender)
    employee.email = data.get('email', employee.email)
    employee.phone = data.get('phone', employee.phone)
    
    db.session.commit()
    return jsonify({"msg": "Employee updated successfully"}), 200



# 受保护的路由示例
@api_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = Employee.query.get(current_user_id)
    return jsonify(username=user.username, email=user.email), 200
