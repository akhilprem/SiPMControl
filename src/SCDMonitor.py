# This should be an observable that the presenter subscribes to.
# This class will also host the thread that talks to the hardware.

from SCDObservable import SCDObservable
from SCDBoardInterface import SCDBoardInterface

class SCDMonitor(SCDObservable):
    
    def __init__(self):
        super(SCDMonitor, self).__init__()
        self._boardInterface = SCDBoardInterface() # TBD: Will need to specify parameters

    def init(self):
        self._boardInterface.init_i2c_channel()
        pass
    
    def startPeriodic(self, timeIntervalInMilliSec):
        pass
        
    def stopPeriodic(self, timeIntervalInMilliSec):
        pass
    
    def read_voltages(self):
        pass
    
    def set_bias_voltage(self, channel, voltage):
        # TBD: Change index to channel in SCDBoardInterface.
        
        # 1. Set the bias voltage
        self._boardInterface.set_bias_voltage(channel, voltage)

        # 2. Read back the current value
        i_leak = self._boardInterface.get_leakage_current(channel)

        # 3. Notify the observers of the change in current.
        self.fire(type="i_leak_changed", channel=channel, current=i_leak)

        ## Send a dummy value just for testing the workflow.
        #self.fire(type="i_leak_changed", channel=channel, current=(float(voltage)/82.0)*500.0)
        
    def set_all_bias_voltages(self, listOfVoltages):
        pass
