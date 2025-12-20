
import time
import threading


lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1():
    with lock_a:
        time.sleep(0.1)  # 确保thread_2拿到lock_b
        with lock_b:     # 这里会永远等待
            print("Thread 1")

def thread_2():
    with lock_b:
        time.sleep(0.1)  # 确保thread_1拿到lock_a
        with lock_a:     # 这里会永远等待
            print("Thread 2")