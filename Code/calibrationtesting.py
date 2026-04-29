#!/usr/bin/env python3
"""
3-point calibration for an S-type load sensor via a Phidget Bridge
connected to a hub5000 over the network.
Saves slope/intercept to a calibration file and plots the fit.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageRatioInput import *
import time

# Register hub5000 network server
Net.addServer("hub5000", "hub5000.local.", 5661, "", 0)

# Sensor and calibration setup
print('Starting Calibration Routine')
SensorLabel  = input('Enter Sensor Label (written with Sharpie on sensor): ')
SensorNo     = input('Enter Sensor No (etched on sensor): ')
HubPort      = int(input('What hub port is the Phidget Bridge connected to? (0-5): '))
nrdngs       = int(input('How many voltage ratio readings to average per calibration point? '))
typeofcalib  = input('Is this a tension or compression calibration? ')

# Known calibration weights (edit as needed)
medium_weight = float(input('Enter the mid-point calibration weight (kg): '))
max_weight    = float(input('Enter the max-point calibration weight (kg): '))

# Connect to VoltageRatioInput on hub5000
voltageRatioInput = VoltageRatioInput()
voltageRatioInput.setHubPort(HubPort)
voltageRatioInput.setIsRemote(True)
voltageRatioInput.setChannel(0)
voltageRatioInput.openWaitForAttachment(20000)
print('Phidget attached.')

def collect_readings(label, nrdngs):
    print('Starting {} data collection.'.format(label))
    rdngs = []
    for _ in range(nrdngs):
        vr = voltageRatioInput.getVoltageRatio()
        print('  Voltage Ratio (V/V) = {:.8f}'.format(vr))
        rdngs.append(vr)
        time.sleep(1)
    avg = np.average(rdngs)
    print('Average {} Voltage Ratio (V/V) = {:.8f}'.format(label, avg))
    return avg

# Zero point
print('\nEnsure the sensor is upright and unloaded.')
input('Press Enter to begin zero-point collection.')
zeropt_vr = collect_readings('Zero-pt', nrdngs)

# Mid point
input('\nLoad the sensor with the mid-point weight ({} kg), then press Enter.'.format(medium_weight))
midpt_vr = collect_readings('Mid-pt', nrdngs)

# Max point
input('\nLoad the sensor with the max-point weight ({} kg), then press Enter.'.format(max_weight))
maxpt_vr = collect_readings('Max-pt', nrdngs)

voltageRatioInput.close()

# Linear fit
VoltageRatios = [zeropt_vr, midpt_vr, maxpt_vr]
Weights       = [0, medium_weight, max_weight]
slope, intercept, r, p, se = stats.linregress(VoltageRatios, Weights)
print('\nSlope: {}; Intercept: {}'.format(slope, intercept))

# Save coefficients
with open('load_sensor_calibration_coeffs_{}.txt'.format(typeofcalib), 'a+') as f:
    f.write('\n {} {} {} {}'.format(SensorLabel, SensorNo, slope, intercept))
print('Calibration coefficients saved.')

# Plot
x = np.linspace(min(VoltageRatios), max(VoltageRatios), 50)
y = slope * x + intercept
fig, ax = plt.subplots()
ax.plot(VoltageRatios, Weights, 'o', label='Data')
ax.plot(x, y, label='Fit')
ax.set_xlabel('Voltage Ratio (V/V)')
ax.set_ylabel('Load (kg)')
ax.set_title('Slope: {:.4f}; Intercept: {:.4f}'.format(slope, intercept))
ax.invert_xaxis()
ax.legend()
plt.tight_layout()
fig.savefig('3ptcalib_Sensor{}_No{}_{}.pdf'.format(SensorLabel, SensorNo, typeofcalib))
print('Calibration plot saved.')
plt.show()