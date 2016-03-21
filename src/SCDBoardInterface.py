import pigpio
import time

class SCDBoardInterface():
    
    def __init__(self):
        self._DAC1_ADDRESS  = 0x54
        self._DAC2_ADDRESS  = 0x55
        self._ADC1_ADDRESS  = 0x48
        self._ADC2_ADDRESS  = 0x49
        self._MUX_ADDRESS   = 0x4C

        self._BV_MAX = 82; # TBD: Is 82 the max voltage value?
        self._BV_MIN = 0;

        self._pi = pigpio.pi()

        self._dac_1 = self._pi.i2c_open(1, self._DAC1_ADDRESS)
        self._dac_2 = self._pi.i2c_open(1, self._DAC2_ADDRESS)
        self._mux   = self._pi.i2c_open(1, self._MUX_ADDRESS) # All 6 MUXes (each with 8 chan) have same address
        self._adc_1 = self._pi.i2c_open(1, self._ADC1_ADDRESS)


    # Set the I2C MUX IC on the ngCCM Control Emulator to open the channel to the SiPM board
    def init_i2c_channel(self):
        i2c_mux = self._pi.i2c_open(1, 0x70)
        i2c_mux_cmd_byte = self._pi.i2c_read_byte(i2c_mux)
        self._pi.i2c_write_byte(i2c_mux, (i2c_mux_cmd_byte | 0x02))
        print "Initialized the board."
        

    def set_bias_voltage(self, index, voltage):
        print "{} : {}".format(index, voltage)

        if ( voltage > self._BV_MAX or voltage < self._BV_MIN ):
            return # TBD: Raise exception?

        ivoltage = int(voltage/(82.0*(68.87/70.0))*4096)
        n = index

        if n < 32:
            reg_no = n
            dac = self._dac_1 # The first 32 BVs come from DAC 1...
        elif n >= 32:
            reg_no = n - 32
            dac = self._dac_2 # ... and the last 16 comes from DAC 2

        dac_config = [0x0c, 0x04, 0x00] # Copied from BaylorCMS github
        dac_chan = reg_no
        
        dac_v_in = [0,0,0]
        dac_v_in[0] = 0xff & dac_chan
        dac_v_in[1] = (0xc0 | (0x3f & (ivoltage >> 6)))
        dac_v_in[2] = (0xfc & ivoltage << 2)
        
        time.sleep(0.1)
        self._pi.i2c_write_device(dac, dac_config)
        time.sleep(0.1)
        self._pi.i2c_write_device(dac, dac_v_in)

        
    def get_leakage_current(self, index):
        n = index
        mux_chan = n % 8
        time.sleep(0.1)
        self._pi.i2c_write_byte(self._mux, 1 << mux_chan ) # Setting input shift register to select channel

        adc_chan_lookup = [0b000, 0b100, 0b001, 0b101, 0b010, 0b110, 0b011, 0b111]
        adc_chan = int(n / 8)
        adc_command = (adc_chan_lookup[adc_chan] << 4) | 0x8C
        # i.e. Single Ended with Internal Ref ON and A/D Converter ON. See Command Byte description in ADS7828 datasheet.

        try:    # TBD: Figure out how to handle the exception more elegantly in the UI.
            self._pi.i2c_write_byte(self._adc_1, adc_command)
            time.sleep(0.1)
        except:
            print "Failed to write to ADC channel: {}, continuing".format(n)

        time.sleep(0.1)
        (count, data) = self._pi.i2c_read_device(self._adc_1, 2)

        voltage = ((data[0] << 8) | data[1])/float(2**12) * 2.5
        return (voltage * 500.0/2.5) # 2.5V ADC readout corresponds to 500 uA I_leak.
        
    def get_peltier_voltage(self):
        print "TBD"
        
    # and etc.
        
