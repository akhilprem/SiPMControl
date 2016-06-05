# Threading code taken from: http://stackoverflow.com/a/19017560

from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class SCDChannelTestParams:
    channels = []
    biasVoltages = []
    saveLoc = ""

class SCDPresenter(QtCore.QObject):

    # Define the signals
    leakageCurrentChanged = QtCore.pyqtSignal(int, float)
    
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

        self.leakageCurrentChanged.connect(self._view.changeCurrent)

    
    def changeBV(self, channel, voltage):
        QtCore.QMetaObject.invokeMethod(self._monitor, 'set_bias_voltage', Qt.QueuedConnection,
                                        QtCore.Q_ARG(int, channel),
                                        QtCore.Q_ARG(int, voltage)) # FIX to float
        # self._monitor.set_bias_voltage(channel, voltage)

    
    # This function will be invoked inside the monitor thread
    def handleMonitorEvent(self, event):
        if event.type is "i_leak_changed":
            self.leakageCurrentChanged.emit(event.channel, event.current)
    
    
    def setChannelTestParams(self, channelsTxt, biasVoltagesTxt, saveLocation):
        try:
            self.channelTestParams.channels = [int(ch) for ch in channelsTxt.split(",")]
        except ValueError: # Empty text also causes value error.
            return (False, "Invalid channel number(s).", "")
        
        try:
            self.channelTestParams.biasVoltages = [float(bv) for bv in biasVoltagesTxt.split(",")]
        except ValueError:
            return (False, "Invalid bias voltage(s).", "")
        
        self.channelTestParams.saveLoc = saveLocation
        
        return (True, "", "")
    
    def runChannelTest(self):
        pass