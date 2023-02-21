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
from update_loadreading_atpos import *
import numpy as np
import time

# Define global variables 
global Upper_North
global Upper_South
global Upper_East
global Upper_West
global Lower_North
global Lower_South
global Lower_East
global Lower_West

# Load ALL Calibration Coefficient Data  
calibtype = input('compression or tension calibration coefficients?')
calibration_data = open('load_sensor_calibration_coeffs_{}.txt'.format(calibtype)).readlines()[1:]
sensorlabels = [line.split(' ')[0] for line in calibration_data]
sensornums = [line.split(' ')[1] for line in calibration_data]
slopes = [line.split(' ')[2] for line in calibration_data]
intercepts = [line.rstrip().split(' ')[3] for line in calibration_data]


# Initialize load sensor info arrays to populate with user-written information 
sensornums_inuse = np.array([])
slopes_inuse = np.array([])
intercepts_inuse = np.array([])
sensor_positions = np.array([])

# Ask user about sensor info for all eight sensors in order to define 
# slope, intercept, Phidget channel and position for each
print ('I need some information about the Phidgets and load sensors attached to them!')

# Hardcoded phidget serial numbers but uncomment first two lines for user-inputted
#Phidget0_serialnum = float(input('What is the Serial No. for Phidget No.0?'))
#Phidget1_serialnum = float(input('What is the Serial No. for Phidget No.1?'))
Phidget0_serialnum = 568485
Phidget1_serialnum = 572895

# Hardcoded info based on how 80/20 set up was configured Sep 22/2021. 
sensornums_inuse = np.array(['515', '514', '513', '424', '347', '516', '429', '519'])
sensor_positions = np.array(['Lower North', 'Upper North', 'Lower East', 'Upper East', 
				 'Lower South', 'Upper South', 'Lower West', 'Upper West'])
slopes_inuse = np.array([32986.63104446241, 33018.57185319304, 33081.593581921494, 
			   32975.13208403447, 33010.401263622225, 33035.3146978213, 33025.17002041806,
			   33015.39935771155])
intercepts_inuse = np.array([ 0.26514389251131254, -0.8241383481841369, -0.24251324478155944, 
				-0.7382129679267921, 0.08721838913772695, -0.6324854522019321, 0.2414177599277174, 
				-0.30513348710706256])

# Uncomment this loop to request info from user
# for phidget_no in range(2):
# 	for channel in range(4):
# 		sensornum = input('What is the etched Sensor No. attached to Phidget No.{} via Channel {}?'.format(str(phidget_no), str(channel)))
# 		sensornums_inuse = np.append(sensornums_inuse, sensornum)
# 		sensorposition = input('What is the position of the Sensor? (e.g., Upper North or Lower West)')
# 		sensor_positions = np.append(sensor_positions, sensorposition)
# 		ind = sensornums.index(sensornum)
# 		slopes_inuse = np.append(slopes_inuse, float(slopes[ind]))
# 		intercepts_inuse = np.append(intercepts_inuse, float(intercepts[ind]))

# 		# Print sensor information to corroborate the code is working correctly
# 		print ('Sensor No.'+sensornum+' is located on the '+str(sensorposition)
# 			+' with a calibration slope = '+str(slopes[ind])+
# 			 ' Kg/(V/V) and an intercept = '+str(intercepts[ind]))
# 		print ('Sensor No.'+sensornum+' is connected to Phidget No.'+str(phidget_no)+
# 			' via Channel No.'+str(channel))

# PHIDGET CONFIGURATION 

# Declare any event handlers here. These will be called every time the associated event occurs.
def onAttach(self):
	print("Phidget No. [" + str(self.getDeviceSerialNumber()) + "] Channel [" + str(self.getChannel()) + "] Attached!")

