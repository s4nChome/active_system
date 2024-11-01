# app.py
from flask import Flask
from config import Config
from flask_cors import CORS
from extensions import db, bcrypt, jwt  # 从 extensions 中导入已经实例化的 jwt
from api import api_blueprint  # 导入 api_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)  # 使用 extensions 中的 jwt 实例

    # 启用 CORS，允许所有来源访问
    CORS(app)

    # 注册蓝图
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app

app = create_app()


# # 创建数据库表
# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
