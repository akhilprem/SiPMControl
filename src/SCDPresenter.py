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

    def handleBVChange(self, item):
        channel = item.row() # The regulators are numbered starting from 0.
        voltage = item.data(QtCore.Qt.DisplayRole)
        self._monitor.set_bias_voltage(channel, voltage)

    def handleMonitorEvent(self, event):
        if event.type is "bv_changed":
            self.leakageCurrentChanged.emit(event.channel, event.current)
