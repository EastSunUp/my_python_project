"""
    设计一个函数,可以传入一个或多个单词的字符串,并返回该字符串,但所有五个或更多字母的单词都前后颠倒。
    示例1
        输入：str = "This is a test"
        输出："This is a test"
    示例2
        输入：str = "This is another test"
        输出："This is rehtona test"

    注1：传入的字符串仅包含字母和空格
    注2：仅当存在多个单词时才包含空格
    要求(时间复杂度与空间复杂度不能超标!)
        输入范围：只包含字母和空格的字符串，可能包含一个或多个单词
        时间复杂度：O (n)，其中 n 是输入字符串的长度
        空间复杂度：O (n)
"""

# str = "This is a testa test"
str = "This is another test"
def solution(str):

    words = str.split() # 分离单词
    # print(f"words:{words}")
    need_change_cnt = 0
    change_index = []*len(words)
    print(f"len(words): {len(words)}")

    # 找出长度大于5的单词 (记录这个单词的位置,第几个单词)
    for i in range(len(words)):
        if len(words[i])>=5:
            need_change_cnt = need_change_cnt+1
            print(f"{words[i]}")    # print(f"{words[i][0]}")
            change_index.append(i)
            # temp = ""
            # for k in range(len(words[i])):
            #     temp = temp+words[i][(len(words[i])-k-1)]
            # words[i] = temp
            # print(f"{words[i]}")

    # 翻转长度大于5的单词
    for i in range(len(change_index)):
        temp = ""
        for k in range(len(words[change_index[i]])):
            temp = temp+words[change_index[i]][(len(words[change_index[i]])-k-1)]
        words[change_index[i]] = temp
    print(f"change index is {change_index}")

    # 设置输出结果格式,不同情况对应不同输出结果形式
    return_str=""
    if need_change_cnt != 0:
        if len(words) == 1:
            return_str = return_str + words[change_index[0]]
        else:
            for i in range(len(words)):
                if i != (len(words)-1):
                    return_str = return_str+words[i]+" "
                else:
                    return_str = return_str + words[i]
    else:
        return_str = return_str + str
    print(f"return_str:{return_str}")
    return return_str

def solution_1(str):
    pass
    # for index, char in enumerate(str):
    #     if char == " ":  # 直接比较空格字符
    #         print(f"空格位置：索引 {index}")

    # index_list = []*len(str)
    # for index, char in enumerate(str):
    #     if char == " ":  # 直接比较空格字符
    #         index_list.append(index)
    # print(f"空格位置: 索引 {index_list}")
    #
    # #  change_index=()
    # for i in range(len(index_list)):
    #     if index_list[i] - index_list[i - 1] > 5:
    #         print(f"空格位置: 索引 {index_list[i-1]}")
    #     else:
    #         print("no need to change !")

    # index_list = [] * len(str)

    # for index, char in enumerate(str):
    #     if char == " ":  # 直接比较空格字符
    #         index_list.append(index)
    # for i in rang(len(index_list)):
    #     if index_list[i] - index_list[i - 1] > 5:
    #         print(f"空格位置：索引 {index_list}")
    # print(f"空格位置：索引 {index_list}")

solution(str)

