
""" attention: 这份代码由AI给出!"""

import time


def advanced_single_thread_simulation():
    """进阶单线程模拟 - 尝试模拟并发效果"""
    send_interval_ms = 10
    process_time_ms = 15  # 处理时间 > 发送间隔
    simulation_duration_ms = 1000

    # 状态变量
    message_queue = []
    current_processing = None
    process_start_time = None
    last_completion_time = None
    simulation_start = time.time()

    print("时间(ms) | 事件 | 队列长度 | 测量间隔(ms)")
    print("-" * 45)

    current_time_ms = 0
    while current_time_ms < simulation_duration_ms:
        current_time = time.time()
        current_time_ms = (current_time - simulation_start) * 1000

        # 1. 检查是否应该发送新消息
        if int(current_time_ms) % send_interval_ms == 0:
            message_id = int(current_time_ms / send_interval_ms)
            message_queue.append({
                'id': message_id,
                'arrival_time': current_time_ms
            })
            print(f"{current_time_ms:7.1f} | 发送消息{message_id} | {len(message_queue):8} |")

        # 2. 检查是否可以开始处理下一条消息
        if current_processing is None and message_queue:
            # 开始处理新消息
            current_processing = message_queue.pop(0)
            process_start_time = current_time_ms
            print(f"{current_time_ms: 7.1f} | 开始处理消息{current_processing['id']} | {len(message_queue): 8} |")

        # 3. 检查当前处理的消息是否完成
        if (current_processing is not None and
                current_time_ms - process_start_time >= process_time_ms):

            # 完成处理, 进行测量
            if last_completion_time is not None:
                interval = current_time_ms - last_completion_time
                print(
                    f"{current_time_ms: 7.1f} | 完成消息{current_processing['id']} | {len(message_queue): 8} | {interval: 13.1f}")
            else:
                print(f"{current_time_ms: 7.1f} | 完成消息{current_processing['id']} | {len(message_queue): 8} |")

            last_completion_time = current_time_ms
            current_processing = None

        # 微小延迟, 避免CPU占用过高
        time.sleep(0.001)


print("进阶单线程模拟（处理时间15ms > 发送间隔10ms）:")
advanced_single_thread_simulation()


