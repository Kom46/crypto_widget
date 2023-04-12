from PyQt5.QtWidgets import QApplication
from widget import ScreenWidget
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_widget = ScreenWidget()
    sys.exit(app.exec_())