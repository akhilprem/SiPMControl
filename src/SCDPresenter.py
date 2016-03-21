from PyQt5 import QtCore

class SCDPresenter:
    def __init__(self, monitor, view):
        self._monitor = monitor
        self._view = view

        self._monitor.init()
        
    def handleBVChange(self, item):
        index = item.row() # It is better to number the regulators from 0
        voltage = item.data(QtCore.Qt.DisplayRole)
        self._monitor.set_bias_voltage(index, voltage)
