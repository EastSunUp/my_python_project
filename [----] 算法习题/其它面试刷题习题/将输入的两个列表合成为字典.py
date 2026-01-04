
list_1 = ["小明", "小红"]
list_2 = ["0301", "0302"]

def soulution(list_a, list_b):
    ret_dic = dict()
    for index, key_val in enumerate(list_a):
        ret_dic[f"{key_val}"] = list_b[index]
    print(f"ret_dic: {ret_dic}")

soulution(list_1, list_2)
