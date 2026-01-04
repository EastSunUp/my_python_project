import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class ConfigWidget(QWidget):
    """配置页面小部件"""

    def __init__(self, title="配置页面"):
        super().__init__()
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # 标题
        title_label = QLabel(f"配置页面: {self.title}")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)

        # 一些配置控件
        form_layout = QFormLayout()
        form_layout.addRow("参数1:", QLineEdit())
        form_layout.addRow("参数2:", QComboBox())
        form_layout.addRow("参数3:", QSpinBox())

        group_box = QGroupBox("设置")
        group_box.setLayout(form_layout)
        layout.addWidget(group_box)

        # 按钮区域
        button_layout = QHBoxLayout()
        btn_apply = QPushButton("应用")
        btn_reset = QPushButton("重置")
        btn_close = QPushButton("关闭")

        button_layout.addWidget(btn_apply)
        button_layout.addWidget(btn_reset)
        button_layout.addStretch()
        button_layout.addWidget(btn_close)

        layout.addLayout(button_layout)

        # 设置样式
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("可拖拽配置页示例")
        self.setGeometry(100, 100, 1200, 800)

        # 存储浮动窗口的列表
        self.floating_windows = []

        self.setup_ui()

        # 设置允许所有停靠区域
        self.setDockOptions(QMainWindow.DockOption.AllowNestedDocks |
                            QMainWindow.DockOption.AllowTabbedDocks |
                            QMainWindow.DockOption.AnimatedDocks)

        # 设置允许拖拽
        self.setTabPosition(Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.North)

    def setup_ui(self):
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # 顶部工具栏
        toolbar = QToolBar("工具栏")
        self.addToolBar(toolbar)

        # 添加配置页的按钮
        self.btn_add_config = QAction("添加配置页", self)
        self.btn_add_config.triggered.connect(self.create_config_page)
        toolbar.addAction(self.btn_add_config)

        # 添加标签页控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setMovable(True)  # 允许标签页拖拽重新排序
        main_layout.addWidget(self.tab_widget)

        # 初始标签页
        initial_tab = QWidget()
        self.tab_widget.addTab(initial_tab, "主页面")

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

    def create_config_page(self, title=None):
        """创建新的配置页面"""
        if title is None:
            title = f"配置页 {self.tab_widget.count() + 1}"

        # 创建配置页面
        config_widget = ConfigWidget(title)

        # 创建dock widget来包装配置页面
        dock_widget = QDockWidget(title, self)
        dock_widget.setWidget(config_widget)
        dock_widget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                                QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                                QDockWidget.DockWidgetFeature.DockWidgetClosable)

        # 设置允许拖拽到标签页
        dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        # 添加到标签页
        self.tab_widget.addTab(config_widget, title)

        # 更新状态栏
        self.status_bar.showMessage(f"已创建配置页: {title}")

        # 如果需要显示为浮动窗口，可以这样设置：
        # dock_widget.setFloating(True)
        # self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock_widget)

    def create_floating_config(self):
        """创建浮动配置窗口"""
        title = f"浮动配置 {len(self.floating_windows) + 1}"

        # 创建配置页面
        config_widget = ConfigWidget(title)

        # 创建独立的浮动窗口
        floating_window = QMainWindow()
        floating_window.setWindowTitle(title)
        floating_window.setGeometry(200, 200, 500, 400)
        floating_window.setCentralWidget(config_widget)

        # 添加拖回按钮
        dock_button = QPushButton("拖回主界面")
        dock_button.clicked.connect(lambda: self.dock_to_main(floating_window, config_widget))

        # 创建工具栏
        toolbar = QToolBar()
        toolbar.addWidget(dock_button)
        floating_window.addToolBar(toolbar)

        # 显示浮动窗口
        floating_window.show()

        # 添加到浮动窗口列表
        self.floating_windows.append(floating_window)

        # 连接关闭事件
        floating_window.destroyed.connect(
            lambda: self.floating_windows.remove(floating_window)
            if floating_window in self.floating_windows else None
        )

        self.status_bar.showMessage(f"已创建浮动窗口: {title}")

    def dock_to_main(self, floating_window, config_widget):
        """将浮动窗口拖回主界面"""
        # 获取配置页面的标题
        title = floating_window.windowTitle()

        # 添加到标签页
        self.tab_widget.addTab(config_widget, title)

        # 关闭浮动窗口
        floating_window.close()

        # 从列表中移除
        if floating_window in self.floating_windows:
            self.floating_windows.remove(floating_window)

        self.status_bar.showMessage(f"已将 {title} 拖回主界面")

    def close_tab(self, index):
        """关闭标签页"""
        if self.tab_widget.count() > 1:  # 至少保留一个标签页
            self.tab_widget.removeTab(index)

    def create_dockable_config(self):
        """创建可停靠的配置窗口"""
        title = f"可停靠配置 {self.tab_widget.count() + 1}"

        # 创建配置页面
        config_widget = ConfigWidget(title)

        # 创建dock widget
        dock_widget = QDockWidget(title, self)
        dock_widget.setWidget(config_widget)

        # 设置dock widget的特性
        dock_widget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                                QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                                QDockWidget.DockWidgetFeature.DockWidgetClosable |
                                QDockWidget.DockWidgetFeature.DockWidgetVerticalTitleBar)

        # 允许停靠到所有区域
        dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        # 添加到右侧停靠区域
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock_widget)

        # 添加拖拽到标签页的功能
        tabify_button = QPushButton("转为标签页")
        tabify_button.clicked.connect(lambda: self.dock_to_tab(dock_widget, title))

        # 在dock widget的标题栏添加按钮
        title_bar_widget = QWidget()
        title_layout = QHBoxLayout(title_bar_widget)
        title_layout.addWidget(QLabel(title))
        title_layout.addStretch()
        title_layout.addWidget(tabify_button)

        dock_widget.setTitleBarWidget(title_bar_widget)

        self.status_bar.showMessage(f"已创建可停靠配置: {title}")

    def dock_to_tab(self, dock_widget, title):
        """将dock widget转为标签页"""
        # 获取dock widget中的部件
        config_widget = dock_widget.widget()

        # 添加到标签页
        self.tab_widget.addTab(config_widget, title)

        # 移除dock widget
        self.removeDockWidget(dock_widget)
        dock_widget.deleteLater()

        self.status_bar.showMessage(f"已将 {title} 转为标签页")


