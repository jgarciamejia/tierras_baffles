#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 14:26:39 2021

GUI Testing
"""

import numpy as np
import random
import time
from GUI_JZ_JGM import *


# Define Callibration coefficients for Load Sensor with Label 1 
slope = -33059.175091382494
intercept = -0.5001197942112554

def go(*args):
	# Querry for the voltage ratio indefinitely, passing value to a variable 
	try:
		while True:
			voltageRatio = random.random()
			load = slope*voltageRatio + intercept 
			#print ('Voltage Ratio (V/V) = '+str(voltageRatio)+'; Load (Kg) = '+str(load))
			Upper_North.set(load)
			root.update()
			# chill for a second before you querry again
			time.sleep(1)
	except KeyboardInterrupt:
		print ('Press Ctrl-C to terminate')

go()
root.update_idletasks()
root.mainloop() 


