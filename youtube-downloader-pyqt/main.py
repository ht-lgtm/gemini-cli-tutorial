import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

class DownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube Downloader')
        self.resize(500, 200)

        # 메인 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DownloaderApp()
    window.show()
    sys.exit(app.exec_())
