from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt


class VehicleScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()

    # 添加自定义的车辆图形项
    def add_vehicle(self, x, y):
        vehicle_item = VehicleGraphicsItem(x, y)    # 车辆图形放置的位置
        self.addItem(vehicle_item)
        # item = QtWidgets.QGraphicsPixmapItem(pix)
        # item.setTransformOriginPoint(origin_x, origin_y)  # 设置变换原点

    # 处理场景事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 处理左键点击
            print(f"Scene clicked at: {event.scenePos()}")
        super().mousePressEvent(event)

    # 清除所有车辆
    def clear_vehicles(self):
        items = self.items()
        for item in items:
            if isinstance(item, VehicleGraphicsItem):
                self.removeItem(item)


class VehicleView(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()
        # 实例化场景并设置
        self.scene = VehicleScene()
        self.setScene(self.scene)

        # 设置视图属性
        self.setRenderHint(QtGui.QPainter.Antialiasing)  # 抗锯齿
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)  # 拖拽模式

    # 缩放控制
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(1.1, 1.1)  # 放大
        else:
            self.scale(0.9, 0.9)  # 缩小

    # 通过视图调用场景方法
    def add_vehicle_to_scene(self, x, y):
        self.scene.add_vehicle(x, y)

    def clear_scene_vehicles(self):
        self.scene.clear_vehicles()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建视图（视图内部创建场景）
        self.vehicle_view = VehicleView()
        self.setCentralWidget(self.vehicle_view)

        # 通过视图调用场景功能
        self.setup_ui()

    def setup_ui(self):
        # 添加工具栏按钮
        toolbar = self.addToolBar("Vehicle Control")

        add_btn = QtWidgets.QAction("Add Vehicle", self)
        add_btn.triggered.connect(self.add_vehicle)
        toolbar.addAction(add_btn)

        clear_btn = QtWidgets.QAction("Clear Vehicles", self)
        clear_btn.triggered.connect(self.clear_vehicles)
        toolbar.addAction(clear_btn)

    def add_vehicle(self):
        # 通过视图调用场景的添加车辆方法
        self.vehicle_view.add_vehicle_to_scene(100, 100)

    def clear_vehicles(self):
        # 通过视图调用场景的清除方法
        self.vehicle_view.clear_scene_vehicles()

