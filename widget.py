import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QDesktopWidget

class ScreenWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Screen Widget')
        self.setGeometry(100, 100, 300, 300)
        self.label = QLabel('This is a screen widget', self)
        self.label.move(50, 50)
        screen = QDesktopWidget().screenGeometry()
        widget_size = self.geometry()
        x = screen.width() - widget_size.width()
        y = 0
        self.move(x, y) # move to top right corner
        self.label.adjustSize()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_widget = ScreenWidget()
    sys.exit(app.exec_())