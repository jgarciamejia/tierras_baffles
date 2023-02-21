#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 11:14:04 2019

@author: jgarciamejia

This code generates photometric error (ppm) vs. Integration time 
plots for different M dwarfs. 
"""

#==============================================================================
# Run this code in Folder: '/Users/jgarciamejia/Documents/2019:20-TierrasProject/DESIGN_CODE/PWV_code/'
#==============================================================================

#==============================================================================
# Load Libraries, Dependencies
#==============================================================================

import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import sys

sys.path.insert(1, '/Users/jgarciamejia/Documents/2019:20-TierrasProject/DESIGN_CODE/PWV_code')
import PWV_func_lib as funcs
from jgm_read_FITS import read_fits
import custom_matplotlib

sys.path.insert(1, '/Users/jgarciamejia/Documents/2019:20-TierrasProject/FILTER')
import config_script_FILTER as cs

#==============================================================================
# Load Data
#==============================================================================

# TAPAS telluric spectrum - Units: nm, fraction
h2o = np.loadtxt('/Users/jgarciamejia/Documents/2019:20-TierrasProject/DESIGN_CODE/Data_Files_for_Code/tapas_600nm_1150nm_H2O.txt', skiprows=21)
h2o_lambda = h2o[:,0] * 10  # convert nm to angstroms
h2o_flux = h2o[:,1]

# Two M-Dwarf Spectra from HST Calspec (Jonathan suggestion)
# M3.5v - Units: ang, erg/s/cm2/ang
Gl555wvs, Gl555flux = read_fits('/Users/jgarciamejia/Documents/2019:20-TierrasProject/DESIGN_CODE/Data_Files_for_Code/bd11d3759_stis_001.fits') 
# M7v - Units: ang, erg/s/cm2/ang
vb8wvs, vb8flux = read_fits('/Users/jgarciamejia/Documents/2019:20-TierrasProject/DESIGN_CODE/Data_Files_for_Code/vb8_stiswfcnic_001.fits')
# G2v 
sco18wvs, sco18flux = read_fits('/Users/jgarciamejia/Documents/2019:20-TierrasProject/DESIGN_CODE/Data_Files_for_Code/18sco_stis_001.fits')

# Experimental CCD QE curve 
QEccd = open('/Users/jgarciamejia/Documents/2019:20-TierrasProject/DESIGN_CODE/Data_Files_for_Code/CCD231-84-x-F64.txt','r').readlines()
QEccd_lam = np.array([]) #nm
QEccd_flx = np.array([]) #units?
for line in QEccd:
    QEccd_lam = np.append(QEccd_lam, float(line.split(', ')[0]))
    QEccd_flx = np.append(QEccd_flx, float(line.split(', ')[1].rstrip()))
QEccd_lam *= 10 #(nm->ang)
QEccd_flx *= 10**(-2)
QEccd_flx = np.clip(QEccd_flx, 0.0,1.0)

#==============================================================================
# Interpolate Data onto Comon Wave Grid
#==============================================================================

# Define common wavelength grid of 44000 data points between 6000-9000 nm 
# Above params selected to match resolution of G. Zhous's Regulus Spec. 
comm_wvs = np.linspace(min(h2o_lambda), 10000, 50000)

# Interpolate ALL data onto common wavelength grid

F_h2o = interp1d(h2o_lambda, h2o_flux, kind = 'linear')
comm_h2o_flux = np.clip(F_h2o(comm_wvs),0.0,1.0)

F_Gl555 = interp1d(Gl555wvs, Gl555flux, kind = 'linear')
comm_Gl555_flux = F_Gl555(comm_wvs)

F_vb8 = interp1d(vb8wvs, vb8flux, kind = 'linear')
comm_vb8_flux = F_vb8(comm_wvs)

F_sco18 = interp1d(sco18wvs, sco18flux, kind = 'linear')
comm_sco18_flux = F_sco18(comm_wvs)

F_ccd = interp1d(QEccd_lam, QEccd_flx, kind='linear')
comm_QEccd_flux = F_ccd(comm_wvs)

#==============================================================================
# # Define Filter
#==============================================================================

# ASAHI Predicted Curve
comm_curved_filt = cs.comm_T1_AOI0deg/100

# Define System throughput 
sys_thrupt = 0.58   # Derived using code Calculate_System_Throughput.py

#==============================================================================
#  Define Constants and Telescope Characteristics
#==============================================================================

alt = 2.3823                            # Observatory altitude, [km]
h = 6.62606885 * 10**(-27)              # Planck, [erg*s]
c = 2.99792458 * 10**(10)               # speed of light [cm/s]
D = 128                                 # effective clear telescope diameter, [cm]
d_hole = 20                             # primary hole diameter, [cm]
A = (np.pi / 4) * (D**2 - d_hole**2)    # effective telescope aperture, [cm^2]

# Using minimum baffle obstruction radius in lieu of diameter of 1ry hole
# Compute baff_r via baffle_optim.py code
baff_r_min =  192.09606823356046          # minimum baffle obstruction radius, [mm]
d_hole2 = (2*baff_r_min)/10               # minimum baffle obstruction diameter, [cm]
A2 = (np.pi / 4) * (D**2 - d_hole2**2)    # effective telescope aperture, [cm^2]

baff_r_max =  208.26152483911468          # maximum baffle obstruction radius, [mm]
d_hole3 = (2*baff_r_max)/10               # maximum baffle obstruction diameter, [cm]
A3 = (np.pi / 4) * (D**2 - d_hole3**2)    # effective telescope aperture, [cm^2]

# Conversion factors
AU_to_Rsun = 214.93946938362
pc_to_AU = 2.063 * 10 ** 5
decimal_to_ppm = 10**(6)

'''

#==============================================================================
# Gl555: A M3.5v moved to 15 pc away
# Airmass of chi = 1.5 -> i.e., OK
# Increase integration time, computing all error sources @ each int time 
#==============================================================================

airmass = 1.5
# MOVE Gl555 to 15pc away
d_Gl555 = 6.25   #pc - Derived from parallax. Source: SIMBAD
d_15pc = 15.00   #pc - Derived from parallax. Source: SIMBAD
d_18sco = 14.13  #pc - Derived from parallax. Source: SIMBAD
Gl555_flx_15pc = comm_Gl555_flux * (d_Gl555/d_15pc)**2
sco18_flx_15pc = comm_sco18_flux * (d_18sco/d_15pc)**2

# Define integration times to test
int_times = np.linspace(60, 300) # Integration time
#int_times = [60]

# Define error arrays to populate
scint_errs = np.array([])
phot_errs = np.array([])
phot_errs2 = np.array([])
phot_errs3 = np.array([])
PWV_errs = np.array([])

# Iterate through each time, at each step...
for t in int_times:
    # calculate scintillation noise
    scint_errs = np.append(scint_errs, funcs.scintillation1p75(airmass, D, t, alt)*decimal_to_ppm)
    # calculate photon noise 
    phot_noise = funcs.calc_precision_nodilution(comm_wvs, comm_h2o_flux, Gl555_flx_15pc, 
                                                 comm_QEccd_flux, comm_curved_filt, A, t,sys_thrupt)
    phot_errs = np.append(phot_errs, phot_noise[1])
    # calculate photon noise w/ min baffle obstruction
    phot_noise2 = funcs.calc_precision_nodilution(comm_wvs, comm_h2o_flux, Gl555_flx_15pc, 
                                                 comm_QEccd_flux, comm_curved_filt, A2, t,sys_thrupt)
    phot_errs2 = np.append(phot_errs2, phot_noise2[1])
    # calculate photon noise w/ max baffle obstruction
    phot_noise3 = funcs.calc_precision_nodilution(comm_wvs, comm_h2o_flux, Gl555_flx_15pc, 
                                                 comm_QEccd_flux, comm_curved_filt, A3, t,sys_thrupt)
    phot_errs3 = np.append(phot_errs3, phot_noise3[1])
    # calculate PWV error
    color_err = funcs.calc_color_err_nodilution(comm_wvs, comm_h2o_flux, Gl555_flx_15pc, 
                                                sco18_flx_15pc, comm_QEccd_flux, comm_curved_filt, 
                                                A, t, 9.592, 0.0, 12.0,sys_thrupt)
    PWV_errs = np.append(PWV_errs, color_err)
    
phot_errs *= decimal_to_ppm
phot_errs2 *= decimal_to_ppm
phot_errs3 *= decimal_to_ppm
PWV_errs *= decimal_to_ppm

total_errs = np.sqrt(scint_errs**2 + phot_errs**2 + PWV_errs**2)
total_errs2 = np.sqrt(scint_errs**2 + phot_errs2**2 + PWV_errs**2)
total_errs3 = np.sqrt(scint_errs**2 + phot_errs3**2 + PWV_errs**2)

#==============================================================================
# M3.5v Star: Plot Phot Err vs. Int Time Results 
#==============================================================================

fig, ax = plt.subplots(figsize=(12,8))

plt.plot(int_times, scint_errs, color = 'blue', label=r'Scintillation Error, $\chi = ${}'.format(airmass))
plt.plot(int_times, phot_errs, color = 'green', label='Photon Noise w/o Baffle')
plt.plot(int_times, phot_errs2, color = 'green', ls='--', label='Photon Noise w/ min Baffle')
plt.plot(int_times, phot_errs3, color = 'green', ls='-.', label='Photon Noise w/ max Baffle')
plt.plot(int_times, PWV_errs, color = 'red', label='PWV Error')
plt.plot(int_times, total_errs, color = 'black', label = 'Quadruture Sum w/o Baffle')
plt.plot(int_times, total_errs2, color = 'black',  ls='--', label = 'Quadruture Sum w/ min Baffle')
plt.plot(int_times, total_errs3, color = 'black',  ls='-.', label = 'Quadruture Sum w/ max Baffle')

ax.set_xlabel(r' Integration Time (sec)', fontsize=20)
ax.set_ylabel(r' Contribution to Photometric Error (ppm)', fontsize=20)

#ax.set_title(r' Gl555 M3.5v Star \& 18 Scorpii G2Va Star, both places 15 pc away.Thruput = 0.50', fontsize=20)
ax.set_title(r' Gl555 M3.5v Star \& 18 Scorpii G2Va Star, d=15 pc. Thruput = 0.58. ASAHI Filter.', fontsize=20)

ax.grid(b=True, which='major', linestyle='--', lw='2', alpha=0.4)
ax.tick_params(direction='in', length=6, width=3, colors='black')
ax.legend(fontsize = 15)

plt.subplots_adjust(left=0.1, bottom=None, right=0.95, top=0.8, wspace=0.1, hspace=0.1)
plt.show()

#fig.savefig('M3.5Star_d15pc_photomerr_vs_inttime_TAPAS.50tp.pdf')
#fig.savefig('photoerrvsinttimeTAPAS_Gl555_tp{}_filtctrwv{}_filtwidth{}_sloped.pdf'.format(sys_thrupt, lam_ctr, del_lam))
#fig.savefig('M3_photerrvsinttine_realfilter.pdf')
fig.savefig('M3_photerrvsinttine_realfilter_minmaxbaff.pdf')

'''

#==============================================================================
# vb8: A M7v moved to 15 pc away
# Airmass of chi = 3.0 -> i.e., BAD
# Increase integration time, computing all error sources @ each int time 
#==============================================================================

airmass = 3.0

# MOVE vb8 to 15pc away
d_vb8 = 6.50     #pc - Derived from parallax. Source: SIMBAD
d_15pc = 15.00   #pc - Derived from parallax. Source: SIMBAD
d_18sco = 14.13  #pc - Derived from parallax. Source: SIMBAD
vb8_flx_15pc = comm_vb8_flux * (d_vb8/d_15pc)**2
sco18_flx_15pc = comm_sco18_flux * (d_18sco/d_15pc)**2

# Define integration times to test
int_times = np.linspace(60, 300) # Integration time
#int_times = [60]

# Define error arrays to populate
scint_errs = np.array([])
phot_errs = np.array([])
phot_errs2 = np.array([])
phot_errs3 = np.array([])
PWV_errs = np.array([])

# Iterate through each time, at each step...
for t in int_times:
    # calculate scintillation noise
    scint_errs = np.append(scint_errs, funcs.scintillation1p75(airmass, D, t, alt)*decimal_to_ppm)
    # calculate photon noise 
    phot_noise = funcs.calc_precision_nodilution(comm_wvs, comm_h2o_flux, vb8_flx_15pc, 
                                                 comm_QEccd_flux, comm_curved_filt, A, t, sys_thrupt)
    phot_errs = np.append(phot_errs, phot_noise[1])
    # calculate photon noise w/ min baffle obstruction
    phot_noise2 = funcs.calc_precision_nodilution(comm_wvs, comm_h2o_flux, vb8_flx_15pc, 
                                                 comm_QEccd_flux, comm_curved_filt, A2, t, sys_thrupt)
    phot_errs2 = np.append(phot_errs2, phot_noise2[1])
    # calculate photon noise w/ max baffle obstruction
    phot_noise3 = funcs.calc_precision_nodilution(comm_wvs, comm_h2o_flux, vb8_flx_15pc, 
                                                 comm_QEccd_flux, comm_curved_filt, A3, t, sys_thrupt)
    phot_errs3 = np.append(phot_errs3, phot_noise3[1])
    # calculate PWV error
    color_err = funcs.calc_color_err_nodilution(comm_wvs, comm_h2o_flux, vb8_flx_15pc, 
                                                sco18_flx_15pc, comm_QEccd_flux, comm_curved_filt, 
                                                A, t, 9.592, 0.0, 12.0, sys_thrupt)
    PWV_errs = np.append(PWV_errs, color_err)
    
phot_errs *= decimal_to_ppm
phot_errs2 *= decimal_to_ppm
phot_errs3 *= decimal_to_ppm
PWV_errs *= decimal_to_ppm

total_errs = np.sqrt(scint_errs**2 + phot_errs**2 + PWV_errs**2)
total_errs2 = np.sqrt(scint_errs**2 + phot_errs2**2 + PWV_errs**2)
total_errs3 = np.sqrt(scint_errs**2 + phot_errs3**2 + PWV_errs**2)


#==============================================================================
# M7v Star: Plot Phot Err vs. Int Time Results 
#==============================================================================

fig, ax = plt.subplots(figsize=(14,10))

plt.plot(int_times, scint_errs, color = 'blue', label=r'Scintillation Error, $\chi = ${}'.format(airmass))
plt.plot(int_times, phot_errs, color = 'green', label='Photon Noise w/o Baffle')
plt.plot(int_times, phot_errs2, color = 'green', ls='--', label='Photon Noise w/ min Baffle')
plt.plot(int_times, phot_errs3, color = 'green', ls='-.', label='Photon Noise w/ max Baffle')
plt.plot(int_times, PWV_errs, color = 'red', label='PWV Error')
plt.plot(int_times, total_errs, color = 'black', label = 'Quadruture Sum w/o Baffle')
plt.plot(int_times, total_errs2, color = 'black',  ls='--', label = 'Quadruture Sum w/ min Baffle')
plt.plot(int_times, total_errs3, color = 'black',  ls='-.', label = 'Quadruture Sum w/ max Baffle')

ax.set_xlabel(r' Integration Time (sec)', fontsize=20)
ax.set_ylabel(r' Contribution to Photometric Error (ppm)', fontsize=20)

#ax.set_title(r' vb8 M7v Star \& 18 Scorpii G2Va Star, both placed 15 pc away. Thruput = {}'.format(sys_thrupt), fontsize=20)
ax.set_title(r' vb8 M7v Star \& 18 Scorpii G2Va Star, d=15 pc.Thruput = {}. ASAHI Filter'.format(sys_thrupt), fontsize=20)

ax.grid(b=True, which='major', linestyle='--', lw='2', alpha=0.4)
ax.tick_params(direction='in', length=6, width=3, colors='black')
ax.legend(fontsize = 15)

plt.subplots_adjust(left=0.1, bottom=None, right=0.95, top=0.8, wspace=0.1, hspace=0.1)
plt.show()

#fig.savefig('M7Star_d15pc_photomerr_vs_inttime_TAPAS_.50tp.pdf')
#fig.savefig('photoerrvsinttimeTAPAS_vb8_tp{}_airmass{}_filtctrwv{}_filtwidth{}_sloped.pdf'.format(sys_thrupt, airmass, lam_ctr, del_lam, ))
#fig.savefig('M7_photerrvsinttine_realfilter.pdf')
fig.savefig('M7_photerrvsinttine_realfilter_minmaxbaff.pdf')

'''
# SUPPLEMENTARY PLOT CHECKS BELOW
#==============================================================================
# Plot and compare synthetic spectra to HST Calspec real data
#==============================================================================

dilut_fac = 5.3*10**(-19)   # (0.2 Rsun / 6.18 pc)^2
fig, ax = plt.subplots(figsize=(7,5))

plt.plot(m_lambda*10,  m_flux*dilut_fac, color='royalblue', alpha=0.8, label='Synthetic M5')
plt.plot(Gl555wvs, Gl555flux, color='red', label='Gl 555 - M3.5V')
plt.plot(vb8wvs, vb8flux, color='green', label='VB8 - M7V')

ax.set_xlabel(r' Wavelength (ang)', fontsize=20)
ax.set_ylabel(r' Flux (erg/s/cm$^2$/ang)', fontsize=20)

ax.grid(b=True, which='major', linestyle='--', lw='2', alpha=0.4)
ax.tick_params(direction='in', length=6, width=3, colors='black')
ax.legend(fontsize = 16)
ax.set_xlim(3000,10000)
#ax.set_xlim(min(m_lambda*10),max(m_lambda*10))

plt.subplots_adjust(left=0.1, bottom=None, right=0.95, top=0.8, wspace=0.1, hspace=0.1)
plt.show()

fig.savefig('Mstars_compared.pdf')
#fig.savefig('Mstars_compared2.pdf')


#==============================================================================
# Solar-like Spectra Checks: Plot Solar-type Star Spectra @ 1 AU from Earth
#==============================================================================

d_sco18 = 4.2895*10**(17)         # meters
d_Sun = 1.496*10**(11)            # meters

fig, ax = plt.subplots(figsize=(7,5))
#plt.plot(sun_lambda, sun_flux*(2.206*10**(-5)))
plt.plot(sco18wvs, sco18flux*((d_sco18/d_Sun)**2))

ax.set_xlabel(r' Wavelength (ang)', fontsize=20)
ax.set_ylabel(r' Flux (erg/s/cm$^2$/ang)', fontsize=20)

ax.set_xlim(3000,10000)



#==============================================================================
# Telluric wavelength coverage check 
#==============================================================================

fig, ax = plt.subplots(figsize=(7,5))

ax.axvspan(lam_left, lam_left+del_lam, alpha=0.2, color='gray', zorder=10)
plt.plot(tel_lambda*10, tel_flux, color='black') # from PWV_load_Data.py
plt.scatter(tel_regulus_lam, tel_regulus_flux, color='green', s=4)
plt.scatter(tel_regulus_lam_even, np.clip(tel_regulus_flux_even,0.0, 1.0), color='blue', s=4)

ax.set_xlabel(r' Wavelength (ang)', fontsize=20)
ax.set_ylabel(r' Norm. Flux ', fontsize=20)

ax.set_xlim(8300,9000)

#==============================================================================
# Plot and compare different H2o spectra to see effect of lowering resolution via interpolation
#==============================================================================

fig, ax = plt.subplots(figsize=(7,5))

plt.plot(h2o_lambda, h2o_flux, color='blue')
plt.plot(comm_wvs, comm_h2o_flux, color='green', alpha= 0.7)
ax.set_xlim(820, 890)

fig, ax = plt.subplots(figsize=(14,10))

plt.plot(h2o_lambda, h2o_flux, color='blue')
plt.plot(h2o_lambda, np.clip(h2o_flux,0.0,1.0)**(12/9.592), color='red', alpha=0.5)
ax.set_xlim(8250, 8300)
'''
plt.plot(comm_xs, ray1_comm_zs)
plt.scatter(comm_xs[ind], sz-ray1_comm_zs[ind])
plt.scatter(comm_xs[ind2], sz-ray1_comm_zs[ind2])