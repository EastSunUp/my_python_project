

# AI写的代码
import tkinter as tk
from tkinter import messagebox
import random
import copy

class Game2048:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2048 游戏")
        self.root.geometry("500x630")
        self.root.resizable(False, False)

        # 游戏状态
        self.grid_size = 4
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
        self.add_random_tile()
        self.add_random_tile()
        self.update_display()

        # 绑定键盘事件
        self.root.bind("<Key>", self.key_pressed)
        self.root.focus_set()

    def setup_ui(self):
        # 标题
        title_label = tk.Label(self.root, text="2048小游戏", font=("Arial", 32, "bold"), fg="#776E65")
        title_label.pack(pady=10)

        # 分数显示
        self.score_label = tk.Label(self.root, text=f"分数: {self.score}", font=("Arial", 16), fg="#776E65")
        self.score_label.pack(pady=5)

        # 游戏说明
        instruction_label = tk.Label(self.root, text="使用方向键移动,相同数字会合并", font=("Arial", 12), fg="#776E65")
        instruction_label.pack(pady=5)

        # 游戏网格框架
        self.grid_frame = tk.Frame(self.root, bg="#BBADA0", padx=10, pady=10)
        self.grid_frame.pack(pady=20)

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

    def add_random_tile(self):
        """在空白位置随机添加2或4"""
        empty_cells = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))

        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice([2, 4])

    def update_display(self):
        """更新界面显示"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                button = self.buttons[i][j]

                if value == 0:
                    button.config(text="", bg=self.colors[0], fg="#776E65")
                else:
                    button.config(text=str(value), bg=self.colors.get(value, "#3C3A32"),
                                  fg="#F9F6F2" if value > 4 else "#776E65")

        self.score_label.config(text=f"分数: {self.score}")

    def key_pressed(self, event):
        """处理键盘输入"""
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
            self.add_random_tile()
            self.update_display()

            if self.check_game_over():
                self.game_over()

    def move_left(self):
        """向左移动"""
        moved = False
        for i in range(self.grid_size):
            row = [cell for cell in self.grid[i] if cell != 0]
            merged_row = self.merge_row(row)
            new_row = merged_row + [0] * (self.grid_size - len(merged_row))

            if new_row != self.grid[i]:
                moved = True
                self.grid[i] = new_row
        return moved

    def move_right(self):
        """向右移动"""
        moved = False
        for i in range(self.grid_size):
            row = [cell for cell in self.grid[i] if cell != 0]
            merged_row = self.merge_row(row)
            new_row = [0] * (self.grid_size - len(merged_row)) + merged_row

            if new_row != self.grid[i]:
                moved = True
                self.grid[i] = new_row
        return moved

    def move_up(self):
        """向上移动"""
        moved = False
        for j in range(self.grid_size):
            column = [self.grid[i][j] for i in range(self.grid_size) if self.grid[i][j] != 0]
            merged_column = self.merge_row(column)
            new_column = merged_column + [0] * (self.grid_size - len(merged_column))

            if new_column != [self.grid[i][j] for i in range(self.grid_size)]:
                moved = True
                for i in range(self.grid_size):
                    self.grid[i][j] = new_column[i]
        return moved

    def move_down(self):
        """向下移动"""
        moved = False
        for j in range(self.grid_size):
            column = [self.grid[i][j] for i in range(self.grid_size) if self.grid[i][j] != 0]
            merged_column = self.merge_row(column)
            new_column = [0] * (self.grid_size - len(merged_column)) + merged_column

            if new_column != [self.grid[i][j] for i in range(self.grid_size)]:
                moved = True
                for i in range(self.grid_size):
                    self.grid[i][j] = new_column[i]
        return moved

    def merge_row(self, row):
        """合并行中的相同数字"""
        if not row:
            return []

        merged = []
        i = 0
        while i < len(row):
            if i < len(row) - 1 and row[i] == row[i + 1]:
                merged.append(row[i] * 2)
                self.score += row[i] * 2
                i += 2
            else:
                merged.append(row[i])
                i += 1
        return merged

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
        messagebox.showinfo("游戏结束", f"游戏结束！最终分数: {self.score}")

    def restart_game(self):
        """重新开始游戏"""
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
        self.update_display()

    def run(self):
        """运行游戏"""
        self.root.mainloop()

if __name__ == "__main__":
    game = Game2048()
    game.run()
