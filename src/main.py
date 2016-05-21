# A tool to control and monitor the SiPM control board.

import sys
from PyQt5.QtWidgets import QApplication

from SCDMonitor import SCDMonitor
from SCDMainWindow import SCDMainWindow

if __name__ == '__main__':
    
    monitor = SCDMonitor()
    
    app = QApplication(sys.argv)
    ex = SCDMainWindow(None)
    sys.exit(app.exec_())