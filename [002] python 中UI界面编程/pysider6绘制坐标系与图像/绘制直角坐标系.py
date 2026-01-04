

import sys
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
                               QSplitter, QMessageBox, QComboBox)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Rectangle, Polygon
import matplotlib.pyplot as plt


class CoordinateInputWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 标题
        title = QLabel("坐标输入")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # 输入说明
        instruction = QLabel("请输入坐标点，每行一个点，格式: x,y 或 x y")
        layout.addWidget(instruction)

        # 坐标输入区域
        self.coord_input = QTextEdit()
        self.coord_input.setPlaceholderText("例如:\n1,2\n3,4\n5,6\n或\n1 2\n3 4\n5 6")
        self.coord_input.setMinimumHeight(150)
        layout.addWidget(self.coord_input)

        # 图形类型选择
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(QLabel("图形类型:"))
        self.graph_type = QComboBox()
        self.graph_type.addItems(["散点图", "折线图", "多边形", "圆形", "矩形"])
        graph_layout.addWidget(self.graph_type)
        layout.addLayout(graph_layout)

        # 按钮区域
        button_layout = QHBoxLayout()

        self.plot_button = QPushButton("绘制图形")
        self.plot_button.clicked.connect(self.emit_plot_signal)
        button_layout.addWidget(self.plot_button)

        self.clear_button = QPushButton("清除")
        self.clear_button.clicked.connect(self.clear_input)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        # 示例区域
        example_label = QLabel("示例:")
        layout.addWidget(example_label)

        example_text = QLabel("1,1\n2,3\n3,2\n4,5\n5,4")
        example_text.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
        layout.addWidget(example_text)

        self.setLayout(layout)

    def emit_plot_signal(self):
        # 这个方法将在子类中重写以发出信号
        pass

    def clear_input(self):
        self.coord_input.clear()


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)

        self.axes = self.fig.add_subplot(111)
        self.axes.grid(True, linestyle='--', alpha=0.7)
        self.axes.set_xlabel('X轴')
        self.axes.set_ylabel('Y轴')
        self.axes.set_title('坐标图')

    def plot_points(self, points, graph_type):
        self.axes.clear()
        self.axes.grid(True, linestyle='--', alpha=0.7)
        self.axes.set_xlabel('X轴')
        self.axes.set_ylabel('Y轴')
        self.axes.set_title('坐标图')

        if not points:
            self.draw()
            return

        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]

        if graph_type == "散点图":
            self.axes.scatter(x_coords, y_coords, color='red', s=50, zorder=5)
            # 添加点标签
            for i, (x, y) in enumerate(points):
                self.axes.annotate(f'({x},{y})', (x, y), textcoords="offset points",
                                   xytext=(0, 10), ha='center', fontsize=8)

        elif graph_type == "折线图":
            self.axes.plot(x_coords, y_coords, 'o-', color='blue', linewidth=2, markersize=6)
            # 添加点标签
            for i, (x, y) in enumerate(points):
                self.axes.annotate(f'({x},{y})', (x, y), textcoords="offset points",
                                   xytext=(0, 10), ha='center', fontsize=8)

        elif graph_type == "多边形" and len(points) >= 3:
            polygon = Polygon(points, closed=True, fill=True, alpha=0.3, color='green')
            self.axes.add_patch(polygon)
            # 绘制顶点
            self.axes.scatter(x_coords, y_coords, color='red', s=50, zorder=5)
            for i, (x, y) in enumerate(points):
                self.axes.annotate(f'({x},{y})', (x, y), textcoords="offset points",
                                   xytext=(0, 10), ha='center', fontsize=8)

        elif graph_type == "圆形" and len(points) >= 2:
            # 使用前两个点：第一个点为圆心，第二个点确定半径
            center = points[0]
            radius = np.sqrt((points[1][0] - center[0]) ** 2 + (points[1][1] - center[1]) ** 2)
            circle = Circle(center, radius, fill=True, alpha=0.3, color='orange')
            self.axes.add_patch(circle)
            # 绘制圆心和半径点
            self.axes.scatter([center[0]], [center[1]], color='red', s=50, zorder=5)
            self.axes.scatter([points[1][0]], [points[1][1]], color='blue', s=50, zorder=5)
            self.axes.annotate(f'圆心({center[0]},{center[1]})', center,
                               textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)
            self.axes.annotate(f'半径点({points[1][0]},{points[1][1]})', points[1],
                               textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

        elif graph_type == "矩形" and len(points) >= 2:
            # 使用前两个点：第一个点为左下角，第二个点为右上角
            x1, y1 = points[0]
            x2, y2 = points[1]
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            rect = Rectangle((min(x1, x2), min(y1, y2)), width, height,
                             fill=True, alpha=0.3, color='purple')
            self.axes.add_patch(rect)
            # 绘制顶点
            self.axes.scatter([x1, x2], [y1, y2], color='red', s=50, zorder=5)
            self.axes.annotate(f'({x1},{y1})', (x1, y1), textcoords="offset points",
                               xytext=(0, 10), ha='center', fontsize=8)
            self.axes.annotate(f'({x2},{y2})', (x2, y2), textcoords="offset points",
                               xytext=(0, 10), ha='center', fontsize=8)

        # 调整坐标轴范围
        if x_coords:
            x_margin = (max(x_coords) - min(x_coords)) * 0.1
            y_margin = (max(y_coords) - min(y_coords)) * 0.1
            self.axes.set_xlim(min(x_coords) - x_margin, max(x_coords) + x_margin)
            self.axes.set_ylim(min(y_coords) - y_margin, max(y_coords) + y_margin)

        self.fig.tight_layout()
        self.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("交互式坐标绘图工具")
        self.setGeometry(100, 100, 1000, 700)

        # 创建中央部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)

        # 左侧：坐标输入部件
        self.input_widget = CoordinateInputWidget()
        # 重写emit_plot_signal方法
        self.input_widget.plot_button.clicked.connect(self.plot_coordinates)

        # 右侧：绘图区域
        self.canvas = MplCanvas(self, width=6, height=5, dpi=100)

        # 将部件添加到分割器
        splitter.addWidget(self.input_widget)
        splitter.addWidget(self.canvas)

        # 设置分割器比例
        splitter.setSizes([300, 700])

        main_layout.addWidget(splitter)

    def plot_coordinates(self):
        text = self.input_widget.coord_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "输入错误", "请输入坐标点")
            return

        points = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 尝试用逗号分隔
            if ',' in line:
                parts = line.split(',')
            else:
                # 否则用空格分隔
                parts = line.split()

            if len(parts) != 2:
                QMessageBox.warning(self, "输入错误", f"坐标格式错误: {line}")
                return

            try:
                x = float(parts[0].strip())
                y = float(parts[1].strip())
                points.append((x, y))
            except ValueError:
                QMessageBox.warning(self, "输入错误", f"坐标值不是有效的数字: {line}")
                return

        graph_type = self.input_widget.graph_type.currentText()
        self.canvas.plot_points(points, graph_type)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QPushButton {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 8px 16px;
            text-align: center;
            text-decoration: none;
            font-size: 14px;
            margin: 4px 2px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        QLineEdit, QTextEdit {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
        }
        QLabel {
            font-size: 14px;
        }
    """)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

