from PyQt5 import QtGui, QtCore, QtWidgets

from SCDMainWindow_Ui import Ui_SCDMainWindow

class SCDMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent = None):
#         QWidget.__init__(self, parent)    # This will work too.
        super(SCDMainWindow, self).__init__()
        self.ui = Ui_SCDMainWindow()
        self.ui.setupUi(self)
        
        self._adcReadOutModel = QtGui.QStandardItemModel(48, 2, self)
        self._adcReadOutModel.setHorizontalHeaderLabels(["ID/Reading", "Value"]) # User vert. header to reg #.
        self.ui.adcTableView.setModel(self._adcReadOutModel)
        
        self._dacVoltagesModel = QtGui.QStandardItemModel(48, 2, self)
        self._dacVoltagesModel.setHorizontalHeaderLabels(["ID", "Bias Voltage"])
        self.ui.dacTableView.setModel(self._dacVoltagesModel)
        
        # Stretch columns to fit available width.
        hHeader = self.ui.adcTableView.horizontalHeader()
        hHeader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        hHeader = self.ui.dacTableView.horizontalHeader()
        hHeader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.ui.adcTableView.verticalHeader().hide()
        self.ui.dacTableView.verticalHeader().hide()
        
        self.show();