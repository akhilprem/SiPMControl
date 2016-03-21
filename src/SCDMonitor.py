# This should be an observable that the presenter subscribes to.
# This class will also host the thread that talks to the hardware.

from SCDBoardInterface import SCDBoardInterface

class SCDMonitor:
    
    def __init__(self):
        self._boardInterface = SCDBoardInterface() # TBD: Will need to specify parameters

    def init(self):
        self._boardInterface.init_i2c_channel()
    
    def startPeriodic(self, timeIntervalInMilliSec):
        print "TBD"
        
    def stopPeriodic(self, timeIntervalInMilliSec):
        print "TBD"
    
    def read_voltages(self):
        print "TBD"
    
    def set_bias_voltage(self, index, voltage):
        self._boardInterface.set_bias_voltage(index, voltage)

        # This should be moved off to an observer mechanism:
        print self._boardInterface.get_leakage_current(index)
        
    def set_all_bias_voltages(self, listOfVoltages):
        print "TBD"
