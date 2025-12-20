
import time
# 低优先级任务永远得不到执行
import threading

high_priority_lock = threading.Lock()

def high_priority_task():
    while True:
        with high_priority_lock:
            # 长期占用资源
            time.sleep(0.1)

def low_priority_task():
    # 这个任务永远拿不到锁
    with high_priority_lock:
        print("这个可能永远不会执行")

