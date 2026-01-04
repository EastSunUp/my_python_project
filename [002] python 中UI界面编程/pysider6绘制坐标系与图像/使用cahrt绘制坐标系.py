
"""
    pysider6中QLineSeries()详解:
        数据操作:
            append(x, y) / append(QPointF)                      添加数据点。
            insert(index, point)                                在指定索引处插入数据点。
            replace(old_point, new_point)                       替换数据点。
            remove(index) / removePoints(index, count)          删除数据点。
            clear()                                             清空所有数据点。
            setModel(QAbstractItemModel)                        将系列绑定到数据模型。
        样式设置
            setPen(QPen)                            设置线条颜色、宽度、线型等。
            setBrush(QBrush)                        设置数据点的填充样式。
            setPointsVisible(bool)                  控制数据点是否可见。
        系列属性
            name                                    系列名称，显示在图例中。
            opacity                                 系列透明度（0.0透明 - 1.0不透明）。
            visible                                 系列是否可见。
            useOpenGL                               是否使用OpenGL加速渲染（仅限QLineSeries和QScatterSeries）。
        信号
            clicked(QPointF point)                  当用户点击系列上的某个数据点时触发。
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import QPointF


class ChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. 创建 QLineSeries 实例
        series = QLineSeries()
        series.setName("示例折线")  # 设置折线名称，会显示在图例中

        # 2. 添加数据点 (有多种方式)
        # 方式一：逐个添加坐标
        series.append(0, 6)
        series.append(1, 3)
        # 方式二：使用 QPointF 列表
        points = [QPointF(2, 4), QPointF(3, 8), QPointF(4, 2)]
        series.append(points)
        # 方式三：直接传入坐标对列表（注意PySide6版本是否支持）
        # series.replace([QPointF(0,0), QPointF(1,1), QPointF(2,2)])

        # 3. 创建图表并添加系列
        chart = QChart()
        chart.setTitle("基础折线图示例")
        chart.addSeries(series)

        # 4. 创建默认坐标轴 (这一步很重要，否则看不到坐标轴)
        chart.createDefaultAxes()

        # 5. 创建图表视图并设置渲染提示
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿，让图形更平滑

        # 6. 将图表视图设置为主窗口的中心部件
        self.setCentralWidget(chart_view)
        self.resize(800, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChartWindow()
    window.show()
    sys.exit(app.exec())
