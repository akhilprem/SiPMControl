from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

from SCDMainWindow_Ui import Ui_SCDMainWindow
from SCDChannelTestDialog_Ui import Ui_SCDChannelTestDialog
from SCDPresenter import SCDPresenter

class SCDMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent = None):
        super(SCDMainWindow, self).__init__()
        self.ui = Ui_SCDMainWindow()
        self.ui.setupUi(self)
        
        self.NUM_CHANNELS = 48  # TBD: This information should come from elsewhere.
        self.CTEST_MIN_SETTLING_TIME_MS = 50
        self.CTEST_MAX_SETTLING_TIME_MS = 5000
        self.CTEST_NOM_SETTLING_TIME_MS = 200
        
        # Setup channel test dialog.
        self.cTestDlg = QDialog()
        self.cTestDlg.ui = Ui_SCDChannelTestDialog()
        self.cTestDlg.ui.setupUi(self.cTestDlg)
        self.cTestDlg.ui.settlingTimeSpinBox.setMinimum(self.CTEST_MIN_SETTLING_TIME_MS)
        self.cTestDlg.ui.settlingTimeSpinBox.setMaximum(self.CTEST_MAX_SETTLING_TIME_MS)
        self.cTestDlg.ui.settlingTimeSpinBox.setValue(self.CTEST_NOM_SETTLING_TIME_MS)
        
        
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
        
        # Setup signals and slots for the UI
        self.ui.setAllBVButton.clicked.connect(self.setAllBVs)
        self.ui.saveToFileButton.clicked.connect(self.saveToFile)
        self.ui.runChannelTestButton.clicked.connect(self.openChannelTestDialog)
        self.cTestDlg.ui.saveLocBrowseButton.clicked.connect(self.browseCTestSaveLoc)

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

    
    # TBD: Change this approach. Set BV should be a single value sent to the monitor.
    def setAllBVs(self, voltage):
        voltage = self.ui.setAllBVSpinBox.value()
        
        for row in range(self.NUM_CHANNELS):
            index = self._channelVoltageCurrentModel.index(row, 1, QtCore.QModelIndex())
            self._channelVoltageCurrentModel.setData(index, voltage)
    
    
    def openChannelTestDialog(self):
        self.cTestDlg.exec_()
        
        if self.cTestDlg.result() == QDialog.Accepted:
            isParamsOk, errorMsg, errorDetails = \
                self._presenter.setChannelTestParams(self.cTestDlg.ui.channelLine.text(),
                                                     self.cTestDlg.ui.bvLine.text(),
                                                     self.cTestDlg.ui.settlingTimeSpinBox.value(),
                                                     self.cTestDlg.ui.saveLocLine.text())
            if isParamsOk is False:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(errorMsg)
                msg.setDetailedText(errorDetails)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            
            # If the parameters are fine run the test.
            self._presenter.startChannelTest()

    def saveToFile(self):
        fileName = self._getSaveLocationFromUser()
        if fileName:
            saveFile = open(fileName, 'w')
            saveFile.write('ID, Bias Voltage(V), Leakage Current (uA)\n')
            
            # A very crude way of serializing the data model.
            for row in range(self.NUM_CHANNELS):
                data = [0, 0, 0]
                for col in range(self._channelVoltageCurrentModel.columnCount()):
                    index = self._channelVoltageCurrentModel.index(row, col, QtCore.QModelIndex())
                    item = self._channelVoltageCurrentModel.itemFromIndex(index)
                    data[col] = item.data(QtCore.Qt.DisplayRole)
                saveFile.write("{},{},{}\n".format(data[0], data[1], data[2]))

            saveFile.close()
    
    
    def browseCTestSaveLoc(self):
        fileName = self._getSaveLocationFromUser()
        self.cTestDlg.ui.saveLocLine.setText(fileName)
    
    
    def _getSaveLocationFromUser(self):
        fileNameExt = QtWidgets.QFileDialog.getSaveFileName(self, 'Save', '~/Data.csv', '*.csv')
        if fileNameExt:
            fileName = fileNameExt[0]
            if fileName[-4:] != '.csv':
                fileName = fileName + '.csv'  # QFileDialog's convenience function doesn't add the extension.
            return fileName
        
        return ""