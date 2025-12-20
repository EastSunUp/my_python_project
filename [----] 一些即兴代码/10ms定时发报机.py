
"""
    从机每10ms发一次报文,主机需要及时处理,
    研究主机在不及时处理从机信息的情况下可能产生的bug
"""
import time


def slave(status, message):
    print(f"status: {status}, message: {message}")
    pass

def master():
    message = [[True, 2], [True,6], [True,3], [True,5], [True,8], [True,0],
               [True,8], [True,3], [True,7], [True,9], [True,1], [True,7],
               [True,8], [True,8], [True,2], [True,7], [True,8], [True,8],
               [True,3], [True,9], [True,1], [True,13], [True,6], [True,9],
               [True,2], [True,6], [True,3], [True,3], [True,1], [True,8],
               [True,3], [True,1], [True,6], [True,8], [True,3], [True,9]]
    timestamp = time.perf_counter()
    timestamp_2 = time.time()
    mes_cnt = 0
    entry_times = 0
    new_entry_times = 0
    missed_message = 0  # 统计丢失信息帧数
    while True:
        if time.perf_counter()- timestamp >= 0.01:
            timestamp = time.perf_counter()
            new_entry_times = new_entry_times +1
            print(f"1 new_entry_times: {new_entry_times}")
            print(f"1 entry_times: {entry_times}")

        if new_entry_times - entry_times == 1:
            entry_times = 0
            new_entry_times = 0
        # print(f"spend entry time: {time.perf_counter()- timestamp}")
            if mes_cnt == 36:
                mes_cnt = 0
                print("------------------------------# another loop #------------------------------")
            slave(message[mes_cnt][0], message[mes_cnt][1])
            mes_cnt = mes_cnt + 1
            # 注入休眠故障状态 !    (休眠11ms)
            time.sleep(0.015)
            # 时间戳记录运行时长 ---------------------------------------------
            print(f"spend time: {time.time() - timestamp_2} s")
            timestamp_2 = time.time()
        elif new_entry_times - entry_times > 1:
            missed_message = new_entry_times - entry_times
            print(f"missed_message: {missed_message}")
            new_entry_times = 0
            entry_times = 0
        else:
            pass

        if time.perf_counter() - timestamp >= 0.01:
            # timestamp = time.perf_counter()
            new_entry_times = new_entry_times + 1
            print("! warning -----------------------")
            print(f"2 new_entry_times: {new_entry_times}")
            print(f"2 entry_times: {entry_times}")

        if missed_message >= 5:
            print(f"error: missed_message {missed_message}!")
            break


master()


