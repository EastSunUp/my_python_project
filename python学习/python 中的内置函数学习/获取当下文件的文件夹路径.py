

import os

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "data", "file.txt")  # 跨平台路径拼接

# 输出示例: /home/project/data/file.txt
print(f"数据文件路径: {data_path}")

