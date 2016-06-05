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
    leakageCurrentChanged = QtCore.pyqtSignal(int, float)
    channelTestFinished = QtCore.pyqtSignal()
    
    def __init__(self, monitor, view):
        super(SCDPresenter, self).__init__()
        self._monitor = monitor
        self._view = view
        self._thread = QtCore.QThread()
        
        self._monitor.subscribe(self.handleMonitorEvent)
        self._monitor.moveToThread(self._thread)
        
        self._thread.started.connect(self._monitor.initialize)
        self._thread.start()
        
        self.channelTestParams = SCDChannelTestParams()
        self.channelTestReadings = {} # Dictionary with structure --> voltage: {channel:i_leak}

        self.leakageCurrentChanged.connect(self._view.changeCurrent)
        self.channelTestFinished.connect(self.saveChannelTestData)

    
    def changeBV(self, channel, voltage):
        QtCore.QMetaObject.invokeMethod(self._monitor, 'set_bias_voltage', Qt.QueuedConnection,
                                        QtCore.Q_ARG(int, channel),
                                        QtCore.Q_ARG(int, voltage)) # FIX to float
        # self._monitor.set_bias_voltage(channel, voltage)

    
    # This function will be invoked inside the monitor thread
    def handleMonitorEvent(self, event):
        if event.type is "i_leak_changed":
            self.leakageCurrentChanged.emit(event.channel, event.current)
        
        elif event.type is "channel_test_finished":
            self.channelTestReadings = event.readings # TBD: Protect this with a mutex.
            self.channelTestFinished.emit()
    
    def setChannelTestParams(self, channelsTxt, biasVoltagesTxt, settlingTime, saveLocation):
        try:
            self.channelTestParams.channels = [int(ch) for ch in channelsTxt.split(",")]
        except ValueError: # Empty text also causes value error.
            return (False, "Invalid channel number(s).", "")
        
        try:
            self.channelTestParams.biasVoltages = [float(bv) for bv in biasVoltagesTxt.split(",")]
        except ValueError:
            return (False, "Invalid bias voltage(s).", "")
        
        self.channelTestParams.settlingTimeMs = settlingTimeMs
        self.channelTestParams.saveLoc = saveLocation
        
        return (True, "", "")
    
    def startChannelTest(self):
        self._monitor.run_channel_test(self.channelTestParams.channels,
                                       self.channelTestParams.biasVoltages,
                                       self.channelTestParams.settlingTimeMs)
        
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
                