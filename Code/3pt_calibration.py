"""
Interactive script to carry out 3pt calibration for one Phidgets S-type load sensor
via a PhidgetBridge1046. Calibration provides slope and intercept to convert 
voltage ratio output from the sensor (V/V) into a load in kg. 

The script saves a plot with the data points collected and the linear regression, 
and adds the coefficients to a file. 
"""

import numpy as np 
import matplotlib.pyplot as plt 
from scipy import stats

from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import time
from datetime import datetime 
import numpy as np


# Begin Calibration and Ask User to Identify Sensor 
print ('Starting Calibration Routine')
SensorLabel = input('Enter Sensor Label (written with Sharpie on sensor):')
SensorNo = input('Enter Sensor No (etched on sensor):')
SensorChannel = int(input('What Channel in the Phidget is sensor attached to?'))
nrdngs= int(input('How many voltage ratio readings do you want to average per calibration point?'))
typeofcalib = input('Is this a tension or compression calibration?')

# Declare any event handlers for the Phidget here.
def onAttach(self):
	print("Phidget Attached!")

def onDetach(self):
	print("Phidget Detached!")

#Create your Phidget channels
voltageRatioInput = VoltageRatioInput()

#Set addressing parameters to specify which channel in Phidget to open
voltageRatioInput.setDeviceSerialNumber(587932)
voltageRatioInput.setChannel(SensorChannel)

#Assign any event handlers you need before calling open so that no events are missed.
voltageRatioInput.setOnAttachHandler(onAttach)
voltageRatioInput.setOnDetachHandler(onDetach)

#Open your Phidgets and wait for attachment
voltageRatioInput.openWaitForAttachment(5000)

####### Begin three point calibration

#0-pt data collection
print ('Starting Zero-pt data collection.')
print ('Ensure the S-load sensor is upright and unloaded.')
input ('Press Enter to Begin')
zeropt_rdngs = np.array([])
for nth_rdng in range(nrdngs):
	voltageRatio = voltageRatioInput.getVoltageRatio()
	print ('Voltage Ratio (V/V) = '+str(voltageRatio))
	zeropt_rdngs = np.append(zeropt_rdngs, voltageRatio)
	time.sleep(1)
zeropt_voltageRatio = np.average(zeropt_rdngs)
print ('Average Zero Pt. Voltage Ratio (V/V) = '+str(zeropt_voltageRatio))

#midpoint data collection 
input ('Load the sensor with a well-characterized weight. Then Press Enter to proceed.')
#medium_weight = float(input ('How heavy is this weight in kilograms?'))
print ('Starting midpoint data collection.')
midpt_rdngs = np.array([])
for nth_rdng in range(nrdngs):
	voltageRatio = voltageRatioInput.getVoltageRatio()
	print ('Voltage Ratio (V/V) = '+str(voltageRatio))
	midpt_rdngs = np.append(midpt_rdngs, voltageRatio)
	time.sleep(1)
midpt_voltageRatio = np.average(midpt_rdngs)
print ('Average Mid Pt. Voltage Ratio (V/V) = '+str(midpt_voltageRatio))

# maxpt data collection 
input ('Load the sensor with another well-characterized weight. Then Press Enter to proceed.')
#max_weight = float(input ('How heavy is this weight in kilograms?'))
print ('Starting max point data collection.')
maxpt_rdngs = np.array([])
for nth_rdng in range(nrdngs):
	voltageRatio = voltageRatioInput.getVoltageRatio()
	print ('Voltage Ratio (V/V) = '+str(voltageRatio))
	maxpt_rdngs = np.append(maxpt_rdngs, voltageRatio)
	time.sleep(1)
maxpt_voltageRatio = np.average(maxpt_rdngs)
print ('Average Max Pt. Voltage Ratio (V/V) = '+str(maxpt_voltageRatio))

print ('Data Collection Done! Proceeding with Calibration Fit...')
#Close your Phidget once the program is done.
voltageRatioInput.close()

###### Carry out linear fit 
VoltageRatios = [zeropt_voltageRatio, midpt_voltageRatio, maxpt_voltageRatio]
medium_weight, max_weight = 1.7717, 4.1839 # kg
Weights = [0, medium_weight, max_weight]  # kg
slope, intercept, r, p, se = stats.linregress(VoltageRatios, Weights)

print ('Slope: '+str(slope)+'; Intercept'+str(intercept))

datafile = open('load_sensor_calibration_coeffs_{}.txt'.format(typeofcalib), 'a+')
datafile.write('\n '+ SensorLabel + ' ' + SensorNo + ' ' + str(slope) +' '+str(intercept))
print ('Calbration fit values saved to calibration file')

####### Plot fit and data
x = np.linspace(zeropt_voltageRatio, maxpt_voltageRatio, 50)
y = (slope * x) + intercept

fig, ax = plt.subplots()
ax.plot(VoltageRatios, Weights, 'o')
ax.plot(x,y)

ax.set_xlabel('Voltage Ratio (V/V)')
ax.set_ylabel('Load (Kg)')
ax.set_title('Slope: '+str(slope)+'; Intercept'+str(intercept))
ax.invert_xaxis()
plt.show()
fig.savefig('3ptcalib_Sensor{0}_No{1}_{2}.pdf'.format(SensorLabel,SensorNo, typeofcalib))
print ('A figure of the fit and collected data was also saved!')





