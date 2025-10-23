from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# 1. 初始化 Flask 应用和 SQLAlchemy
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# 配置 SQLite 数据库 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 2. 定义数据模型 (Model) - 对应数据库中的一张表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """将用户对象转换为字典，方便后续序列化为 JSON"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }


# 3. 创建数据库表（只在第一次运行时创建）
with app.app_context():
    db.create_all()


# 4. ----------- CRUD 操作的核心路由 -----------

# Create (增): 创建一个新用户
@app.route('/users', methods=['POST'])
def create_user():
    """接收 JSON 数据,创建新用户"""
    data = request.get_json()

    # 简单的数据校验
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({"error": "Missing username or email"}), 400

    # 检查用户是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 409

    # 创建 User 模型实例
    new_user = User(username=data['username'], email=data['email'])

    # 添加到数据库会话并提交
    db.session.add(new_user)
    db.session.commit()

    # 返回创建成功的用户信息
    return jsonify(new_user.to_dict()), 201


# Read (查): 获取用户列表或单个用户
# 获取所有用户
@app.route('/users', methods=['GET'])
def get_all_users():
    """从数据库获取所有用户"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


# 根据ID获取单个用户
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """根据ID获取单个用户"""
    user = User.query.get_or_404(user_id)  # 如果找不到返回404
    return jsonify(user.to_dict())


# Update (改): 更新某个用户的信息
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """根据ID更新用户信息"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    # 更新字段（如果请求中提供了的话）
    if 'username' in data:
        # 检查新用户名是否与他人重复
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"error": "Username already taken"}), 409
        user.username = data['username']
    if 'email' in data:
        # 检查新邮箱是否与他人重复
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"error": "Email already in use"}), 409
        user.email = data['email']

    # 提交更改
    db.session.commit()
    return jsonify(user.to_dict())


# Delete (删): 删除某个用户
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """根据ID删除用户"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user_id} has been deleted"}), 200


# 5. 运行应用
if __name__ == '__main__':
    app.run(debug=True)
