import sys
import math
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont


class PureSemiCircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 400)  # 更扁平的窗口，强调上半圆
        self.data = []

    def set_data(self, data):
        self.data = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置绘制区域
        margin = 60
        width = self.width() - 2 * margin
        height = (self.height() - 2 * margin) * 0.7  # 只使用上半部分高度

        center_x = self.width() / 2
        center_y = self.height() - margin  # 圆心在底部

        # 半径
        radius = min(width, height * 2) / 2

        # 绘制白色背景
        painter.fillRect(self.rect(), Qt.white)

        # 绘制半圆极坐标
        self.draw_pure_semi_circle(painter, center_x, center_y, radius)

    def draw_pure_semi_circle(self, painter, center_x, center_y, radius):
        """绘制纯粹的上半圆量角器"""

        # 1. 绘制底部直线
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(center_x - radius, center_y, center_x + radius, center_y)

        # 2. 绘制半圆外弧
        painter.setPen(QPen(Qt.black, 2))
        painter.drawArc(int(center_x - radius), int(center_y - radius),
                        int(2 * radius), int(2 * radius), 0, 180 * 16)

        # 3. 绘制半径刻度线（从圆心向外）
        painter.setPen(QPen(QColor(150, 150, 150), 1))
        for i in range(1, 6):
            r = radius * i / 5
            # 只绘制上半部分的圆弧
            painter.drawArc(int(center_x - r), int(center_y - r),
                            int(2 * r), int(2 * r), 0, 180 * 16)

            # 半径标签
            painter.setPen(QPen(Qt.black))
            painter.drawText(int(center_x - r - 15), int(center_y + 5), f"{int(i * 20)}")
            painter.setPen(QPen(QColor(150, 150, 150), 1))

        # 4. 绘制角度线和标签
        painter.setPen(QPen(Qt.black, 1))
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)

        # 绘制主要角度线
        for angle in [0, 30, 60, 90, 120, 150, 180]:
            rad = math.radians(angle)

            # 计算线的终点
            end_x = center_x + radius * math.cos(rad)
            end_y = center_y - radius * math.sin(rad)

            # 绘制角度线
            painter.drawLine(int(center_x), int(center_y), int(end_x), int(end_y))

            # 角度标签
            label_radius = radius + 20
            label_x = center_x + label_radius * math.cos(rad)
            label_y = center_y - label_radius * math.sin(rad)

            # 调整标签位置
            text = f"{angle}°"
            text_rect = painter.fontMetrics().boundingRect(text)
            painter.drawText(int(label_x - text_rect.width() / 2),
                             int(label_y + text_rect.height() / 4),
                             text)

        # 5. 绘制数据点
        if self.data:
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            painter.setPen(QPen(QColor(150, 0, 0), 1))

            for angle, value in self.data:
                rad = math.radians(angle)
                point_radius = radius * value / 100

                x = center_x + point_radius * math.cos(rad)
                y = center_y - point_radius * math.sin(rad)

                painter.drawEllipse(QPointF(x, y), 5, 5)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("纯粹上半圆量角器")

        # 创建半圆部件
        self.semi_circle = PureSemiCircleWidget()

        # 设置示例数据
        sample_data = [
            (0, 80),  # 0度方向，半径80
            (30, 60),  # 30度方向，半径60
            (45, 90),  # 45度方向，半径90
            (60, 40),  # 60度方向，半径40
            (90, 70),  # 90度方向，半径70
            (120, 85),  # 120度方向，半径85
            (150, 65),  # 150度方向，半径65
            (180, 80)  # 180度方向，半径80
        ]
        self.semi_circle.set_data(sample_data)

        self.setCentralWidget(self.semi_circle)
        self.resize(800, 400)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


