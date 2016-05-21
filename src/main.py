# A tool to control and monitor the SiPM control board.

import sys
from PyQt5.QtWidgets import QApplication

from SCDMonitor import SCDMonitor
from SCDPresenter import SCDPresenter
from SCDMainWindow import SCDMainWindow

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    monitor = SCDMonitor()
    view = SCDMainWindow()
    presenter = SCDPresenter(monitor, view)
    view.setPresenter(presenter)
    view.show()
    sys.exit(app.exec_())