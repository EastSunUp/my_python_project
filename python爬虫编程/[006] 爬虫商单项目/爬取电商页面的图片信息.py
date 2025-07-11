import sys
import os
import re
import time
import threading
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                             QProgressBar, QFileDialog, QMessageBox, QCheckBox, QSpinBox, QDialog)
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize, QBuffer, QByteArray
from fake_useragent import UserAgent


class ImageDownloader(QThread):
    progress_updated = pyqtSignal(int, int)
    image_found = pyqtSignal(str, str, str, QByteArray)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    # 在关于菜单中添加
    def show_about(self):
        text = """<b>拼多多商品图片爬取工具</b><p>
        本工具仅用于技术学习，请遵守:<ul>
        <li>《网络安全法》</li>
        <li>《电子商务法》</li>
        <li>拼多多用户协议</li></ul>
        使用本工具即表示您同意:<br>
        1. 不进行大规模商业爬取<br>
        2. 不绕过网站反爬措施<br>
        3. 24小时内请求不超过500次</p>"""
        QMessageBox.about(self, "法律声明", text)

    def __init__(self, url, min_size=0, max_size=9999):
        super().__init__()
        self.url = url
        self.min_size = min_size
        self.max_size = max_size
        self.image_urls = []
        self.running = True

    def run(self):
        try:
            # 获取网页内容
            ua = UserAgent()
            headers = {'User-Agent': ua.random}
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()

            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')

            # 收集图片URL
            base_url = self.url
            for i, img in enumerate(img_tags):
                if not self.running:
                    return

                src = img.get('src') or img.get('data-src')
                if not src:
                    continue

                # 处理相对URL
                img_url = urljoin(base_url, src)

                # 检查图片尺寸
                try:
                    img_response = requests.head(img_url, headers=headers, timeout=5)
                    img_size = int(img_response.headers.get('Content-Length', 0))

                    if self.min_size <= img_size <= self.max_size:
                        self.image_urls.append(img_url)
                        # 获取缩略图用于预览
                        thumb_data = self.get_thumbnail(img_url)
                        self.image_found.emit(img_url, f"图片 {len(self.image_urls)}", f"大小: {img_size // 1024} KB",
                                              thumb_data)
                        self.progress_updated.emit(i + 1, len(img_tags))
                except Exception as e:
                    continue
        except Exception as e:
            self.error_occurred.emit(f"错误: {str(e)}")
        finally:
            self.finished.emit()

    def get_thumbnail(self, img_url):
    # 爬取缩略图
        try:
            ua = UserAgent()
            headers = {'User-Agent': ua.random}
            response = requests.get(img_url, headers=headers, stream=True, timeout=5)
            response.raise_for_status()

            # 读取图片数据
            img_data = response.content

            # 创建QImage并调整大小
            image = QImage()
            image.loadFromData(img_data)

            # 调整大小为缩略图
            thumb = image.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # 转换为字节数组
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QBuffer.WriteOnly)
            thumb.save(buffer, "PNG")
            return byte_array
        except:
            return QByteArray()

    def stop(self):
        self.running = False


class ImageCrawlerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("电商图片爬取工具 v1.0")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QWidget {
                background-color: #34495e;
                color: #ecf0f1;
                font-family: 'Segoe UI', Arial;
            }
            QLineEdit, QListWidget, QProgressBar {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #3498db;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1d6fa5;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
            }
            QLabel {
                color: #ecf0f1;
            }
            QProgressBar {
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                width: 10px;
            }
            QCheckBox {
                spacing: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #7f8c8d;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)

        self.init_ui()
        self.downloader = None
        self.save_path = os.path.expanduser("~/Downloads")  # 指定的文件默认保存路径

        # 创建历史记录文件
        self.history_file = "crawler_history.txt"
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                pass

        self.load_history()

    def init_ui(self):
        # 主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 标题
        title_label = QLabel("电商图片爬取工具")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # URL输入区域
        url_layout = QHBoxLayout()
        url_label = QLabel("商品URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("请输入电商商品页面URL...")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input, 1)

        # 历史记录按钮
        self.history_btn = QPushButton("历史记录")
        self.history_btn.clicked.connect(self.show_history)
        url_layout.addWidget(self.history_btn)
        main_layout.addLayout(url_layout)

        # 图片大小筛选
        size_layout = QHBoxLayout()
        size_label = QLabel("图片大小筛选:")
        self.min_size_spin = QSpinBox()
        self.min_size_spin.setRange(0, 9999)
        self.min_size_spin.setValue(50)
        self.min_size_spin.setSuffix(" KB")
        self.max_size_spin = QSpinBox()
        self.max_size_spin.setRange(1, 10000)
        self.max_size_spin.setValue(1024)
        self.max_size_spin.setSuffix(" KB")
        size_layout.addWidget(size_label)
        size_layout.addWidget(QLabel("最小:"))
        size_layout.addWidget(self.min_size_spin)
        size_layout.addWidget(QLabel("最大:"))
        size_layout.addWidget(self.max_size_spin)
        size_layout.addStretch()
        main_layout.addLayout(size_layout)

        # 按钮区域
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始爬取")
        self.start_btn.clicked.connect(self.start_crawling)
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_crawling)
        self.save_btn = QPushButton("设置保存路径")
        self.save_btn.clicked.connect(self.set_save_path)
        self.download_btn = QPushButton("下载选中图片")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_selected)
        self.download_all_btn = QPushButton("下载全部图片")
        self.download_all_btn.setEnabled(False)
        self.download_all_btn.clicked.connect(self.download_all)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.download_btn)
        btn_layout.addWidget(self.download_all_btn)
        main_layout.addLayout(btn_layout)

        # 进度条
        self.progress_label = QLabel("就绪")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.progress_label)
        main_layout.addWidget(self.progress_bar)

        # 图片列表
        list_layout = QHBoxLayout()
        self.image_list = QListWidget()
        self.image_list.setIconSize(QSize(100, 100))
        self.image_list.setSelectionMode(QListWidget.ExtendedSelection)
        list_layout.addWidget(self.image_list, 2)

        # 预览区域
        preview_layout = QVBoxLayout()
        preview_label = QLabel("图片预览")
        preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(300, 300)
        self.preview_label.setStyleSheet("background-color: #2c3e50; border: 1px solid #3498db; border-radius: 4px;")
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.preview_label, 1)
        preview_layout.addStretch()

        # 图片信息
        info_layout = QVBoxLayout()
        self.info_label = QLabel("图片信息将显示在这里")
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)
        preview_layout.addLayout(info_layout)

        list_layout.addLayout(preview_layout, 1)
        main_layout.addLayout(list_layout, 1)

        # 连接信号
        self.image_list.itemSelectionChanged.connect(self.update_preview)

        # 状态栏
        self.statusBar().showMessage("就绪")
        self.path_label = QLabel(f"保存路径: {self.save_path}")
        self.statusBar().addPermanentWidget(self.path_label)

    def start_crawling(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "输入错误", "请输入有效的URL")
            return

        # 保存到历史记录
        self.save_to_history(url)

        # 清除之前的图片
        self.image_list.clear()
        self.preview_label.clear()
        self.info_label.clear()
        self.progress_bar.setValue(0)

        # 获取大小设置
        min_size = self.min_size_spin.value() * 1024
        max_size = self.max_size_spin.value() * 1024

        # 创建下载器线程
        self.downloader = ImageDownloader(url, min_size, max_size)
        self.downloader.progress_updated.connect(self.update_progress)
        self.downloader.image_found.connect(self.add_image_item)
        self.downloader.finished.connect(self.crawling_finished)
        self.downloader.error_occurred.connect(self.show_error)

        # 更新UI状态
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_label.setText("正在爬取图片...")
        self.statusBar().showMessage(f"正在爬取: {url}")

        self.downloader.start()

    def stop_crawling(self):
        if self.downloader:
            self.downloader.stop()
            self.downloader = None
            self.progress_label.setText("爬取已停止")
            self.statusBar().showMessage("爬取已停止")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

    def crawling_finished(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.download_btn.setEnabled(self.image_list.count() > 0)
        self.download_all_btn.setEnabled(self.image_list.count() > 0)
        self.progress_label.setText(f"爬取完成，找到 {self.image_list.count()} 张图片")
        self.statusBar().showMessage("爬取完成")

    def update_progress(self, current, total):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.progress_label.setText(f"正在分析: {current}/{total} 张图片")

    def add_image_item(self, url, title, info, thumb_data):
        item = QListWidgetItem()
        item.setText(f"{title}\n{info}")
        item.setData(Qt.UserRole, url)  # 存储原始URL

        # 设置缩略图
        if thumb_data and not thumb_data.isEmpty():
            pixmap = QPixmap()
            pixmap.loadFromData(thumb_data)
            item.setIcon(QIcon(pixmap))

        self.image_list.addItem(item)

    def update_preview(self):
        selected_items = self.image_list.selectedItems()
        if not selected_items:
            self.preview_label.clear()
            self.info_label.setText("请选择一张图片进行预览")
            return

        item = selected_items[0]
        url = item.data(Qt.UserRole)
        self.info_label.setText(f"图片URL:\n{url}")

        # 在单独的线程中加载预览图
        threading.Thread(target=self.load_preview_image, args=(url,), daemon=True).start()

    def load_preview_image(self, url):
        try:
            ua = UserAgent()
            headers = {'User-Agent': ua.random}
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()

            img_data = response.content
            image = QImage()
            image.loadFromData(img_data)

            # 调整大小以适应预览区域
            scaled = image.scaled(self.preview_label.width(), self.preview_label.height(),
                                  Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap = QPixmap.fromImage(scaled)

            # 在主线程更新UI
            self.preview_label.setPixmap(pixmap)
            self.statusBar().showMessage(f"预览: {os.path.basename(url)}")
        except Exception as e:
            self.preview_label.setText("无法加载预览图")
            self.statusBar().showMessage(f"预览错误: {str(e)}")

    def set_save_path(self):
        path = QFileDialog.getExistingDirectory(self, "选择保存路径", self.save_path)
        if path:
            self.save_path = path
            self.path_label.setText(f"保存路径: {path}")

    def download_selected(self):
        selected_items = self.image_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "选择错误", "请选择要下载的图片")
            return

        self.download_images([item.data(Qt.UserRole) for item in selected_items])

    def download_all(self):
        if self.image_list.count() == 0:
            QMessageBox.warning(self, "下载错误", "没有可下载的图片")
            return

        urls = [self.image_list.item(i).data(Qt.UserRole) for i in range(self.image_list.count())]
        self.download_images(urls)

    def download_images(self, urls):
        if not urls:
            return

        # 创建保存目录
        save_dir = os.path.join(self.save_path, "crawled_images")
        os.makedirs(save_dir, exist_ok=True)

        # 下载进度
        self.progress_label.setText(f"正在下载 0/{len(urls)} 张图片...")
        self.progress_bar.setMaximum(len(urls))
        self.progress_bar.setValue(0)
        self.statusBar().showMessage(f"正在下载图片到: {save_dir}")

        # 在后台线程下载
        def download_thread():
            ua = UserAgent()
            success = 0
            for i, url in enumerate(urls):
                try:
                    filename = os.path.basename(url).split('?')[0]
                    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        filename += '.jpg'

                    filepath = os.path.join(save_dir, filename)

                    # 防止文件名重复
                    counter = 1
                    while os.path.exists(filepath):
                        # 分类文件名、文件格式名
                        name, ext = os.path.splitext(filename)
                        filepath = os.path.join(save_dir, f"{name}_{counter}{ext}")
                        counter += 1

                    headers = {'User-Agent': ua.random}
                    response = requests.get(url, headers=headers, timeout=15)
                    response.raise_for_status()

                    with open(filepath, 'wb') as f:
                        f.write(response.content)

                    success += 1
                except Exception as e:
                    print(f"下载失败: {url} - {str(e)}")

                # 更新进度
                self.progress_bar.setValue(i + 1)
                self.progress_label.setText(f"正在下载 {i + 1}/{len(urls)} 张图片...")

            # 完成后更新UI
            self.progress_label.setText(f"下载完成! 成功: {success}/{len(urls)}")
            self.statusBar().showMessage(f"图片已保存到: {save_dir}")
            QMessageBox.information(self, "下载完成", f"成功下载 {success} 张图片到:\n{save_dir}")

        threading.Thread(target=download_thread, daemon=True).start()

    def save_to_history(self, url):
        # 保存到历史记录文件
        with open(self.history_file, 'a') as f:
            f.write(url + '\n')

    def load_history(self):
        # 加载历史记录
        try:
            with open(self.history_file, 'r') as f:
                self.history = [line.strip() for line in f.readlines() if line.strip()]
        except:
            self.history = []

    def show_history(self):
        if not self.history:
            QMessageBox.information(self, "历史记录", "没有历史记录")
            return

        # 创建历史记录对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("历史记录")
        dialog.setGeometry(300, 300, 500, 400)
        layout = QVBoxLayout()

        list_widget = QListWidget()
        list_widget.addItems(self.history)
        layout.addWidget(list_widget)

        btn_layout = QHBoxLayout()
        load_btn = QPushButton("加载选中")
        load_btn.clicked.connect(lambda: self.load_selected_url(list_widget, dialog))
        clear_btn = QPushButton("清除历史")
        clear_btn.clicked.connect(lambda: self.clear_history(list_widget, dialog))
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.close)

        btn_layout.addWidget(load_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def load_selected_url(self, list_widget, dialog):
        selected = list_widget.selectedItems()
        if selected:
            self.url_input.setText(selected[0].text())
            dialog.close()

    def clear_history(self, list_widget, dialog):
        reply = QMessageBox.question(self, "确认", "确定要清除所有历史记录吗?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.history = []
            list_widget.clear()
            open(self.history_file, 'w').close()
            dialog.close()

    def show_error(self, message):
        QMessageBox.critical(self, "错误", message)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_label.setText("爬取失败")

    def closeEvent(self, event):
        if self.downloader and self.downloader.isRunning():
            self.downloader.stop()
            self.downloader.wait(1000)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCrawlerApp()
    window.show()
    sys.exit(app.exec_())
