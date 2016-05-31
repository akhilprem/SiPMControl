# This should be an observable that the presenter subscribes to.
# This class will also host the thread that talks to the hardware.

from SCDObservable import SCDObservable
from SCDBoardInterface import SCDBoardInterface

class SCDMonitor(SCDObservable):
    
    def __init__(self):
        super(SCDMonitor, self).__init__()
        self._boardInterface = SCDBoardInterface() # TBD: Will need to specify parameters

    def init(self):
        # self._boardInterface.init_i2c_channel()
        print "TBD"
    
    def startPeriodic(self, timeIntervalInMilliSec):
        print "TBD"
        
    def stopPeriodic(self, timeIntervalInMilliSec):
        print "TBD"
    
    def read_voltages(self):
        print "TBD"
    
    def set_bias_voltage(self, channel, voltage):
        # TBD: Change index to channel in SCDBoardInterface.
        # self._boardInterface.set_bias_voltage(channel, voltage)

        # self.fire(type="bv_changed", channel=channel, current=self._boardInterface.get_leakage_current(index))

        # Send a dummy value just for testing the workflow.
        self.fire(type="bv_changed", channel=channel, current=(float(voltage)/82.0)*500.0)
        
    def set_all_bias_voltages(self, listOfVoltages):
        print "TBD"
