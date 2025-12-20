
import tkinter as tk


# 1. 鼠标事件：
#     <Button-1>：鼠标左键按下
#     <Button-2>：鼠标中键按下
#     <Button-3>：鼠标右键按下
#     <B1-Motion>：按住左键拖动
#     <ButtonRelease-1>：左键释放
#     <Double-Button-1>：双击左键
#     <Enter>：鼠标指针进入控件
#     <Leave>：鼠标指针离开控件
# 2. 键盘事件：
#     <Key>：任何按键被按下
#     <KeyPress>：同 <Key>
#     <KeyRelease>：按键释放
#     具体按键：如 <KeyPress-A>（按下A键），<KeyPress-Up>（按下上方向键）
# 3. 窗口事件：
#     <Configure>：窗口大小或位置改变
#     <Map>：窗口被映射（例如从最小化恢复）
#     <Unmap>：窗口被取消映射（例如最小化）
#     <Destroy>：窗口被销毁
# 4. 焦点事件：
#     <FocusIn>：控件获得焦点
#     <FocusOut>：控件失去焦点
# 5. 其他事件：
#     <Return>：回车键
#     <Tab>：Tab键
#     <Shift_L>：左Shift键
#     <Control_R>：右Control键


def on_click(event):
    print(f"鼠标点击 at {event.x}, {event.y}")

def on_motion(event):
    print(f"鼠标移动 to {event.x}, {event.y}")

def on_key(event):
    print(f"按键: {event.keysym}")    # 这里指的是电脑的键盘输入

def on_enter(event):
    print("鼠标进入控件")

def on_leave(event):
    print("鼠标离开控件")

def on_resize(event):
    print(f"窗口大小改变: {event.width}x{event.height}")

root = tk.Tk()
root.geometry("400x300")


# 绑定多种事件
root.bind("<Button-1>", on_click)        # 鼠标左键点击
root.bind("<B1-Motion>", on_motion)      # 鼠标拖动
root.bind("<Key>", on_key)               # 键盘按键
root.bind("<Enter>", on_enter)           # 鼠标进入窗口
root.bind("<Leave>", on_leave)           # 鼠标离开窗口
root.bind("<Configure>", on_resize)      # 窗口大小改变

root.focus_set()
root.mainloop()

