
"""
    介绍了关于Tk页面生成库的使用
    pack、grid、place
"""

import tkinter as tk
from tkinter import ttk


class LayoutDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter 布局管理器演示")
        self.root.geometry("800x600")

        # 创建标签页(横向每个都是一页)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)  # 打包并显示对应内容?

        # 为每种布局创建标签页
        self.create_pack_tab()
        self.create_grid_tab()
        self.create_place_tab()
        self.create_comparison_tab()

    def create_pack_tab(self):
        """pack() 布局演示"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="pack() 布局")

        # 说明
        label = tk.Label(frame, text="pack() 按顺序排列控件，适合简单布局",
                         font=("Arial", 12), fg="blue")
        label.pack(pady=10)

        # 演示 pack
        demo_frame = tk.Frame(frame, bg="lightgray", height=300)
        demo_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # 创建一些按钮展示 pack 布局
        btn1 = tk.Button(demo_frame, text="按钮1 (pack top)", bg="red", fg="white")
        btn1.pack(pady=5)

        btn2 = tk.Button(demo_frame, text="按钮2 (pack bottom)", bg="green", fg="white")
        btn2.pack(pady=5)

        btn3 = tk.Button(demo_frame, text="按钮3 (pack left)", bg="blue", fg="white")
        btn3.pack(side='left', padx=5)

        btn4 = tk.Button(demo_frame, text="按钮4 (pack right)", bg="orange", fg="white")
        btn4.pack(side='right', padx=5)

        # pack 布局特点
        features = """
pack() 布局特点:
• 按添加顺序自动排列控件
• 可以使用 side 参数控制方向 (top, bottom, left, right)
• 简单易用，适合快速布局
• 不适合复杂网格状布局
"""
        info = tk.Label(frame, text=features, justify='left', font=("Arial", 10))
        info.pack(pady=10)

    def create_grid_tab(self):
        """grid() 布局演示"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="grid() 布局")

        # 说明
        label = tk.Label(frame, text="grid() 按行和列排列控件，适合表格布局",
                         font=("Arial", 12), fg="blue")
        label.pack(pady=10)

        # 演示 grid
        demo_frame = tk.Frame(frame, bg="lightgray", height=300)
        demo_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # 创建3x3网格按钮
        for i in range(3):
            for j in range(3):
                btn = tk.Button(demo_frame, text=f"({i},{j})",
                                bg="purple", fg="white", width=8)
                btn.grid(row=i, column=j, padx=2, pady=2)

        # 创建一个跨列的按钮
        btn_wide = tk.Button(demo_frame, text="跨两列", bg="darkred", fg="white")
        btn_wide.grid(row=3, column=0, columnspan=2, sticky='ew', padx=2, pady=5)

        # 创建一个跨行的按钮
        btn_tall = tk.Button(demo_frame, text="跨\n两\n行", bg="darkgreen", fg="white")
        btn_tall.grid(row=0, column=3, rowspan=2, sticky='ns', padx=5, pady=2)

        # grid 布局特点
        features = """
grid() 布局特点:
• 基于行和列的网格系统
• 适合表格、表单等规整布局
• 支持跨行(rowspan)和跨列(columnspan)
• 可以使用 sticky 参数控制控件在单元格内的对齐
• 非常适合2048这类网格游戏
"""
        info = tk.Label(frame, text=features, justify='left', font=("Arial", 10))
        info.pack(pady=10)

    def create_place_tab(self):
        """place() 布局演示"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="place() 布局")

        # 说明
        label = tk.Label(frame, text="place() 使用绝对或相对坐标定位，适合精确控制",
                         font=("Arial", 12), fg="blue")
        label.pack(pady=10)

        # 演示 place
        demo_frame = tk.Frame(frame, bg="lightgray", height=300)
        demo_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # 使用绝对坐标放置按钮
        btn1 = tk.Button(demo_frame, text="(50,30)", bg="brown", fg="white")
        btn1.place(x=50, y=30)

        # 使用相对坐标放置按钮
        btn2 = tk.Button(demo_frame, text="右下角", bg="teal", fg="white")
        btn2.place(relx=0.9, rely=0.9, anchor='se')

        # 使用相对坐标居中
        btn3 = tk.Button(demo_frame, text="居中", bg="navy", fg="white")
        btn3.place(relx=0.5, rely=0.5, anchor='center')

        # 使用相对大小
        btn4 = tk.Button(demo_frame, text="半宽", bg="maroon", fg="white")
        btn4.place(relx=0.1, rely=0.1, relwidth=0.5, height=30)

        # place 布局特点
        features = """
place() 布局特点:
• 使用绝对坐标(x,y)或相对坐标(relx,rely)
• 可以精确控制位置和大小
• 支持相对定位和相对大小
• 布局不会自动调整，需要手动计算位置
• 适合需要精确定位的特殊控件
"""
        info = tk.Label(frame, text=features, justify='left', font=("Arial", 10))
        info.pack(pady=10)

    def create_comparison_tab(self):
        """三种布局对比"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="布局对比")

        # 说明
        label = tk.Label(frame, text="三种布局管理器对比和选择指南",
                         font=("Arial", 12, "bold"), fg="darkred")
        label.pack(pady=10)

        # 对比表格
        comparison_text = """
布局选择指南:

1. pack() - 简单顺序布局
   适用场景:
   • 简单的垂直或水平排列
   • 快速原型开发
   • 工具栏、状态栏
   示例:
     label.pack()
     button.pack(side='left')

2. grid() - 表格网格布局  
   适用场景:
   • 表单、数据表格
   • 棋盘类游戏(如2048)
   • 任何需要行列对齐的界面
   示例:
     button.grid(row=0, column=1)

3. place() - 精确位置布局
   适用场景:
   • 自定义图形界面
   • 游戏中的精灵定位
   • 需要重叠控件的情况
   示例:
     button.place(x=100, y=50)

通用建议:
• 优先使用 grid(), 它最灵活
• 简单布局用 pack() 更快捷
• 非必要时避免使用 place()
• 不要在同一个容器中混用多种布局管理器
"""
        comparison = tk.Label(frame, text=comparison_text, justify='left',
                              font=("Arial", 10), bg="lightyellow")
        comparison.pack(pady=10, padx=20, fill='both', expand=True)


# 运行演示
if __name__ == "__main__":
    root = tk.Tk()
    app = LayoutDemo(root)
    root.mainloop()
