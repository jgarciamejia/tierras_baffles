#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 14:26:39 2021

Loop to communicate to one S type load sensor of known callibration 
through a PhidgetBridge 1046 and querry for a voltage ratio coming through 
a specific channel, consequently returning a load value (kg) and printing both onto the terminal every second
"""

from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import time
import numpy as np

# Load Calibration Coefficient Data  
calibtype = input('compression or tension calibration coefficients?')
calibration_data = open('load_sensor_calibration_coeffs_{}.txt'.format(calibtype)).readlines()[1:]
sensorlabels = [line.split(' ')[0] for line in calibration_data]
sensornums = [line.split(' ')[1] for line in calibration_data]
slopes = [line.split(' ')[2] for line in calibration_data]
intercepts = [line.rstrip().split(' ')[3] for line in calibration_data]

# Inquire about sensor info to define slope, intercept, and Phidget channel 
SensorNo = input('what is the Sensor No.? (etched on sensor)')
SensorChannel = int(input('what Phidget channel is sensor attached to?'))
ind = sensornums.index(SensorNo)
slope = float(slopes[ind])
intercept = float(intercepts[ind])

# Print slope and intercept in use
print ('Slope: '+str(slope)+'; Intercept'+str(intercept))

# Declare any event handlers for the Phidgets here. These will be called every time the associated event occurs.
def onAttach(self):
	print("Phidget Attached!")

def onDetach(self):
	print("Phidget Detached!")
 
# Describe sequence of actions to perform with Phidgets 

def main():

	#Create your Phidget channels
	voltageRatioInput = VoltageRatioInput()

	#Set addressing parameters to specify which channel to open
	#voltageRatioInput.setDeviceSerialNumber(568485)
	voltageRatioInput.setDeviceSerialNumber(587976)
	#voltageRatioInput.setDeviceSerialNumber(587932)
	voltageRatioInput.setChannel(SensorChannel)

	#Assign any event handlers you need before calling open so that no events are missed.
	voltageRatioInput.setOnAttachHandler(onAttach)
	voltageRatioInput.setOnDetachHandler(onDetach)

	#Open your Phidgets and wait for attachment
	voltageRatioInput.openWaitForAttachment(5000)

	# Querry for the voltage ratio indefinitely, passing value to a variable 
	try:
		while True:
			voltageRatio = voltageRatioInput.getVoltageRatio()
			load = slope*voltageRatio + intercept 
			print ('Voltage Ratio (V/V) = '+str(voltageRatio)+'; Load (Kg) = '+str(load))
			# chill for a second before you querry again
			time.sleep(1)
	except KeyboardInterrupt:
		print ('Press Ctrl-C to terminate')

	#Close your Phidget once the program is done.
	voltageRatioInput.close()

main()






