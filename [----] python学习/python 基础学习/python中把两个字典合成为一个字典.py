

# 1.使用 update() 方法（原地修改）
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

dict1.update(dict2)
print(dict1)  # 输出: {'a': 1, 'b': 3, 'c': 4}

# -----------------------------------------------------------------------------------------
# 2.使用字典解包（Python 3.5+）
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

merged_dict = {**dict1, **dict2}
print(merged_dict)  # 输出: {'a': 1, 'b': 3, 'c': 4}

# -----------------------------------------------------------------------------------------
# 3.使用 | 合并运算符（Python 3.9+）
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

merged_dict = dict1 | dict2
print(merged_dict)  # 输出: {'a': 1, 'b': 3, 'c': 4}

# -----------------------------------------------------------------------------------------
# 4.使用字典推导式
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

merged_dict = {k: v for d in [dict1, dict2] for k, v in d.items()}
print(merged_dict)  # 输出: {'a': 1, 'b': 3, 'c': 4}

# -----------------------------------------------------------------------------------------
# 使用 collections.ChainMap
from collections import ChainMap

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

chain = ChainMap(dict1, dict2)
print(dict(chain))  # 输出: {'a': 1, 'b': 2, 'c': 4}


