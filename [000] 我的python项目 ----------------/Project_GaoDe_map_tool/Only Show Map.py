import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class SimpleMapViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高德地图")
        self.setGeometry(100, 100, 1200, 800)

        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建浏览器视图
        self.browser = QWebEngineView()

        # 加载高德地图
        amap_url = QUrl("https://www.amap.com/")
        self.browser.setUrl(amap_url)

        # 将浏览器添加到布局
        layout.addWidget(self.browser)


def main():
    app = QApplication(sys.argv)
    window = SimpleMapViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()