# SiPMControl

Installation:

The SiPM Control App is written in Python 2.7. Raspbian's default Python installation should support the app.

1. Enable I2C on the Raspberry Pi by follwing the instructions at:

	http://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/

2. Install PIGPIO library by following the instructions at:

	http://abyz.co.uk/rpi/pigpio/download.html

3. Install PyQt5 with the commands:

	sudo apt-get install python-pyqt5
	sudo apt-get install pyqt5-dev-tools

4. Clone the SiPM repository with the command:

	git clone https://github.com/akhilprem/SiPMControl.git

5. Before running the app for the first time, go to the 'ui' folder and run:

	pyuic5 SCDMainWindow.ui > SCDMainWindow_Ui.py
	pyuic5 SCDChannelTestDialog.ui > SCDChannelTestDialog_Ui.py

and copy SCDChannelTestDialog_Ui.py and SCDMainWindow_Ui.py to the src folder.

6. Start the PIGPIO daemon using (IMPORTANT - This is to be done after every reboot of the Pi):

	sudo pigpiod

7. Run the application using:

	python main.py

