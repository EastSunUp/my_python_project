
# test_webengine.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

app = QApplication(sys.argv)

view = QWebEngineView()
view.setUrl(QUrl("https://www.baidu.com"))
view.show()

sys.exit(app.exec())
