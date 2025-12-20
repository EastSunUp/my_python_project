
import threading
import time

balance = 100

def withdraw(amount):
    global balance
    if balance >= amount:
        # 在这里可能被其他线程打断
        time.sleep(0.001)  # 模拟处理时间
        balance -= amount
        return True
    return False

# 两个线程同时执行withdraw(80)
# 可能两个都成功，余额变成-60！

