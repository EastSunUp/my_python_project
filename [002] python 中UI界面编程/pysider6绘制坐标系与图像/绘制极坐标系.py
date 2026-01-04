

import sys
import math
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel
from PySide6.QtCharts import QChartView, QPolarChart, QLineSeries, QScatterSeries, QSplineSeries
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen, QColor


class PolarChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 极坐标图示例")
        self.setGeometry(100, 100, 1000, 700)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 图表类型选择
        control_layout = QVBoxLayout()
        self.chart_type = QComboBox()
        self.chart_type.addItems(["螺旋线", "散点图", "样条曲线", "玫瑰线", "随机数据"])
        self.chart_type.currentTextChanged.connect(self.update_chart)
        control_layout.addWidget(QLabel("选择图表类型:"))
        control_layout.addWidget(self.chart_type)
        layout.addLayout(control_layout)

        # 创建极坐标图
        self.chart = QPolarChart()
        self.chart.setTitle("极坐标图示例 - 角度(度) vs 半径")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # 创建图表视图
        self.chart_view = QChartView(self.chart)
        layout.addWidget(self.chart_view)

        # 初始图表
        self.update_chart()

    def generate_spiral_data(self):
        """生成螺旋线数据"""
        series = QLineSeries()
        series.setName("螺旋线")

        points = 200
        for i in range(points):
            angle = i * 2 * math.pi / 20  # 角度（弧度）
            radius = 0.5 + angle * 0.5  # 半径随角度增加
            # 转换为极坐标点（角度为度，半径）
            series.append(math.degrees(angle), radius)

        return series

    def generate_scatter_data(self):
        """生成散点数据"""
        series = QScatterSeries()
        series.setName("散点")
        series.setMarkerSize(10)

        points = 50
        for i in range(points):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(0.5, 5)
            series.append(math.degrees(angle), radius)

        return series

    def generate_spline_data(self):
        """生成样条曲线数据"""
        series = QSplineSeries()
        series.setName("样条曲线")

        points = 100
        for i in range(points):
            angle = i * 2 * math.pi / 25
            radius = 3 + 2 * math.sin(angle * 2)  # 正弦波形状
            series.append(math.degrees(angle), radius)

        return series

    def generate_rose_data(self):
        """生成玫瑰线数据"""
        series = QLineSeries()
        series.setName("玫瑰线")

        points = 200
        for i in range(points):
            angle = i * 2 * math.pi / points * 4
            radius = 3 * math.sin(3 * angle)  # 三叶玫瑰线
            series.append(math.degrees(angle), radius)

        return series

    def generate_random_wave_data(self):
        """生成随机波动数据"""
        series = QLineSeries()
        series.setName("随机波动")

        points = 150
        current_radius = 2.5
        for i in range(points):
            angle = i * 2 * math.pi / 30
            # 添加一些随机波动
            current_radius += random.uniform(-0.3, 0.3)
            current_radius = max(0.5, min(5, current_radius))  # 限制范围
            series.append(math.degrees(angle), current_radius)

        return series

    def update_chart(self):
        """更新图表"""
        # 清除现有系列
        self.chart.removeAllSeries()

        # 根据选择生成数据
        chart_type = self.chart_type.currentText()
        if chart_type == "螺旋线":
            series = self.generate_spiral_data()
            pen = QPen(QColor(255, 0, 0))
            pen.setWidth(2)
            series.setPen(pen)
        elif chart_type == "散点图":
            series = self.generate_scatter_data()
        elif chart_type == "样条曲线":
            series = self.generate_spline_data()
            pen = QPen(QColor(0, 0, 255))
            pen.setWidth(2)
            series.setPen(pen)
        elif chart_type == "玫瑰线":
            series = self.generate_rose_data()
            pen = QPen(QColor(0, 150, 0))
            pen.setWidth(2)
            series.setPen(pen)
        else:  # 随机数据
            series = self.generate_random_wave_data()
            pen = QPen(QColor(150, 0, 150))
            pen.setWidth(2)
            series.setPen(pen)

        # 添加系列到图表
        self.chart.addSeries(series)

        # 创建坐标轴（角度轴和径向轴）
        from PySide6.QtCharts import QValueAxis

        # 角度轴 (0-360度)
        angular_axis = QValueAxis()
        angular_axis.setRange(0, 360)
        angular_axis.setTickCount(13)  # 每30度一个刻度
        angular_axis.setLabelFormat("%d°")
        angular_axis.setTitleText("角度")

        # 径向轴
        radial_axis = QValueAxis()
        radial_axis.setRange(0, 6)
        radial_axis.setTickCount(7)
        radial_axis.setTitleText("半径")

        # 将坐标轴添加到图表
        self.chart.addAxis(angular_axis, QPolarChart.PolarOrientationAngular)
        self.chart.addAxis(radial_axis, QPolarChart.PolarOrientationRadial)

        # 将系列附加到坐标轴
        series.attachAxis(angular_axis)
        series.attachAxis(radial_axis)


def main():
    # 创建应用
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle('Fusion')

    # 创建并显示窗口
    window = PolarChartWindow()
    window.show()

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()




