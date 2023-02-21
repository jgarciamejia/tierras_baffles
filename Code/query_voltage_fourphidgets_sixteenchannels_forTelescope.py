#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 14:26:39 2021

Loop to communicate to sixteen S type load sensors of known callibration 
through four PhidgetBridge 1046 (each bridge can communicate with four 
sensors)and query for a voltage ratio from each, consequently
returning a load value (kg) for each given their individual 
callibrations, and updating their load values onto a GUI
"""

from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import numpy as np
import time
import tkinter as tk
from tkinter import ttk
import tkinter.ttk

# 
def update_load(voltageRatioInput, slope, intercept, sigdigs, globvar):
	#voltageRatio = voltageRatioInput.getVoltageRatio()
	load = round(float(slope)*(voltageRatioInput.getVoltageRatio()) + float(intercept),sigdigs) # Kg
	load = round(load*2.20462, sigdigs) # Kg to Lbs
	#global globvar
	globvar.set(load)

# Define global variables 

#Primary Baffle, Prmry_Baff
global Prmry_Baff_Upper_North
global Prmry_Baff_Upper_South
global Prmry_Baff_Upper_East
global Prmry_Baff_Upper_West
global Prmry_Baff_Lower_North
global Prmry_Baff_Lower_South
global Prmry_Baff_Lower_East
global Prmry_Baff_Lower_West

#Secondary Baffle, Scdry_Baff
global Scdry_Baff_Upper_North
global Scdry_Baff_Upper_South
global Scdry_Baff_Upper_East
global Scdry_Baff_Upper_West
global Scdry_Baff_Lower_North
global Scdry_Baff_Lower_South
global Scdry_Baff_Lower_East
global Scdry_Baff_Lower_West

Prmry_Baff_Upper_North = 0.0
Prmry_Baff_Upper_South = 0.0
Prmry_Baff_Upper_East = 0.0
Prmry_Baff_Upper_West = 0.0
Prmry_Baff_Lower_North = 0.0
Prmry_Baff_Lower_South = 0.0
Prmry_Baff_Lower_East = 0.0
Prmry_Baff_Lower_West = 0.0

Scdry_Baff_Upper_North = 0.0
Scdry_Baff_Upper_South = 0.0
Scdry_Baff_Upper_East = 0.0
Scdry_Baff_Upper_West = 0.0
Scdry_Baff_Lower_North = 0.0
Scdry_Baff_Lower_South = 0.0
Scdry_Baff_Lower_East = 0.0
Scdry_Baff_Lower_West = 0.0

# Load ALL Calibration Coefficient Data
# Order of file info corresponds to Phidget 0, Chn 0,1,2,3, Phidget 1, Chn 0,1,2,3 etc...   
#calibtype = input('compression or tension calibration coefficients?')
calibtype = 'tension' # should be tension when installing baffles!!
#calibtype = 'compression'
calibration_data = open('load_sensor_calibration_coeffs_{}.txt'.format(calibtype)).readlines()[1:]
sensorlabels = [line.split(' ')[0] for line in calibration_data]
sensornums = [line.split(' ')[1] for line in calibration_data]
slopes = [line.split(' ')[2] for line in calibration_data]
intercepts = [line.rstrip().split(' ')[3] for line in calibration_data]

slopes_inuse = np.array(slopes).astype(float)
intercepts_inuse = np.array(intercepts).astype(float)

# Phidget serial numbers 
Phidget0_serialnum = 568485
Phidget1_serialnum = 587976
Phidget2_serialnum = 572895
Phidget3_serialnum = 587932

# PHIDGET CONFIGURATION 

# Declare any event handlers here. These will be called every time the associated event occurs.
def onAttach(self):
	print("Phidget No. [" + str(self.getDeviceSerialNumber()) + "] Channel [" + str(self.getChannel()) + "] Attached!")

def onDetach(self):
	print("Phidget No. [" + str(self.getDeviceSerialNumber()) + "] Channel [" + str(self.getChannel()) + "] Dettached!")

# Describe sequence of actions to perform with Phidget and Channels
def main(*args):
	globvars = np.array([Prmry_Baff_Lower_North, Prmry_Baff_Upper_North, 
					 Prmry_Baff_Lower_East, Prmry_Baff_Upper_East,  
					 Prmry_Baff_Lower_South, Prmry_Baff_Upper_South,
					 Prmry_Baff_Lower_West, Prmry_Baff_Upper_West,
					 Scdry_Baff_Lower_North, Scdry_Baff_Upper_North, 
					 Scdry_Baff_Lower_East, Scdry_Baff_Upper_East,  
					 Scdry_Baff_Lower_South, Scdry_Baff_Upper_South,
					 Scdry_Baff_Lower_West, Scdry_Baff_Upper_West])

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

	#Create your Phidget 2 channels
	voltageRatioInput20 = VoltageRatioInput()
	voltageRatioInput21 = VoltageRatioInput()
	voltageRatioInput22 = VoltageRatioInput()
	voltageRatioInput23 = VoltageRatioInput()
	voltageRatioInputs2 = np.array([voltageRatioInput20, 
		voltageRatioInput21, voltageRatioInput22, 
		voltageRatioInput23])

	#Create your Phidget 3 channels
	voltageRatioInput30 = VoltageRatioInput()
	voltageRatioInput31 = VoltageRatioInput()
	voltageRatioInput32 = VoltageRatioInput()
	voltageRatioInput33 = VoltageRatioInput()
	voltageRatioInputs3 = np.array([voltageRatioInput30, 
		voltageRatioInput31, voltageRatioInput32, 
		voltageRatioInput33])

	#Set addressing parameters to specify which Phidget 0-3 channels to open (if any)
	# Phidget 0
	for ch_ind, voltageRatioInput in enumerate(voltageRatioInputs0):
		voltageRatioInput.setDeviceSerialNumber(Phidget0_serialnum)
		voltageRatioInput.setChannel(ch_ind)
	# Phidget 1
	for ch_ind, voltageRatioInput in enumerate(voltageRatioInputs1):
		voltageRatioInput.setDeviceSerialNumber(Phidget1_serialnum)
		voltageRatioInput.setChannel(ch_ind)
	#Phidget 2
	for ch_ind, voltageRatioInput in enumerate(voltageRatioInputs2):
		voltageRatioInput.setDeviceSerialNumber(Phidget2_serialnum)
		voltageRatioInput.setChannel(ch_ind)
	#Phidget 3
	for ch_ind, voltageRatioInput in enumerate(voltageRatioInputs3):
		voltageRatioInput.setDeviceSerialNumber(Phidget3_serialnum)
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
	#Phidget 2
	for voltageRatioInput in voltageRatioInputs2:
		voltageRatioInput.setOnAttachHandler(onAttach)
		voltageRatioInput.setOnDetachHandler(onDetach)
	#Phidget 3
	for voltageRatioInput in voltageRatioInputs3:
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
	voltageRatioInput20.openWaitForAttachment(5000)
	voltageRatioInput21.openWaitForAttachment(5000)
	voltageRatioInput22.openWaitForAttachment(5000)
	voltageRatioInput23.openWaitForAttachment(5000)
	voltageRatioInput30.openWaitForAttachment(5000)
	voltageRatioInput31.openWaitForAttachment(5000)
	voltageRatioInput32.openWaitForAttachment(5000)
	voltageRatioInput33.openWaitForAttachment(5000)

	# Querry for the voltage ratio through each channel indefinitely or until user CtrC, 
	# passing values to GUI via update_loadreading function.  

	# Note that order is hard-coded. Future code upgrade would be to make it 
	# more dynamic based on changing order of load sensors  
	sigdigs = 2
	ALLvoltageRatioInputs = np.array([voltageRatioInputs0,voltageRatioInputs1,
							voltageRatioInputs2,voltageRatioInputs3]).flatten()
	try:
		while True:
			for ind, voltageRatioInput in enumerate(ALLvoltageRatioInputs):
					update_load(voltageRatioInput, slopes[ind], intercepts[ind], sigdigs, globvars[ind])
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
	voltageRatioInput20.close()
	voltageRatioInput21.close()
	voltageRatioInput22.close()
	voltageRatioInput23.close()
	voltageRatioInput20.close()
	voltageRatioInput31.close()
	voltageRatioInput32.close()
	voltageRatioInput33.close()

# Configure GUI 

root = tk.Tk()
root.geometry("800x800")
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

Prmry_Baff_Upper_North = tk.DoubleVar()
Prmry_Baff_Upper_South = tk.DoubleVar()
Prmry_Baff_Upper_East = tk.DoubleVar()
Prmry_Baff_Upper_West = tk.DoubleVar()
Prmry_Baff_Lower_North = tk.DoubleVar()
Prmry_Baff_Lower_South = tk.DoubleVar()
Prmry_Baff_Lower_East = tk.DoubleVar()
Prmry_Baff_Lower_West = tk.DoubleVar()

Scdry_Baff_Upper_North = tk.DoubleVar()
Scdry_Baff_Upper_South = tk.DoubleVar()
Scdry_Baff_Upper_East = tk.DoubleVar()
Scdry_Baff_Upper_West = tk.DoubleVar()
Scdry_Baff_Lower_North = tk.DoubleVar()
Scdry_Baff_Lower_South = tk.DoubleVar()
Scdry_Baff_Lower_East = tk.DoubleVar()
Scdry_Baff_Lower_West = tk.DoubleVar()

#tk.ttk.Label(mainframe, text="Tierras, Load Readings (Kg)", style="T1.TLabel", font=('Helvetica', 100, 'bold'), foreground='darkslategrey').grid(columnspan=10, row=1)
tk.ttk.Label(mainframe, text="Tierras, Load Readings (Lbs)", style="T1.TLabel", font=('Helvetica', 60, 'bold'), foreground='darkslategrey').grid(columnspan=10, row=1)

# Primary Baffle
mirrorfont = ('Helvetica', 50)
mirrortxtcolor = 'darkslategrey'
tk.ttk.Label(mainframe, text="Primary Baffles", style="T1.TLabel", font=mirrorfont, foreground=mirrortxtcolor).grid(column=2, row=3)

cablefont = ('Helvetica', 50)
cabletxtcolor = 'darkslategrey'
tk.ttk.Label(mainframe, text="Upper Cables", style="T1.TLabel", font=cablefont, foreground=cabletxtcolor).grid(column=2, row=4)
tk.ttk.Label(mainframe, text="Lower Cables", style="T1.TLabel", font=cablefont, foreground=cabletxtcolor).grid(column=3, row=4)

tk.ttk.Separator(mainframe, orient=tk.HORIZONTAL).grid(row=5,columnspan=15,ipadx=0, sticky=tk.NSEW)

cardinalfont = ('Helvetica', 50)
cardinaltxtcolor = 'darkslategrey'
tk.ttk.Label(mainframe, text="NE", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=6)
tk.ttk.Label(mainframe, text="SW", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=7)
tk.ttk.Label(mainframe, text="SE", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=8)
tk.ttk.Label(mainframe, text="NW", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=9)
#tk.ttk.Button(mainframe, text="QUIT",style='C.TButton',command=exit).grid(column=3, row=10, sticky=tk.W)

# set up load sensor boxes for primary  baffle
loadreadingfont = ('Helvetica', 30)
loadreadingtxtcolor = 'white'
loadrdngbgcolor = 'white'
txtw = 1
Prmry_Baff_Upper_North_Entry = tk.ttk.Entry(mainframe, width=txtw, textvariable=Prmry_Baff_Upper_North, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Prmry_Baff_Upper_South_Entry = tk.ttk.Entry(mainframe, width=txtw, textvariable=Prmry_Baff_Upper_South, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Prmry_Baff_Upper_East_Entry =  tk.ttk.Entry(mainframe, width=txtw, textvariable=Prmry_Baff_Upper_East,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Prmry_Baff_Upper_West_Entry =  tk.ttk.Entry(mainframe, width=txtw, textvariable=Prmry_Baff_Upper_West,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Prmry_Baff_Lower_North_Entry = tk.ttk.Entry(mainframe, width=txtw, textvariable=Prmry_Baff_Lower_North, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Prmry_Baff_Lower_South_Entry = tk.ttk.Entry(mainframe, width=txtw, textvariable=Prmry_Baff_Lower_South, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Prmry_Baff_Lower_East_Entry =  tk.ttk.Entry(mainframe, width=txtw, textvariable=Prmry_Baff_Lower_East,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Prmry_Baff_Lower_West_Entry =  tk.ttk.Entry(mainframe, width=txtw, textvariable=Prmry_Baff_Lower_West,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)

Prmry_Baff_Upper_North_Entry.grid(column=2, row=6, sticky=(tk.W, tk.E))
Prmry_Baff_Upper_South_Entry.grid(column=2, row=7, sticky=(tk.W, tk.E))
Prmry_Baff_Upper_East_Entry.grid( column=2, row=8, sticky=(tk.W, tk.E))
Prmry_Baff_Upper_West_Entry.grid( column=2, row=9, sticky=(tk.W, tk.E))
Prmry_Baff_Lower_North_Entry.grid(column=3, row=6, sticky=(tk.W, tk.E))
Prmry_Baff_Lower_South_Entry.grid(column=3, row=7, sticky=(tk.W, tk.E))
Prmry_Baff_Lower_East_Entry.grid( column=3, row=8, sticky=(tk.W, tk.E))
Prmry_Baff_Lower_West_Entry.grid( column=3, row=9, sticky=(tk.W, tk.E))

# Secondary Baffle
tk.ttk.Separator(mainframe, orient=tk.HORIZONTAL).grid(row=10,columnspan=10,ipadx=0, sticky=tk.NSEW)

tk.ttk.Label(mainframe, text="Secondary Baffles", style="T1.TLabel", font=mirrorfont, foreground=mirrortxtcolor).grid(column=2, row=11)
tk.ttk.Label(mainframe, text="Upper Cables", style="T1.TLabel", font=cablefont, foreground=cabletxtcolor).grid(column=2, row=12)
tk.ttk.Label(mainframe, text="Lower Cables", style="T1.TLabel", font=cablefont, foreground=cabletxtcolor).grid(column=3, row=12)

tk.ttk.Label(mainframe, text="N", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=13)
tk.ttk.Label(mainframe, text="S", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=14)
tk.ttk.Label(mainframe, text="E", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=15)
tk.ttk.Label(mainframe, text="W", style="T1.TLabel", font=cardinalfont, foreground=cardinaltxtcolor).grid(column=1, row=16)

# set up load sensor boxes for secondary baffle
Scdry_Baff_Upper_North_Entry = tk.ttk.Entry(mainframe, width=txtw, textvariable=Scdry_Baff_Upper_North, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Scdry_Baff_Upper_South_Entry = tk.ttk.Entry(mainframe, width=txtw, textvariable=Scdry_Baff_Upper_South, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Scdry_Baff_Upper_East_Entry =  tk.ttk.Entry(mainframe, width=txtw, textvariable=Scdry_Baff_Upper_East,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Scdry_Baff_Upper_West_Entry =  tk.ttk.Entry(mainframe, width=txtw, textvariable=Scdry_Baff_Upper_West,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Scdry_Baff_Lower_North_Entry = tk.ttk.Entry(mainframe, width=txtw, textvariable=Scdry_Baff_Lower_North, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Scdry_Baff_Lower_South_Entry = tk.ttk.Entry(mainframe, width=txtw, textvariable=Scdry_Baff_Lower_South, style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Scdry_Baff_Lower_East_Entry =  tk.ttk.Entry(mainframe, width=txtw, textvariable=Scdry_Baff_Lower_East,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)
Scdry_Baff_Lower_West_Entry =  tk.ttk.Entry(mainframe, width=txtw, textvariable=Scdry_Baff_Lower_West,  style='C2.TEntry', font=loadreadingfont, foreground=loadreadingtxtcolor, background= loadrdngbgcolor)

Scdry_Baff_Upper_North_Entry.grid(column=2, row=13, sticky=(tk.W, tk.E))
Scdry_Baff_Upper_South_Entry.grid(column=2, row=14, sticky=(tk.W, tk.E))
Scdry_Baff_Upper_East_Entry.grid( column=2, row=15, sticky=(tk.W, tk.E))
Scdry_Baff_Upper_West_Entry.grid( column=2, row=16, sticky=(tk.W, tk.E))
Scdry_Baff_Lower_North_Entry.grid(column=3, row=13, sticky=(tk.W, tk.E))
Scdry_Baff_Lower_South_Entry.grid(column=3, row=14, sticky=(tk.W, tk.E))
Scdry_Baff_Lower_East_Entry.grid( column=3, row=15, sticky=(tk.W, tk.E))
Scdry_Baff_Lower_West_Entry.grid( column=3, row=16, sticky=(tk.W, tk.E))

main()
root.update_idletasks()
root.mainloop()
