# A tool to control and monitor the SiPM control board.

import sys
from PyQt5.QtWidgets import QApplication
from SCDMainWindow import SCDMainWindow

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = SCDMainWindow(None)
    sys.exit(app.exec_())