def onDetach(self):
	print("Phidget No. [" + str(self.getDeviceSerialNumber()) + "] Channel [" + str(self.getChannel()) + "] Dettached!")

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

	#Set addressing parameters to specify which Phidget 0 & 1 channels to open (if any)
	# Phidget 0
	for ch_ind, voltageRatioInput in enumerate(voltageRatioInputs0):
		voltageRatioInput.setDeviceSerialNumber(568485)
		voltageRatioInput.setChannel(ch_ind)
	# Phidget 1
	for ch_ind, voltageRatioInput in enumerate(voltageRatioInputs1):
		voltageRatioInput.setDeviceSerialNumber(Phidget1_serialnum)
		voltageRatioInput.setChannel(ch_ind)

	#Assign any event handlers you need before calling open so that no events are missed.
	#Phidget 0
	for voltageRatioInput in voltageRatioInputs0:
		voltageRatioInput.setOnAttachHandler(onAttach)
		voltageRatioInput.setOnDetachHandler(onDetach)
	#Phidget 1
	for voltageRatioInput in voltageRatioInputs1:
		voltageRatioInput.setOnAttachHandler(onAttach)
		voltageRatioInput.setOnDetachHandler(onDetach)

	#Open your Phidget Channels and wait for attachment
	voltageRatioInput00.openWaitForAttachment(5000)
	voltageRatioInput01.openWaitForAttachment(5000)
	voltageRatioInput02.openWaitForAttachment(5000)
	voltageRatioInput03.openWaitForAttachment(5000)
	voltageRatioInput10.openWaitForAttachment(5000)
	voltageRatioInput11.openWaitForAttachment(5000)
	voltageRatioInput12.openWaitForAttachment(5000)
	voltageRatioInput13.openWaitForAttachment(5000)

	# Loop below will allowOnVoltageRatioChangeHandler to print voltage to terminal
	# until user presss enter to interrupt

	# Querry for the voltage ratio through each channel indefinitely or until user CtrC, 
	# passing values to GUI via update_loadreading function.  
	try:
		while True:
			for channel_index in range(4):
				voltageRatio0 = voltageRatioInputs0[channel_index].getVoltageRatio()
				voltageRatio1 = voltageRatioInputs1[channel_index].getVoltageRatio()
				load0 = slopes_inuse[channel_index]*voltageRatio0 + intercepts_inuse[channel_index]
				load1 = slopes_inuse[channel_index+4]*voltageRatio0 + intercepts_inuse[channel_index+4]
				location = sensor_positions[channel_index]
				# cleaner method that all the above if statements, but requires that I figure out 
				# how to use global variables correctly 
				update_load0 = update_loadreading_at_position(sensor_positions[channel_index], load0, 
					Upper_North, Upper_South, Upper_East, Upper_West, Lower_North, Lower_South, Lower_East, Lower_West)
				update_load1 = update_loadreading_at_position(sensor_positions[channel_index+4], load1, 
					Upper_North, Upper_South, Upper_East, Upper_West, Lower_North, Lower_South, Lower_East, Lower_West)

				#print ('Phidget No. {}, Channel {}, Sensor {}: (V/V) = '.format(Phidget0_serialnum, ch_ind, sensornums_inuse[ch_ind])+str(voltageRatio)+'; Load (Kg) = '+str(load))
				#print ('Phidget No. {}, Channel {}, Sensor {}: (V/V) = '.format(Phidget1_serialnum, ch_ind, sensornums_inuse[ch_ind])+str(voltageRatio)+'; Load (Kg) = '+str(load))

			# chill time before you querry again
			time.sleep(.5)
	except KeyboardInterrupt:
		print ('Press Ctrl-C to terminate')

	#Close your Phidgets once the program is done.
	voltageRatioInput00.close()
	voltageRatioInput01.close()
	voltageRatioInput02.close()
	voltageRatioInput03.close()
	voltageRatioInput10.close()
	voltageRatioInput11.close()
	voltageRatioInput12.close()
	voltageRatioInput13.close()

main()




