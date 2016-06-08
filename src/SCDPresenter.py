# Threading code taken from: http://stackoverflow.com/a/19017560

from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class SCDChannelTestParams:
    channels = []
    biasVoltages = []
    settlingTimeMs = 0
    saveLoc = ""

class SCDPresenter(QtCore.QObject):

    # Define the signals
    biasVoltageAdjusted = QtCore.pyqtSignal(int, float)
    leakageCurrentChanged = QtCore.pyqtSignal(int, float)
    setAllBVFinished = QtCore.pyqtSignal()
    channelTestFinished = QtCore.pyqtSignal()
    readDiagnosticsFinished = QtCore.pyqtSignal(list)
#     biasVoltageSet = QtCore.pyqtSignal(int, float)
    
    def __init__(self, monitor, view):
        super(SCDPresenter, self).__init__()
        self._monitor = monitor
        self._view = view
        self._thread = QtCore.QThread()
        
#         self.biasVoltageSet.connect(self._monitor.set_bias_voltage)
        self._monitor.subscribe(self.handleMonitorEvent)
        self._monitor.moveToThread(self._thread)
        
        self._thread.started.connect(self._monitor.initialize)
        self._thread.start()
        
        self.channelTestParams = SCDChannelTestParams()
        self.channelTestReadings = {} # Dictionary with structure --> voltage: {channel:i_leak}
        
        self.biasVoltageAdjusted.connect(self._view.changeVoltageDisplay)
        self.leakageCurrentChanged.connect(self._view.changeCurrentDisplay)
        self.channelTestFinished.connect(self.saveChannelTestData)
        self.setAllBVFinished.connect(self._view.handleSequentialOperationFinished)
        self.channelTestFinished.connect(self._view.handleSequentialOperationFinished)
        self.readDiagnosticsFinished.connect(self._view.changeDiagnosticsDisplay)

    def startPeriodic(self, timeIntervalInMs):
        QtCore.QMetaObject.invokeMethod(self._monitor, 'start_periodic', Qt.QueuedConnection,
                                        QtCore.Q_ARG(int, timeIntervalInMs))


    def stopPeriodic(self):
        self._monitor.stop_periodic() # NOTE: Only this method is directly invoked.

    
    def readAllDiagnostics(self):
        QtCore.QMetaObject.invokeMethod(self._monitor, 'read_diagnostics', Qt.QueuedConnection)
    
    
    def changeBV(self, channel, voltage):
        QtCore.QMetaObject.invokeMethod(self._monitor, 'set_bias_voltage', Qt.QueuedConnection,
                                        QtCore.Q_ARG(int, channel),
                                        QtCore.Q_ARG(float, voltage))
        
#         self.biasVoltageSet.emit(channel, float(voltage))


    def setAllBVs(self, voltage):
        QtCore.QMetaObject.invokeMethod(self._monitor, 'set_all_bias_voltages', Qt.QueuedConnection,
                                        QtCore.Q_ARG(float, voltage))
    
    
    # This function will be invoked inside the monitor thread. We communicate the changes made in
    # the hardware via Qt signals and slots which automatically takes care of communication between threads.
    def handleMonitorEvent(self, event):
        if event.type is "bv_adjusted":
            self.biasVoltageAdjusted.emit(event.channel, event.voltage)
        
        elif event.type is "i_leak_changed":
            self.leakageCurrentChanged.emit(event.channel, event.current)

        elif event.type is "set_all_bv_finished":
            self.setAllBVFinished.emit()
        
        elif event.type is "channel_test_finished":
            self.channelTestReadings = event.readings # TBD: Protect this with a mutex.
            self.channelTestFinished.emit()
            
        elif event.type is "read_diagnostics_finished":
            self.readDiagnosticsFinished.emit(event.voltages)
    
    
    def setChannelTestParams(self, channelsTxt, biasVoltagesTxt, settlingTimeMs, saveLocation):
        try:
            self.channelTestParams.channels = [int(ch) for ch in channelsTxt.split(",")]
        except ValueError: # Empty text also causes value error.
            return (False, "Invalid channel number(s).", "")
        
        try:
            self.channelTestParams.biasVoltages = [float(bv) for bv in biasVoltagesTxt.split(",")]
        except ValueError:
            return (False, "Invalid bias voltage(s).", "")
        
        self.channelTestParams.settlingTimeMs = int(settlingTimeMs)
        self.channelTestParams.saveLoc = saveLocation
        
        return (True, "", "")
    
    
    def startChannelTest(self):
        QtCore.QMetaObject.invokeMethod(self._monitor, 'run_channel_test', Qt.QueuedConnection,
                                        QtCore.Q_ARG(list, self.channelTestParams.channels),
                                        QtCore.Q_ARG(list, self.channelTestParams.biasVoltages),
                                        QtCore.Q_ARG(int, self.channelTestParams.settlingTimeMs))
        
    
    def saveChannelTestData(self):
        try:
            saveFile = open(self.channelTestParams.saveLoc, 'w')
            saveFile.write('ID, Bias Voltage(V), Leakage Current (uA)\n')
            
            for voltage, readings in self.channelTestReadings.items():
                for channel, current in readings.items():
                    saveFile.write("{},{},{}\n".format(channel, voltage, current))
    
            saveFile.close()
            
        except Exception as e:
            print "Error saving channel test data to file."

    def setPulserLED(self, enable):
        QtCore.QMetaObject.invokeMethod(self._monitor, 'set_pulser_LED', Qt.QueuedConnection,
                                        QtCore.Q_ARG(bool, enable))
                
