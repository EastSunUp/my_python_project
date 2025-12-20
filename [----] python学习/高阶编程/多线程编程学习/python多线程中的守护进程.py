
import multiprocessing
import time
 # 守护进程是二等公民
 # TODO: 请补全该部分的代码

# 场景1: 日志监控

def log_monitor():
    """监控日志，不重要，可以随时终止"""
    while True:
     # 检查日志文件
     time.sleep(1)

# 场景2: 数据处理
import multiprocessing
import time


# def process_data(data_chunk):
#     """处理重要数据，必须完成"""
#     result = heavy_computation(data_chunk)
#     save_to_database(result)
#     return result


# if __name__ == "__main__":
#     chunks = split_data()
#     processes = []
#
#     for chunk in chunks:
#         # 非守护进程, 必须保证数据处理完成
#         p = multiprocessing.Process(
#             target=process_data,
#             args=(chunk,),
#             daemon=False  # 默认, 但明确写出来更好
#         )
#         p.start()
#         processes.append(p)
#
#     # 等待所有数据处理完成
#     for p in processes:
#         p.join()
#
#     print("所有数据处理完成")


if __name__ == "__main__":
     # 守护进程，主程序退出时自动结束
     monitor = multiprocessing.Process(target=log_monitor, daemon=True)
     monitor.start()

     # 主程序做重要工作
     time.sleep(10)
     # 主程序结束，监控进程自动终止

     