class AdvancedExample(QMainWindow):
    """更高级的示例，模拟浏览器标签页行为"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("浏览器式标签页示例")
        self.setGeometry(100, 100, 1400, 900)

        self.setup_ui()

        # 创建菜单栏
        self.create_menu()

    def setup_ui(self):
        # 创建中央的标签页控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setMovable(True)

        # 启用拖拽功能
        self.tab_widget.setAcceptDrops(True)
        self.tab_widget.tabBar().setAcceptDrops(True)

        # 设置标签页拖拽事件
        self.tab_widget.tabBar().installEventFilter(self)

        self.setCentralWidget(self.tab_widget)

        # 创建初始标签页
        self.add_new_tab("主页")

        # 用于存储分离的窗口
        self.detached_windows = {}

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("文件")

        new_tab_action = QAction("新建标签页", self)
        new_tab_action.triggered.connect(lambda: self.add_new_tab(f"标签页 {self.tab_widget.count() + 1}"))
        file_menu.addAction(new_tab_action)

        detach_action = QAction("分离当前标签页", self)
        detach_action.triggered.connect(self.detach_current_tab)
        file_menu.addAction(detach_action)

        # 工具栏
        toolbar = QToolBar("标签页工具")
        self.addToolBar(toolbar)

        btn_new = QToolButton()
        btn_new.setText("+")
        btn_new.clicked.connect(lambda: self.add_new_tab(f"标签页 {self.tab_widget.count() + 1}"))
        toolbar.addWidget(btn_new)

        toolbar.addSeparator()

    def add_new_tab(self, title):
        """添加新标签页"""
        content_widget = ConfigWidget(title)
        self.tab_widget.addTab(content_widget, title)

        # 添加关闭按钮到标签页
        tab_index = self.tab_widget.indexOf(content_widget)
        close_button = QToolButton()
        close_button.setText("×")
        close_button.setCursor(Qt.CursorShape.ArrowCursor)
        close_button.clicked.connect(lambda: self.tab_widget.removeTab(tab_index))

        self.tab_widget.tabBar().setTabButton(tab_index, QTabBar.ButtonPosition.RightSide, close_button)

    def detach_current_tab(self):
        """分离当前标签页为新窗口"""
        current_index = self.tab_widget.currentIndex()
        if current_index < 0:
            return

        # 获取当前标签页的内容
        widget = self.tab_widget.widget(current_index)
        title = self.tab_widget.tabText(current_index)

        # 创建新窗口
        new_window = QMainWindow()
        new_window.setWindowTitle(title)
        new_window.setGeometry(self.geometry().translated(20, 20))

        # 将widget移动到新窗口
        self.tab_widget.removeTab(current_index)
        new_window.setCentralWidget(widget)

        # 添加返回按钮
        toolbar = QToolBar()
        reattach_btn = QPushButton("返回主窗口")
        reattach_btn.clicked.connect(lambda: self.reattach_tab(new_window, widget, title))
        toolbar.addWidget(reattach_btn)
        new_window.addToolBar(toolbar)

        # 显示新窗口
        new_window.show()

        # 存储窗口引用
        self.detached_windows[new_window] = (widget, title)

        # 连接关闭事件
        new_window.destroyed.connect(
            lambda: self.detached_windows.pop(new_window, None)
        )

    def reattach_tab(self, window, widget, title):
        """将分离的窗口重新附加到主窗口"""
        # 将widget添加回标签页
        self.tab_widget.addTab(widget, title)
        self.tab_widget.setCurrentWidget(widget)

        # 关闭分离的窗口
        window.close()

    def close_tab(self, index):
        """关闭标签页"""
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 简单示例
    # window = MainWindow()

    # 高级示例（更像浏览器）
    window = AdvancedExample()

    window.show()
    sys.exit(app.exec())
