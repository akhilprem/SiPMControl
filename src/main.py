# A tool to control and monitor the SiPM control board.

# Make sure to:
#   1. Convert the .ui files in the /ui folder to a .py file using:
#       pyuic5 SCDMainWindow.ui > SCDMainWindow_Ui.py
#   and copy the latter to the src folder.
#
#   2. Start the pigpio daemon using the command:
#   sudo pigpiod

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
