
# TODO 文件需要commit
import time

class Hello:
    def print_hi(self,name):
        # Use a breakpoint in the code line below to debug your script.
        print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.

class Timer_Acquirer(object):

    def Get_sys_time(self):
        sys_time=time.perf_counter()
        print(f'the sys time is {sys_time} ')

    def Get_Sys_time_ns(self):
        print('we begin get system time !')
        sys_ns=time.process_time_ns()
        print(f'the system time by ns is {sys_ns} !')

    def Delay_One_Second(self):
        print('we begin to delay !')
        time.sleep(1)
        print(f'the time has delayed one second')

    def User_Delayer(self, seconds= None):
        print(f'you have defined delay {seconds} s !')
        time.sleep(seconds)
        print(f'the time has delayed {seconds} second')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Case=Hello()
    Case.print_hi('PyCharm')

    Delayer=Timer_Acquirer()
    Delayer.Get_sys_time()
    Delayer.Get_Sys_time_ns()