import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class DetachableTabWidget(QTabWidget):
    """可分离的标签页控件，支持拖出为独立窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.tabBar().setAcceptDrops(True)
        self.tabBar().installEventFilter(self)
        self.tabs = []  # 存储标签页信息
        self.detached_windows = []  # 存储分离的窗口

        # 自定义标签页右键菜单
        self.tabBar().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabBar().customContextMenuRequested.connect(self.show_tab_context_menu)

        # 创建初始标签页
        self.create_tab("主页面")

    def create_tab(self, title, content=None):
        """创建新标签页"""
        if content is None:
            content = self.create_content(title)

        index = self.addTab(content, title)
        self.setCurrentIndex(index)

        # 存储标签页信息
        tab_info = {
            'widget': content,
            'title': title,
            'index': index
        }
        self.tabs.append(tab_info)

        # 添加自定义关闭按钮
        self.add_close_button(index)

        return content

    def create_content(self, title):
        """创建标签页内容"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 标题
        label = QLabel(f"这是标签页: {title}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 20px;")
        layout.addWidget(label)

        # 一些示例内容
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(f"在 {title} 中输入内容...")
        text_edit.setMinimumHeight(150)
        layout.addWidget(text_edit)

        # 状态显示
        status_label = QLabel("状态: 已连接到主窗口")
        status_label.setStyleSheet("color: green; margin: 5px;")
        layout.addWidget(status_label)

        # 底部按钮
        button_layout = QHBoxLayout()
        btn_detach = QPushButton("分离标签页")
        btn_detach.clicked.connect(lambda: self.detach_tab_by_button(widget))
        button_layout.addWidget(btn_detach)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        return widget

    def add_close_button(self, index):
        """添加自定义关闭按钮到标签页"""
        close_button = QPushButton("×")
        close_button.setFixedSize(20, 20)
        close_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 10px;
                background-color: #e0e0e0;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff6b6b;
                color: white;
            }
        """)
        close_button.clicked.connect(lambda: self.close_tab(index))

        # 将关闭按钮添加到标签页
        self.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, close_button)

    def show_tab_context_menu(self, position):
        """显示标签页右键菜单"""
        index = self.tabBar().tabAt(position)
        if index >= 0:
            menu = QMenu()

            detach_action = QAction("分离标签页", self)
            detach_action.triggered.connect(lambda: self.detach_tab(index))

            close_action = QAction("关闭标签页", self)
            close_action.triggered.connect(lambda: self.close_tab(index))

            close_others_action = QAction("关闭其他标签页", self)
            close_others_action.triggered.connect(lambda: self.close_other_tabs(index))

            menu.addAction(detach_action)
            menu.addSeparator()
            menu.addAction(close_action)
            menu.addAction(close_others_action)

            menu.exec(self.tabBar().mapToGlobal(position))

    def eventFilter(self, obj, event):
        """事件过滤器，用于处理拖拽事件"""
        if obj == self.tabBar():
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.drag_start_position = event.position().toPoint()
            elif event.type() == QEvent.Type.MouseMove:
                if (event.buttons() & Qt.MouseButton.LeftButton and
                        (event.position().toPoint() - self.drag_start_position).manhattanLength() > 10):
                    index = self.tabBar().tabAt(self.drag_start_position)
                    if index >= 0:
                        self.detach_tab(index)
                        return True
        return super().eventFilter(obj, event)

    def detach_tab(self, index):
        """分离标签页为新窗口"""
        if index < 0:
            return

        # 获取要分离的部件和标题
        widget = self.widget(index)
        title = self.tabText(index)

        # 从当前标签页中移除
        self.removeTab(index)

        # 创建浮动窗口
        floating_window = DetachedWindow(self, widget, title)
        floating_window.show()
        floating_window.move(QCursor.pos() - QPoint(50, 20))

        # 存储窗口引用
        self.detached_windows.append(floating_window)

        # 更新状态显示
        self.update_status(f"已分离标签页: {title}")

    def detach_tab_by_button(self, widget):
        """通过按钮分离标签页"""
        index = self.indexOf(widget)
        if index >= 0:
            self.detach_tab(index)

    def reattach_tab(self, window, widget, title):
        """将窗口重新附加到主界面"""
        # 添加回标签页
        self.create_tab(title, widget)

        # 关闭浮动窗口
        window.close()

        # 从列表中移除
        if window in self.detached_windows:
            self.detached_windows.remove(window)

        # 更新状态显示
        self.update_status(f"已重新附加标签页: {title}")

    def close_tab(self, index):
        """关闭标签页"""
        if self.count() > 1:  # 至少保留一个标签页
            title = self.tabText(index)
            self.removeTab(index)
            self.update_status(f"已关闭标签页: {title}")

    def close_other_tabs(self, index):
        """关闭其他标签页"""
        for i in range(self.count() - 1, -1, -1):
            if i != index:
                self.close_tab(i)

    def update_status(self, message):
        """更新状态显示"""
        # 可以通过信号发送到状态栏，这里简单打印
        print(f"状态: {message}")


class DetachedWindow(QMainWindow):
    """分离的浮动窗口"""

    def __init__(self, parent_tab_widget, widget, title):
        super().__init__()
        self.parent_tab_widget = parent_tab_widget
        self.original_widget = widget
        self.original_title = title

        self.setWindowTitle(f"{title} [分离]")
        self.setMinimumSize(400, 300)

        # 设置窗口标志，使其保持在顶层
        self.setWindowFlags(Qt.WindowType.Window |
                            Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.CustomizeWindowHint |
                            Qt.WindowType.WindowCloseButtonHint |
                            Qt.WindowType.WindowMinMaxButtonsHint)

        # 创建中央部件
        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        # 添加原始部件
        layout.addWidget(widget)

        # 添加拖回按钮
        reattach_button = QPushButton("拖回主窗口")
        reattach_button.clicked.connect(self.reattach)
        layout.addWidget(reattach_button)

        # 安装事件过滤器以支持拖拽
        self.installEventFilter(self)

        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                border: 2px solid #cccccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 5px;
                margin: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: #4a9eff;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a7eff;
            }
        """)

    def eventFilter(self, obj, event):
        """事件过滤器，支持拖拽窗口回到主界面"""
        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                self.drag_offset = event.position().toPoint()
                return True

        elif event.type() == QEvent.Type.MouseMove:
            if event.buttons() & Qt.MouseButton.LeftButton:
                # 移动窗口
                self.move(self.mapToParent(event.position().toPoint() - self.drag_offset))
                return True

        elif event.type() == QEvent.Type.MouseButtonRelease:
            # 检查是否拖到了主窗口区域
            main_window = self.parent_tab_widget.window()
            if main_window.geometry().contains(event.globalPosition().toPoint()):
                self.reattach()
                return True

        return super().eventFilter(obj, event)

    def reattach(self):
        """将窗口重新附加到主界面"""
        self.parent_tab_widget.reattach_tab(self, self.original_widget, self.original_title)

    def closeEvent(self, event):
        """关闭窗口时重新附加标签页"""
        self.reattach()
        event.accept()


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("浏览器式标签页示例")
        self.setGeometry(100, 100, 1000, 700)

        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()

        # 设置窗口图标
        self.setWindowIcon(QIcon.fromTheme("applications-internet"))

    def setup_ui(self):
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建可分离的标签页控件
        self.tab_widget = DetachableTabWidget()
        layout.addWidget(self.tab_widget)

        # 添加一些示例标签页
        for i in range(1, 4):
            self.tab_widget.create_tab(f"标签页 {i}")

    def setup_menu(self):
        """设置菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")

        new_tab_action = QAction("新建标签页", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_tab_action)

        detach_action = QAction("分离当前标签页", self)
        detach_action.setShortcut("Ctrl+Shift+D")
        detach_action.triggered.connect(self.detach_current_tab)
        file_menu.addAction(detach_action)

        file_menu.addSeparator()

        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 视图菜单
        view_menu = menubar.addMenu("视图")

        show_status_action = QAction("显示状态栏", self)
        show_status_action.setCheckable(True)
        show_status_action.setChecked(True)
        show_status_action.triggered.connect(self.toggle_statusbar)
        view_menu.addAction(show_status_action)

    def setup_statusbar(self):
        """设置状态栏"""
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("就绪 - 拖拽标签页可分离，拖回窗口可合并")

    def new_tab(self):
        """新建标签页"""
        count = self.tab_widget.count() + 1
        self.tab_widget.create_tab(f"新标签页 {count}")
        self.statusbar.showMessage(f"已创建新标签页: 新标签页 {count}")

    def detach_current_tab(self):
        """分离当前标签页"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.tab_widget.detach_tab(current_index)

    def toggle_statusbar(self, visible):
        """切换状态栏显示"""
        self.statusbar.setVisible(visible)


