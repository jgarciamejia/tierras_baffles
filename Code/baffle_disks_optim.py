#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:52:39 2020

@author: jgarciamejia

This code may be used to find optimal position of 
primary baffle inner disks.  
"""



#==============================================================================
# Load Dependencies
#==============================================================================

import baffle_func_lib as funcs
import baffle_optim as optim
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import sys
sys.path.insert(1, '/Users/jgarciamejia/Documents/2019:20-TierrasProject/DESIGN_CODE/PWV_code')
import custom_matplotlib

#==============================================================================
# Load Data
#==============================================================================


#==============================================================================
# Plot Results
# ######## User Note: rays 2&3 change with each iteration, but you need not modify code
#==============================================================================

fig, ax = plt.subplots(figsize=(12,12))
plt.title('F/5.5 Baffles for Tierras Observatory, April 2020 Design'.format(optim.guess_no), fontsize=18)

####### Mirrors #######
plt.plot([optim.px],[optim.pz], 'X', color='black', label='Primary Mirror Vertex, (0,0)', zorder=10)
plt.plot([optim.sx],[optim.sz], 'X', color='gray', label='Secondary Mirror Vertex, (0, -2190.998)')
plt.plot(optim.primary_xys, optim.primary_zs, color='black')
plt.plot(optim.phole_xys, optim.phole_zs, color='white', lw=4)
plt.plot(optim.primary_xys, 82.52*np.ones(len(optim.primary_xys)), color='black')
plt.plot(optim.phole_xys, 82.52*np.ones(len(optim.phole_xys)), color='white', lw=4)
plt.plot(optim.secondary_xys, optim.secondary_zs, color='gray')

####### Lenses #######
lens_color, lens_alpha = 'gray', 0.4
ax.fill_between(optim.filter1_xys, optim.filer1_zs, optim.filer2_zs, facecolor='gray', alpha=0.5)
ax.fill_between(optim.terr1001_1_xys, optim.terr1001_1_zs, optim.terr1001_2_zs, facecolor='gray', alpha=0.5)
ax.fill_between(optim.terr1002_1_xys, optim.terr1002_1_zs, np.max(optim.terr1002_2_zs)*np.ones(len(optim.terr1002_1_xys)), 
                facecolor=lens_color, alpha=0.5)
ax.fill_between(optim.terr1002_2_xys, optim.terr1002_2_zs, np.max(optim.terr1002_2_zs)*np.ones(len(optim.terr1002_2_xys)), 
                facecolor='white')
ax.fill_between(optim.terr1003_1_xys, optim.terr1003_1_zs, np.max(optim.terr1003_2_zs)*np.ones(len(optim.terr1003_1_xys)), 
                facecolor=lens_color, alpha=0.5)
ax.fill_between(optim.terr1003_2_xys, optim.terr1003_2_zs, np.max(optim.terr1003_2_zs)*np.ones(len(optim.terr1003_2_xys)), 
                facecolor='white')
ax.fill_between(optim.terr1004_1_xys, optim.terr1004_1_zs, np.max(optim.terr1004_2_zs)*np.ones(len(optim.terr1004_1_xys)), 
                facecolor=lens_color, alpha=0.5)
ax.fill_between(optim.terr1004_2_xys, optim.terr1004_2_zs, np.max(optim.terr1004_2_zs)*np.ones(len(optim.terr1004_2_xys)), 
                facecolor='white')
####### CCD #######
plt.plot([-optim.ccd_x, optim.ccd_x], [optim.ccd_z, optim.ccd_z], ls='-',color='gray',label='Image Plane')

####### Rays #######
#plt.plot(optim.ray1_xs, optim.ray1_zs, lw=1, ls='--', color='red', label='1AB')
#plt.plot(optim.ray2_xs[1:3], optim.ray2_zs[1:3], lw=1,ls='--', color='green', label='2ABC')
#plt.plot(optim.ray3_xs, optim.ray3_zs, lw=1,ls='--', color='blueviolet', label='3A')

#plt.plot(-optim.ray1_xs, optim.ray1_zs, lw=1,ls='--', color='red', label='1AB')
#plt.plot(-optim.ray2_xs[1:3], optim.ray2_zs[1:3], lw=1,ls='--', color='green', label='2ABC')
#plt.plot(-optim.ray3_xs, optim.ray3_zs, lw=1,ls='--', color='blueviolet', label='3A')

# Baffle Guesses
plt.plot(optim.baffg_xs, optim.baffg_zs, color='black', label=r'2ry Baffle bottom edge, h={0:.0f} mm'.format(optim.baffH_guess))
#plt.plot(optim.baff_r, optim.baff_h, 'o', color='black', label='Bottom of 2ry Baffle')
#plt.plot(optim.intrsct_1b2bx, optim.intrsct_1b2bz, 'o', color='blueviolet', label='Top of 1ry Baffle')
plt.plot([-optim.intrsct_1b2bx,optim.intrsct_1b2bx], [optim.intrsct_1b2bz,optim.intrsct_1b2bz], color='black', label='Top of 1ry Baffle')

####### Reverse Rays and Optimal Disk Radii Locations #######

# Define ray path and normalized coordinates
path = '/Users/jgarciamejia/Documents/2019:20-TierrasProject/BAFFLES/ReverseRays/'
Pxs = np.arange(.5,.85,.05)
Pxs = np.sort(np.append(Pxs, np.array([.78, .83])))
#Pxs = np.array([.8])
Hx=1

# Define rays 1b & 2b slopes and z-intercepts 
ray1b_m, ray1b_b = funcs.define_line_from_pts(optim.ray1_xs[1], optim.ray1_xs[2],optim.ray1_zs[1], optim.ray1_zs[2])
ray2b_m, ray2b_b = funcs.define_line_from_pts(optim.ray2_xs[1], optim.ray2_xs[2],optim.ray2_zs[1], optim.ray2_zs[2])

# Loop through Px values, loading and plotting each reverse ray 
# and then finding ideal disk inner and outer radii
disk_coords = np.array([])
intz1b_old = 0
for Px in Pxs:
    # Load Data, taking care of sign transformations! 
    rayfn = 'Hx{}_Px{:.2f}.txt'.format(Hx, Px)
    ray_data = np.loadtxt(path+rayfn, delimiter='\t', skiprows=21, max_rows=14, usecols=(1,2,3), encoding='utf-16')
    ray_xs, ray_zs = -ray_data[:,0], -ray_data[:,2]
    # Plot ray
    #plt.plot(ray_xs[:-1], ray_zs[:-1], color='blue', ls='--')
    # Define ray slope and z-intercept
    ray_m ,ray_b = funcs.define_line_from_pts(ray_xs[11], ray_xs[12],ray_zs[11], ray_zs[12])
    # Find x,z location where reverse ray intercepts ray1b and 2b
    intx1b, intz1b = funcs.find_line_intercept(ray1b_m, ray1b_b, ray_m ,ray_b)
    intx2b, intz2b = (intz1b - ray2b_b) / ray2b_m, intz1b
    intz1b_coord = np.abs(intz1b) - np.abs(intz1b_old)
    # Save z-location, z-coord for Zemax LDE, inner and outer radii of disks 
    disk_coords = np.append(disk_coords, np.array([intz1b, intz1b_coord, intx1b, intx2b]))
    # Plot disk out to ray 2b
    plt.plot([intx1b,intx2b],[intz1b,intz2b], color='black')
    plt.plot([-intx1b,-intx2b],[intz1b,intz2b], color='black')
    intz1b_old = intz1b

# Aesthetics
leftx, rightx = -750, 750
bottomz, topz = -2500, 500
ax.set_xlabel(r' X-Y Dimension (mm)', fontsize=20)
ax.set_ylabel(r' Z Dimension (mm) ', fontsize=20)
#ax.set_xlim(left=-120, right=120)
#ax.set_ylim(bottom=50, top=300)
ax.set_xlim(left=leftx, right=rightx)
ax.set_ylim(bottom=bottomz, top=topz)
ax.invert_yaxis()
ax.set_facecolor('white')
plt.gca().set_aspect('equal', adjustable='box')
plt.yticks(np.arange(bottomz, topz+1, 250))
ax.tick_params(direction='in', length=6, width=3, colors='black')
ax.grid(b=True, which='major', linestyle='--', lw='2', alpha=0.2)
#ax.legend(fontsize = 10, loc=(1.05, 0.5),fancybox=True, framealpha=0.9)

#fig.savefig('baffle_reverserays_guessNo.{0}_res{1}.pdf'.format(optim.guess_no, optim.stp))
fig.savefig('baffle_1rydisks_guessNo.{0}_res{1}.pdf'.format(optim.guess_no, optim.stp))
fig.savefig('baffle_1rydisks_guessNo.{0}_res{1}_v3.pdf'.format(optim.guess_no, optim.stp))

# Save Disk coordinates ready for LDE!
#fname = 'baffle_1rydisks_coords_guessNo.{0}_res{1}.txt'.format(optim.guess_no, optim.stp)
fname = 'baffle_1rydisks_coords_guessNo.{0}_res{1}_v3.txt'.format(optim.guess_no, optim.stp)
header = 'Z-Location (mm), Z-Coordinate, Inner Radius (mm), Outer Radius (mm)'
np.savetxt(fname, disk_coords.reshape(len(Pxs), 4), fmt='%6f', delimiter=' ', header=header)









