
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QPixmap

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("仿WeGame登录")
        self.resize(800, 600)
        # 在这里添加从Qt Designer生成的界面加载代码，以及按钮、输入框等

    def paintEvent(self, event):
        """ 绘制背景图片，此方法对PNG图片支持较好 """
        painter = QPainter(self)
        pixmap = QPixmap("your_background_image.png") # 替换为你的背景图路径
        # 缩放图片以适应窗口大小
        painter.drawPixmap(self.rect(), pixmap.scaled(self.size()))

    def setup_connections(self):
        """ 在这里绑定按钮点击信号与对应的功能函数 """
        # 例如：self.ui.login_button.clicked.connect(self.check_login)
        pass

if __name__ == "__main__":
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()
