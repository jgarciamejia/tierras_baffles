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
#from GUI_JZ_JGM import *
#from update_loadreading_atpos import *
import numpy as np
import time
import tkinter as tk
from tkinter import ttk
import tkinter.ttk


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
#calibtype = input('compression or tension calibration coefficients?')
calibtype = 'tension' # should be tension when using! 
#calibtype = 'compression' # for testing in lab only
calibration_data = open('load_sensor_calibration_coeffs_{}.txt'.format(calibtype)).readlines()[9:]
sensorlabels = [line.split(' ')[0] for line in calibration_data]
sensornums = [line.split(' ')[1] for line in calibration_data]
slopes = [line.split(' ')[2] for line in calibration_data]
intercepts = [line.rstrip().split(' ')[3] for line in calibration_data]

slopes_inuse = np.array(slopes).astype(float)
intercepts_inuse = np.array(intercepts).astype(float)
sensor_positions = np.array([])


# Hardcoded phidget serial numbers
# In global code, secondary baffle phidgest are assigned Phidgets index values 2 and 3. 
Phidget0_serialnum = 572895
Phidget1_serialnum = 587932

# PHIDGET CONFIGURATION 

# Declare any event handlers here. These will be called every time the associated event occurs.
def onAttach(self):
	print("Phidget No. [" + str(self.getDeviceSerialNumber()) + "] Channel [" + str(self.getChannel()) + "] Attached!")

def onDetach(self):
	print("Phidget No. [" + str(self.getDeviceSerialNumber()) + "] Channel [" + str(self.getChannel()) + "] Dettached!")

# Describe sequence of actions to perform with Phidget and Channels
def main(*args):

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
		voltageRatioInput.setDeviceSerialNumber(Phidget0_serialnum)
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

	# Note that order is hard-coded. Future code upgrade would be to make it 
	# more dynamic based on changing order of load sensors  
	sigdigs = 2
	try:
		while True:
			voltageRatio00 = voltageRatioInput00.getVoltageRatio()
			load00 = round(slopes_inuse[0]*voltageRatio00 + intercepts_inuse[0],sigdigs) # Kg
			load00 = round(load00*2.20462, sigdigs) # Kg to Lbs
			Lower_North.set(load00)

			voltageRatio01 =voltageRatioInput01.getVoltageRatio()
			load01 = round(slopes_inuse[1]*voltageRatio01 + intercepts_inuse[1],sigdigs)
			load01 = round(load01*2.20462, sigdigs) # Kg to Lbs
			Upper_North.set(load01)

			voltageRatio02 =voltageRatioInput02.getVoltageRatio()
			load02 = round(slopes_inuse[2]*voltageRatio02 + intercepts_inuse[2],sigdigs)
			load02 = round(load02*2.20462, sigdigs) # Kg to Lbs
			Lower_East.set(load02)

			voltageRatio03 =voltageRatioInput03.getVoltageRatio()
			load03 = round(slopes_inuse[3]*voltageRatio03 + intercepts_inuse[3],sigdigs)
			load03 = round(load03*2.20462, sigdigs) # Kg to Lbs
			Upper_East.set(load03)

			voltageRatio10 =voltageRatioInput10.getVoltageRatio()
			load10 = round(slopes_inuse[4]*voltageRatio10 + intercepts_inuse[4],sigdigs)
			load10 = round(load10*2.20462, sigdigs) # Kg to Lbs
			Lower_South.set(load10)

			voltageRatio11 =voltageRatioInput11.getVoltageRatio()
			load11 = round(slopes_inuse[5]*voltageRatio11 + intercepts_inuse[5],sigdigs)
			load11 = round(load11*2.20462, sigdigs) # Kg to Lbs
			Upper_South.set(load11)
			
			voltageRatio12 =voltageRatioInput12.getVoltageRatio()
			load12 = round(slopes_inuse[6]*voltageRatio12 + intercepts_inuse[6],sigdigs)
			load12 = round(load12*2.20462, sigdigs) # Kg to Lbs
			Lower_West.set(load12)

			voltageRatio13 =voltageRatioInput13.getVoltageRatio()
			load13 = round(slopes_inuse[7]*voltageRatio13 + intercepts_inuse[7],sigdigs)
			load13 = round(load13*2.20462, sigdigs) # Kg to Lbs
			Upper_West.set(load13)

			# chill time before you querry again
			root.update()
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


