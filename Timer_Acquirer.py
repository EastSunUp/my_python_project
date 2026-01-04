

# TODO 文件需要commit
import time


class TimerAcquirer(object):

    def __init__(self):
        pass

    def get_sys_time(self):
        sys_time=time.perf_counter()
        print(f'the sys time is {sys_time} ')

    def get_sys_time_ns(self):
        print('we begin get system time !')
        sys_ns=time.process_time_ns()
        print(f'the system time by ns is {sys_ns} !')

    def delay_one_second(self):
        print('we begin to delay !')
        time.sleep(1)
        print(f'the time has delayed one second')

    def user_delayer(self, seconds= None):
        print(f'you have defined delay {seconds} s !')
        time.sleep(seconds)
        print(f'the time has delayed {seconds} second')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Delayer=TimerAcquirer()
    Delayer.get_sys_time()
    Delayer.get_sys_time_ns()


