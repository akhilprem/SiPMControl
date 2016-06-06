# This should be an observable that the presenter subscribes to.
# This class will also host the thread that talks to the hardware.

import time

from PyQt5 import QtCore

from SCDObservable import SCDObservable
from SCDBoardInterface import SCDBoardInterface
from SCDConstants import SCDConstants

class SCDMonitor(QtCore.QObject, SCDObservable):
    
    def __init__(self):
        super(SCDMonitor, self).__init__()
        self._boardInterface = SCDBoardInterface() # TBD: Will need to specify parameters

        self._isRunPeriodic = False
        self._mutex = QtCore.QMutex()

    @QtCore.pyqtSlot()
    def initialize(self):
        self._boardInterface.init_i2c_channel()
        pass

    @QtCore.pyqtSlot(int)
    def start_periodic(self, timeIntervalInMs):
        self._mutex.lock()
        self._isRunPeriodic = True
        self._mutex.unlock()

        channel = 0
        start_time = 0
        end_time = 0
        wait_time = 0
        
        while True:
            self._mutex.lock()
            if self._isRunPeriodic is False:
                self._mutex.unlock()
                break
            self._mutex.unlock()

            if channel == 0:
                start_time = time.time()
                
            i_leak = self._boardInterface.get_leakage_current(channel)     
            self.fire(type="i_leak_changed", channel=channel, current=i_leak)

            channel += 1
            if channel == SCDConstants.NUM_CHANNELS:
                end_time = time.time()
                wait_time = max(0, timeIntervalInMs/1000.0 - (end_time - start_time))
                time.sleep(wait_time)
                channel = 0

    # This has to called from the presenter directly, i.e. from the UI thread.
    def stop_periodic(self):
        self._mutex.lock()
        self._isRunPeriodic = False
        self._mutex.unlock()
    
    
    @QtCore.pyqtSlot(int, float)
    def set_bias_voltage(self, channel, voltage):
        # TBD: Change index to channel in SCDBoardInterface.
        
        # 1. Set the bias voltage
        self._boardInterface.set_bias_voltage(channel, voltage)
 
        # 2. Read back the current value
        i_leak = self._boardInterface.get_leakage_current(channel)
 
        # 3. Notify the observers of the change in current.
        self.fire(type="i_leak_changed", channel=channel, current=i_leak)

#         # Send a dummy value just for testing the workflow.
#         self.fire(type="i_leak_changed", channel=channel, current=(float(voltage)/82.0)*500.0)
    
    
    @QtCore.pyqtSlot(float)    
    def set_all_bias_voltages(self, voltage):
        channels = range(SCDConstants.NUM_CHANNELS)
        for channel in channels:
            self._boardInterface.set_bias_voltage(channel, voltage)
            self.fire(type="bv_adjusted", channel=channel, voltage=voltage)
        
        time.sleep(SCDConstants.DAC_SETTLING_TIME/1000.0)
        
        for channel in channels:
            i_leak = self._boardInterface.get_leakage_current(channel)
            # Also update observers in "real-time"
            self.fire(type="i_leak_changed", channel=channel, current=i_leak)
    
    
    # This method runs the channel test, and then sends back the collected data all together.
    @QtCore.pyqtSlot(list, list, int)
    def run_channel_test(self, channels, biasVoltages, settlingTimeMs):
        readings = {} # Dictionary of voltage: {channel:i_leak}
        
        for voltage in biasVoltages:
            i_readings = {} # Dictionary of current readings for each channel i.e. channel:i_leak
            # 1. Set the voltage for all channels in the list
            for channel in channels:
                self._boardInterface.set_bias_voltage(channel, voltage)
                self.fire(type="bv_adjusted", channel=channel, voltage=voltage)
            
            # 2. Wait for all channels to settle
            time.sleep(settlingTimeMs/1000.0)
            
            # 3. Read back the current value for each channel and save it
            for channel in channels:
                i_leak = self._boardInterface.get_leakage_current(channel)
                i_readings[channel] = i_leak
                # Also update observers in "real-time"
                self.fire(type="i_leak_changed", channel=channel, current=i_leak)
            
            readings[voltage] = i_readings # Save readings across channels for this voltage.
            
        self.fire(type="channel_test_finished", readings=readings)

    @QtCore.pyqtSlot(bool)
    def set_pulser_LED(self, enable):
        self._boardInterface.set_pulser_LED(enable)
