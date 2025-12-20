

'''
    在 Python 中，with open() 是一种上下文管理器（Context Manager），用于安全高效地处理文件操作。
    它自动管理文件的打开和关闭，确保资源被正确释放，即使发生异常也能保证文件关闭。

    参数详解
    参数	            说明	                        常见值
    file_path	    文件路径（必选）	            'data.txt', './docs/test.md'
    mode	        文件打开模式（可选，默认 'r'）	'r', 'w', 'a', 'r+' 等
    encoding	    文本编码（可选，默认系统编码）	'utf-8', 'gbk', 'latin-1'
    newline	        换行控制（可选）	            None（通用换行）, '\n', '\r\n'
    errors	        编解码错误处理（可选）	        'strict', 'ignore', 'replace'

    文件模式详解
    模式	    全称	        功能
    r	    read	    只读（默认）。文件必须存在,否则报错 FileNotFoundError
    w	    write	    写入。创建新文件/覆盖已有文件。注意：会清空原内容！
    a	    append	    追加。在文件末尾写入,保留原内容
    x	    create	    排他创建。文件必须不存在,否则报错 FileExistsError
    b	    binary	    二进制模式（需组合使用）,如 'rb', 'wb'
    t	    text	    文本模式（默认）
    +	    update	    读写模式（需组合使用）,如 'r+', 'w+'

    场景	            推荐模式
    读取文本文件	    'r' 或 'rt'
    写入新文本文件	    'w'
    追加日志文件	    'a'
    读写二进制数据	    'rb'/'wb'
    需要修改已有文件	'r+'

    with open() 写法的核心优势:
        1.自动关闭文件:   无需手动调用 file.close()
        2.异常安全:      即使代码块中出现异常,文件也会被正确关闭
        3.代码简洁:      减少样板代码，提高可读性
'''
import os


# os.path.abspath
file_path = os.path.dirname(os.path.abspath(__file__))

# 基础语法
with open(file_path, mode='r', encoding=None) as file_object:
    # 在此代码块中操作文件
    data = file_object.read()
# 退出代码块后文件自动关闭

# ------------------------------------------------------------------------------------------
# 读取文件
# 读取整个文件
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# ------------------------------------------------------------------------------------------
# 写入文件
# 覆盖写入（文件不存在则创建）
with open('output.txt', 'w') as f:
    f.write("Hello World!\n")
    f.writelines(["Line1\n", "Line2\n"])

# 追加写入
with open('log.txt', 'a') as f:
    f.write("New log entry\n")

# ------------------------------------------------------------------------------------------
# 二进制文件操作
# 复制图片
with open('input.jpg', 'rb') as src, open('copy.jpg', 'wb') as dst:
    dst.write(src.read())

# ------------------------------------------------------------------------------------------
# 读写混合模式
# 修改文件内容
with open('data.txt', 'r+') as f:
    content = f.read()
    f.seek(0)  # 移动指针到文件头
    f.write("New Header\n" + content)

# ------------------------------------------------------------------------------------------
# 逐行读取（推荐大文件）
with open('log.txt') as f:
    for line in f:
        print(line.strip())  # .strip() 移除行尾换行符


with open('data.txt') as f:
    data = f.read()
# 此处文件已关闭

# ------------------------------------------------------------------------------------------
# 以下为危险写法
f = open('data.txt')
try:
    data = f.read()
finally:
    f.close()  # 必须手动关闭


