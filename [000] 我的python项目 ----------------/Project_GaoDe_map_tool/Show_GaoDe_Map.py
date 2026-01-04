
# TODO: 使用PySide6加载显示高德地图

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QLineEdit, QStatusBar
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QIcon, QAction


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高德地图浏览器")
        self.setGeometry(100, 100, 1200, 800)

        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建浏览器视图
        self.browser = QWebEngineView()

        # 创建工具栏
        self.create_toolbar()

        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("准备就绪")

        # 加载高德地图
        self.load_amap()

        # 将浏览器添加到布局
        layout.addWidget(self.browser)

        # 连接信号
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadProgress.connect(self.update_progress)
        self.browser.loadFinished.connect(self.on_load_finished)

    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # 后退按钮
        back_action = QAction(QIcon.fromTheme("go-previous"), "后退", self)
        back_action.triggered.connect(self.browser.back)
        toolbar.addAction(back_action)

        # 前进按钮
        forward_action = QAction(QIcon.fromTheme("go-next"), "前进", self)
        forward_action.triggered.connect(self.browser.forward)
        toolbar.addAction(forward_action)

        # 刷新按钮
        refresh_action = QAction(QIcon.fromTheme("view-refresh"), "刷新", self)
        refresh_action.triggered.connect(self.browser.reload)
        toolbar.addAction(refresh_action)

        # 主页按钮
        home_action = QAction(QIcon.fromTheme("go-home"), "主页", self)
        home_action.triggered.connect(self.load_amap)
        toolbar.addAction(home_action)

        toolbar.addSeparator()

        # URL地址栏
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

        # 搜索按钮
        go_action = QAction(QIcon.fromTheme("go-jump"), "前往", self)
        go_action.triggered.connect(self.navigate_to_url)
        toolbar.addAction(go_action)

    def load_amap(self):
        """加载高德地图"""
        # 使用高德地图网页版
        amap_url = QUrl("https://www.amap.com/")
        self.browser.setUrl(amap_url)
        self.url_bar.setText(amap_url.toString())
        self.status_bar.showMessage("正在加载高德地图...")

    def navigate_to_url(self):
        """导航到URL地址栏中的网址"""
        url_text = self.url_bar.text()

        # 确保URL有协议前缀
        if not url_text.startswith(('http://', 'https://')):
            url_text = 'https://' + url_text

        url = QUrl(url_text)
        self.browser.setUrl(url)

    def update_url_bar(self, url):
        """更新URL地址栏"""
        self.url_bar.setText(url.toString())

    def update_progress(self, progress):
        """更新加载进度"""
        self.status_bar.showMessage(f"正在加载... {progress}%")

    def on_load_finished(self, success):
        """页面加载完成"""
        if success:
            self.status_bar.showMessage("页面加载完成")
        else:
            self.status_bar.showMessage("页面加载失败")


def main():
    # 创建应用实例
    app = QApplication(sys.argv)
    app.setApplicationName("高德地图浏览器")

    # 创建并显示主窗口
    window = BrowserWindow()
    window.show()

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