class BrowserStyleTabWidget(QMainWindow):
    """更完整的浏览器风格标签页实现"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("高级标签页浏览器")
        self.setGeometry(150, 150, 1200, 800)

        self.tab_history = []  # 标签页历史记录
        self.setup_ui()

    def setup_ui(self):
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)

        # 创建地址栏和工具栏
        self.create_toolbar()

        # 初始标签页
        self.add_tab("起始页")

        # 设置拖拽相关
        self.tab_widget.tabBar().setAcceptDrops(True)
        self.tab_widget.tabBar().installEventFilter(self)

    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar("导航栏")
        self.addToolBar(toolbar)

        # 后退按钮
        back_btn = QAction("←", self)
        back_btn.triggered.connect(self.go_back)
        toolbar.addAction(back_btn)

        # 前进按钮
        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(self.go_forward)
        toolbar.addAction(forward_btn)

        toolbar.addSeparator()

        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("输入网址或搜索...")
        self.url_bar.returnPressed.connect(self.navigate)
        toolbar.addWidget(self.url_bar)

        # 新建标签页按钮
        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(lambda: self.add_tab("新标签页"))
        toolbar.addAction(new_tab_btn)

        # 分离按钮
        detach_btn = QAction("分离", self)
        detach_btn.triggered.connect(self.detach_current)
        toolbar.addAction(detach_btn)

    def add_tab(self, title, url=None):
        """添加标签页"""
        # 创建浏览器页面
        browser_page = QWidget()
        layout = QVBoxLayout(browser_page)

        # 简单模拟浏览器内容
        content = QLabel(f"<h2>{title}</h2><p>这是模拟的浏览器页面</p>")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(content)

        if url:
            self.url_bar.setText(url)

        # 添加到标签页
        index = self.tab_widget.addTab(browser_page, title)
        self.tab_widget.setCurrentIndex(index)

        # 记录历史
        self.tab_history.append({
            'title': title,
            'url': url,
            'time': QDateTime.currentDateTime().toString("hh:mm:ss")
        })

    def close_tab(self, index):
        """关闭标签页"""
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def detach_current(self):
        """分离当前标签页"""
        # 这里可以扩展为创建真正的浮动窗口
        QMessageBox.information(self, "提示", "这是分离标签页功能")

    def navigate(self):
        """导航到地址"""
        url = self.url_bar.text()
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            new_title = f"访问: {url[:20]}..." if len(url) > 20 else f"访问: {url}"
            self.tab_widget.setTabText(current_index, new_title)

    def go_back(self):
        """后退"""
        if len(self.tab_history) > 1:
            self.tab_history.pop()
            prev = self.tab_history[-1]
            self.url_bar.setText(prev['url'] if prev['url'] else "")

    def go_forward(self):
        """前进 - 这里简化处理"""
        pass


# 两种实现的选择
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 选择要运行的示例
    choice = input("请选择示例 (1: 基础版, 2: 浏览器风格版): ").strip()

    if choice == "2":
        window = BrowserStyleTabWidget()
    else:
        window = MainWindow()

    window.show()
    sys.exit(app.exec())
