
# 这份代码是我自己自主编写的代码,微信聊天记录可查!
# TODO 这个文件的代码不见了,记得之前是有代码的,请补齐该文件的代码
# 代码内容补齐日期: 2025/07/11

# 查找数组中无重复最长的数字占用长度
class soulution:

    def __init__(self):
        pass

    def find_min_length(self, target_list):
        head = 0
        ans = 0
        temp_solve = []

        # 找出目标列表中的最大值,以用于哈希表映射处理
        max_val = -99999999
        for no in range(len(target_list)):
            if target_list[no] > max_val:
                max_val = max(target_list[no], max_val)
        print(f'the max val of list is {max_val}')
        # 对哈希表进行初始化
        for no in range(max_val+1):
            temp_solve.append(0)
        print(f'temp_solve:{temp_solve}')

        for tail in range(len(target_list)):
            if temp_solve[target_list[tail]] == 0:
                temp_solve[target_list[tail]] = 1 # 如果已经遍历, 则标记这个数字
                tem_cnt = tail - head + 1
                ans = max(tem_cnt, ans)
            else:
                # 找出最近的相等值的位置
                nearst_no  = 0
                for no in range(tail - 1):
                    if target_list[no] == target_list[tail]:
                        nearst_no = no
                print(f'nearst_no:{nearst_no}, tail :{tail}')
                # 去除最近相等值之前的值的标记, 并将头指针移动到这个位置的后一个位置
                for no in range(nearst_no):
                    temp_solve[target_list[no]] = 0
                # print(f'The temp_solve after handle is {temp_solve}')
                head = nearst_no+1
        print(f'the answer is {ans}')

data_list=[12,13,15,14,16,22,29,30,13,12,15,16]
sin_list =[1 , 2, 3, 0, 4, 0, 0, 0, 2, 1, 3, 4]
MyRun=soulution()
MyRun.find_min_length(target_list=data_list)


