from PyQt5 import QtCore

class SCDPresenter(QtCore.QObject):

    # Define the signals
    leakageCurrentChanged = QtCore.pyqtSignal(int, float)
    
    def __init__(self, monitor, view):
        super(SCDPresenter, self).__init__()
        self._monitor = monitor
        self._view = view

        self._monitor.init()
        self._monitor.subscribe(self.handleMonitorEvent)

        self.leakageCurrentChanged.connect(self._view.changeCurrent)

    def changeBV(self, channel, voltage):
        self._monitor.set_bias_voltage(channel, voltage)

    def handleMonitorEvent(self, event):
        if event.type is "i_leak_changed":
            self.leakageCurrentChanged.emit(event.channel, event.current)
