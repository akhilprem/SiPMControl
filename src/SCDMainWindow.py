from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

from SCDMainWindow_Ui import Ui_SCDMainWindow
from SCDChannelTestDialog_Ui import Ui_SCDChannelTestDialog
from SCDPresenter import SCDPresenter
from SCDConstants import SCDConstants

class SCDMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent = None):
        super(SCDMainWindow, self).__init__()
        self.ui = Ui_SCDMainWindow()
        self.ui.setupUi(self)
        
        # Setup channel test dialog.
        self.cTestDlg = QDialog()
        self.cTestDlg.ui = Ui_SCDChannelTestDialog()
        self.cTestDlg.ui.setupUi(self.cTestDlg)
        self.cTestDlg.ui.settlingTimeSpinBox.setMinimum(SCDConstants.CTEST_MIN_SETTLING_TIME_MS)
        self.cTestDlg.ui.settlingTimeSpinBox.setMaximum(SCDConstants.CTEST_MAX_SETTLING_TIME_MS)
        self.cTestDlg.ui.settlingTimeSpinBox.setValue(SCDConstants.CTEST_NOM_SETTLING_TIME_MS)
        
        self.ui.i2cBusLineEdit.setText(str(SCDConstants.DEFAULT_I2C_BUS))
        
        self.ui.readPerTimeSpinBox.setMinimum(SCDConstants.MIN_PERIODIC_READ_INTERVAL_MS)
        self.ui.readPerTimeSpinBox.setMaximum(SCDConstants.MAX_PERIODIC_READ_INTERVAL_MS)
        self.ui.readPerTimeSpinBox.setValue(SCDConstants.DEFAULT_PERIODIC_READ_INTERVAL_MS)
        
        self._diagnosticVoltagesModel = QtGui.QStandardItemModel(SCDConstants.NUM_DIAGNOSTICS, 2, self)
        self._diagnosticVoltagesModel.setHorizontalHeaderLabels(["Reading", "Value(V)"]) # User vert. header to reg #.
        self.ui.adcTableView.setModel(self._diagnosticVoltagesModel)
        
        readingLabels = ["Vin/6", "Vdd/2", "BV-IN/79", "V_Peltier/6", "I_Peltier", "*T/RH-1", "*T/RH-2"]
        for row in range(SCDConstants.NUM_DIAGNOSTICS): 
            index = self._diagnosticVoltagesModel.index(row, 0, QtCore.QModelIndex())
            self._diagnosticVoltagesModel.setData(index, readingLabels[row])
            item = self._diagnosticVoltagesModel.itemFromIndex(index)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
        
        self._channelVoltageCurrentModel = QtGui.QStandardItemModel(SCDConstants.NUM_CHANNELS, 3, self)
        self._channelVoltageCurrentModel.setHorizontalHeaderLabels(["ID", "Bias Voltage(V)", "Leakage Current(uA)"])
        self.ui.dacTableView.setModel(self._channelVoltageCurrentModel)
        
        # Stretch columns to fit available width.
        hHeader = self.ui.adcTableView.horizontalHeader()
        hHeader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        hHeader = self.ui.dacTableView.horizontalHeader()
        hHeader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        hHeader.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        
        self.ui.adcTableView.verticalHeader().hide()
        self.ui.dacTableView.verticalHeader().hide()
        
        # Fill column 1 with channel id and make the first and third column uneditable.
        # Is there a better way to do the latter in one sweep?
        for row in range(SCDConstants.NUM_CHANNELS): 
            index_0 = self._channelVoltageCurrentModel.index(row, 0, QtCore.QModelIndex())
            index_1 = self._channelVoltageCurrentModel.index(row, 1, QtCore.QModelIndex())
            index_2 = self._channelVoltageCurrentModel.index(row, 2, QtCore.QModelIndex())
            self._channelVoltageCurrentModel.setData(index_0, row)
            item = self._channelVoltageCurrentModel.itemFromIndex(index_0)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            item = self._channelVoltageCurrentModel.itemFromIndex(index_1)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item = self._channelVoltageCurrentModel.itemFromIndex(index_2)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)       
        

    def setPresenter(self, presenter):
        self._presenter = presenter
        
        # Setup signals and slots for the UI
        self._channelVoltageCurrentModel.itemChanged.connect(self.handleChannelItemChange)
        self.ui.readPerStartButton.clicked.connect(self.startPeriodic)
        self.ui.readPerStopButton.clicked.connect(self._presenter.stopPeriodic)
        self.ui.readOnceButton.clicked.connect(self._presenter.readAllOnce)
        self.ui.setAllBVButton.clicked.connect(self.setAllBVs)
        self.ui.saveToFileButton.clicked.connect(self.saveToFile)
        self.ui.runChannelTestButton.clicked.connect(self.openChannelTestDialog)
        self.cTestDlg.ui.saveLocBrowseButton.clicked.connect(self.browseCTestSaveLoc)

        turnLEDOn = lambda : self._presenter.setPulserLED(True)
        turnLEDOff = lambda : self._presenter.setPulserLED(False)
        self.ui.pulserLEDOnButton.clicked.connect(turnLEDOn)
        self.ui.pulserLEDOffButton.clicked.connect(turnLEDOff) 


    def handleChannelItemChange(self, item):
        if item.column() == 1: # i.e. if the voltage was changed
            channel = item.row() # The regulators are numbered starting from 0.
            voltage = item.data(QtCore.Qt.DisplayRole)
            self._presenter.changeBV(int(channel), float(voltage))
        
    @QtCore.pyqtSlot(int, float)
    def changeVoltageDisplay(self, channel, voltage):
        index = self._channelVoltageCurrentModel.index(channel, 1, QtCore.QModelIndex())
        self._channelVoltageCurrentModel.setData(index, voltage)
    
    @QtCore.pyqtSlot(int, float)
    def changeCurrentDisplay(self, channel, current):
        index = self._channelVoltageCurrentModel.index(channel, 2, QtCore.QModelIndex())
        self._channelVoltageCurrentModel.setData(index, current)

    @QtCore.pyqtSlot(list)
    def changeDiagnosticsDisplay(self, voltages):
        if len(voltages) != SCDConstants.NUM_DIAGNOSTICS:
            return  # There was some problem reading the data.
        
        for row in range(SCDConstants.NUM_DIAGNOSTICS): 
            index = self._diagnosticVoltagesModel.index(row, 1, QtCore.QModelIndex())
            self._diagnosticVoltagesModel.setData(index, voltages[row])
    
    def startPeriodic(self):
        self._presenter.startPeriodic(self.ui.readPerTimeSpinBox.value())

    
    # TBD: Change this approach. Set BV should be a single value sent to the monitor.
    def setAllBVs(self, voltage):
        voltage = self.ui.setAllBVSpinBox.value()
        self._presenter.setAllBVs(voltage)
    
    
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
            
            # Disconnect itemChanged signal so that 'bv_adjusted' event does not
            # cause the current to be set a second time. This will be reconnected on
            # 'channel_test_finished' event.
            self._channelVoltageCurrentModel.itemChanged.disconnect(self.handleChannelItemChange)
            self._presenter.startChannelTest()


    def handleChannelTestFinished(self):
        self._channelVoltageCurrentModel.itemChanged.connect(self.handleChannelItemChange)


    def saveToFile(self):
        fileName = self._getSaveLocationFromUser()
        if fileName:
            saveFile = open(fileName, 'w')
            saveFile.write('ID, Bias Voltage(V), Leakage Current (uA)\n')
            
            # A very crude way of serializing the data model.
            for row in range(SCDConstants.NUM_CHANNELS):
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
