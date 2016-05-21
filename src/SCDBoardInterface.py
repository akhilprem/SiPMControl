
class SCDBoardInterface():
    
    def __init__(self):
        self._DAC1_ADDRESS  = 0x54
        self._DAC2_ADDRESS  = 0x55
        self._ADC1_ADDRESS  = 0x48
        self._ADC2_ADDRESS  = 0x49
        self._MUX_ADDRESS   = 0x4C
        
    def set_bias_voltage(self, index, voltage):
        print "{} : {}".format(index, voltage)
        
    def get_reg_voltage(self, index):
        print "TBD"
        
    def get_peltier_voltage(self):
        print "TBD"
        
    # and etc.
        