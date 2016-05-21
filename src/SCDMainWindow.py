from PyQt5 import QtGui, QtCore, QtWidgets

from SCDMainWindow_Ui import Ui_SCDMainWindow

class SCDMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent = None):
#         QWidget.__init__(self, parent)    # This will work too.
        super(SCDMainWindow, self).__init__()
        self.ui = Ui_SCDMainWindow()
        self.ui.setupUi(self)
        
        self._model = QtGui.QStandardItemModel(48, 2, self)
        self._model.setHorizontalHeaderLabels(["Reading", "Value"]) # User vert. header to reg #.
        self.ui.adcTableView.setModel(self._model)
        
        # Stretch columns to fit available width.
        hHeader = self.ui.adcTableView.horizontalHeader()
        hHeader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.show();