# Configure GUI 

root = tk.Tk()
root.geometry("1500x800")
#root.title("Tierras, Load Readings (Kg)")
root.title("Tierras, Load Readings (Lbs)")
stl = ttk.Style()

stl.configure('.', font=('Helvetica',12), background='antique white')
stl.map('C.TButton', foreground=[('pressed','red'),('active','blue')])

stl.configure('T1.TLabel', foreground='green')
stl.configure('T2.TLabel', foreground='blue')

#stl.configure('C.TButton', foreground=[('pressed','red'),('active','blue')])
stl.configure('C2.TEntry', foreground='red', background='teal', font=('Helvetica',18))

mainframe = tk.ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

Upper_North = tk.DoubleVar()
Upper_South = tk.DoubleVar()
Upper_East = tk.DoubleVar()
Upper_West = tk.DoubleVar()
Lower_North = tk.DoubleVar()
Lower_South = tk.DoubleVar()
Lower_East = tk.DoubleVar()
Lower_West = tk.DoubleVar()


#tk.ttk.Label(mainframe, text="Tierras, Load Readings (Kg)", style="T1.TLabel", font=('Helvetica', 100, 'bold'), foreground='darkslategrey').grid(columnspan=10, row=1)
tk.ttk.Label(mainframe, text="Tierras, Load Readings (Lbs)", style="T1.TLabel", font=('Helvetica', 100, 'bold'), foreground='darkslategrey').grid(columnspan=10, row=1)


cablefont = ('Helvetica', 90)
cabletxtcolor = 'darkslategrey'
tk.ttk.Label(mainframe, text="Upper Cables", style="T1.TLabel", font=cablefont, foreground=cabletxtcolor).grid(column=2, row=2)
tk.ttk.Label(mainframe, text="Lower Cables", style="T1.TLabel", font=cablefont, foreground=cabletxtcolor).grid(column=3, row=2)

tk.ttk.Separator(mainframe, orient=tk.HORIZONTAL).grid(row=3,columnspan=15,ipadx=0, sticky=tk.NSEW)

cardinalfont = ('Helvetica', 90)
cardinaltxtcolor = 'darkslategrey'
tk.ttk.Label(mainframe, text="N", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=4)
tk.ttk.Label(mainframe, text="S", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=5)
tk.ttk.Label(mainframe, text="E", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=6)
tk.ttk.Label(mainframe, text="W", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=7)
#tk.ttk.Button(mainframe, text="QUIT",style='C.TButton',command=exit).grid(column=3, row=10, sticky=tk.W)

loadreadingfont = ('Helvetica', 90)
loadreadingtxtcolor = 'white'
loadrdngbgcolor = 'white'
Upper_North_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Upper_North, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Upper_South_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Upper_South, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Upper_East_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Upper_East,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Upper_West_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Upper_West,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Lower_North_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Lower_North, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Lower_South_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Lower_South, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Lower_East_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Lower_East,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Lower_West_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Lower_West,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)

Upper_North_Entry.grid(column=2, row=4, sticky=(tk.W, tk.E))
Upper_South_Entry.grid(column=2, row=5, sticky=(tk.W, tk.E))
Upper_East_Entry.grid( column=2, row=6, sticky=(tk.W, tk.E))
Upper_West_Entry.grid( column=2, row=7, sticky=(tk.W, tk.E))
Lower_North_Entry.grid(column=3, row=4, sticky=(tk.W, tk.E))
Lower_South_Entry.grid(column=3, row=5, sticky=(tk.W, tk.E))
Lower_East_Entry.grid( column=3, row=6, sticky=(tk.W, tk.E))
Lower_West_Entry.grid( column=3, row=7, sticky=(tk.W, tk.E))

main()
root.update_idletasks()
root.mainloop()


