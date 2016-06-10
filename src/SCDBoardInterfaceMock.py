import time

from SCDConstants import SCDConstants

class SCDBoardInterfaceMock:
    def __init__(self):
        self._i_leak = [0.0 for i in range(SCDConstants.NUM_CHANNELS)]
        self._diag_voltages = [1.5, 1.85, 0.5, 0.4, 0.3, 0.2, 0.1]
    
    def init_i2c_channel(self):
        print "Warning: Board Interface is being mocked."
    
    def set_bias_voltage(self, channel, voltage):
        self._i_leak[channel] = (float(voltage)/82.0)*500.0
        time.sleep(0.2)
    
    def get_leakage_current(self, channel):
        time.sleep(0.3)
        return self._i_leak[channel]

    def set_pulser_LED(self, enable):
        if enable:
            print "LED ON"
        else:
            print "LED OFF"
    
    def get_diagnostic_voltage(self, adc_chan):
        return self._diag_voltages[adc_chan]
