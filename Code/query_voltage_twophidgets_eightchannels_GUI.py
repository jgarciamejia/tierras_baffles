#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 14:26:39 2021

Loop to communicate to eight S type load sensors of known callibration 
through two PhidgetBridge 1046 (each bridge can communicate with four 
sensors)and query for a voltage ratio from each, consequently
returning a load value (kg) for each given their individual 
callibrations, and printing both the V/V and load values for each onto 
the terminal every second
"""

from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
from GUI_JZ_JGM import *
import numpy as np
import time

# Load ALL Calibration Coefficient Data  
calibtype = input('compression or tension calibration coefficients?')
calibration_data = open('load_sensor_calibration_coeffs_{}.txt'.format(calibtype)).readlines()[1:]
sensorlabels = [line.split(' ')[0] for line in calibration_data]
sensornums = [line.split(' ')[1] for line in calibration_data]
slopes = [line.split(' ')[2] for line in calibration_data]
intercepts = [line.rstrip().split(' ')[3] for line in calibration_data]


# Initialize arrays to populate with user-written information 
sensornums_inuse = np.array([])
slopes_inuse = np.array([])
intercepts_inuse = np.array([])
sensor_positions = np.array([])

# Ask user about sensor info for all four sensors in order to define 
# slope, intercept, Phidget channel and position for each
print ('I need some information about the Phidgets and load sensors attached to them!')
Phidget0_serialnum = float(input('What is the Serial No. for Phidget No.1?'))
Phidget1_serialnum = float(input('What is the Serial No. for Phidget No.2?'))
for phidget_no in range(2):
	for channel in range(4):
		sensornum = input('What is the etched Sensor No. attached to Phidget No.{} via Channel {}?'.format(str(phidget_no), str(channel)))
		sensornums_inuse = np.append(sensornums_inuse, sensornum)
		sensorposition = input('What is the position of the Sensor? (e.g., Upper North or Lower West)')
		sensor_positions = np.append(sensor_positions, sensorposition)
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

	#Create your Phidget 0 channels
	voltageRatioInput00 = VoltageRatioInput()
	voltageRatioInput01 = VoltageRatioInput()
	voltageRatioInput02 = VoltageRatioInput()
	voltageRatioInput03 = VoltageRatioInput()
	voltageRatioInputs0 = np.array([voltageRatioInput00, 
		voltageRatioInput01, voltageRatioInput02, 
		voltageRatioInput03])

	#Create your Phidget 1 channels
	voltageRatioInput10 = VoltageRatioInput()
	voltageRatioInput11 = VoltageRatioInput()
	voltageRatioInput12 = VoltageRatioInput()
	voltageRatioInput13 = VoltageRatioInput()
	voltageRatioInputs1 = np.array([voltageRatioInput10, 
		voltageRatioInput11, voltageRatioInput12, 
		voltageRatioInput13])



	#Set addressing parameters to specify which 
	# Phidget 1 & 2 channels to open (if any)
	for channel_index in range(4):
		voltageRatioInputs0[channel_index].setDeviceSerialNumber(Phidget0_serialnum)
		voltageRatioInputs0[channel_index].setChannel(channel_index)	
		voltageRatioInputs1[channel_index].setDeviceSerialNumber(Phidget1_serialnum)
		voltageRatioInputs1[channel_index].setChannel(channel_index)
	

	#Assign any event handlers you need before calling open so that no events are missed.
	for channel_index in range(4):
		voltageRatioInputs0[channel_index].setOnAttachHandler(onAttach)
		voltageRatioInputs0[channel_index].setOnAttachHandler(onDetach)
		voltageRatioInputs1[channel_index].setOnAttachHandler(onAttach)
		voltageRatioInputs1[channel_index].setOnAttachHandler(onDetach)

	#Open your Phidgets and wait for attachment
	for channel_index in range(4):
		voltageRatioInputs0[channel_index].openWaitForAttachment(5000)
		voltageRatioInputs1[channel_index].openWaitForAttachment(5000)

	# Loop below will allowOnVoltageRatioChangeHandler to print voltage to terminal
	# until user presss enter to interrupt

	# Querry for the voltage ratio through each channel indefinitely or until user CtrC, 
	# passing values to variables voltageRatio and load that DO NOT get stored, simply redefined 
	try:
		while True:
			for channel_index in range(4):
				voltageRatio0 = voltageRatioInputs0[channel_index].getVoltageRatio()
				voltageRatio1 = voltageRatioInputs1[channel_index].getVoltageRatio()
				load0 = slopes_inuse[channel_index]*voltageRatio0 + intercepts_inuse[channel_index]
				load1 = slopes_inuse[channel_index+4]*voltageRatio0 + intercepts_inuse[channel_index+4]
				if sensor_positions

				#print ('Phidget No. {}, Channel {}, Sensor {}: (V/V) = '.format(Phidget0_serialnum, ch_ind, sensornums_inuse[ch_ind])+str(voltageRatio)+'; Load (Kg) = '+str(load))
				#print ('Phidget No. {}, Channel {}, Sensor {}: (V/V) = '.format(Phidget1_serialnum, ch_ind, sensornums_inuse[ch_ind])+str(voltageRatio)+'; Load (Kg) = '+str(load))

			# chill time before you querry again
			time.sleep(1)
	except KeyboardInterrupt:
		print ('Press Ctrl-C to terminate')

	#Close your Phidgets once the program is done.
	for channel_index in range(4):
		voltageRatioInputs0[channel_index].close()
		voltageRatioInputs1[channel_index].close()

main()




