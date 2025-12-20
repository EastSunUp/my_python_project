
'''
    给定一个数字,计算这个数字之内,1到这个数字,其3，6，9出现的次数
    示例-1: num = 10
        则:  1,2,3,4,5,6,7,8,9,
            其中,3,6,9总共出现3次,返回答案为 3
    示例-2: num = 35
        则: 1,2,3,4,5,6,7,8,9,10,
            11,12,13,14,15,16,17,18,19,20,
            21,22,23,24,25,26,27,28,29,30,
            31,32,33,34,
            其中3,6,9共出现15次,分别为:
                3,6,9,13,16,19,23,26,29,30,31,32,33,34,
                其中33出现了两个3,算两次,依次类推,369算3次
    示例-3: num = 100
        则: answer = 60 (具体自己去计算出来这个答案!)

    注意事项:
        num的大小不确定,所以在写代码的时候请考虑num的大小!
'''

def solution(num):
    # 在这⾥写代码
    ans_res = 0

    for i in range(1, num):
        # if (num <= 10)&(i in (3, 6, 9)):
        #     ans_res = ans_res+1
        if (i <10) & (i in (3, 6, 9)):
            ans_res = ans_res +1
        num_cnt = 0
        if i > 10:
            # 计算i一共有几位数(10,两位数; 100,三位数)
            k = 1
            while k <= i:
                num_cnt = num_cnt +1
                k = ( k *10)
            # i =10 , k =100, num_cnt = 2
            cacu_val = i
            for _ in range(num_cnt):
                k = k // 10
                # 取出最高位,计算最高位中是否含有(3,6,9)
                if (cacu_val // k) in (3, 6, 9):
                    ans_res = ans_res +1
                # 减去最高位,继续进行下一轮循环
                cacu_val = cacu_val - (cacu_val//k ) *k

    return ans_res

num=10000
print(f"the answer is {solution(num)}")

