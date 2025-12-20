

# 电脑已经安装了pysider6,没法再安装pyqt5了, 两个包不兼容.

from PyQt5 import QtWidgets
import sys
try:

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.setWindowTitle("PyQt Test")
    window.setGeometry(100, 100, 400, 200)  # 设置窗口位置和大小
    window.show()

    sys.exit(app.exec_())
    print("PyQt5 已正确安装并可运行。")

except ImportError:
    print("PyQt5 未安装。")
