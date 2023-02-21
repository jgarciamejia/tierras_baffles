#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 14:26:39 2021

Loop to communicate to four S type load sensors of known callibration 
through a single PhidgetBridge 1046 and query for a voltage ratio from each, consequently
returning a load value (kg) for each given their individual callibrations, 
and printing both the V/V and load values for each onto the terminal every second
"""

from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import numpy as np
import time

# Load ALL Calibration Coefficient Data  
calibtype = input('compression or tension calibration coefficients?')
calibration_data = open('load_sensor_calibration_coeffs_{}.txt'.format(calibtype)).readlines()[1:]
sensorlabels = [line.split(' ')[0] for line in calibration_data]
sensornums = [line.split(' ')[1] for line in calibration_data]
slopes = [line.split(' ')[2] for line in calibration_data]
intercepts = [line.rstrip().split(' ')[3] for line in calibration_data]

# Inquire about sensor info for all four sensors in order to define 
# slope, intercept, and Phidget channel for each 
sensornums_inuse = np.array([])
slopes_inuse = np.array([])
intercepts_inuse = np.array([])
for channel in range(4):
	sensornum = input('Etched Sensor No. attached to Phidget Channel {}?'.format(str(channel)))
	sensornums_inuse = np.append(sensornums_inuse, sensornum)
	ind = sensornums.index(sensornum)
	slopes_inuse = np.append(slopes_inuse, float(slopes[ind]))
	intercepts_inuse = np.append(intercepts_inuse, float(intercepts[ind]))


# PHIDGET CONFIGURATION 

# Declare any event handlers here. These will be called every time the associated event occurs.
def onAttach(self):
	print("Phidget Channel [" + str(self.getChannel()) + "] Attached!")

def onDetach(self):
	print("Phidget Channel [" + str(self.getChannel()) + "] Dettached!")


# Describe sequence of actions to perform with Phidget and Channels
def main():
	#Create your Phidget channels

	voltageRatioInput0 = VoltageRatioInput()
	voltageRatioInput1 = VoltageRatioInput()
	voltageRatioInput2 = VoltageRatioInput()
	voltageRatioInput3 = VoltageRatioInput()
	voltageRatioInputs = np.array([voltageRatioInput0, 
		voltageRatioInput1, voltageRatioInput2, 
		voltageRatioInput3])

	#Set addressing parameters to specify which channel to open (if any)
	for ch_ind, voltageRatioInput in enumerate(voltageRatioInputs):
		voltageRatioInput.setDeviceSerialNumber(572895) #568485
		voltageRatioInput.setChannel(ch_ind)

	#Assign any event handlers you need before calling open so that no events are missed.
	for voltageRatioInput in voltageRatioInputs:
		voltageRatioInput.setOnAttachHandler(onAttach)
		voltageRatioInput.setOnDetachHandler(onDetach)

	#Open your Phidgets and wait for attachment
	voltageRatioInput0.openWaitForAttachment(5000)
	voltageRatioInput1.openWaitForAttachment(5000)
	voltageRatioInput2.openWaitForAttachment(5000)
	voltageRatioInput3.openWaitForAttachment(5000)

	
	# Loop below will allowOnVoltageRatioChangeHandler to print voltage to terminal
	# until user presss enter to interrupt

	# Querry for the voltage ratio through each channel indefinitely or until user CtrC, 
	# passing values to variables voltageRatio and load that DO NOT get stored, simply redefined 
	try:
		while True:
			for ch_ind, voltageRatioInput in enumerate(voltageRatioInputs):
				voltageRatio = voltageRatioInput.getVoltageRatio()
				load = slopes_inuse[ch_ind]*voltageRatio + intercepts_inuse[ch_ind] 
				print ('Channel {}, Sensor {}: (V/V) = '.format(ch_ind, sensornums_inuse[ch_ind])+str(voltageRatio)+'; Load (Kg) = '+str(load))
			# chill time before you querry again
			time.sleep(1)
	except KeyboardInterrupt:
		print ('Press Ctrl-C to terminate')

	#Close your Phidgets once the program is done.
	voltageRatioInput0.close()
	voltageRatioInput1.close()
	voltageRatioInput2.close()
	voltageRatioInput3.close()

main()




