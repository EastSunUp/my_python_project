
from typing import Callable
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("2048 游戏")
root.geometry("500x600")
# root.resizable(False, False)

def key_pressed(event):
    if event.keysym == "Up":
        print("↑")
    elif event.keysym == "Down":
        print("↓")
    elif event.keysym == "Left":
        print("←")
    elif event.keysym == "Right":
        print("→")
    else:
        print(f"{event.keysym}")    # 打印被按下的按键!


# 标题
title_label = tk.Label(root, text="2048小游戏", font=("Arial", 20, "bold"), fg="#776E65")
title_label.pack(pady=10)
# .pack(): Tkinter 的几何布局管理器,用于将控件放置在父容器中
# pady=10 表示在标签的上方和下方各添加10像素的空白间距
# 这使得标题不会紧贴窗口边缘，视觉效果更美观

# 0
# 颜色设置
colors = {
            0: "#CDC1B4",
            2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179", 16: "#F59563",
            32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72", 256: "#EDCC61",
            512: "#EDC850", 1024: "#EDC53F", 2048: "#EDC22E"
        }

# 游戏网格框架
grid_frame = tk.Frame(root, bg="#BBADA0", padx=1, pady=1)
grid_frame.pack(pady=100)
# 设置按钮?
Button=tk.Button(
                    grid_frame,
                    text="",
                    font=("Arial", 20, "bold"),
                    width=4,
                    height=2,
                    bg=colors[0],
                    fg="#776E65",
                    relief="flat",
                    bd=0
                )
value = 4
# i ,j = 3,3
Button.grid(row=1, column=1, padx=2, pady=2)
Button_2=tk.Button(
                    grid_frame,
                    text="",
                    font=("Arial", 20, "bold"),
                    width=4,
                    height=2,
                    bg=colors[0],
                    fg="#776E65",
                    relief="flat",
                    bd=0
                )
value_2 = 8
# i ,j = 3,3
Button_2.grid(row=4, column=4, padx=2, pady=2)
# Button.config(text="", bg=colors[0], fg="#776E65")
Button.config(text=str(value), bg=colors.get(value, "#3C3A32"),
                                  fg="#F9F6F2" if value > 4 else "#776E65")
# 配置按钮2
Button_2.config(text=str(value_2), bg=colors.get(value_2, "#3C3A32"),
                                  fg="#F9F6F2" if value_2 > 4 else "#776E65")
# ------------------------------------------------------------------------------------------------------------


# 键盘绑定事件
callback: Callable[[tk.Event], None] = key_pressed  # 定义回调函数
root.bind("<Key>", func=callback)
root.focus_set()
# focus_set() 方法用于将键盘焦点设置到指定的窗口或控件上
# root.focus_set() 表示将焦点设置到主窗口（root）

# 界面显示的主循环
root.mainloop()


