from PyQt5 import QtGui, QtCore, QtWidgets

from SCDMainWindow_Ui import Ui_SCDMainWindow
from SCDPresenter import SCDPresenter

class SCDMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent = None):
#         QWidget.__init__(self, parent)    # This will work too.
        super(SCDMainWindow, self).__init__()
        self.ui = Ui_SCDMainWindow()
        self.ui.setupUi(self)
        
        self.NUM_ROWS = 48  # TBD: This information should come from elsewhere.
        
        self._adcReadOutModel = QtGui.QStandardItemModel(self.NUM_ROWS, 2, self)
        self._adcReadOutModel.setHorizontalHeaderLabels(["ID/Reading", "Value"]) # User vert. header to reg #.
        self.ui.adcTableView.setModel(self._adcReadOutModel)
        
        self._dacVoltagesModel = QtGui.QStandardItemModel(self.NUM_ROWS, 2, self)
        self._dacVoltagesModel.setHorizontalHeaderLabels(["ID", "Bias Voltage"])
        self.ui.dacTableView.setModel(self._dacVoltagesModel)
        
        # Stretch columns to fit available width.
        hHeader = self.ui.adcTableView.horizontalHeader()
        hHeader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        hHeader = self.ui.dacTableView.horizontalHeader()
        hHeader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.ui.adcTableView.verticalHeader().hide()
        self.ui.dacTableView.verticalHeader().hide()
        
        # Make the first column uneditable. Is there a better way to do this?
        for row in range(self.NUM_ROWS): 
            index = self._dacVoltagesModel.index(row, 0, QtCore.QModelIndex())
            self._dacVoltagesModel.setData(index, row + 1)
            item = self._dacVoltagesModel.itemFromIndex(index)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        
    def setPresenter(self, presenter):
        self._presenter = presenter
        self._dacVoltagesModel.itemChanged.connect(self._presenter.handleBVChange)