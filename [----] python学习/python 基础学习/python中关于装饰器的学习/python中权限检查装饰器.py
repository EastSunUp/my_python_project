

from functools import wraps

def require_login(required_role="user"):
    """权限检查装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if not user.get('is_authenticated', False):
                raise PermissionError("用户未登录")
            if required_role not in user.get('roles', []):
                raise PermissionError(f"需要{required_role}权限")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

# 使用权限检查装饰器
@require_login(required_role="admin")
def delete_user(user, username):
    print(f"用户 {username} 已被 {user['name']} 删除")

# 测试
user_admin = {'name': 'Alice', 'is_authenticated': True, 'roles': ['admin', 'user']}
user_guest = {'name': 'Bob', 'is_authenticated': True, 'roles': ['user']}

try:
    delete_user(user_admin, "Charlie")
    delete_user(user_guest, "Dave")
except PermissionError as e:
    print(f"权限错误: {e}")
