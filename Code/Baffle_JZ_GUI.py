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
from datetime import datetime 

import tkinter as tk
from tkinter import ttk
import tkinter.ttk
import time
import sys

# Define Callibration coefficients for Load Sensor with Label 1 
slope = -33059.175091382494
intercept = -0.5001197942112554


global Upper_North
global Upper_South
global Upper_East
global Upper_West
global Lower_North
global Lower_South
global Lower_East
global Lower_West


# Declare any event handlers for the Phidgets here. These will be called every time the associated event occurs.
def onAttach(self):
	print("Phidget Attached!")

def onDetach(self):
	print("Phidget Detached!")
 
# Describe sequence of actions to perform with Phidgets 

def go(*args):

	#Create your Phidget channels
	voltageRatioInput = VoltageRatioInput()

	#Set addressing parameters to specify which channel to open
	voltageRatioInput.setDeviceSerialNumber(572895)
	voltageRatioInput.setChannel(0)

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
			Upper_North.set(load)
			# chill for a second before you querry again
			root.update()
			time.sleep(1)
	except KeyboardInterrupt:
		print ('Press Ctrl-C to terminate')

	#Close your Phidget once the program is done.
	voltageRatioInput.close()

####################################################################

root = tk.Tk()
#root.geometry("400x400")
root.title("TIERRAS OBSERVATORY")
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

#Upper_North.set(10)

tk.ttk.Label(mainframe, text="TIERRAS OBSERVATORY", style="T1.TLabel")      .grid(columnspan=10, row=1)
tk.ttk.Label(mainframe, text="Upper Cables", style="T1.TLabel")      .grid(column=2, row=2)
tk.ttk.Label(mainframe, text="Lower Cables", style="T1.TLabel")      .grid(column=3, row=2)
tk.ttk.Separator(mainframe, orient=tk.HORIZONTAL) .grid(row=3,  columnspan=15,ipadx=0, sticky=tk.NSEW)
tk.ttk.Label(mainframe, text="N", style="T1.TLabel")      .grid(column=1, row=4)
tk.ttk.Label(mainframe, text="S", style="T1.TLabel")      .grid(column=1, row=5)
tk.ttk.Label(mainframe, text="E", style="T1.TLabel")      .grid(column=1, row=6)
tk.ttk.Label(mainframe, text="W", style="T1.TLabel")      .grid(column=1, row=7)
#tk.ttk.Button(mainframe, text="QUIT",style='C.TButton',command=exit)       .grid(column=3, row=10, sticky=tk.W)

Upper_North_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Upper_North, style='C2.TEntry')
Upper_South_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Upper_South, style='C2.TEntry')
Upper_East_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Upper_East,  style='C2.TEntry')
Upper_West_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Upper_West,  style='C2.TEntry')
Lower_North_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Lower_North, style='C2.TEntry')
Lower_South_Entry = tk.ttk.Entry(mainframe, width=3, textvariable=Lower_South, style='C2.TEntry')
Lower_East_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Lower_East,  style='C2.TEntry')
Lower_West_Entry =  tk.ttk.Entry(mainframe, width=3, textvariable=Lower_West,  style='C2.TEntry')

Upper_North_Entry.grid(column=2, row=4, sticky=(tk.W, tk.E))
Upper_South_Entry.grid(column=2, row=5, sticky=(tk.W, tk.E))
Upper_East_Entry.grid( column=2, row=6, sticky=(tk.W, tk.E))
Upper_West_Entry.grid( column=2, row=7, sticky=(tk.W, tk.E))
Lower_North_Entry.grid(column=3, row=4, sticky=(tk.W, tk.E))
Lower_South_Entry.grid(column=3, row=5, sticky=(tk.W, tk.E))
Lower_East_Entry.grid( column=3, row=6, sticky=(tk.W, tk.E))
Lower_West_Entry.grid( column=3, row=7, sticky=(tk.W, tk.E))

go()
#root.bind('<Return>',go)
root.update_idletasks()
root.mainloop()






