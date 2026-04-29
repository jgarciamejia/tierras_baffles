#!/usr/bin/env python3
"""
Continuously reads voltage ratio from an S-type load sensor via a Phidget Bridge
connected to a hub5000 over the network, and converts to load (kg) using
saved calibration coefficients.
"""

from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageRatioInput import *
import time

# Register hub5000 network server
Net.addServer("hub5000", "hub5000.local.", 5661, "", 0)

# Load calibration coefficients
calibtype = input('compression or tension calibration coefficients? ')
calibration_data = open('load_sensor_calibration_coeffs_{}.txt'.format(calibtype)).readlines()[1:]
sensorlabels = [line.split(' ')[1] for line in calibration_data]
sensornums   = [line.split(' ')[2] for line in calibration_data]
slopes       = [line.split(' ')[3] for line in calibration_data]
intercepts   = [line.rstrip().split(' ')[4] for line in calibration_data]

SensorNo    = input('What is the Sensor No.? (etched on sensor) ')
HubPort     = int(input('What hub port is the Phidget Bridge connected to? (0-5): '))
ind         = sensornums.index(SensorNo)
slope       = float(slopes[ind])
intercept   = float(intercepts[ind])

print('Slope: {}; Intercept: {}'.format(slope, intercept))

def main():
    # ports = [10, 11]
    # for i in ports:
    #     VRIs = []
    #     VRs = []
        
    VRIs = [voltageRatioInput30 := VoltageRatioInput(), 
            voltageRatioInput31 := VoltageRatioInput()]
    for j in range(len(VRIs)): 
        i = VRIs[j] 
        i.setHubPort(3)
        i.setIsRemote(True)
        i.setChannel(j)
        i.openWaitForAttachment(20000)
        print(f'{i} Phidget attached. Reading... Press Ctrl-C to stop.\n')

    try:
        while True:
            VRs = [vr10 := voltageRatioInput30.getVoltageRatio(), 
                   vr11 := voltageRatioInput31.getVoltageRatio()]
            for i in VRs:
                load = slope * i + intercept 
                print(i, 'Voltage Ratio (V/V) = {:.8f} ; Load (kg) = {:.4f}'.format(i, load)) 
                time.sleep(1) 
            # vr11   = voltageRatioInput11.getVoltageRatio()
            # load = slope * vr11 + intercept
            # print('Voltage Ratio (V/V) = {:.8f} ; Load (kg) = {:.4f}'.format(vr11, load))
            # time.sleep(1)
    except KeyboardInterrupt:
        print('\nStopped by user.')

    voltageRatioInput30.close()
    voltageRatioInput31.close()

main()

