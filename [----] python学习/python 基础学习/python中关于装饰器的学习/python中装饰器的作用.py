

"""
装饰器的主要作用:
    代码复用 - 将通用功能封装成装饰器,避免重复代码
    功能扩展 - 为现有函数添加新功能而不修改其内部实现
    权限检查 - 验证用户权限或参数合法性
    日志记录 - 自动记录函数调用信息
    性能测试 - 测量函数执行时间
    事务处理 - 管理数据库事务等
"""

import time
from functools import wraps

# 计时装饰器
def timer_decorator(func):
    @wraps(func)  # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper

# 使用装饰器
@timer_decorator
def calculate_sum(n):
    """计算1到n的和"""
    return sum(range(1, n+1))

# 测试
result = calculate_sum(100)
print(f"计算结果: {result}")