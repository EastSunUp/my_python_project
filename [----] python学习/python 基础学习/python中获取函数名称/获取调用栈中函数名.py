
import traceback
import inspect

def function_a():
    function_b()

def function_b():
    function_c()

def function_c():
    # 获取调用栈信息
    stack = inspect.stack()
    print("调用栈:")
    for frame_info in stack:
        print(f"- {frame_info.function} (文件: {frame_info.filename}, 行: {frame_info.lineno})")

    # 或者使用 traceback
    print("\n使用 traceback:")
    for line in traceback.format_stack():
        print(line.strip())

function_a()

