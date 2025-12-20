

# 该代码由AI生成.
# TODO 这个文件的代码不见了,记得之前是有代码的,请补齐该文件的代码
# 使用消息队列传递线程间的消息与数据.

import threading
import queue
import time


class MessageHandler:
    def __init__(self):
        self.message_queue = queue.Queue()
        self.running = True

    def thread_a(self):
        """线程A：每隔10ms发送消息"""
        count = 0
        while self.running:
            # 构造消息
            message = f"Message from A - {count}"
            # 发送到队列
            self.message_queue.put(("A", message))
            count += 1
            time.sleep(0.01)  # 10ms

    def thread_b(self):
        """线程B：接收并处理消息"""
        while self.running:
            try:
                # 阻塞获取消息，可设置超时
                source, message = self.message_queue.get(timeout=1.0)
                if source == "A":
                    self.handle_message_from_a(message)
                # 可以扩展处理其他来源的消息
                self.message_queue.task_done()
            except queue.Empty:
                # 超时，可以执行其他操作或继续等待
                continue

    def handle_message_from_a(self, message):
        """处理来自线程A的消息"""
        print(f"B received: {message}")
        # 具体的消息处理逻辑

    def start(self):
        thread_a = threading.Thread(target=self.thread_a)
        thread_b = threading.Thread(target=self.thread_b)

        thread_a.daemon = True
        thread_b.daemon = True

        thread_a.start()
        thread_b.start()

    def stop(self):
        self.running = False


