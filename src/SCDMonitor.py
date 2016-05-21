# This shou;d be an observable that the presenter subscribes to.
# This class will also host the thread that talks to the hardware.

from SCDBoardInterface import SCDBoardInterface

class SCDMonitor:
    
    def __init__(self):
        self._boardInterface = SCDBoardInterface()
    
    def startPeriodic(self, timeIntervalInMilliSec):
        print "TBD"
        
    def stopPeriodic(self, timeIntervalInMilliSec):
        print "TBD"
    
    def read_voltages(self):
        print "TBD"
    
    def set_bias_voltage(self, index, voltage):
        print "TBD"
        
    def set_all_bias_voltages(self, listOfVoltages):
        print "TBD"