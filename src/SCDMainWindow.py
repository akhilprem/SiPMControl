from PyQt5 import QtGui, QtCore, QtWidgets

from SCDMainWindow_Ui import Ui_SCDMainWindow
from SCDPresenter import SCDPresenter

class SCDMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent = None):
        super(SCDMainWindow, self).__init__()
        self.ui = Ui_SCDMainWindow()
        self.ui.setupUi(self)
        
        self.NUM_CHANNELS = 48  # TBD: This information should come from elsewhere.
        
        self._adcReadOutModel = QtGui.QStandardItemModel(self.NUM_CHANNELS, 2, self)
        self._adcReadOutModel.setHorizontalHeaderLabels(["Reading", "Value(V)"]) # User vert. header to reg #.
        self.ui.adcTableView.setModel(self._adcReadOutModel)
        
        self._channelVoltageCurrentModel = QtGui.QStandardItemModel(self.NUM_CHANNELS, 3, self)
        self._channelVoltageCurrentModel.setHorizontalHeaderLabels(["ID", "Bias Voltage(V)", "Leakage Current(uA)"])
        self.ui.dacTableView.setModel(self._channelVoltageCurrentModel)
        
        # Stretch columns to fit available width.
        hHeader = self.ui.adcTableView.horizontalHeader()
        hHeader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        hHeader = self.ui.dacTableView.horizontalHeader()
        hHeader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.ui.adcTableView.verticalHeader().hide()
        self.ui.dacTableView.verticalHeader().hide()
        
        # Fill column 1 with channel id and make the first and third column uneditable.
        # Is there a better way to do the latter in one sweep?
        for row in range(self.NUM_CHANNELS): 
            index_0 = self._channelVoltageCurrentModel.index(row, 0, QtCore.QModelIndex())
            index_2 = self._channelVoltageCurrentModel.index(row, 2, QtCore.QModelIndex())
            self._channelVoltageCurrentModel.setData(index_0, row)
            item = self._channelVoltageCurrentModel.itemFromIndex(index_0)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            item = self._channelVoltageCurrentModel.itemFromIndex(index_2)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

        self.ui.setAllBVButton.clicked.connect(self.setAllBVs)

    def setPresenter(self, presenter):
        self._presenter = presenter
        self._channelVoltageCurrentModel.itemChanged.connect(self.handleChannelItemChange)


    def handleChannelItemChange(self, item):
        if item.column() == 1: # i.e. if the voltage was changed
            channel = item.row() # The regulators are numbered starting from 0.
            voltage = item.data(QtCore.Qt.DisplayRole)
            self._presenter.changeBV(channel, voltage)
        
    def changeCurrent(self, channel, current):
        index = self._channelVoltageCurrentModel.index(channel, 2, QtCore.QModelIndex())
        self._channelVoltageCurrentModel.setData(index, current)

    def setAllBVs(self, voltage):
        voltage = self.ui.setAllBVSpinBox.value()
        
        for row in range(self.NUM_CHANNELS):
            index = self._channelVoltageCurrentModel.index(row, 1, QtCore.QModelIndex())
            self._channelVoltageCurrentModel.setData(index, voltage)
    
        
