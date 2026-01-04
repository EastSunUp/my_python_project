
# 推荐使用pygame包进行游戏开发
# 这个文件本身是没有代码的,属于空文件
# TODO 后续有空记得补充完善相应代码内容

import tkinter as tk
from tkinter import messagebox
import random
import copy

class Game2048:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2048 游戏")
        # self.root.geometry("700x1050")
        self.root.resizable(False, False)

        # 游戏状态
        self.grid_size = 8
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0

        # 颜色配置
        self.colors = {
            0: "#CDC1B4",
            2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179", 16: "#F59563",
            32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72", 256: "#EDCC61",
            512: "#EDC850", 1024: "#EDC53F", 2048: "#EDC22E"
        }

        self.setup_ui()
        self.add_random_brick()
        self.add_random_brick()
        self.update_display()

        # 绑定键盘事件
        self.root.bind("<Key>", self.key_pressed)
        self.root.focus_set()   # 只有当窗口位于最前端的时候才有效 ?

    def setup_ui(self):
        # 标题
        title_label = tk.Label(self.root, text="2048小游戏", font=("Arial", 32, "bold"), fg="#776E65")
        title_label.pack(pady=10)

        # 分数显示
        self.score_label = tk.Label(self.root, text=f"当前分数: {self.score}", font=("Arial", 16), fg="#776E65")
        self.score_label.pack(pady=5)

        # 游戏说明
        instruction_label = tk.Label(self.root, text="使用方向键移动,相同数字会合并", font=("Arial", 12),
                                     fg="#776E65")
        instruction_label.pack(pady=5)

        # 游戏网格框架
        self.grid_frame = tk.Frame(self.root, bg="#BBADA0", padx=10, pady=10)
        self.grid_frame.pack(pady=5)

        # 创建网格按钮
        self.buttons = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                btn = tk.Button(
                    self.grid_frame,
                    text="",
                    font=("Arial", 20, "bold"),
                    width=4,
                    height=2,
                    bg=self.colors[0],
                    fg="#776E65",
                    relief="flat",
                    bd=0
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)

        # 重新开始按钮
        restart_btn = tk.Button(
            self.root,
            text="重新开始",
            font=("Arial", 14),
            bg="#8F7A66",
            fg="white",
            relief="flat",
            command=self.restart_game
        )
        restart_btn.pack(pady=10)

    def update_display(self):
        for pos_x in range(self.grid_size):
            for pos_y in range(self.grid_size):
                button = self.buttons[pos_x][pos_y]
                value = self.grid[pos_x][pos_y]
                if value == 0:
                    button.config(text="", bg=self.colors[0], fg="#776E65")
                else:
                    button.config(text=str(value), bg=self.colors.get(value, "#3C3A32"),
                                  fg="#F9F6F2" if value > 4 else "#776E65")
        # 刷新分数
        self.score_label.config(text=f"分数: {self.score}")

    def add_random_brick(self):
        pos_choicer = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)]
        pos_x, pos_y = random.choice(pos_choicer)
        while self.grid[pos_x][pos_y] != 0:
            pos_x, pos_y = random.choice(pos_choicer)
        self.grid[pos_x][pos_y] = random.choice([2,4,8])
        print(f"random:({pos_x},{pos_y}) val:{self.grid[pos_x][pos_y]}")

    def key_pressed(self, event):
        moved = False
        if event.keysym == "Up":
            moved = self.move_up()
        elif event.keysym == "Down":
            moved = self.move_down()
        elif event.keysym == "Left":
            moved = self.move_left()
        elif event.keysym == "Right":
            moved = self.move_right()
        if moved:
            self.add_random_brick()
            self.update_display()
            if self.check_game_over():
                self.game_over()
            print(" ------------------------------------------- ")

    def move_up(self):
        moved = True
        print("move up!")
        for pos_y in range(self.grid_size):
            for pos_x in range(self.grid_size):
                # 寻找这一列不为0的数.
                if self.grid[pos_x][pos_y] != 0:
                    id_x = pos_x - 1
                    while id_x >= 0:
                        if self.grid[id_x][pos_y] == 0:
                            id_x = id_x - 1
                            if id_x > -1:
                                continue
                        print(f"id_x:{id_x}")
                        if id_x == -1:
                            # 应该写成交换的形式
                            self.grid[id_x+1][pos_y], self.grid[pos_x][pos_y] = (
                                self.grid[pos_x][pos_y], self.grid[id_x+1][pos_y])
                        else:
                            if self.grid[id_x][pos_y] == self.grid[pos_x][pos_y]:
                                self.grid[id_x][pos_y] = self.grid[id_x][pos_y]*2
                                self.grid[pos_x][pos_y] = 0
                                # 计算分数
                                self.score = self.score + self.grid[id_x][pos_y]
                            else:
                                self.grid[id_x + 1][pos_y], self.grid[pos_x][pos_y] = (
                                    self.grid[pos_x][pos_y], self.grid[id_x + 1][pos_y])
                        break

        return moved

    def move_down(self):
        moved = True
        print("move down!")
        for pos_y in range(self.grid_size):
            for pos_x in range(self.grid_size-1, -1, -1):
                # 寻找这一列不为0的数.
                if self.grid[pos_x][pos_y] != 0:
                    id_x = pos_x + 1
                    while id_x <= self.grid_size-1:
                        # print("x:{pos_x},y:{pos_y}")
                        if self.grid[id_x][pos_y] == 0:
                            id_x = id_x + 1
                            if id_x < self.grid_size:
                                continue
                        print(f"id_x:{id_x}")
                        if id_x == self.grid_size:
                            # 应该写成交换的形式
                            self.grid[id_x - 1][pos_y], self.grid[pos_x][pos_y] = (
                                self.grid[pos_x][pos_y], self.grid[id_x - 1][pos_y])
                        else:
                            if self.grid[id_x][pos_y] == self.grid[pos_x][pos_y]:
                                self.grid[id_x][pos_y] = self.grid[id_x][pos_y] * 2
                                self.grid[pos_x][pos_y] = 0
                                # 计算分数
                                self.score = self.score + self.grid[id_x][pos_y]
                            else:
                                self.grid[id_x - 1][pos_y], self.grid[pos_x][pos_y] = (
                                    self.grid[pos_x][pos_y], self.grid[id_x - 1][pos_y])
                        break

        return moved

    def move_left(self):
        moved = True
        print("move left!")
        for pos_x in range(self.grid_size):
            for pos_y in range(self.grid_size):
                # 寻找这一列不为0的数.
                if self.grid[pos_x][pos_y] != 0:
                    id_y = pos_y - 1
                    while id_y >= 0:
                        if self.grid[pos_x][id_y] == 0:
                            id_y = id_y - 1
                            if id_y > -1:
                                continue
                        print(f"id_y:{id_y}")
                        if id_y == -1:
                            # 应该写成交换的形式
                            self.grid[pos_x][id_y+1], self.grid[pos_x][pos_y] = (
                                self.grid[pos_x][pos_y], self.grid[pos_x][id_y+1])
                        else:
                            if self.grid[pos_x][id_y] == self.grid[pos_x][pos_y]:
                                self.grid[pos_x][id_y] = self.grid[pos_x][id_y]*2
                                self.grid[pos_x][pos_y] = 0
                                # 计算分数
                                self.score = self.score + self.grid[pos_x][id_y]
                            else:
                                self.grid[pos_x][id_y + 1], self.grid[pos_x][pos_y] = (
                                    self.grid[pos_x][pos_y], self.grid[pos_x][id_y + 1])
                        break
        return moved

    def move_right(self):
        moved = True
        print("move right!")
        for pos_x in range(self.grid_size):
            for pos_y in range(self.grid_size-1, -1, -1):
                # 寻找这一列不为0的数.
                if self.grid[pos_x][pos_y] != 0:
                    id_y = pos_y + 1
                    while id_y <= self.grid_size - 1:
                        if self.grid[pos_x][id_y] == 0:
                            id_y = id_y + 1
                            if id_y < self.grid_size:
                                continue
                        print(f"id_y:{id_y}")
                        if id_y == self.grid_size:
                            # 应该写成交换的形式
                            self.grid[pos_x][id_y - 1], self.grid[pos_x][pos_y] = (
                                self.grid[pos_x][pos_y], self.grid[pos_x][id_y - 1])
                        else:
                            if self.grid[pos_x][id_y] == self.grid[pos_x][pos_y]:
                                self.grid[pos_x][id_y] = self.grid[pos_x][id_y] * 2
                                self.grid[pos_x][pos_y] = 0
                                # 计算分数
                                self.score = self.score + self.grid[pos_x][id_y]
                            else:
                                self.grid[pos_x][id_y - 1], self.grid[pos_x][pos_y] = (
                                    self.grid[pos_x][pos_y], self.grid[pos_x][id_y - 1])
                        break

        return moved

    def check_game_over(self):
        """检查游戏是否结束"""
        # 检查是否有空格
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False

        # 检查是否可以合并
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                current = self.grid[i][j]
                # 检查右边
                if j < self.grid_size - 1 and self.grid[i][j + 1] == current:
                    return False
                # 检查下边
                if i < self.grid_size - 1 and self.grid[i + 1][j] == current:
                    return False

        return True

    def game_over(self):
        """游戏结束处理"""
        messagebox.showinfo("游戏结束", f"游戏结束! 最终分数: {self.score}")

    def restart_game(self):
        """重新开始游戏"""
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.add_random_brick()
        self.add_random_brick()
        self.update_display()

    def run(self):
        """运行游戏"""
        self.root.mainloop()


if __name__ == "__main__":
    game = Game2048()
    game.run()


