import time

from SCDConstants import SCDConstants

class SCDBoardInterfaceMock:
    def __init__(self):
        self._i_leak = [0.0 for i in range(SCDConstants.NUM_CHANNELS)]
    
    def init_i2c_channel(self):
        print "Warning: Board Interface is being mocked."
    
    def set_bias_voltage(self, channel, voltage):
        self._i_leak[channel] = (float(voltage)/82.0)*500.0
        time.sleep(0.2)
    
    def get_leakage_current(self, channel):
        time.sleep(0.3)
        return self._i_leak[channel]