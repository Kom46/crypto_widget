from PyQt5.QtWidgets import QApplication
from widget import ScreenWidget
import sys
from finance import stockClient

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_widget = ScreenWidget()
    client = stockClient()
    sys.exit(app.exec_())